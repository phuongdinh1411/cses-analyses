#!/usr/bin/env python3
"""
Download all images referenced in ByteByteGo lesson raw JSON files.

Images are publicly accessible (no auth needed) but require a User-Agent header.
Downloads mirror the URL path structure under bytebytego_content/images/.

Usage:
    python3 download_bytebytego_images.py
    python3 download_bytebytego_images.py --dry-run       # just list, don't download
    python3 download_bytebytego_images.py --delay 0.05    # faster (default 0.1s)
"""

import argparse
import json
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://bytebytego.com"
CONTENT_DIR = Path("bytebytego_content")
IMAGES_DIR = CONTENT_DIR / "images"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def collect_image_urls():
    """Extract all unique image paths from raw JSON files."""
    urls = set()
    for f in CONTENT_DIR.glob("*/raw/*.json"):
        with open(f) as fh:
            code = json.load(fh).get("code", "")
        for m in re.finditer(r'"(/images/[^"]+)"', code):
            urls.add(m.group(1))
    return sorted(urls)


def download_image(path, delay):
    """Download a single image. Returns (ok, size, existed) tuple."""
    # path is like /images/courses/..., save under CONTENT_DIR so it becomes
    # bytebytego_content/images/courses/...
    local_path = CONTENT_DIR / path.lstrip("/")
    if local_path.exists():
        return True, local_path.stat().st_size, True  # already exists

    local_path.parent.mkdir(parents=True, exist_ok=True)

    url = BASE_URL + path
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(local_path, "wb") as f:
            f.write(data)
        time.sleep(delay)
        return True, len(data), False
    except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
        return False, 0, False


def main():
    parser = argparse.ArgumentParser(description="Download ByteByteGo images")
    parser.add_argument("--dry-run", action="store_true", help="List images without downloading")
    parser.add_argument("--delay", type=float, default=0.1, help="Delay between downloads (seconds)")
    args = parser.parse_args()

    urls = collect_image_urls()
    print(f"Found {len(urls)} unique images")

    if args.dry_run:
        for u in urls:
            exists = (CONTENT_DIR / u.lstrip("/")).exists()
            status = "EXISTS" if exists else "MISSING"
            print(f"  [{status}] {u}")
        existing = sum(1 for u in urls if (CONTENT_DIR / u.lstrip("/")).exists())
        print(f"\n{existing} already downloaded, {len(urls) - existing} remaining")
        return

    downloaded = 0
    skipped = 0
    failed = 0
    total_bytes = 0

    for i, path in enumerate(urls):
        ok, size, existed = download_image(path, args.delay)
        if existed:
            skipped += 1
        elif ok:
            downloaded += 1
            total_bytes += size
            if downloaded % 50 == 0:
                print(f"  [{i+1}/{len(urls)}] downloaded {downloaded}, "
                      f"{total_bytes / 1024 / 1024:.1f} MB so far...")
        else:
            failed += 1
            print(f"  FAIL: {path}")

    print(f"\nDone: {downloaded} downloaded ({total_bytes / 1024 / 1024:.1f} MB), "
          f"{skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
