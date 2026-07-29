#!/usr/bin/env python3
"""
JG Mart — Product Image Generator
Generates high-quality SVG product images for the catalog.
No external dependencies, works offline, instant loading.

Usage:
    python generate_product_images.py
    python generate_product_images.py --reset

Features:
    - Category-themed gradient backgrounds
    - Large product emoji
    - Product name text
    - Consistent brand colors
    - 400x400px output
"""

import os
import sys
from pathlib import Path

# Product definitions: [id, name, category, emoji, search_term_for_future_real_images]
PRODUCTS = [
    ["p01", "Premium Miniket Rice", "rice_dal", "🍚"],
    ["p02", "Chinigura Rice", "rice_dal", "🍚"],
    ["p03", "Nazirshail Rice", "rice_dal", "🍚"],
    ["p04", "Basmati Rice", "rice_dal", "🍚"],
    ["p05", "Moshur Dal (Red)", "rice_dal", "🟠"],
    ["p06", "Moong Dal (Yellow)", "rice_dal", "🟡"],
    ["p07", "Chola (Bengal Gram)", "rice_dal", "🟤"],
    ["p08", "Soybean Oil", "oil_spices", "🫗"],
    ["p09", "Mustard Oil", "oil_spices", "🫗"],
    ["p10", "Sunflower Oil", "oil_spices", "🌻"],
    ["p11", "Turmeric Powder", "oil_spices", "🧡"],
    ["p12", "Chili Powder", "oil_spices", "🌶️"],
    ["p13", "Cumin Powder", "oil_spices", "🟤"],
    ["p14", "Coriander Powder", "oil_spices", "🌿"],
    ["p15", "White Sugar", "oil_spices", "🍚"],
    ["p16", "Potato", "vegetables", "🥔"],
    ["p17", "Red Onion", "vegetables", "🧅"],
    ["p18", "Tomato", "vegetables", "🍅"],
    ["p19", "Eggplant (Brinjal)", "vegetables", "🍆"],
    ["p20", "Cauliflower", "vegetables", "🥦"],
    ["p21", "Cabbage", "vegetables", "🥬"],
    ["p22", "Green Chili", "vegetables", "🌶️"],
    ["p23", "Coriander Leaves", "vegetables", "🌿"],
    ["p24", "Lady Finger (Okra)", "vegetables", "🥒"],
    ["p25", "Green Papaya", "vegetables", "🫛"],
    ["p26", "Fresh Ginger", "vegetables", "🫚"],
    ["p27", "Fresh Garlic", "vegetables", "🧄"],
    ["p28", "Ruhi Fish", "fish", "🐟"],
    ["p29", "Tilapia Fish", "fish", "🐟"],
    ["p30", "Hilsa (Ilish)", "fish", "🐟"],
    ["p31", "Prawns (Large)", "fish", "🦐"],
    ["p32", "Katla Fish", "fish", "🐟"],
    ["p33", "Shrimp (Medium)", "fish", "🦐"],
    ["p34", "Chicken (Broiler)", "meat", "🍗"],
    ["p35", "Chicken (Sonali)", "meat", "🐔"],
    ["p36", "Beef (Premium Cut)", "meat", "🥩"],
    ["p37", "Mutton (Curry Cut)", "meat", "🍖"],
    ["p38", "Beef Liver", "meat", "🥩"],
    ["p39", "Farm Eggs (Dozen)", "dairy_eggs", "🥚"],
    ["p40", "Fresh Cow Milk", "dairy_eggs", "🥛"],
    ["p41", "Full Cream Milk", "dairy_eggs", "🥛"],
    ["p42", "Mishti Doi", "dairy_eggs", "🍯"],
    ["p43", "Fresh Paneer", "dairy_eggs", "🧀"],
    ["p44", "Butter (Block)", "dairy_eggs", "🧈"],
    ["p45", "Banana (Sagor)", "fruits", "🍌"],
    ["p46", "Apple (Red)", "fruits", "🍎"],
    ["p47", "Mango (Himsagar)", "fruits", "🥭"],
    ["p48", "Mango (Fazli)", "fruits", "🥭"],
    ["p49", "Watermelon", "fruits", "🍉"],
    ["p50", "Orange", "fruits", "🍊"],
    ["p51", "Toothpaste (Colgate)", "fmcg", "🪥"],
    ["p52", "Dove Soap", "fmcg", "🧼"],
    ["p53", "Washing Powder", "fmcg", "🧺"],
    ["p54", "Shampoo (Sunsilk)", "fmcg", "🧴"],
    ["p55", "Coca-Cola (1.5L)", "beverages", "🥤"],
    ["p56", "Pepsi (2L)", "beverages", "🥤"],
    ["p57", "7UP (2L)", "beverages", "🥤"],
    ["p58", "Mineral Water (2L)", "beverages", "💧"],
    ["p59", "Tea (Ispahani)", "beverages", "🫖"],
    ["p60", "Parle-G Biscuits", "snacks", "🍪"],
    ["p61", "Lays Classic Chips", "snacks", "🍟"],
    ["p62", "Chicken Momos", "snacks", "🥟"],
    ["p63", "Maggi Noodles", "snacks", "🍜"],
    ["p64", "Marie Biscuits", "snacks", "🍪"],
    ["p65", "Salt (Premium)", "oil_spices", "🧂"],
]

CATEGORY_COLORS = {
    "rice_dal": {"start": "#FFF8E1", "end": "#FFECB3", "text": "#5D4037"},
    "oil_spices": {"start": "#FFF3E0", "end": "#FFE0B2", "text": "#5D4037"},
    "vegetables": {"start": "#E8F5E9", "end": "#C8E6C9", "text": "#2E7D32"},
    "fish": {"start": "#E3F2FD", "end": "#BBDEFB", "text": "#1565C0"},
    "meat": {"start": "#FBE9E7", "end": "#FFCCBC", "text": "#BF360C"},
    "dairy_eggs": {"start": "#FFFDE7", "end": "#FFF9C4", "text": "#5D4037"},
    "fruits": {"start": "#FCE4EC", "end": "#F8BBD0", "text": "#C2185B"},
    "fmcg": {"start": "#F3E5F5", "end": "#E1BEE7", "text": "#6A1B9A"},
    "beverages": {"start": "#E0F7FA", "end": "#B2EBF2", "text": "#00695C"},
    "snacks": {"start": "#FFF3E0", "end": "#FFE0B2", "text": "#E65100"},
}

BRAND_COLORS = {
    "primary": "#00442D",
    "gold": "#c9a227",
    "white": "#ffffff",
    "dark": "#1a1a1a",
}

SCRIPT_DIR = Path(__file__).resolve().parent
IMAGES_DIR = SCRIPT_DIR.parent / "src" / "web" / "catalog" / "images"


def generate_product_svg(product_id: str, name: str, category: str, emoji: str) -> str:
    """Generate a product card SVG."""
    colors = CATEGORY_COLORS.get(category, {"start": "#f5f7f5", "end": "#e8f5ef", "text": "#1a1a1a"})
    
    # Truncate long names
    display_name = name if len(name) <= 20 else name[:18] + ".."
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors["start"]};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors["end"]};stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="400" height="400" fill="url(#bg)" rx="16"/>
  
  <!-- Category indicator bar -->
  <rect x="0" y="0" width="400" height="8" fill="{BRAND_COLORS["primary"]}" rx="16"/>
  
  <!-- Emoji area -->
  <text x="200" y="180" text-anchor="middle" font-size="120" dominant-baseline="middle">{emoji}</text>
  
  <!-- Product name -->
  <text x="200" y="280" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="700" fill="{colors["text"]}">{display_name}</text>
  
  <!-- JG Mart branding -->
  <text x="200" y="320" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="{BRAND_COLORS["primary"]}">JG Mart</text>
  
  <!-- Price placeholder (admin can update) -->
  <text x="200" y="355" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="{BRAND_COLORS["gold"]}">৳ ---</text>
  
  <!-- Corner accent -->
  <circle cx="360" cy="40" r="30" fill="{BRAND_COLORS["gold"]}" opacity="0.2"/>
  <text x="360" y="45" text-anchor="middle" font-size="16">⭐</text>
</svg>'''
    return svg


def generate_category_svg(category_id: str, label_en: str, label_bn: str, emoji: str) -> str:
    """Generate a category placeholder SVG."""
    colors = CATEGORY_COLORS.get(category_id, {"start": "#f5f7f5", "end": "#e8f5ef", "text": "#1a1a1a"})
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 220" width="300" height="220">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors["start"]};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors["end"]};stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="300" height="220" fill="url(#bg)" rx="12"/>
  
  <!-- Top bar -->
  <rect x="0" y="0" width="300" height="6" fill="{BRAND_COLORS["primary"]}" rx="12"/>
  
  <!-- Emoji -->
  <text x="150" y="90" text-anchor="middle" font-size="64">{emoji}</text>
  
  <!-- Category name -->
  <text x="150" y="140" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="{colors["text"]}">{label_en}</text>
  <text x="150" y="170" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="600" fill="{colors["text"]}" opacity="0.8">{label_bn}</text>
  
  <!-- JG Mart branding -->
  <text x="150" y="200" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" fill="{BRAND_COLORS["primary"]}">JG Mart</text>
</svg>'''
    return svg


def main():
    reset = "--reset" in sys.argv
    
    if not IMAGES_DIR.exists():
        print(f"❌ Images directory not found: {IMAGES_DIR}")
        sys.exit(1)
    
    print(f"📁 Images directory: {IMAGES_DIR}")
    print(f"🔄 Reset mode: {'YES' if reset else 'NO'}")
    print()
    
    # Generate product images
    generated = 0
    skipped = 0
    
    for prod in PRODUCTS:
        pid, name, category, emoji = prod
        dest = IMAGES_DIR / f"{pid}.svg"
        
        if dest.exists() and not reset:
            skipped += 1
            continue
        
        svg = generate_product_svg(pid, name, category, emoji)
        dest.write_text(svg, encoding="utf-8")
        generated += 1
        print(f"  ✅ {pid} — {name}")
    
    print()
    print(f"Product images: {generated} generated, {skipped} skipped")
    
    # Generate/update category SVGs
    categories = [
        ("rice_dal", "Rice & Dal", "চাল ও ডাল", "🍚"),
        ("oil_spices", "Oil & Spices", "তেল ও মশলা", "🧂"),
        ("vegetables", "Vegetables", "সবজি", "🥬"),
        ("fish", "Fish", "মাছ", "🐟"),
        ("meat", "Meat", "মাংস", "🍗"),
        ("dairy_eggs", "Dairy & Eggs", "দুধ ও ডিম", "🥛"),
        ("fruits", "Fruits", "ফল", "🍎"),
        ("fmcg", "Household", "গৃহস্থালি", "🧴"),
        ("beverages", "Drinks", "পানীয়", "🥤"),
        ("snacks", "Snacks", "স্ন্যাকস", "🍪"),
    ]
    
    cat_generated = 0
    cat_skipped = 0
    
    for cat_id, label_en, label_bn, emoji in categories:
        dest = IMAGES_DIR / f"{cat_id}.svg"
        
        if dest.exists() and not reset:
            cat_skipped += 1
            continue
        
        svg = generate_category_svg(cat_id, label_en, label_bn, emoji)
        dest.write_text(svg, encoding="utf-8")
        cat_generated += 1
        print(f"  📂 {cat_id}.svg")
    
    print()
    print(f"Category images: {cat_generated} generated, {cat_skipped} skipped")
    print()
    print("=" * 50)
    print(f"Total images in folder: {len(list(IMAGES_DIR.glob('*.svg')) + list(IMAGES_DIR.glob('*.jpg')))}")
    print("=" * 50)
    print()
    print("💡 Note: These are high-quality SVG placeholders.")
    print("   For real photos, run: python download_product_images.py")
    print("   when external APIs are available.")


if __name__ == "__main__":
    main()
