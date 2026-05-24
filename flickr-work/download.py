#!/usr/bin/env python3
"""Download all photos (including private) from a Flickr account with EXIF/metadata preserved."""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import flickrapi
import requests

ROOT = Path(__file__).resolve().parent
PHOTOS_DIR = ROOT / "photos"
META_DIR = ROOT / "metadata"
DONE_FILE = ROOT / "done.txt"
FAILED_FILE = ROOT / "failed.txt"
CREDS_FILE = Path.home() / "flickr_creds.txt"

PHOTOS_DIR.mkdir(exist_ok=True)
META_DIR.mkdir(exist_ok=True)


def load_creds():
    creds = {}
    for line in CREDS_FILE.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip()
    return creds["key"], creds["secret"]


def load_done():
    if not DONE_FILE.exists():
        return set()
    return set(DONE_FILE.read_text().split())


def mark_done(pid):
    with DONE_FILE.open("a") as f:
        f.write(pid + "\n")


def mark_failed(pid, reason):
    with FAILED_FILE.open("a") as f:
        f.write(f"{pid}\t{reason}\n")


def year_for(photo):
    dt = photo.get("datetaken") or ""
    if dt and not dt.startswith("0000"):
        return dt[:4]
    up = photo.get("dateupload")
    if up:
        try:
            return datetime.utcfromtimestamp(int(up)).strftime("%Y")
        except (ValueError, TypeError):
            pass
    return "unknown"


def sanitize(name, maxlen=80):
    name = re.sub(r"[^\w\s.-]", "_", name or "").strip()
    name = re.sub(r"\s+", "_", name)
    return name[:maxlen]


def auth(api_key, api_secret):
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format="parsed-json", cache=True)
    if not flickr.token_valid(perms="read"):
        flickr.get_request_token(oauth_callback="oob")
        url = flickr.auth_url(perms="read")
        print("\n=== ONE-TIME AUTHORIZATION ===")
        print(f"Open this URL in your browser:\n\n{url}\n")
        print("After authorizing, Flickr will show you a 9-digit code.")
        code = input("Paste the code here: ").strip()
        flickr.get_access_token(code)
        print("Authorized.\n")
    return flickr


def original_url(photo):
    # From extras=url_o
    url = photo.get("url_o")
    if url:
        return url, photo.get("original_format", "jpg")
    return None, None


def get_video_url(flickr, pid):
    sizes = flickr.photos.getSizes(photo_id=pid)["sizes"]["size"]
    # Prefer "Video Original", fall back to "Site MP4", "HD MP4"
    for pref in ("Video Original", "HD MP4", "Site MP4", "Mobile MP4"):
        for s in sizes:
            if s["label"] == pref:
                return s["source"], "mp4"
    return None, None


_last_download = [0.0]
MIN_INTERVAL = 0.4  # seconds between downloads (~2.5/sec cap)


def download(url, dest):
    tmp = dest.with_suffix(dest.suffix + ".part")
    backoffs = [5, 15, 45, 120, 300]
    for attempt, wait in enumerate([0] + backoffs):
        if wait:
            print(f"    429/err, sleeping {wait}s before retry {attempt}...")
            time.sleep(wait)
        # Throttle: ensure min interval between downloads
        gap = time.time() - _last_download[0]
        if gap < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - gap)
        _last_download[0] = time.time()
        try:
            with requests.get(url, stream=True, timeout=120) as r:
                if r.status_code == 429:
                    # back off harder on rate limit
                    ra = r.headers.get("Retry-After")
                    if ra and ra.isdigit():
                        time.sleep(min(int(ra), 300))
                    continue
                r.raise_for_status()
                with tmp.open("wb") as f:
                    shutil.copyfileobj(r.raw, f)
            tmp.rename(dest)
            return
        except requests.exceptions.RequestException:
            if attempt == len(backoffs):
                raise
            continue


def stamp_exif(path, photo):
    """Write Flickr metadata into file tags so Google Photos picks them up."""
    title = photo.get("title", "") or ""
    # description is a dict with _content when using parsed-json with extras
    desc = photo.get("description", "")
    if isinstance(desc, dict):
        desc = desc.get("_content", "")
    tags = (photo.get("tags") or "").split()
    date_taken = photo.get("datetaken")  # "YYYY-MM-DD HH:MM:SS"
    lat = photo.get("latitude")
    lon = photo.get("longitude")
    owner = photo.get("ownername", "")

    args = ["exiftool", "-overwrite_original", "-P", "-q", "-m"]
    if title:
        args += [f"-IPTC:ObjectName={title}", f"-XMP-dc:Title={title}"]
    if desc:
        args += [
            f"-EXIF:ImageDescription={desc}",
            f"-IPTC:Caption-Abstract={desc}",
            f"-XMP-dc:Description={desc}",
        ]
    for t in tags:
        args += [f"-IPTC:Keywords+={t}", f"-XMP-dc:Subject+={t}"]
    if date_taken and date_taken != "0000-00-00 00:00:00":
        args += [f"-EXIF:DateTimeOriginal={date_taken}",
                 f"-EXIF:CreateDate={date_taken}",
                 f"-XMP:DateCreated={date_taken}"]
    if lat and lon and str(lat) != "0" and str(lon) != "0":
        try:
            latf, lonf = float(lat), float(lon)
            args += [
                f"-GPSLatitude={abs(latf)}",
                f"-GPSLatitudeRef={'N' if latf >= 0 else 'S'}",
                f"-GPSLongitude={abs(lonf)}",
                f"-GPSLongitudeRef={'E' if lonf >= 0 else 'W'}",
            ]
        except ValueError:
            pass
    if owner:
        args += [f"-XMP-dc:Creator={owner}"]

    args += [str(path)]

    if len(args) > 7:  # more than just the base args + path
        try:
            subprocess.run(args, check=True, capture_output=True, timeout=60)
        except subprocess.CalledProcessError as e:
            # exiftool sometimes warns on weird files; don't fail the whole download
            sys.stderr.write(f"  exiftool warning on {path.name}: {e.stderr.decode()[:200]}\n")


def process_photo(flickr, photo, done):
    pid = photo["id"]
    if pid in done:
        return "skip"

    media = photo.get("media", "photo")
    url, ext = original_url(photo)
    if not url and media == "video":
        url, ext = get_video_url(flickr, pid)
    if not url:
        # Fall back to getSizes for photos where url_o wasn't returned
        try:
            sizes = flickr.photos.getSizes(photo_id=pid)["sizes"]["size"]
            for s in reversed(sizes):  # largest usually last
                if s["label"] in ("Original", "Large 2048", "Large 1600", "Large"):
                    url = s["source"]
                    ext = url.rsplit(".", 1)[-1]
                    break
        except Exception as e:
            mark_failed(pid, f"no_url: {e}")
            return "fail"

    if not url:
        mark_failed(pid, "no_url_available")
        return "fail"

    title = sanitize(photo.get("title") or "")
    fname = f"{pid}_{title}.{ext}" if title else f"{pid}.{ext}"
    year_dir = PHOTOS_DIR / year_for(photo)
    year_dir.mkdir(exist_ok=True)
    dest = year_dir / fname

    # Save metadata sidecar
    (META_DIR / f"{pid}.json").write_text(json.dumps(photo, indent=2))

    if not dest.exists():
        try:
            download(url, dest)
        except Exception as e:
            mark_failed(pid, f"download: {e}")
            return "fail"

    if media == "photo":
        stamp_exif(dest, photo)

    mark_done(pid)
    return "ok"


def main():
    api_key, api_secret = load_creds()
    flickr = auth(api_key, api_secret)
    done = load_done()
    print(f"Already downloaded: {len(done)}")

    extras = "description,date_taken,date_upload,geo,tags,machine_tags,views,media,url_o,original_format,owner_name,license"

    # Get total count first
    first = flickr.people.getPhotos(user_id="me", per_page=1, page=1, extras=extras)
    total = int(first["photos"]["total"])
    print(f"Total photos on Flickr: {total}")

    ok = fail = skip = 0
    start = time.time()
    n = 0

    page = 1
    per_page = 500
    while True:
        resp = flickr.people.getPhotos(user_id="me", per_page=per_page, page=page, extras=extras)
        photos = resp["photos"]["photo"]
        if not photos:
            break
        pages = int(resp["photos"]["pages"])
        print(f"\n--- Page {page}/{pages} ({len(photos)} photos) ---")
        for photo in photos:
            n += 1
            result = process_photo(flickr, photo, done)
            if result == "ok":
                ok += 1
                done.add(photo["id"])
            elif result == "fail":
                fail += 1
            else:
                skip += 1
            if n % 10 == 0 or result == "fail":
                elapsed = time.time() - start
                rate = n / elapsed if elapsed else 0
                remaining = (total - len(done)) / rate if rate else 0
                print(f"  [{n}/{total}] ok={ok} fail={fail} skip={skip}  "
                      f"{rate:.1f} photos/s  ETA {remaining/60:.0f}min")
        if page >= pages:
            break
        page += 1

    print(f"\nDone. ok={ok} fail={fail} skip={skip}")
    if fail:
        print(f"See {FAILED_FILE} for failures. Re-run the script to retry them"
              " (remove their IDs from done.txt is not needed — failures aren't marked done).")


if __name__ == "__main__":
    main()
