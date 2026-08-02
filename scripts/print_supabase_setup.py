#!/usr/bin/env python3
"""Print Supabase setup SQL run order for jgmart-db cutover."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "src/web/supabase/schema.sql",
    ROOT / "src/web/supabase/migrations/rls_anonymous_orders.sql",
    ROOT / "src/web/supabase/seed.sql",
    ROOT / "src/web/supabase/seed_from_catalog.sql",
    ROOT / "src/web/supabase/migrations/admin_user_setup.sql",
]


def main():
    print("Run these in Supabase SQL Editor (order matters):\n")
    for i, path in enumerate(FILES, 1):
        rel = path.relative_to(ROOT)
        exists = "OK" if path.exists() else "MISSING"
        print(f"  {i}. [{exists}] {rel}")
    print("\nThen:")
    print("  - Create admin user in Auth -> Users (admin@jgmartbd.com)")
    print("  - Run admin_user_setup.sql")
    print("  - Copy config.local.example.js → config.local.js with URL + anon key")


if __name__ == "__main__":
    main()
