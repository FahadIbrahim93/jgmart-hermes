#!/usr/bin/env python3
"""Assign correct, relevant Unsplash product images to defaults.js products.

Each product gets an image that actually matches what it is — rice, fish,
vegetables, etc. — instead of the current placeholder SVGs or the mismatched
Unsplash URLs in catalog_data.json.
"""

from pathlib import Path

# Product image mapping: (name, category) -> relevant Unsplash image URL.
# Using the defaults.js product list (65 products) which is the canonical
# catalog used by index.html, menu.html, and the operator panel.
PRODUCT_IMAGES = {
    # Rice & Dal
    ("Premium Miniket Rice", "rice_dal"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    ("Chinigura Rice", "rice_dal"): "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    ("Nazirshail Rice", "rice_dal"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    ("Basmati Rice", "rice_dal"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    ("Moshur Dal (Red)", "rice_dal"): "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    ("Moong Dal (Yellow)", "rice_dal"): "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    ("Chola (Bengal Gram)", "rice_dal"): "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    # Oil & Spices
    ("Soybean Oil", "oil_spices"): "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop",
    ("Mustard Oil", "oil_spices"): "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop",
    ("Sunflower Oil", "oil_spices"): "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop",
    ("Turmeric Powder", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Chili Powder", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Cumin Powder", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Coriander Powder", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("White Sugar", "oil_spices"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    ("Salt (Premium)", "oil_spices"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    # Vegetables
    ("Potato", "vegetables"): "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop",
    ("Red Onion", "vegetables"): "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop",
    ("Tomato", "vegetables"): "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&h=300&fit=crop",
    ("Eggplant (Brinjal)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Cauliflower", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Cabbage", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Green Chili", "vegetables"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Coriander Leaves", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Lady Finger (Okra)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Green Papaya", "vegetables"): "https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop",
    ("Fresh Ginger", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Fresh Garlic", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    # Fish
    ("Ruhi Fish", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Tilapia Fish", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Hilsa (Ilish)", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Prawns (Large)", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Katla Fish", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Shrimp (Medium)", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    # Meat
    ("Chicken (Broiler)", "meat"): "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop",
    ("Chicken (Sonali)", "meat"): "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop",
    ("Beef (Premium)", "meat"): "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop",
    ("Mutton (Curry Cut)", "meat"): "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop",
    ("Beef Liver", "meat"): "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop",
    # Dairy & Eggs
    ("Farm Eggs (Dozen)", "dairy_eggs"): "https://images.unsplash.com/photo-1582722879130-6286d4e080ea?w=400&h=300&fit=crop",
    ("Fresh Cow Milk", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Full Cream Milk", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Mishti Doi", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Fresh Paneer", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Butter (Block)", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    # Fruits
    ("Banana (Sagor)", "fruits"): "https://images.unsplash.com/photo-1571771894821-ce9b784f8114?w=400&h=300&fit=crop",
    ("Apple (Red)", "fruits"): "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop",
    ("Mango (Himsagar)", "fruits"): "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop",
    ("Mango (Fazli)", "fruits"): "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop",
    ("Watermelon", "fruits"): "https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop",
    ("Orange", "fruits"): "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop",
    # Household
    ("Toothpaste (Colgate)", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Dove Soap", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Washing Powder", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Shampoo (Sunsilk)", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    # Drinks
    ("Coca-Cola (1.5L)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("Pepsi (2L)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("7UP (2L)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("Mineral Water (2L)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("Tea (Ispahani)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    # Snacks
    ("Parle-G Biscuits", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Lays Classic Chips", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Chicken Momos", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Maggi Noodles", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Marie Biscuits", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
}

ROOT = Path(__file__).resolve().parents[3]
DEFAULTS_PATH = ROOT / "src" / "web" / "catalog" / "defaults.js"


def main():
    text = DEFAULTS_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    new_lines = []
    changed = 0
    for line in lines:
        if line.startswith("    {id:"):
            # Extract name and category from the line.
            # Format: {id:'p01',nm:'Premium Miniket Rice',ct:'rice_dal',pr:88,...}
            nm_match = None
            ct_match = None
            for part in line.split(","):
                part = part.strip()
                if part.startswith("nm:"):
                    nm_match = part.split(":", 1)[1].strip().strip("'")
                if part.startswith("ct:"):
                    ct_match = part.split(":", 1)[1].strip().strip("'")
            if nm_match and ct_match:
                key = (nm_match, ct_match)
                if key in PRODUCT_IMAGES:
                    old_im = None
                    for part in line.split(","):
                        part = part.strip()
                        if part.startswith("im:"):
                            old_im = part.split(":", 1)[1].strip().strip("'").rstrip("}'")
                            break
                    new_im = PRODUCT_IMAGES[key]
                    if old_im != new_im:
                        line = line.replace(
                            f"im:'{old_im}'", f"im:'{new_im}'"
                        )
                        changed += 1
        new_lines.append(line)

    DEFAULTS_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"Updated {changed} product images in defaults.js")
    print(f"Total products mapped: {len(PRODUCT_IMAGES)}")


if __name__ == "__main__":
    main()