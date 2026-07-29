#!/usr/bin/env python3
"""
Sync catalog_data.json products into Supabase-compatible SQL seed file.

Usage:
  python src/scripts/automation/sync_catalog_to_supabase.py
  python src/scripts/automation/sync_catalog_to_supabase.py --output src/web/supabase/seed_from_catalog.sql

With live sync (requires SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY in env):
  python src/scripts/automation/sync_catalog_to_supabase.py --push
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CATALOG_JSON = ROOT / "src" / "web" / "catalog" / "catalog_data.json"
DEFAULT_OUTPUT = ROOT / "src" / "web" / "supabase" / "seed_from_catalog.sql"


def legacy_uuid(legacy_id: str) -> str:
    """Deterministic UUID from legacy product id (p001, p01, etc.)."""
    namespace = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    return str(uuid.uuid5(namespace, f"jg-mart-{legacy_id}"))


def sql_escape(value: str) -> str:
    return value.replace("'", "''")


def build_sql(products: list[dict]) -> str:
    lines = [
        "-- Auto-generated from catalog_data.json",
        "-- Run AFTER schema.sql in Supabase SQL Editor",
        "",
    ]

    for index, product in enumerate(products):
        pid = legacy_uuid(product["id"])
        category = sql_escape(product.get("category", "fmcg"))
        name = sql_escape(product.get("name", "Product"))
        name_bn = sql_escape(product.get("name_bn", ""))
        desc = sql_escape(product.get("desc", ""))
        desc_bn = sql_escape(product.get("desc_bn", ""))
        price = int(product.get("price", 0))
        unit = sql_escape(product.get("unit", "pc"))
        emoji = sql_escape(product.get("emoji", "🛒"))
        image = sql_escape(product.get("image", ""))
        in_stock = product.get("stock_status", "in_stock") != "out_of_stock"
        featured = index < 6
        sort_order = index + 1
        metadata = json.dumps(
            {"legacy_id": product["id"], "emoji": product.get("emoji", "🛒")}
        )

        lines.append(f"""INSERT INTO public.products (
  id, category_id, name, name_bn, description, description_bn,
  price, unit, image_url, in_stock, is_featured, sort_order, metadata
) VALUES (
  '{pid}', '{category}', '{name}', '{name_bn}', '{desc}', '{desc_bn}',
  {price}, '{unit}', '{image}', {str(in_stock).lower()}, {str(featured).lower()}, {sort_order}, '{metadata}'::jsonb
) ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  price = EXCLUDED.price,
  in_stock = EXCLUDED.in_stock,
  updated_at = NOW();
""")

    return "\n".join(lines)


def push_to_supabase(products: list[dict]) -> None:
    try:
        import requests
    except ImportError:
        print("Install requests: pip install requests", file=sys.stderr)
        sys.exit(1)

    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key:
        print(
            "Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY to use --push",
            file=sys.stderr,
        )
        sys.exit(1)

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }

    rows = []
    for index, product in enumerate(products):
        rows.append(
            {
                "id": legacy_uuid(product["id"]),
                "category_id": product.get("category", "fmcg"),
                "name": product.get("name"),
                "name_bn": product.get("name_bn"),
                "description": product.get("desc"),
                "description_bn": product.get("desc_bn"),
                "price": int(product.get("price", 0)),
                "unit": product.get("unit", "pc"),
                "image_url": product.get("image"),
                "in_stock": product.get("stock_status", "in_stock") != "out_of_stock",
                "is_featured": index < 6,
                "sort_order": index + 1,
                "metadata": {
                    "legacy_id": product["id"],
                    "emoji": product.get("emoji", "🛒"),
                },
            }
        )

    response = requests.post(
        f"{url}/rest/v1/products",
        headers=headers,
        json=rows,
        timeout=60,
    )
    if not response.ok:
        print(
            f"Supabase push failed: {response.status_code} {response.text}",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Pushed {len(rows)} products to Supabase.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync catalog JSON to Supabase SQL/API"
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--push", action="store_true", help="Push directly to Supabase REST API"
    )
    args = parser.parse_args()

    if not CATALOG_JSON.exists():
        print(f"Missing {CATALOG_JSON}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    products = data.get("products", [])
    if not products:
        print("No products in catalog_data.json", file=sys.stderr)
        sys.exit(1)

    sql = build_sql(products)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(sql, encoding="utf-8")
    print(f"Wrote {len(products)} products to {args.output}")

    if args.push:
        push_to_supabase(products)


if __name__ == "__main__":
    main()
