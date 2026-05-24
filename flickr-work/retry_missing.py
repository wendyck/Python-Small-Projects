#!/usr/bin/env python3
"""Re-download photos that are marked done but missing on disk."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from download import (auth, download, load_creds, original_url, sanitize,
                      stamp_exif, year_for, PHOTOS_DIR, META_DIR)

api_key, api_secret = load_creds()
flickr = auth(api_key, api_secret)

done_ids = set(Path("done.txt").read_text().split())
on_disk_ids = {p.name.split("_", 1)[0].split(".", 1)[0]
               for p in PHOTOS_DIR.rglob("*") if p.is_file()}
missing = sorted(done_ids - on_disk_ids)
print(f"Missing: {len(missing)}")

for pid in missing:
    meta = META_DIR / f"{pid}.json"
    if not meta.exists():
        print(f"  {pid}: no metadata, skip")
        continue
    photo = json.loads(meta.read_text())
    url, ext = original_url(photo)
    if not url:
        try:
            sizes = flickr.photos.getSizes(photo_id=pid)["sizes"]["size"]
            for s in reversed(sizes):
                if s["label"] in ("Original", "Large 2048", "Large 1600", "Large"):
                    url = s["source"]; ext = url.rsplit(".", 1)[-1]; break
        except Exception as e:
            print(f"  {pid}: getSizes failed: {e}"); continue
    if not url:
        print(f"  {pid}: no url"); continue

    title = sanitize(photo.get("title") or "")
    fname = f"{pid}_{title}.{ext}" if title else f"{pid}.{ext}"
    year_dir = PHOTOS_DIR / year_for(photo)
    year_dir.mkdir(exist_ok=True)
    dest = year_dir / fname
    try:
        download(url, dest)
        if photo.get("media", "photo") == "photo":
            stamp_exif(dest, photo)
        print(f"  {pid}: ok -> {dest.relative_to(PHOTOS_DIR.parent)}")
    except Exception as e:
        print(f"  {pid}: FAILED {e}")
