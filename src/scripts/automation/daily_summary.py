#!/usr/bin/env python3
"""
JG Mart — Daily Summary Report Generator
=========================================
Hyperlocal grocery delivery — Japan Garden City, Dhaka.

Generates a formatted daily summary report from exported JSON files.
Reads from exported data (customers, partners), orders, and finance files,
then outputs a clean text report Fahad can read or share.

USAGE:
    python daily_summary.py --data jgmart_data_2026-08-01.json --orders jgmart_orders_2026-08-01.json
    python daily_summary.py --date 2026-08-01    (auto-looks for files with that date)
    python daily_summary.py --today              (uses today's date, auto-looks for files)
    python daily_summary.py --data data.json     (show what you can with just data)
    python daily_summary.py --orders orders.json (show what you can with just orders)
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from collections import Counter

# ─── CONSTANTS ──────────────────────────────────────────────────────────
EXPORT_DIR = Path(__file__).parent.resolve()

# File name patterns
DATA_PREFIX = "jgmart_data_"
ORDERS_PREFIX = "jgmart_orders_"
FINANCE_PREFIX = "jgmart_finance_"

BOX_H = "═" * 39
SEP = "─" * 47

# ANSI colour support
USE_COLOR = os.name == "posix" or os.environ.get("TERM", "").startswith("xterm")


def _c(code, text):
    """Wrap text in ANSI colour code if colour is enabled."""
    if USE_COLOR:
        return f"\033[{code}m{text}\033[0m"
    return text


def green(t): return _c("32", t)
def yellow(t): return _c("33", t)
def red(t): return _c("31", t)
def cyan(t): return _c("36", t)
def bold(t): return _c("1", t)
def dim(t): return _c("2", t)


def fmt_taka(amount):
    """Format a number as Bangladeshi Taka."""
    if amount is None:
        return "N/A"
    return f"৳{amount:,.0f}"


def fmt_pct(part, total):
    """Format a percentage, handling division by zero."""
    if total and total > 0:
        return f"({part / total * 100:.0f}%)"
    return ""


# ─── FILE LOADING ───────────────────────────────────────────────────────


def find_file(prefix, date_str):
    """Look for a file matching the prefix and date in the export directory."""
    pattern = f"{prefix}{date_str}.json"
    candidate = EXPORT_DIR / pattern
    if candidate.exists():
        return candidate
    # Try a broader glob — maybe the date is embedded with extra text
    # e.g. jgmart_data_2026-08-01_v2.json
    for f in EXPORT_DIR.glob(f"{prefix}{date_str}*.json"):
        return f
    return None


def load_json(filepath):
    """Load a JSON file, returning None on failure with a printed warning."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(yellow(f"  ⚠  File not found: {filepath}"))
    except json.JSONDecodeError as e:
        print(red(f"  ✖  Invalid JSON in {filepath}: {e}"))
    except Exception as e:
        print(red(f"  ✖  Error reading {filepath}: {e}"))
    return None


# ─── PARSERS — extract structured data from various JSON shapes ─────────


def parse_orders(raw):
    """
    Parse orders from the JSON blob.
    Expected shape (orders.html export):
      { "orders": [ { "id": …, "customer": …, "status": …, "items": […], "total": … }, … ] }
    Also accepts a bare list, or a dict with an 'orders' key.
    Returns a list of order dicts with normalised keys.
    """
    if raw is None:
        return []

    orders = []

    # Try several common structures
    if isinstance(raw, dict):
        # { "orders": [...] } — most common
        source = raw.get("orders", raw.get("data", raw.get("items", [])))
        if isinstance(source, list):
            orders = source
        # Maybe the whole dict is a single order with an 'id' field
        elif raw.get("id") or raw.get("order_id"):
            orders = [raw]
    elif isinstance(raw, list):
        orders = raw

    # Normalise keys
    normalised = []
    for o in orders:
        if not isinstance(o, dict):
            continue
        entry = {
            "id": o.get("id") or o.get("order_id") or o.get("orderId", ""),
            "customer": o.get("customer") or o.get("customer_name") or o.get("customerName", ""),
            "status": o.get("status", "").lower().strip(),
            "total": _parse_number(o.get("total") or o.get("amount") or o.get("revenue") or 0),
            "items": o.get("items") or o.get("products") or [],
        }
        normalised.append(entry)

    return normalised


def parse_customers(raw):
    """
    Parse customers from the JSON blob.
    Expected shape (data.html export):
      { "customers": [ { "name": …, "building": …, "active": true }, … ] }
    Returns a list of customer dicts.
    """
    if raw is None:
        return []

    if isinstance(raw, dict):
        source = raw.get("customers", raw.get("clients", raw.get("users", [])))
        if isinstance(source, list):
            return source
    elif isinstance(raw, list):
        return raw
    return []


def parse_partners(raw):
    """
    Parse partners/vendors from the JSON blob.
    Expected shape (data.html export):
      { "partners": [ { "name": …, "category": …, "active": true }, … ] }
    Returns a list of partner dicts.
    """
    if raw is None:
        return []

    if isinstance(raw, dict):
        source = raw.get("partners", raw.get("vendors", raw.get("suppliers", [])))
        if isinstance(source, list):
            return source
    elif isinstance(raw, list):
        return raw
    return []


def parse_finance(raw):
    """
    Parse financial data.
    Expected shape (finance.html export or embedded in data):
      { "revenue_today": …, "costs_today": …, "profit_today": …,
        "month_to_date": …, "cash_position": … }
    Also looks inside a 'finance' or 'financials' key if present.
    Returns a dict or None.
    """
    if raw is None:
        return None

    if isinstance(raw, dict):
        src = raw.get("finance") or raw.get("financials") or raw.get("finances") or raw
        if isinstance(src, dict):
            return {
                "revenue_today": _parse_number(src.get("revenue_today") or src.get("revenueToday") or src.get("revenue")),
                "costs_today": _parse_number(src.get("costs_today") or src.get("costsToday") or src.get("costs") or src.get("expenses")),
                "profit_today": _parse_number(src.get("profit_today") or src.get("profitToday") or src.get("profit")),
                "month_to_date": _parse_number(src.get("month_to_date") or src.get("monthToDate") or src.get("mtd")),
                "cash_position": _parse_number(src.get("cash_position") or src.get("cashPosition") or src.get("cash")),
            }
    return None


def parse_settings(raw):
    """
    Parse settings/metadata from the JSON blob.
    Expected shape (data.html export):
      { "settings": { "cash_position": …, "name": … } }
    Returns a dict or None.
    """
    if raw is None:
        return None
    if isinstance(raw, dict):
        return raw.get("settings") or raw
    return None


def _parse_number(val):
    """Safely parse a number from various types."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return val
    if isinstance(val, str):
        # Remove currency symbols, commas, whitespace
        cleaned = val.replace("৳", "").replace("$", "").replace(",", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


# ─── REPORT GENERATION ─────────────────────────────────────────────────


def generate_report(data_raw, orders_raw, finance_raw, report_date):
    """Build and return the full report string."""
    lines = []

    # ── Parse all inputs ──────────────────────────────────────────────
    orders = parse_orders(orders_raw)
    customers = parse_customers(data_raw)
    partners = parse_partners(data_raw)
    settings = parse_settings(data_raw)
    finances = parse_finance(finance_raw if finance_raw else data_raw)

    # ── Header ────────────────────────────────────────────────────────
    date_str = report_date.strftime("%Y-%m-%d") if isinstance(report_date, date) else str(report_date)
    lines.append("")
    lines.append(bold("JG MART — DAILY SUMMARY"))
    lines.append(f"Date: {date_str}")
    lines.append(BOX_H)

    # ── ORDERS SECTION ────────────────────────────────────────────────
    lines.append("")
    lines.append(bold("📦 ORDERS"))

    if orders:
        total_orders = len(orders)
        delivered = sum(1 for o in orders if o["status"] in ("delivered", "completed", "done"))
        pending = sum(1 for o in orders if o["status"] in ("pending", "processing", "new"))
        cancelled = sum(1 for o in orders if o["status"] in ("cancelled", "canceled"))
        other = total_orders - delivered - pending - cancelled

        totals_list = [o["total"] for o in orders if o["total"] is not None]
        total_revenue = sum(totals_list)
        avg_value = total_revenue / len(totals_list) if totals_list else 0
        delivered_pct = delivered / total_orders * 100 if total_orders else 0

        lines.append(f"  Total Today:      {total_orders}")
        lines.append(f"  Delivered:        {delivered} {green(f'({delivered_pct:.0f}%)')}")
        if pending:
            lines.append(f"  Pending:          {yellow(str(pending))}")
        if cancelled:
            lines.append(f"  Cancelled:        {red(str(cancelled))}")
        if other:
            lines.append(f"  Other:            {other}")
        lines.append(f"  Avg Value:        {fmt_taka(avg_value)}")
        lines.append(f"  Total Revenue:    {green(fmt_taka(total_revenue))}")
    else:
        lines.append(dim("  No orders data available."))

    # ── FINANCIALS SECTION ────────────────────────────────────────────
    lines.append("")
    lines.append(bold("💰 FINANCIALS"))

    if finances:
        rev = finances.get("revenue_today")
        costs = finances.get("costs_today")
        profit = finances.get("profit_today")
        mtd = finances.get("month_to_date")
        cash = finances.get("cash_position")

        # Fallback: compute from orders if revenue_today is missing
        if rev is None and orders:
            rev = sum(o["total"] for o in orders if o["total"] is not None)

        if rev is not None:
            lines.append(f"  Revenue Today:    {green(fmt_taka(rev))}")
        if costs is not None:
            lines.append(f"  Costs Today:      {fmt_taka(costs)}")
            if costs is not None and rev is not None and rev > 0:
                margin_pct = (rev - costs) / rev * 100
                lines.append(f"  Margin:           {margin_pct:.1f}%")
        if profit is not None:
            p_str = green(fmt_taka(profit)) if profit >= 0 else red(fmt_taka(profit))
            lines.append(f"  Profit Today:     {p_str}")
        if mtd is not None:
            lines.append(f"  Month to Date:    {fmt_taka(mtd)}")
        if cash is not None:
            lines.append(f"  Cash Position:    {fmt_taka(cash)}")
    else:
        # Fallback: estimate from orders
        if orders:
            total_rev = sum(o["total"] for o in orders if o["total"] is not None)
            est_cost_per_order = 67
            fixed_cost = 3750 - (est_cost_per_order * len(orders))
            est_costs = (est_cost_per_order * len(orders)) + max(fixed_cost, 0)
            est_profit = total_rev - est_costs
            lines.append(f"  Revenue Today:    {green(fmt_taka(total_rev))}")
            lines.append(f"  Costs Today:      {fmt_taka(est_costs)} (est.)")
            lines.append(f"  Profit Today:     {green(fmt_taka(est_profit))}")
            lines.append(dim("  (Estimated — no finance file provided)"))
        else:
            lines.append(dim("  No financial data available."))

    # ── CUSTOMERS SECTION ─────────────────────────────────────────────
    lines.append("")
    lines.append(bold("👥 CUSTOMERS"))

    if customers:
        active = [c for c in customers if str(c.get("active", "true")).lower() == "true" or c.get("active") is True]
        total_active = len(active)

        # New customers today — check if there's a 'created' or 'joined' field
        new_today = sum(
            1 for c in customers
            if c.get("created") == date_str
            or c.get("joined") == date_str
            or c.get("created_at", "").startswith(date_str)
            or c.get("date_added", "").startswith(date_str)
        )

        # Top building
        buildings = Counter(
            c.get("building") or c.get("building_name") or c.get("area") or "Unknown"
            for c in active
        )
        top_building, top_b_count = buildings.most_common(1)[0] if buildings else ("N/A", 0)

        lines.append(f"  Total Active:     {total_active}")
        lines.append(f"  New Today:        {new_today}")
        lines.append(f"  Top Location:     {top_building} ({top_b_count} {'customer' if top_b_count == 1 else 'customers'})")
    else:
        lines.append(dim("  No customer data available."))

    # ── Build order-building cross-reference ──────────────────────────
    building_order_counts = Counter()
    if orders and customers:
        # Build a lookup: customer name → building
        name_to_building = {}
        for c in customers:
            name = (c.get("name") or c.get("customer_name") or "").strip().lower()
            bldg = c.get("building") or c.get("building_name") or c.get("area") or "Unknown"
            if name:
                name_to_building[name] = bldg

        for o in orders:
            cname = (o.get("customer") or "").strip().lower()
            if cname in name_to_building:
                building_order_counts[name_to_building[cname]] += 1

    if building_order_counts:
        top_bldg, top_bldg_count = building_order_counts.most_common(1)[0]
        # Replace the top location line with order-based data
        # (find and update in the customer section)
        for i, line in enumerate(lines):
            if line.strip().startswith("Top Location"):
                lines[i] = f"  Top Location:     {top_bldg} ({top_bldg_count} orders)"
                break

    # ── PARTNERS SECTION ─────────────────────────────────────────────
    lines.append("")
    lines.append(bold("🚚 PARTNERS"))

    if partners:
        # Count orders by partner category
        category_counts = Counter()
        partner_orders = Counter()

        for p in partners:
            name = p.get("name", "Unknown")
            category = p.get("category") or p.get("type") or "General"
            category_counts[category] += 1

            # If we have orders, count how many items reference this partner
            if orders:
                # Check order items for partner name
                for o in orders:
                    for item in (o.get("items") or []):
                        item_source = (item.get("supplier") or item.get("vendor") or item.get("partner") or "").lower()
                        if name.lower() in item_source or item_source in name.lower():
                            partner_orders[name] += 1

        cat_str = ", ".join(f"{cat} {count}" for cat, count in category_counts.most_common())
        lines.append(f"  Partners:         {cat_str}")

        if partner_orders:
            top_partner, top_p_count = partner_orders.most_common(1)[0]
            lines.append(f"  Most Orders:      {top_partner} ({top_p_count} orders)")
        else:
            # Fallback: show partner names
            names = [p.get("name", "Unknown") for p in partners]
            lines.append(f"  Active Partners:  {', '.join(names[:5])}")
            if len(names) > 5:
                lines.append(f"  + {len(names) - 5} more")
    else:
        lines.append(dim("  No partner data available."))

    # ── TOP PRODUCTS SECTION ──────────────────────────────────────────
    lines.append("")
    lines.append(bold("🏆 TOP PRODUCTS"))

    if orders:
        product_units = Counter()
        for o in orders:
            for item in (o.get("items") or []):
                prod_name = item.get("name") or item.get("product") or item.get("product_name") or item.get("item") or ""
                qty = _parse_number(item.get("qty") or item.get("quantity") or item.get("count") or 1)
                unit = item.get("unit") or ""
                key = f"{prod_name} — {qty} {unit}".strip(" —")
                if prod_name:
                    display = f"{prod_name} {f'({unit})' if unit else ''}".strip()
                    product_units[display] += qty or 1

        if product_units:
            rank = 1
            for prod, qty in product_units.most_common(5):
                qty_str = f"{qty:.0f}" if qty == int(qty) else f"{qty:.1f}"
                unit_label = "units"
                # Try to extract unit from accumulated data
                lines.append(f"  {rank}. {prod} — {qty_str} units")
                rank += 1
        else:
            lines.append(dim("  No product details found in orders."))
    else:
        lines.append(dim("  No orders data — cannot compute top products."))

    # ── ACTION ITEMS SECTION ──────────────────────────────────────────
    lines.append("")
    lines.append(bold("⚠️  ACTION ITEMS"))

    has_actions = False

    if orders:
        pending_orders = [o for o in orders if o["status"] in ("pending", "processing", "new")]
        if pending_orders:
            lines.append(f"  • {len(pending_orders)} order(s) still pending delivery")
            has_actions = True

    if customers and orders:
        # Check for customers who ordered but aren't in the customer list
        order_names = set((o.get("customer") or "").strip().lower() for o in orders if o.get("customer"))
        known_names = set((c.get("name") or "").strip().lower() for c in customers)
        new_names = order_names - known_names
        if new_names:
            lines.append(f"  • {len(new_names)} new customer(s) not yet in directory: {', '.join(sorted(new_names)[:3])}")
            has_actions = True

    if finances:
        cash = finances.get("cash_position")
        if cash is not None and cash < 50000:
            lines.append(f"  • Low cash position ({fmt_taka(cash)}) — consider injection")
            has_actions = True

    if not has_actions:
        lines.append(dim("  No outstanding action items."))

    lines.append("")
    lines.append(BOX_H)
    lines.append(green("✅ Report generated"))
    lines.append(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    return "\n".join(lines)


# ─── SAMPLE DATA GENERATION ──────────────────────────────────────────


def generate_sample_files(date_str):
    """Generate sample JSON files for testing/demonstration."""
    data_file = EXPORT_DIR / f"{DATA_PREFIX}{date_str}.json"
    orders_file = EXPORT_DIR / f"{ORDERS_PREFIX}{date_str}.json"
    finance_file = EXPORT_DIR / f"{FINANCE_PREFIX}{date_str}.json"

    sample_data = {
        "customers": [
            {"name": "Rafiq", "building": "Bldg 3", "active": True, "joined": "2026-07-15"},
            {"name": "Nusrat", "building": "Bldg 3", "active": True, "joined": "2026-06-01"},
            {"name": "Kabir", "building": "Bldg 1", "active": True, "joined": date_str},
            {"name": "Shamim", "building": "Bldg 5", "active": True, "joined": "2026-05-20"},
            {"name": "Fatima", "building": "Bldg 2", "active": True, "joined": date_str},
            {"name": "Hasan", "building": "Bldg 3", "active": True, "joined": "2026-04-10"},
            {"name": "Jahanara", "building": "Bldg 4", "active": True, "joined": "2026-06-15"},
            {"name": "Anik", "building": "Bldg 6", "active": False, "joined": "2026-03-01"},
            {"name": "Tania", "building": "Bldg 2", "active": True, "joined": "2026-07-01"},
            {"name": "Shahid", "building": "Bldg 1", "active": True, "joined": "2026-05-10"},
            {"name": "Parvin", "building": "Bldg 3", "active": True, "joined": "2026-07-20"},
            {"name": "Rashed", "building": "Bldg 5", "active": True, "joined": "2026-04-22"},
            {"name": "Nazma", "building": "Bldg 4", "active": True, "joined": "2026-06-05"},
            {"name": "Foysal", "building": "Bldg 7", "active": True, "joined": date_str},
            {"name": "Selina", "building": "Bldg 2", "active": False, "joined": "2026-02-15"},
            {"name": "Mizan", "building": "Bldg 3", "active": True, "joined": "2026-05-25"},
        ],
        "partners": [
            {"name": "Rice House", "category": "Rice", "active": True},
            {"name": "Vegi Fresh", "category": "Vegetables", "active": True},
            {"name": "Fish Bazar", "category": "Fish", "active": True},
            {"name": "Meat Corner", "category": "Meat", "active": True},
            {"name": "Dairy Farm", "category": "Dairy", "active": True},
            {"name": "Spice World", "category": "Spices", "active": True},
            {"name": "Beverage Hub", "category": "Beverages", "active": False},
        ],
        "settings": {
            "business_name": "JG Mart",
            "location": "Japan Garden City, Dhaka",
            "currency": "BDT",
            "delivery_fee": 30,
            "min_order": 200,
            "cash_position": 255910,
        },
        "finance": {
            "revenue_today": 9660,
            "costs_today": 3750,
            "profit_today": 5910,
            "month_to_date": 5910,
            "cash_position": 255910,
        },
    }

    sample_orders = {
        "orders": [
            {"id": "ORD-001", "customer": "Rafiq", "status": "delivered", "total": 850,
             "items": [{"name": "Chinigura Rice", "qty": 2, "unit": "kg"}, {"name": "Potato", "qty": 1, "unit": "kg"}]},
            {"id": "ORD-002", "customer": "Nusrat", "status": "delivered", "total": 1200,
             "items": [{"name": "Eggs", "qty": 2, "unit": "dozen"}, {"name": "Chicken", "qty": 1, "unit": "kg"}]},
            {"id": "ORD-003", "customer": "Kabir", "status": "delivered", "total": 450,
             "items": [{"name": "Eggs", "qty": 1, "unit": "dozen"}, {"name": "Bread", "qty": 2, "unit": "pack"}]},
            {"id": "ORD-004", "customer": "Shamim", "status": "delivered", "total": 780,
             "items": [{"name": "Chinigura Rice", "qty": 3, "unit": "kg"}]},
            {"id": "ORD-005", "customer": "Fatima", "status": "delivered", "total": 620,
             "items": [{"name": "Fish (Rui)", "qty": 1, "unit": "kg"}, {"name": "Potato", "qty": 2, "unit": "kg"}]},
            {"id": "ORD-006", "customer": "Hasan", "status": "pending", "total": 340,
             "items": [{"name": "Eggs", "qty": 1, "unit": "dozen"}]},
            {"id": "ORD-007", "customer": "Jahanara", "status": "delivered", "total": 950,
             "items": [{"name": "Chinigura Rice", "qty": 2, "unit": "kg"}, {"name": "Chicken", "qty": 1, "unit": "kg"}]},
            {"id": "ORD-008", "customer": "Tania", "status": "delivered", "total": 520,
             "items": [{"name": "Beef", "qty": 0.5, "unit": "kg"}, {"name": "Potato", "qty": 1, "unit": "kg"}]},
            {"id": "ORD-009", "customer": "Shahid", "status": "delivered", "total": 1100,
             "items": [{"name": "Chinigura Rice", "qty": 4, "unit": "kg"}]},
            {"id": "ORD-010", "customer": "Parvin", "status": "pending", "total": 680,
             "items": [{"name": "Fish (Rui)", "qty": 1, "unit": "kg"}, {"name": "Eggs", "qty": 1, "unit": "dozen"}]},
            {"id": "ORD-011", "customer": "Rashed", "status": "delivered", "total": 870,
             "items": [{"name": "Chicken", "qty": 2, "unit": "kg"}, {"name": "Rice (Miniket)", "qty": 1, "unit": "kg"}]},
            {"id": "ORD-012", "customer": "Foysal", "status": "delivered", "total": 1290,
             "items": [{"name": "Chinigura Rice", "qty": 5, "unit": "kg"}, {"name": "Beef", "qty": 1, "unit": "kg"}]},
        ]
    }

    sample_finance = {
        "revenue_today": 9660,
        "costs_today": 3750,
        "profit_today": 5910,
        "month_to_date": 255910,
        "cash_position": 255910,
    }

    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Created {data_file.name}")

    with open(orders_file, "w", encoding="utf-8") as f:
        json.dump(sample_orders, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Created {orders_file.name}")

    with open(finance_file, "w", encoding="utf-8") as f:
        json.dump(sample_finance, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Created {finance_file.name}")

    return data_file, orders_file, finance_file


# ─── CLI ──────────────────────────────────────────────────────────────


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="JG Mart — Daily Summary Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python daily_summary.py --data jgmart_data_2026-08-01.json --orders jgmart_orders_2026-08-01.json
  python daily_summary.py --date 2026-08-01
  python daily_summary.py --today
  python daily_summary.py --sample 2026-08-01    # Generate sample files for testing
        """,
    )

    # File arguments
    parser.add_argument("--data", metavar="FILE", help="Path to data JSON (customers, partners, settings)")
    parser.add_argument("--orders", metavar="FILE", help="Path to orders JSON")
    parser.add_argument("--finance", metavar="FILE", help="Path to finance JSON (optional — data.html may embed it)")

    # Convenience flags
    parser.add_argument("--date", metavar="YYYY-MM-DD", help="Date for auto-file lookup (e.g. 2026-08-01)")
    parser.add_argument("--today", action="store_true", help="Use today's date for auto-file lookup")

    # Utility
    parser.add_argument("--sample", metavar="YYYY-MM-DD", help="Generate sample JSON files for a given date")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colour output")

    return parser.parse_args(argv)


def main():
    args = parse_args()

    global USE_COLOR
    if args.no_color:
        USE_COLOR = False

    # ── Sample mode ───────────────────────────────────────────────────
    if args.sample:
        print(f"\n📝 Generating sample files for {args.sample}...\n")
        generate_sample_files(args.sample)
        print(f"\n✅ Sample files created in {EXPORT_DIR}/\n")
        print("  Now run:  python daily_summary.py --date " + args.sample)
        return

    # ── Resolve date and file paths ───────────────────────────────────
    report_date = None

    if args.today:
        report_date = date.today()
    elif args.date:
        try:
            report_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(red(f"✖ Invalid date format: {args.date}  (use YYYY-MM-DD)"))
            sys.exit(1)

    if report_date:
        date_str = report_date.strftime("%Y-%m-%d")
    else:
        date_str = None

    # Resolve file paths
    data_path = args.data
    orders_path = args.orders
    finance_path = args.finance

    if date_str:
        if not data_path:
            found = find_file(DATA_PREFIX, date_str)
            if found:
                data_path = str(found)
        if not orders_path:
            found = find_file(ORDERS_PREFIX, date_str)
            if found:
                orders_path = str(found)
        if not finance_path:
            found = find_file(FINANCE_PREFIX, date_str)
            if found:
                finance_path = str(found)

    # ── Show what we're doing ─────────────────────────────────────────
    print(f"\n{bold('JG Mart — Daily Summary Generator')}")
    print(f"{SEP}")
    if data_path:
        print(f"  Data:   {data_path}")
    if orders_path:
        print(f"  Orders: {orders_path}")
    if finance_path:
        print(f"  Finance: {finance_path}")
    if report_date:
        print(f"  Date:   {date_str}")
    print(f"{SEP}")

    # ── Load all files ────────────────────────────────────────────────
    if date_str and not data_path and not orders_path and not finance_path:
        print(yellow(f"\n  ⚠  No files found for date: {date_str}"))
        print(f"  Expected in: {EXPORT_DIR}/")
        print(f"  Tried prefixes: {DATA_PREFIX}, {ORDERS_PREFIX}, {FINANCE_PREFIX}")
        print(f"\n  Generate sample files with:  python daily_summary.py --sample {date_str}\n")
        sys.exit(1)

    data_raw = load_json(data_path) if data_path else None
    orders_raw = load_json(orders_path) if orders_path else None
    finance_raw = load_json(finance_path) if finance_path else None

    if not data_raw and not orders_raw and not finance_raw:
        print(red("\n✖ No usable data loaded. Nothing to report.\n"))
        sys.exit(1)

    # Determine report date
    if not report_date:
        # Try to extract from a filename
        for p in [data_path, orders_path, finance_path]:
            if p:
                for fmt in ("%Y-%m-%d", "%Y%m%d"):
                    try:
                        # Pull YYYY-MM-DD from filename
                        import re
                        m = re.search(r"(\d{4}-\d{2}-\d{2})", str(p))
                        if m:
                            report_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                            break
                    except ValueError:
                        continue
                if report_date:
                    break
        if not report_date:
            report_date = date.today()

    # ── Generate & print report ───────────────────────────────────────
    report = generate_report(data_raw, orders_raw, finance_raw, report_date)
    print(report)


if __name__ == "__main__":
    main()
