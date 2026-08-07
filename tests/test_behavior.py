#!/usr/bin/env python3
"""
JG Mart — Real behavioral tests.

These test the actual business logic of the project (Python automation
scripts), not just HTML tag balance. They run against the local filesystem
and do not require a live Supabase instance.

Run:
    pytest tests/test_behavior.py -v
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "src" / "web" / "catalog"
SUPABASE = ROOT / "src" / "web" / "supabase"
MIGRATIONS = SUPABASE / "migrations"


# ── Product catalog integrity ────────────────────────────────────────────────


class TestCatalogIntegrity:
    """Static checks on the product catalog data."""

    @pytest.fixture
    def catalog(self):
        path = CATALOG / "catalog_data.json"
        assert path.exists(), "catalog_data.json must exist"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_catalog_has_products_and_categories(self, catalog):
        assert "products" in catalog, "catalog must have a 'products' key"
        assert "categories" in catalog, "catalog must have a 'categories' key"
        assert len(catalog["products"]) > 0, "catalog must contain products"
        assert len(catalog["categories"]) > 0, "catalog must contain categories"

    def test_products_have_required_fields(self, catalog):
        for p in catalog["products"]:
            assert "id" in p, f"product missing id: {p}"
            assert "name" in p, f"product missing name: {p}"
            assert "price" in p, f"product missing price: {p}"
            assert "category" in p, f"product missing category: {p}"
            assert isinstance(p["price"], (int, float)), f"price must be numeric: {p}"
            assert p["price"] >= 0, f"price must be >= 0: {p}"

    def test_no_duplicate_product_ids(self, catalog):
        ids = [p["id"] for p in catalog["products"]]
        assert len(ids) == len(set(ids)), "product ids must be unique"

    def test_all_categories_exist_in_products(self, catalog):
        cat_ids = {c["id"] for c in catalog["categories"]}
        product_cats = {p["category"] for p in catalog["products"]}
        for cat in cat_ids:
            assert cat in product_cats, f"category {cat} has no products"


# ── Order pricing logic (server-side pricing contract) ───────────────────────


class TestOrderPricing:
    """
    Verify the contract that the order RPC now prices server-side.

    The RPC (rewrite_create_public_order.sql) accepts only item_id + qty per
    line and computes subtotal/fee/total from the products table. The client
    (db.js) must no longer send price/total fields to the RPC.
    """

    def test_rpc_accepts_only_item_id_and_qty(self):
        """The RPC signature must not accept client-sent price/total fields."""
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        # The new RPC must NOT accept p_subtotal, p_delivery_fee, p_total,
        # or p_status as parameters — those are computed server-side.
        for forbidden in ("p_subtotal", "p_delivery_fee", "p_total", "p_status"):
            assert (
                forbidden not in sql
            ), f"RPC must not accept {forbidden}; pricing must be server-side"

    def test_rpc_computes_subtotal_from_products(self):
        """The RPC must look up product prices and compute subtotal."""
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "product_row.price" in sql, "RPC must use product price"
        assert "subtotal" in sql, "RPC must compute subtotal"

    def test_client_no_longer_sends_price_to_rpc(self):
        """db.js must send only product_id + qty to the RPC, not price/total."""
        db = (CATALOG / "db.js").read_text(encoding="utf-8")
        # The RPC call must use the new item format {product_id, qty}.
        assert "product_id" in db, "db.js must send product_id to RPC"
        assert "qty: item.qty" in db, "db.js must send qty to RPC"
        # The RPC call must NOT send p_subtotal/p_total/p_delivery_fee.
        rpc_call = re.search(
            r"supabase\.rpc\('create_public_order',\s*\{([^}]+)\}",
            db,
            re.DOTALL,
        )
        assert rpc_call, "could not find create_public_order RPC call in db.js"
        rpc_args = rpc_call.group(1)
        for forbidden in ("p_subtotal", "p_total", "p_delivery_fee"):
            assert (
                forbidden not in rpc_args
            ), f"db.js must not send {forbidden} to RPC"


# ── Admin auth (PIN fallback removed) ────────────────────────────────────────


class TestAdminAuth:
    """Verify the PIN fallback has been removed from admin auth."""

    def test_no_hardcoded_default_pin_in_auth(self):
        auth = (ROOT / "src" / "web" / "auth.js").read_text(encoding="utf-8")
        assert "DEFAULT_PIN" not in auth, "auth.js must not reference DEFAULT_PIN"
        assert "'1234'" not in auth, "auth.js must not contain the default PIN"

    def test_no_hardcoded_default_pin_in_admin(self):
        admin = (CATALOG / "admin.html").read_text(encoding="utf-8")
        assert "DEFAULT_PIN" not in admin, "admin.html must not reference DEFAULT_PIN"
        assert "'1234'" not in admin, "admin.html must not contain the default PIN"

    def test_admin_login_requires_supabase(self):
        admin = (CATALOG / "admin.html").read_text(encoding="utf-8")
        # The PIN form must be removed; login must use Supabase sign-in.
        assert "Unlock with PIN" not in admin, "admin.html must not have a PIN login form"
        assert "Default PIN:" not in admin, "admin.html must not display the default PIN"


# ── Security: sanitizer and validation ───────────────────────────────────────


class TestSecurity:
    """Checks on the security module."""

    def test_sanitize_html_exists(self):
        security = (CATALOG / "security.js").read_text(encoding="utf-8")
        assert "sanitizeHtml" in security, "security.js must export sanitizeHtml"

    def test_validate_phone_exists(self):
        security = (CATALOG / "security.js").read_text(encoding="utf-8")
        assert "validatePhone" in security, "security.js must export validatePhone"

    def test_rpc_validates_payment_method(self):
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "payment_method" in sql, "RPC must validate payment method"

    def test_rpc_validates_customer_phone(self):
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "customer phone required" in sql, "RPC must require customer phone"

    def test_rpc_validates_items_not_empty(self):
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "no items" in sql, "RPC must reject empty items"


# ── CI: pytest must be able to fail the build ───────────────────────────────


class TestCIConfig:
    """Verify CI is wired so tests can actually fail the build."""

    def test_ci_test_job_has_no_escape_hatch(self):
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        # The test job must NOT have '|| echo' or '|| true' after pytest,
        # because that lets a failing test suite still pass the build.
        test_section = re.search(
            r"test:.*?(?=\n  [a-z]|\Z)", ci, re.DOTALL
        )
        assert test_section, "could not find test job in ci.yml"
        assert (
            "|| echo" not in test_section.group(0)
        ), "test job must not have '|| echo' escape hatch"
        assert (
            "|| true" not in test_section.group(0)
        ), "test job must not have '|| true' escape hatch"

    def test_ci_security_job_has_no_escape_hatch(self):
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        security_section = re.search(
            r"security:.*?(?=\n  [a-z]|\Z)", ci, re.DOTALL
        )
        assert security_section, "could not find security job in ci.yml"
        assert (
            "|| true" not in security_section.group(0)
        ), "security job must not have '|| true' escape hatch"