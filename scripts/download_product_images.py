#!/usr/bin/env python3
"""
JG Mart — Product Image Downloader
Downloads real product images from free sources (Unsplash/Pexels)
and saves them to src/web/catalog/images/ with correct filenames.

Usage:
    python download_product_images.py
    python download_product_images.py --limit 10
    python download_product_images.py --reset

Features:
    - Downloads from Unsplash Source API (free, no key needed)
    - Falls back to category SVG placeholders if download fails
    - Skips existing files unless --reset is passed
    - Idempotent: safe to re-run
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

# Configuration
PRODUCTS = [
    # [id, name, category, search_term_for_image]
    ["p01", "Premium Miniket Rice", "rice_dal", "miniket rice"],
    ["p02", "Chinigura Rice", "rice_dal", "aromatic rice"],
    ["p03", "Nazirshail Rice", "rice_dal", "rice bowl"],
    ["p04", "Basmati Rice", "rice_dal", "basmati rice"],
    ["p05", "Moshur Dal (Red)", "rice_dal", "red lentils"],
    ["p06", "Moong Dal (Yellow)", "rice_dal", "yellow lentils"],
    ["p07", "Chola (Bengal Gram)", "rice_dal", "chickpeas"],
    ["p08", "Soybean Oil", "oil_spices", "soybean oil bottle"],
    ["p09", "Mustard Oil", "oil_spices", "mustard oil"],
    ["p10", "Sunflower Oil", "oil_spices", "sunflower oil"],
    ["p11", "Turmeric Powder", "oil_spices", "turmeric powder"],
    ["p12", "Chili Powder", "oil_spices", "chili powder"],
    ["p13", "Cumin Powder", "oil_spices", "cumin seeds"],
    ["p14", "Coriander Powder", "oil_spices", "coriander powder"],
    ["p15", "White Sugar", "oil_spices", "white sugar"],
    ["p16", "Potato", "vegetables", "potatoes"],
    ["p17", "Red Onion", "vegetables", "red onions"],
    ["p18", "Tomato", "vegetables", "tomatoes"],
    ["p19", "Eggplant (Brinjal)", "vegetables", "eggplant brinjal"],
    ["p20", "Cauliflower", "vegetables", "cauliflower"],
    ["p21", "Cabbage", "vegetables", "green cabbage"],
    ["p22", "Green Chili", "vegetables", "green chilies"],
    ["p23", "Coriander Leaves", "vegetables", "coriander leaves cilantro"],
    ["p24", "Lady Finger (Okra)", "vegetables", "okra lady finger"],
    ["p25", "Green Papaya", "vegetables", "green papaya"],
    ["p26", "Fresh Ginger", "vegetables", "fresh ginger"],
    ["p27", "Fresh Garlic", "vegetables", "garlic cloves"],
    ["p28", "Ruhi Fish", "fish", "fresh fish ruhi"],
    ["p29", "Tilapia Fish", "fish", "tilapia fish"],
    ["p30", "Hilsa (Ilish)", "fish", "hilsa ilish fish"],
    ["p31", "Prawns (Large)", "fish", "jumbo prawns shrimp"],
    ["p32", "Katla Fish", "fish", "katla fish"],
    ["p33", "Shrimp (Medium)", "fish", "medium shrimp"],
    ["p34", "Chicken (Broiler)", "meat", "broiler chicken"],
    ["p35", "Chicken (Sonali)", "meat", "free range chicken"],
    ["p36", "Beef (Premium Cut)", "meat", "premium beef"],
    ["p37", "Mutton (Curry Cut)", "meat", "mutton curry"],
    ["p38", "Beef Liver", "meat", "beef liver"],
    ["p39", "Farm Eggs (Dozen)", "dairy_eggs", "farm eggs dozen"],
    ["p40", "Fresh Cow Milk", "dairy_eggs", "fresh cow milk"],
    ["p41", "Full Cream Milk", "dairy_eggs", "full cream milk"],
    ["p42", "Mishti Doi", "dairy_eggs", "mishti doi sweet yogurt"],
    ["p43", "Fresh Paneer", "dairy_eggs", "fresh paneer"],
    ["p44", "Butter (Block)", "dairy_eggs", "butter block"],
    ["p45", "Banana (Sagor)", "fruits", "bananas sagor"],
    ["p46", "Apple (Red)", "fruits", "red apples"],
    ["p47", "Mango (Himsagar)", "fruits", "himsagar mango"],
    ["p48", "Mango (Fazli)", "fruits", "fazli mango"],
    ["p49", "Watermelon", "fruits", "watermelon"],
    ["p50", "Orange", "fruits", "oranges"],
    ["p51", "Toothpaste (Colgate)", "fmcg", "colgate toothpaste"],
    ["p52", "Dove Soap", "fmcg", "dove soap bar"],
    ["p53", "Washing Powder", "fmcg", "washing powder detergent"],
    ["p54", "Shampoo (Sunsilk)", "fmcg", "sunsilk shampoo"],
    ["p55", "Coca-Cola (1.5L)", "beverages", "coca cola bottle"],
    ["p56", "Pepsi (2L)", "beverages", "pepsi bottle"],
    ["p57", "7UP (2L)", "beverages", "7up lemon drink"],
    ["p58", "Mineral Water (2L)", "beverages", "mineral water bottle"],
    ["p59", "Tea (Ispahani)", "beverages", "ispahani tea"],
    ["p60", "Parle-G Biscuits", "snacks", "parle g biscuits"],
    ["p61", "Lays Classic Chips", "snacks", "lays chips"],
    ["p62", "Chicken Momos", "snacks", "chicken momos"],
    ["p63", "Maggi Noodles", "snacks", "maggi noodles"],
    ["p64", "Marie Biscuits", "snacks", "marie biscuits"],
    ["p65", "Salt (Premium)", "oil_spices", "iodized salt"],
]

CATEGORY_SVGS = {
    "rice_dal": "images/rice_dal.svg",
    "oil_spices": "images/oil_spices.svg",
    "vegetables": "images/vegetables.svg",
    "fish": "images/fish.svg",
    "meat": "images/meat.svg",
    "dairy_eggs": "images/dairy_eggs.svg",
    "fruits": "images/fruits.svg",
    "fmcg": "images/fmcg.svg",
    "beverages": "images/beverages.svg",
    "snacks": "images/snacks.svg",
}

CATALOG_DIR = Path(__file__).resolve().parent.parent / "src" / "web" / "catalog"
IMAGES_DIR = CATALOG_DIR / "images"

# Unsplash Source API (no key required for reasonable usage)
UNSPLASH_URL = "https://source.unsplash.com/400x400/?{query}"

# Alternative: Picsum Photos (reliable fallback)
PICSUM_URL = "https://picsum.photos/400/400?random={seed}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; JGMart-ImageBot/1.0)",
    "Accept": "image/jpeg,image/*,*/*",
}


def get_image_path(product_id: str) -> Path:
    """Get the expected JPG path for a product ID."""
    num = product_id[1:].zfill(3)
    return IMAGES_DIR / f"p{num}.jpg"


def download_image(url: str, dest: Path, timeout: int = 15) -> bool:
    """Download image from URL to destination path."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return False
            data = resp.read()
            if len(data) < 1024:  # Too small, probably error page
                return False
            dest.write_bytes(data)
            return True
    except Exception as e:
        print(f"    ⚠ Download failed: {e}")
        return False


def create_fallback_jpg(product_id: str, category: str) -> bool:
    """Create a simple JPG fallback from category SVG (copy SVG as JPG for now).
    In production, you'd use Pillow to render text on colored background."""
    svg_path = IMAGES_DIR / CATEGORY_SVGS.get(category, "images/placeholder.svg")
    jpg_path = get_image_path(product_id)

    # If SVG exists, copy it as a placeholder JPG
    # The catalog's onerror will show emoji anyway, so this is just for completeness
    if svg_path.exists():
        try:
            # Read SVG and create a minimal JPG header + SVG content
            # This is a hack: browsers will render it, and onerror shows emoji
            svg_content = svg_path.read_text(encoding="utf-8")
            jpg_path.write_bytes(svg_content.encode("utf-8"))
            return True
        except Exception:
            pass
    return False


def main():
    reset = "--reset" in sys.argv
    limit = None
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
            break

    if not IMAGES_DIR.exists():
        print(f"❌ Images directory not found: {IMAGES_DIR}")
        sys.exit(1)

    print(f"📁 Images directory: {IMAGES_DIR}")
    print(f"🔄 Reset mode: {'YES' if reset else 'NO'}")
    print(
        f"📊 Products to process: {len(PRODUCTS[:limit]) if limit else len(PRODUCTS)}"
    )
    print()

    downloaded = 0
    skipped = 0
    failed = 0

    for prod in PRODUCTS[:limit] if limit else PRODUCTS:
        pid, name, category, query = prod
        dest = get_image_path(pid)

        # Skip if exists and not reset mode
        if dest.exists() and not reset:
            skipped += 1
            continue

        print(f"⬇ {pid} — {name} ({query})")

        # Try Unsplash first
        url = UNSPLASH_URL.format(query=urllib.parse.quote(query))
        if download_image(url, dest):
            print(f"  ✅ Downloaded from Unsplash")
            downloaded += 1
        else:
            # Fallback: create placeholder
            if create_fallback_jpg(pid, category):
                print(f"  ⚠ Using category SVG fallback")
                downloaded += 1
            else:
                print(f"  ❌ Failed completely")
                failed += 1

        # Be polite to free APIs
        time.sleep(0.5)

    print()
    print("=" * 50)
    print(f"✅ Downloaded/Created: {downloaded}")
    print(f"⏭ Skipped (exists):    {skipped}")
    print(f"❌ Failed:              {failed}")
    print(f"📁 Total in folder:     {len(list(IMAGES_DIR.glob('p*.jpg')))}")
    print("=" * 50)


if __name__ == "__main__":
    main()
