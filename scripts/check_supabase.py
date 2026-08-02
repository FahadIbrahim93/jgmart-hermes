#!/usr/bin/env python3
"""Verify Supabase setup: tables, counts, RLS health."""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cfg = ROOT / "src/web/supabase/config.local.js"
text = cfg.read_text(encoding="utf-8")
url_m = re.search(r"SUPABASE_URL\s*=\s*['\"]([^'\"]+)", text) or re.search(
    r"url:\s*['\"]([^'\"]+)", text
)
key_m = re.search(r"SUPABASE_ANON_KEY\s*=\s*['\"]([^'\"]+)", text) or re.search(
    r"anonKey:\s*['\"]([^'\"]+)", text
)
if not url_m or not key_m:
    print("FAIL: config.local.js missing url or anon key")
    sys.exit(1)

url, key = url_m.group(1), key_m.group(1)
headers = {"apikey": key, "Authorization": f"Bearer {key}"}


def get(path):
    req = urllib.request.Request(f"{url}{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.status, json.loads(resp.read().decode())


def try_get(label, path):
    try:
        status, data = get(path)
        count = len(data) if isinstance(data, list) else 1
        print(f"OK   {label}: HTTP {status}, rows={count}")
        return True, data
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"FAIL {label}: HTTP {e.code}")
        try:
            err = json.loads(body)
            print(f"      {err.get('message', body[:120])}")
        except json.JSONDecodeError:
            print(f"      {body[:120]}")
        return False, None


print("Supabase verification\n" + "=" * 40)
ok_products, products = try_get("products", "/rest/v1/products?select=id,name&limit=5")
ok_categories, _ = try_get("categories", "/rest/v1/categories?select=id")
ok_orders, _ = try_get("orders", "/rest/v1/orders?select=id&limit=1")

if ok_products:
    try:
        _, all_products = get("/rest/v1/products?select=id")
        print(f"\nProduct count: {len(all_products)} (expected 65)")
        if len(all_products) == 65:
            print("PASS product seed")
        elif len(all_products) > 0:
            print("WARN product seed incomplete")
        else:
            print("FAIL no products seeded")
    except Exception as e:
        print(f"WARN could not count products: {e}")

if not (ok_products and ok_categories):
    print(
        "\nLikely fix: run src/web/supabase/migrations/fix_profiles_rls.sql in SQL Editor"
    )
    sys.exit(1)

print("\nOverall: Supabase looks healthy")
sys.exit(0)
