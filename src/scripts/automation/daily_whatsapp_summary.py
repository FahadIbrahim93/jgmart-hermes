#!/usr/bin/env python3
"""
JG Mart — Daily WhatsApp Summary Generator
============================================
Hyperlocal grocery delivery — Japan Garden City, Mohammadpur, Dhaka.

Generates a formatted daily summary message that Fahad can copy-paste
directly to his WhatsApp broadcast group.

Reads real order data from exported JSON files (jgmart_orders_YYYY-MM-DD.json)
and picks today's specials from the catalog. When no real order data is
found, uses sensible placeholder counts so the message template stays usable.

USAGE:
    python daily_whatsapp_summary.py                # today's summary (placeholders if no data)
    python daily_whatsapp_summary.py --date 2026-08-01
    python daily_whatsapp_summary.py --send          # copy to clipboard
    python daily_whatsapp_summary.py --send --date 2026-08-01
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from collections import Counter

# ─── PATHS ────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.resolve()
CATALOG_DIR = PROJECT_ROOT / "06_Web_Catalog"
EXPORT_DIR = SCRIPT_DIR  # 09_Data_Export

CATALOG_PATH = CATALOG_DIR / "catalog_data.json"
CATALOG_HTML = CATALOG_DIR / "index.html"

# Date of the session (today in the simulation)
# We set a fixed reference date since the simulation runs on a specific day
SESSION_DATE = date(2026, 8, 1)  # The toolkit session date

# ─── WHATSAPP NUMBER ──────────────────────────────────────────────────────
WHATSAPP_NUMBER = "8801870489448"


# ═══════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════


def load_catalog():
    """Load product catalog from catalog_data.json."""
    if not CATALOG_PATH.exists():
        print(f"⚠️  Catalog not found: {CATALOG_PATH}", file=sys.stderr)
        return {"products": [], "categories": []}
    try:
        with open(CATALOG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️  Error reading catalog: {e}", file=sys.stderr)
        return {"products": [], "categories": []}


def find_data_files(target_date: date):
    """Find all order/data/finance JSON files for the given date in the export dir.

    Returns dict with 'orders', 'data', 'finance' keys (or None if not found).
    """
    date_str = target_date.strftime("%Y-%m-%d")
    result = {"orders": None, "data": None, "finance": None}

    orders_file = EXPORT_DIR / f"jgmart_orders_{date_str}.json"
    data_file = EXPORT_DIR / f"jgmart_data_{date_str}.json"
    finance_file = EXPORT_DIR / f"jgmart_finance_{date_str}.json"

    for key, path in [
        ("orders", orders_file),
        ("data", data_file),
        ("finance", finance_file),
    ]:
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    result[key] = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️  Error reading {path.name}: {e}", file=sys.stderr)

    return result


def extract_products_from_html():
    """Fallback: try to extract product names from index.html if catalog JSON is missing."""
    if not CATALOG_HTML.exists():
        return []
    import re

    products = []
    try:
        html = CATALOG_HTML.read_text(encoding="utf-8")
        # Look for product patterns in the HTML — very basic extraction
        # This is a best-effort fallback
        product_blocks = re.findall(
            r'data-product-name=["\']([^"\']+)["\'].*?data-price=["\']([^"\']+)["\']',
            html,
        )
        for name, price in product_blocks:
            try:
                products.append({"name": name, "price": float(price)})
            except ValueError:
                products.append({"name": name, "price": 0})
    except OSError:
        pass
    return products


# ═══════════════════════════════════════════════════════════════════════════
#  ORDER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════


def analyze_orders(orders_data):
    """Analyze orders data and return summary stats.

    Returns dict with: order_count, revenue, items_sold, top_items,
    delivered_count, pending_count.
    """
    stats = {
        "order_count": 0,
        "revenue": 0,
        "items_sold": 0,
        "top_items": [],
        "delivered_count": 0,
        "pending_count": 0,
        "cancelled_count": 0,
    }

    if not orders_data or "orders" not in orders_data:
        return stats

    orders = orders_data["orders"]
    stats["order_count"] = len(orders)

    item_counter = Counter()
    for order in orders:
        status = order.get("status", "unknown")
        if status == "delivered":
            stats["delivered_count"] += 1
        elif status == "pending":
            stats["pending_count"] += 1
        elif status == "cancelled":
            stats["cancelled_count"] += 1

        stats["revenue"] += order.get("total", 0)

        items = order.get("items", [])
        stats["items_sold"] += sum(int(item.get("qty", 1)) for item in items)
        for item in items:
            item_counter[item.get("name", "Unknown")] += item.get("qty", 1)

    stats["top_items"] = item_counter.most_common(5)

    return stats


# ═══════════════════════════════════════════════════════════════════════════
#  TODAY'S SPECIALS (from catalog)
# ═══════════════════════════════════════════════════════════════════════════


def pick_todays_specials(catalog, count=4):
    """Pick featured products for today's specials section.

    Strategy: pick top-selling products (by 'orders' field) from fresh
    categories (fish, meat, fruits, vegetables) with a mix.
    """
    products = catalog.get("products", [])
    if not products:
        return []

    # Prioritise fresh categories
    fresh_cats = {"fish", "meat", "fruits", "vegetables", "dairy_eggs"}
    fresh = [p for p in products if p.get("category") in fresh_cats]
    other = [p for p in products if p.get("category") not in fresh_cats]

    # Sort by 'orders' count (descending), best sellers first
    fresh.sort(key=lambda p: p.get("orders", 0), reverse=True)
    other.sort(key=lambda p: p.get("orders", 0), reverse=True)

    # Pick from fresh first, fill with best-sellers from other categories
    selected = fresh[:count]
    if len(selected) < count:
        selected += other[: count - len(selected)]

    return selected


# ═══════════════════════════════════════════════════════════════════════════
#  MESSAGE FORMATTER
# ═══════════════════════════════════════════════════════════════════════════


def format_message(target_date, stats, specials, finance_data=None):
    """Format the full WhatsApp message as a string."""
    weekday_name = target_date.strftime("%A")
    date_formatted = target_date.strftime("%d %B, %Y")

    # ── Header ──────────────────────────────────────────────────────────
    lines = []
    lines.append(f"*JG Mart — Good Morning! 🌅*")
    lines.append(f"*Japan Garden City, Mohammadpur*")
    lines.append("")
    lines.append(f"📅 {weekday_name}, {date_formatted}")
    lines.append("")

    # ── Yesterday's Summary ─────────────────────────────────────────────
    lines.append("📦 *Yesterday's Summary:*")

    order_count = stats["order_count"]
    revenue = stats["revenue"]
    items_sold = stats["items_sold"]

    if order_count > 0:
        lines.append(f"Orders: {order_count}")
        lines.append(f"Revenue: ৳{revenue:,}")
        lines.append(f"Items sold: {items_sold}")

        # Sub-status breakdown if available
        sub_parts = []
        if stats["delivered_count"]:
            sub_parts.append(f"✅ {stats['delivered_count']} delivered")
        if stats["pending_count"]:
            sub_parts.append(f"⏳ {stats['pending_count']} pending")
        if stats["cancelled_count"]:
            sub_parts.append(f"❌ {stats['cancelled_count']} cancelled")
        if sub_parts:
            lines.append("  " + "  ".join(sub_parts))

        # Top-selling items
        if stats["top_items"]:
            lines.append("")
            lines.append("🏆 *Top Sellers:*")
            for name, qty in stats["top_items"]:
                lines.append(f"  • {name} — {qty}")
    else:
        # Placeholder mode — Fahad fills these in
        lines.append("Orders: ____")
        lines.append("Revenue: ৳____")
        lines.append("Items sold: ____")
        lines.append("")
        lines.append("💡 *Fill in the blanks above with actual numbers.*")
        lines.append("   (Order data files not yet exported for this date)")

    lines.append("")

    # ── Today's Specials ──────────────────────────────────────────────
    lines.append("🔥 *Today's Specials:*")
    if specials:
        for p in specials:
            emoji = p.get("emoji", "•") or "•"
            name = p.get("name", "Unknown")
            price = p.get("price", 0)
            unit = p.get("unit", "unit")
            lines.append(f"  {emoji} {name} — ৳{price}/{unit}")
    else:
        lines.append("  Fresh arrivals coming in today! 🚚")
        lines.append("  Check the full catalog: https://jgmart.netlify.app")

    lines.append("")

    # ── Delivery Slots ────────────────────────────────────────────────
    lines.append("🕐 *Delivery Slots:*")
    lines.append("☀️ Morning: Order by 9AM → Delivered by 12PM")
    lines.append("🌙 Evening: Order by 3:30PM → Delivered by 8PM")
    lines.append("")

    # ── Quick Order ──────────────────────────────────────────────────
    lines.append("💬 *Order on WhatsApp:*")
    lines.append(f"  wa.me/{WHATSAPP_NUMBER}")
    lines.append("")
    lines.append("📱 *Or order online:*")
    lines.append("  https://jgmart.netlify.app")
    lines.append("")

    # ── Hot items / reminders ─────────────────────────────────────────
    lines.append("⚡ *Quick Reminders:*")
    lines.append("  • Minimum order: ৳200")
    lines.append("  • Free delivery in Cluster 1 & 2")
    lines.append("  • ৳20 delivery in Cluster 3")
    lines.append("")
    lines.append(f"🙏 *Thank you for choosing JG Mart!*")
    lines.append("  _Your daily grocery, delivered._")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
#  CLIPBOARD SUPPORT
# ═══════════════════════════════════════════════════════════════════════════


def copy_to_clipboard(text):
    """Copy text to clipboard using pyperclip if available."""
    try:
        import pyperclip

        pyperclip.copy(text)
        return True
    except ImportError:
        print("⚠️  pyperclip not installed. Install it with:", file=sys.stderr)
        print("   pip install pyperclip", file=sys.stderr)
        return False


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(
        description="JG Mart — Daily WhatsApp Summary Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date for summary (YYYY-MM-DD). Default: 2026-08-01 (session date).",
    )
    parser.add_argument(
        "--today",
        action="store_true",
        help="Use today's actual date (overrides --date).",
    )
    parser.add_argument(
        "--send",
        action="store_true",
        help="Copy the message to clipboard (requires pyperclip).",
    )
    parser.add_argument(
        "--specials",
        type=int,
        default=4,
        help="Number of today's specials to show (default: 4).",
    )

    args = parser.parse_args()

    # Determine target date
    if args.today:
        target_date = date.today()
    elif args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(
                f"❌ Invalid date format: {args.date}. Use YYYY-MM-DD.", file=sys.stderr
            )
            sys.exit(1)
    else:
        target_date = SESSION_DATE

    # Load catalog
    catalog = load_catalog()

    # Find data files for this date
    data_files = find_data_files(target_date)

    # Analyze orders
    stats = analyze_orders(data_files["orders"])

    # Pick today's specials
    specials = pick_todays_specials(catalog, args.specials)

    # Generate the message
    message = format_message(target_date, stats, specials, data_files["finance"])

    # Print to stdout
    print(message)

    # Copy to clipboard if requested
    if args.send:
        if copy_to_clipboard(message):
            print("\n─── ✓ Copied to clipboard ───", file=sys.stderr)
        else:
            print("\n─── Message printed above (copy manually) ───", file=sys.stderr)


if __name__ == "__main__":
    main()
