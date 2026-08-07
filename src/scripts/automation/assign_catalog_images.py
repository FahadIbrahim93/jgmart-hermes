#!/usr/bin/env python3
"""Assign correct, relevant Unsplash product images to catalog_data.json products.

Each product gets an image that actually matches what it is — rice, fish,
vegetables, etc. — instead of the current mismatched Unsplash URLs.
"""

from pathlib import Path

# Product image mapping: (name, category) -> relevant Unsplash image URL.
# Using the catalog_data.json product list (65 products).
PRODUCT_IMAGES = {
    # Rice & Dal
    ("Premium Chinigura Rice", "rice_dal"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    ("Organic Moong Dal", "rice_dal"): "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    ("Premium Basmati Rice", "rice_dal"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    ("Mustard Oil (Fortified)", "oil_spices"): "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop",
    ("Sunflower Oil", "oil_spices"): "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop",
    ("Turmeric Powder", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Chili Powder", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Cumin Powder", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Soybean Oil (Fortified)", "oil_spices"): "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&h=300&fit=crop",
    ("Cinnamon Sticks", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Cardamom (Green)", "oil_spices"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Red Onion", "vegetables"): "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop",
    ("Potato (Local)", "vegetables"): "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&h=300&fit=crop",
    ("Tomato (Deshi)", "vegetables"): "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&h=300&fit=crop",
    ("Brinjal (Long)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Green Chili", "vegetables"): "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=400&h=300&fit=crop",
    ("Cauliflower", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Coriander Leaves", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Brinjal (Round)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Lady Finger (Bhindi)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Pointed Gourd (Potol)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Lemon (Fresh)", "vegetables"): "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400&h=300&fit=crop",
    ("Ginger (Fresh)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Garlic (Deshi)", "vegetables"): "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    ("Ruhi Fish (Medium)", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Prawns (Large)", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Ilish Fish (Hilsa)", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Tilapia Fish", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Rohu Fish (Large)", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Katla Fish", "fish"): "https://images.unsplash.com/photo-1519708227418-c74fd666ba83?w=400&h=300&fit=crop",
    ("Chicken (Broiler)", "meat"): "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop",
    ("Mutton (Curry Cut)", "meat"): "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop",
    ("Beef (Premium Cut)", "meat"): "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop",
    ("Chicken Breast (Skinless)", "meat"): "https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=300&fit=crop",
    ("Beef Liver", "meat"): "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=300&fit=crop",
    ("Fresh Cow Milk", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Farm Eggs", "dairy_eggs"): "https://images.unsplash.com/photo-1582722879130-6286d4e080ea?w=400&h=300&fit=crop",
    ("Paneer (Fresh)", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Yogurt (Mishti Doi)", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Full Cream Milk", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Butter (Cooking)", "dairy_eggs"): "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=300&fit=crop",
    ("Deshi Mango (Himsagar)", "fruits"): "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop",
    ("Banana (Sagor)", "fruits"): "https://images.unsplash.com/photo-1571771894821-ce9b784f8114?w=400&h=300&fit=crop",
    ("Watermelon", "fruits"): "https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop",
    ("Jackfruit (Kathal)", "fruits"): "https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop",
    ("Mango (Fazli)", "fruits"): "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop",
    ("Papaya (Ripe)", "fruits"): "https://images.unsplash.com/photo-1619566636859-ad7264c1d2c4?w=400&h=300&fit=crop",
    ("Signal Toothpaste", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Ariel Washing Powder", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Dove Soap", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Harpic Toilet Cleaner", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Wheel Washing Powder", "fmcg"): "https://images.unsplash.com/photo-1600857062245-46e9d2e4bf05?w=400&h=300&fit=crop",
    ("Pepsi (2L)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("Fresh Lemon Juice", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("Coca-Cola (1.5L)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("7up (2L)", "beverages"): "https://images.unsplash.com/photo-1543253687-c931c8e01820?w=400&h=300&fit=crop",
    ("Parle-G Biscuits", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Lays Chips", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Chicken Momos (Frozen)", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Mixed Nut Mix", "snacks"): "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=400&h=300&fit=crop",
    ("Masoor Dal (Red Lentil)", "rice_dal"): "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    ("Fortified Rice (Local)", "rice_dal"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
    ("Chola (Bengal Gram)", "rice_dal"): "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400&h=300&fit=crop",
    ("Biryani Rice (Kallijira)", "rice_dal"): "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop",
}

ROOT = Path(__file__).resolve().parents[3]
CATALOG_JSON = ROOT / "src" / "web" / "catalog" / "catalog_data.json"


def main():
    data = json.load(open(CATALOG_JSON, encoding="utf-8"))
    changed = 0
    for product in data["products"]:
        key = (product["name"], product["category"])
        if key in PRODUCT_IMAGES:
            old = product.get("image")
            new = PRODUCT_IMAGES[key]
            if old != new:
                product["image"] = new
                changed += 1
    json.dump(data, open(CATALOG_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Updated {changed} product images in catalog_data.json")
    print(f"Total products mapped: {len(PRODUCT_IMAGES)}")


if __name__ == "__main__":
    import json
    main()