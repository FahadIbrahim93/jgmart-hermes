#!/usr/bin/env python3
"""
Add placeholder image URLs to all products in catalog_data.json.
Uses placehold.co with a green theme matching JGMart branding.
"""

import json
import os
import urllib.parse

CATALOG_PATH = "G:/JGC Mart/JGC Mart - Hermes/06_Web_Catalog/catalog_data.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

added = 0
for product in catalog["products"]:
    if "image" not in product:
        name = product["name"]
        emoji = product.get("image_emoji", "🛒")
        # Create a meaningful URL-safe label with emoji and product name
        label = f"{emoji} {name}"
        encoded = urllib.parse.quote(label)
        # Green background (#2E7D32), white text, 400x400
        product["image"] = f"https://placehold.co/400x400/2E7D32/FFF?text={encoded}"
        added += 1

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"✅ Added image URLs to {added} products in catalog_data.json")
