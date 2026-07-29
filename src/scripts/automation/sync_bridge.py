#!/usr/bin/env python3
"""
JG Mart — Data Sync Bridge
===========================
Syncs master data exports across all 13+ HTML web apps.

Reads a master JSON file (exported from data.html — keys: customers,
partners, settings, totalOrders) and generates per-app import files
that can be injected via each app's Import button or browser dev console.

Usage:
    python sync_bridge.py --input jgmart_data_2026-08-01.json
    python sync_bridge.py --input data.json --output-dir ./sync_out
    python sync_bridge.py --input data.json --verbose
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any

# ──────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────
APP_NAME = "JG Mart — Data Sync Bridge"
VERSION = "1.0.0"

# Map of every localStorage key used by the JG Mart apps
LOCALSTORAGE_KEYS: dict[str, str] = {
    "jgmart_data": "data.html — master customer/partner data",
    "jgmart_finance": "finance.html — financial records & P&L",
    "jgmart_orders": "orders.html — order management",
    "jgmart_analytics": "analytics.html — weekly analytics dashboard",
    "jgmart_cart": "cart.html — active shopping cart",
    "jgmart_lang": "shared — language/localisation preference",
    "jgmart_launch_checks": "launch_checks.html — launch readiness checklist",
    "jgmart_finance_entries": "finance.html — individual finance entry rows",
    "jgmart_chat": "chat.html — message history",
    "jgmart_inventory": "inventory.html — stock tracking",
    "jgmart_delivery": "delivery.html — delivery zone/routing",
    "jgmart_settings": "data.html — app-wide settings",
    "jgmart_notifications": "notifications.html — in-app alerts",
    "jgmart_partners": "partners.html — partner/vendor management",
}

REQUIRED_MASTER_KEYS = {"customers", "partners", "settings", "totalOrders"}

# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _ok(msg: str) -> None:
    print(f"  ✓  {msg}")


def _warn(msg: str) -> None:
    print(f"  ⚠  {msg}", file=sys.stderr)


def _err(msg: str) -> None:
    print(f"  ✖  {msg}", file=sys.stderr)


def _die(msg: str, code: int = 1) -> None:
    _err(msg)
    sys.exit(code)


# ──────────────────────────────────────────────────────────────────────
# Master data loading & validation
# ──────────────────────────────────────────────────────────────────────


def load_master(path: str | Path) -> dict[str, Any]:
    """Load and validate the master JSON file from data.html export."""
    path = Path(path)
    if not path.exists():
        _die(f"Input file not found: {path}")
    if not path.suffix.lower() in (".json",):
        _warn(f"File does not have a .json extension: {path}")

    try:
        raw = path.read_text(encoding="utf-8-sig")
    except Exception as exc:
        _die(f"Cannot read {path}: {exc}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _die(f"Invalid JSON in {path}: {exc}")

    if not isinstance(data, dict):
        _die(f"Expected a JSON object (dict) at top level, got {type(data).__name__}")

    # Check required keys — be lenient: warn but don't abort for missing optional keys
    missing = REQUIRED_MASTER_KEYS - set(data.keys())
    if missing:
        _warn(
            f"Master data is missing expected key(s): {', '.join(sorted(missing))}. "
            "Generated files may be incomplete."
        )

    # Validate types where present
    for key in ("customers", "partners"):
        if key in data and not isinstance(data[key], list):
            _warn(f"'{key}' should be a list, got {type(data[key]).__name__}")

    if "settings" in data and not isinstance(data["settings"], dict):
        _warn(f"'settings' should be a dict, got {type(data['settings']).__name__}")

    if "totalOrders" in data and not isinstance(data["totalOrders"], (int, float, str)):
        _warn(
            f"'totalOrders' should be a number, got {type(data['totalOrders']).__name__}"
        )

    return data


# ──────────────────────────────────────────────────────────────────────
# Output file builders
# ──────────────────────────────────────────────────────────────────────


def _import_instructions(app_name: str, local_key: str, method: str = "console") -> str:
    """Return a comment block showing how to import the file into the app."""
    if method == "console":
        snippet = textwrap.dedent(f"""\
            // Paste this in the browser DevTools console:
            localStorage.setItem('{local_key}', JSON.stringify({{PASTE_CONTENT_HERE}}));
            location.reload();""")
    else:
        snippet = f"Use the '{app_name}' Import button and select this file."

    return textwrap.dedent(f"""\
        // ────────────────────────────────────────────────────────
        //  TARGET APP : {app_name}
        //  LOCALSTORAGE: {local_key}
        //  IMPORT      : {snippet}
        // ────────────────────────────────────────────────────────""")


def build_orders_import(master: dict[str, Any]) -> dict[str, Any]:
    """orders_import.json — formatted for orders.html (localStorage: jgmart_orders)."""
    customers = master.get("customers", [])
    orders = master.get("orders", [])

    # Derive orders from customers if no explicit orders key
    derived_orders: list[dict[str, Any]] = []
    if not orders and customers:
        for c in customers:
            customer_orders = c.get("orders", c.get("history", []))
            if isinstance(customer_orders, list):
                for o in customer_orders:
                    if isinstance(o, dict):
                        o.setdefault(
                            "customerId", c.get("id", c.get("name", "unknown"))
                        )
                        o.setdefault("customerName", c.get("name", "Unknown"))
                        derived_orders.append(o)
                    elif isinstance(o, (str, int, float)):
                        derived_orders.append(
                            {
                                "customerId": c.get("id", c.get("name", "unknown")),
                                "customerName": c.get("name", "Unknown"),
                                "orderRef": str(o),
                            }
                        )

    # If no orders at all, make empty placeholder
    if not orders and not derived_orders:
        _warn("No orders found in master data — orders_import.json will be empty")

    return {
        "_meta": {
            "generated": _now(),
            "source": "sync_bridge.py",
            "app": "orders.html",
            "localStorageKey": "jgmart_orders",
        },
        "_instructions": _import_instructions(
            "orders.html", "jgmart_orders", "console"
        ),
        "orders": orders or derived_orders,
        "orderCount": len(orders or derived_orders),
    }


def build_finance_import(master: dict[str, Any]) -> dict[str, Any]:
    """finance_import.json — P&L data for finance.html (localStorage: jgmart_finance)."""
    customers = master.get("customers", [])
    transactions: list[dict[str, Any]] = []

    for c in customers:
        # Collect payments / transactions from each customer
        cust_txns = c.get("payments", c.get("transactions", []))
        if isinstance(cust_txns, list):
            for txn in cust_txns:
                if isinstance(txn, dict):
                    txn.setdefault("customerId", c.get("id", c.get("name", "unknown")))
                    txn.setdefault("customerName", c.get("name", "Unknown"))
                    transactions.append(txn)

    total_orders_raw = master.get("totalOrders", 0)
    try:
        total_orders = float(total_orders_raw)
    except (ValueError, TypeError):
        total_orders = 0.0

    settings = master.get("settings", {})
    revenue = settings.get("revenue", settings.get("totalRevenue", 0))
    try:
        revenue = float(revenue)
    except (ValueError, TypeError):
        revenue = total_orders  # fallback

    return {
        "_meta": {
            "generated": _now(),
            "source": "sync_bridge.py",
            "app": "finance.html",
            "localStorageKey": "jgmart_finance",
        },
        "_instructions": _import_instructions(
            "finance.html", "jgmart_finance", "console"
        ),
        "summary": {
            "totalOrders": total_orders,
            "revenue": revenue,
            "transactionCount": len(transactions),
        },
        "transactions": transactions,
        "entries": master.get("financeEntries", master.get("finance_entries", [])),
    }


def build_analytics_import(master: dict[str, Any]) -> dict[str, Any]:
    """analytics_import.json — weekly stats for analytics.html (localStorage: jgmart_analytics)."""
    customers = master.get("customers", [])
    settings = master.get("settings", {})

    total_orders_raw = master.get("totalOrders", 0)
    try:
        total_orders = float(total_orders_raw)
    except (ValueError, TypeError):
        total_orders = 0

    revenue = settings.get("revenue", settings.get("totalRevenue", 0))
    try:
        revenue = float(revenue)
    except (ValueError, TypeError):
        revenue = 0

    # Build weekly breakdown if available, else derive from total
    weekly = master.get("weeklyAnalytics", master.get("weekly_analytics", []))
    if not weekly and total_orders > 0:
        weekly = [
            {
                "week": _stamp()[:8],
                "orders": (
                    int(total_orders) if total_orders < 1000 else int(total_orders / 4)
                ),
                "revenue": round(revenue / 4, 2) if revenue > 0 else 0,
                "customers": len(customers),
            }
        ]

    return {
        "_meta": {
            "generated": _now(),
            "source": "sync_bridge.py",
            "app": "analytics.html",
            "localStorageKey": "jgmart_analytics",
        },
        "_instructions": _import_instructions(
            "analytics.html", "jgmart_analytics", "console"
        ),
        "totalOrders": total_orders,
        "totalCustomers": len(customers),
        "totalRevenue": revenue,
        "weeklyAnalytics": weekly,
    }


def build_backup_all(master: dict[str, Any]) -> dict[str, Any]:
    """backup_all.json — combined file with ALL localStorage keys for every app."""
    customers = master.get("customers", [])
    settings = master.get("settings", {})

    backup: dict[str, Any] = {}

    # jgmart_data — full master copy
    backup["jgmart_data"] = master

    # jgmart_orders
    orders = master.get("orders", [])
    if not orders:
        for c in customers:
            co = c.get("orders", c.get("history", []))
            if isinstance(co, list):
                orders.extend(co)
    backup["jgmart_orders"] = {"orders": orders, "orderCount": len(orders)}

    # jgmart_finance
    transactions = []
    for c in customers:
        txns = c.get("payments", c.get("transactions", []))
        if isinstance(txns, list):
            transactions.extend(txns)
    backup["jgmart_finance"] = {
        "summary": {
            "totalOrders": master.get("totalOrders", 0),
            "revenue": settings.get("revenue", 0),
        },
        "transactions": transactions,
    }

    # jgmart_analytics
    backup["jgmart_analytics"] = {
        "totalOrders": master.get("totalOrders", 0),
        "totalCustomers": len(customers),
        "weeklyAnalytics": master.get("weeklyAnalytics", []),
    }

    # jgmart_cart — empty seed (carts are ephemeral)
    backup["jgmart_cart"] = {
        "items": [],
        "total": 0,
        "note": "Empty seed — cart state is session-local",
    }

    # jgmart_lang
    backup["jgmart_lang"] = settings.get("language", settings.get("lang", "bn"))

    # jgmart_launch_checks
    backup["jgmart_launch_checks"] = master.get(
        "launchChecks", master.get("launch_checks", {})
    )

    # jgmart_finance_entries
    backup["jgmart_finance_entries"] = master.get(
        "financeEntries", master.get("finance_entries", [])
    )

    # jgmart_chat
    backup["jgmart_chat"] = master.get("chatHistory", master.get("chat_history", []))

    # jgmart_inventory
    backup["jgmart_inventory"] = master.get("inventory", master.get("stock", {}))

    # jgmart_delivery
    backup["jgmart_delivery"] = master.get("delivery", master.get("deliveryZones", {}))

    # jgmart_settings
    backup["jgmart_settings"] = settings

    # jgmart_notifications
    backup["jgmart_notifications"] = master.get("notifications", [])

    # jgmart_partners
    backup["jgmart_partners"] = {"partners": master.get("partners", [])}

    return {
        "_meta": {
            "generated": _now(),
            "source": "sync_bridge.py",
            "type": "full_backup",
            "description": "Complete localStorage backup for all JG Mart apps",
        },
        "_instructions": textwrap.dedent("""\
            // ────────────────────────────────────────────────────────
            //  FULL BACKUP — ALL JG Mart localStorage keys
            //  To restore any key, paste this in the browser DevTools:
            //
            //     const backup = <PASTE_CONTENT_HERE>;
            //     Object.keys(backup).forEach(key => {
            //       if (key.startsWith('jgmart_')) {
            //         localStorage.setItem(key, JSON.stringify(backup[key]));
            //       }
            //     });
            //     location.reload();
            //
            //  To restore a single key:
            //
            //     localStorage.setItem('jgmart_orders',
            //       JSON.stringify(backup.jgmart_orders));
            //     location.reload();
            // ────────────────────────────────────────────────────────"""),
        "backup": backup,
        "keyCount": len(backup),
    }


def build_settings_guide(master: dict[str, Any]) -> str:
    """settings_guide.txt — reference for every localStorage key and how to inject data."""
    customers = master.get("customers", [])
    settings = master.get("settings", {})

    lines = [
        "=" * 72,
        f"  JG Mart — localStorage Key Reference Guide",
        f"  Generated: {_now()}",
        "=" * 72,
        "",
        "Every JG Mart HTML app stores its data in a dedicated browser",
        "localStorage key. Use this guide to manually inject or verify",
        "data via the browser's DevTools console (F12 → Console).",
        "",
        "─" * 72,
        "  QUICK INJECTION SNIPPET (works for any key)",
        "─" * 72,
        "",
        "  localStorage.setItem('KEY_NAME', JSON.stringify(YOUR_DATA));",
        "  location.reload();",
        "",
        "─" * 72,
        "  APP-BY-APP KEY REFERENCE",
        "─" * 72,
        "",
    ]

    for key, desc in sorted(LOCALSTORAGE_KEYS.items()):
        lines.append(f"  {key}")
        lines.append(f"    App     : {desc}")
        lines.append(
            f"    Console : localStorage.setItem('{key}', JSON.stringify(data));"
        )
        lines.append("")

    lines.extend(
        [
            "─" * 72,
            "  DATA SUMMARY FROM MASTER FILE",
            "─" * 72,
            "",
            f"  Customers        : {len(customers)}",
            f"  Partners         : {len(master.get('partners', []))}",
            f"  Total Orders     : {master.get('totalOrders', 'N/A')}",
            f"  Language         : {settings.get('language', settings.get('lang', 'N/A'))}",
            f"  Revenue          : {settings.get('revenue', settings.get('totalRevenue', 'N/A'))}",
            "",
            "─" * 72,
            "  TROUBLESHOOTING",
            "─" * 72,
            "",
            "  • Data not showing after import?",
            "    → Open DevTools (F12) → Application → Local Storage.",
            "      Verify the key exists and has the expected value.",
            "",
            "  • 'undefined' after reload?",
            "    → The app may expect a different data shape.",
            "      Check the app's source code for the expected schema.",
            "",
            "  • Import button not working?",
            "    → Use the console snippet above — it always works.",
            "",
            "  • Accidental data loss?",
            "    → Restore from backup_all.json (see generated file).",
            "",
            "=" * 72,
            "  END OF GUIDE",
            "=" * 72,
        ]
    )

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────────────
# Writer
# ──────────────────────────────────────────────────────────────────────


def write_json(data: Any, path: Path, verbose: bool = False) -> None:
    """Write data as pretty-printed JSON, creating parent dirs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        size = path.stat().st_size
        _ok(f"{path.name}  ({_human_size(size)})")
        if verbose:
            print(f"       → {path.resolve()}")
    except Exception as exc:
        _err(f"Failed to write {path}: {exc}")


def write_text(text: str, path: Path, verbose: bool = False) -> None:
    """Write plain text, creating parent dirs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(text, encoding="utf-8")
        size = path.stat().st_size
        _ok(f"{path.name}  ({_human_size(size)})")
        if verbose:
            print(f"       → {path.resolve()}")
    except Exception as exc:
        _err(f"Failed to write {path}: {exc}")


def _human_size(bytes_: int) -> str:
    """Format byte count for display."""
    if bytes_ < 1024:
        return f"{bytes_} B"
    elif bytes_ < 1024**2:
        return f"{bytes_ / 1024:.1f} KB"
    else:
        return f"{bytes_ / 1024 ** 2:.1f} MB"


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sync_bridge",
        description=f"{APP_NAME} v{VERSION} — Sync master data across all JG Mart apps.",
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s --input jgmart_data_2026-08-01.json
              %(prog)s --input data.json --output-dir ./sync_out
              %(prog)s --input data.json --verbose
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        metavar="FILE",
        help="Path to master JSON file (exported from data.html)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        metavar="DIR",
        default=None,
        help="Output directory (default: same directory as input file)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print full output paths and additional diagnostics",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )

    return parser.parse_args(argv)


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()

    print(f"\n  {APP_NAME} v{VERSION}")
    print(f"  {'═' * (len(APP_NAME) + 5)}\n")

    # 1. Load master
    _ok("Loading master data...")
    if args.verbose:
        print(f"     Input: {Path(args.input).resolve()}")
    master = load_master(args.input)
    print(
        f"     Found {len(master.get('customers', []))} customer(s), "
        f"{len(master.get('partners', []))} partner(s), "
        f"{master.get('totalOrders', 'N/A')} total orders\n"
    )

    # 2. Determine output directory
    input_path = Path(args.input)
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        out_dir = input_path.parent

    out_dir = out_dir.resolve()
    if args.verbose:
        print(f"  Output directory: {out_dir}\n")

    # 3. Build and write all output files
    print("  Generating output files...\n")

    outputs = [
        ("orders_import.json", write_json, build_orders_import(master)),
        ("finance_import.json", write_json, build_finance_import(master)),
        ("analytics_import.json", write_json, build_analytics_import(master)),
        ("backup_all.json", write_json, build_backup_all(master)),
        ("settings_guide.txt", write_text, build_settings_guide(master)),
    ]

    for filename, writer, content in outputs:
        writer(content, out_dir / filename, verbose=args.verbose)

    # 4. Summary
    print(f"\n  {'─' * 50}")
    print(f"  All files written to: {out_dir}")
    print(f"  {'─' * 50}")
    print()
    for key, desc in sorted(LOCALSTORAGE_KEYS.items()):
        print(f"    {key}")
    print()
    print("  Next steps:")
    print("    1. Open the target HTML app in your browser")
    print("    2. Open DevTools (F12) → Console")
    print("    3. Copy the injection snippet from the generated JSON file")
    print("    4. Paste and press Enter, then location.reload()")
    print("    5. Verify data appears in the app")
    print()


if __name__ == "__main__":
    main()
