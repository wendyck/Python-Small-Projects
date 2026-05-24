#!/usr/bin/env python3
"""Move already-downloaded flat photos into photos/{year}/ subfolders using metadata JSON."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHOTOS_DIR = ROOT / "photos"
META_DIR = ROOT / "metadata"


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


moved = 0
skipped = 0
for f in PHOTOS_DIR.iterdir():
    if not f.is_file():
        continue
    pid = f.name.split("_", 1)[0].split(".", 1)[0]
    meta = META_DIR / f"{pid}.json"
    if not meta.exists():
        print(f"  no metadata for {f.name}, skipping")
        skipped += 1
        continue
    photo = json.loads(meta.read_text())
    year = year_for(photo)
    year_dir = PHOTOS_DIR / year
    year_dir.mkdir(exist_ok=True)
    dest = year_dir / f.name
    if dest.exists():
        print(f"  {dest} already exists, skipping")
        skipped += 1
        continue
    f.rename(dest)
    moved += 1

print(f"\nMoved {moved}, skipped {skipped}")
