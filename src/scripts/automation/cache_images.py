#!/usr/bin/env python3
"""
cache_images.py - Pre-cache product images from JGMart catalog

Reads catalog_data.json, downloads all product images to a local cache folder,
updates the catalog to point to local paths, and creates a placeholder SVG
for any images that fail to download.

Usage:
    python cache_images.py

Output:
    - Downloads images to 06_Web_Catalog/images/<product_id>.<ext>
    - Updates catalog_data.json with local image paths
    - Creates 06_Web_Catalog/images/placeholder.svg for failed downloads
    - Prints summary of results
"""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path("G:/JGC Mart/JGC Mart - Hermes")
CATALOG_PATH = BASE_DIR / "06_Web_Catalog" / "catalog_data.json"
IMAGES_DIR = BASE_DIR / "06_Web_Catalog" / "images"
PLACEHOLDER_PATH = IMAGES_DIR / "placeholder.svg"

# ── Placeholder SVG ────────────────────────────────────────────────────────
PLACEHOLDER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">
  <rect width="400" height="400" fill="#4CAF50" rx="8" ry="8"/>
  <rect x="20" y="20" width="360" height="360" fill="#388E3C" rx="6" ry="6"/>
  <text x="200" y="200" font-size="120" text-anchor="middle" dominant-baseline="central">🛒</text>
  <text x="200" y="300" font-family="Arial,sans-serif" font-size="24" fill="white" text-anchor="middle" font-weight="bold">Image Unavailable</text>
</svg>"""


def ensure_images_dir():
    """Create the images directory if it doesn't exist."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def ensure_placeholder():
    """Write the placeholder SVG file if it doesn't already exist."""
    if not PLACEHOLDER_PATH.exists():
        PLACEHOLDER_PATH.write_text(PLACEHOLDER_SVG, encoding="utf-8")
        print(f"  📄 Created placeholder: {PLACEHOLDER_PATH}")
        return True
    return False


def load_catalog() -> dict:
    """Load catalog from JSON file."""
    if not CATALOG_PATH.exists():
        print(f"❌ ERROR: Catalog not found at {CATALOG_PATH}")
        sys.exit(1)
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_catalog(catalog: dict):
    """Save updated catalog back to JSON file."""
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)


def get_extension_from_url(url: str) -> str:
    """
    Determine file extension from the URL.
    Falls back to .jpg if unable to determine.
    """
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    # Try to get extension from filename in URL path
    _, ext = os.path.splitext(path)
    if ext and ext.lower() in (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".svg",
        ".bmp",
    ):
        return ext.lower()
    # Check for query-encoded format hints
    query = urllib.parse.parse_qs(parsed.query)
    if "fm" in query:
        fmt = query["fm"][0].lower()
        if fmt in ("jpg", "jpeg", "png", "webp", "gif"):
            return f".{fmt}"
    # Default
    return ".jpg"


def download_image(url: str, dest_path: Path) -> bool:
    """
    Download an image from URL to destination path.
    Returns True on success, False on failure.
    """
    try:
        # Build a request with a common User-Agent to avoid 403 errors
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/125.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            # Check for valid image content
            content_type = response.headers.get("Content-Type", "")
            if "image" not in content_type and len(data) < 100:
                # Probably a non-image response (e.g. HTML error page)
                print(
                    f"    ⚠  Response was not an image (Content-Type: {content_type})"
                )
                return False
            if len(data) < 100:
                print(f"    ⚠  Response too small ({len(data)} bytes) — skipping")
                return False
            dest_path.write_bytes(data)
        return True
    except urllib.error.HTTPError as e:
        print(f"    ⚠  HTTP {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"    ⚠  URL error: {e.reason}")
        return False
    except OSError as e:
        print(f"    ⚠  OS error: {e}")
        return False
    except Exception as e:
        print(f"    ⚠  Unexpected error: {type(e).__name__}: {e}")
        return False


def main():
    print("=" * 60)
    print("  JGMart — Image Cache Tool")
    print("=" * 60)
    print()

    # ── Setup ──────────────────────────────────────────────────────────────
    ensure_images_dir()
    placeholder_created = ensure_placeholder()

    # ── Load catalog ───────────────────────────────────────────────────────
    print("📖 Loading catalog...")
    catalog = load_catalog()
    products = catalog.get("products", [])
    print(f"   Found {len(products)} products in catalog")
    print()

    # ── Process each product ───────────────────────────────────────────────
    downloaded = 0
    skipped = 0
    failed = 0
    already_cached = 0
    updated_products = 0

    for product in products:
        pid = product.get("id", "unknown")
        image_url = product.get("image", "")

        # Skip products without an image URL
        if not image_url:
            print(f"  ⏭  {pid}: No image URL — skipping")
            skipped += 1
            continue

        # Skip if already a local path
        if image_url.startswith("images/"):
            print(f"  ✓  {pid}: Already cached ({image_url})")
            already_cached += 1
            continue

        # Determine filename extension from URL
        ext = get_extension_from_url(image_url)
        dest_filename = f"{pid}{ext}"
        dest_path = IMAGES_DIR / dest_filename

        # Check if already cached (by filename)
        if dest_path.exists():
            local_ref = f"images/{dest_filename}"
            product["image"] = local_ref
            updated_products += 1
            print(f"  ✓  {pid}: Already cached → {local_ref}")
            already_cached += 1
            continue

        # Download the image
        print(f"  ↓  {pid}: Downloading {image_url[:70]}...")
        success = download_image(image_url, dest_path)

        if success:
            local_ref = f"images/{dest_filename}"
            product["image"] = local_ref
            updated_products += 1
            downloaded += 1
            size_kb = dest_path.stat().st_size / 1024
            print(f"     ✅ Saved → {local_ref} ({size_kb:.1f} KB)")
        else:
            # Use placeholder
            local_ref = "images/placeholder.svg"
            product["image"] = local_ref
            updated_products += 1
            failed += 1
            print(f"     ❌ Failed → using placeholder.svg")

    # ── Save updated catalog ───────────────────────────────────────────────
    if updated_products > 0:
        save_catalog(catalog)
        print()
        print(f"💾 Catalog updated — {updated_products} product image paths changed")

    # ── Summary ────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"  Products in catalog:          {len(products)}")
    print(f"  Images freshly downloaded:    {downloaded}")
    print(f"  Already cached (skipped):     {already_cached}")
    print(f"  No image URL (skipped):       {skipped}")
    print(f"  Failed / fell back to placeholder: {failed}")
    print(f"  Placeholder SVG {'created' if placeholder_created else 'already exists'}")
    print(f"  Cache directory:              {IMAGES_DIR}")
    print("=" * 60)

    if failed > 0:
        print("  📌 Some images failed — placeholder.svg used as fallback.")
    if downloaded == 0 and already_cached == 0 and skipped == 0 and failed == 0:
        print("  ⚠  No images were processed. Check the catalog structure.")
    print()


if __name__ == "__main__":
    main()
