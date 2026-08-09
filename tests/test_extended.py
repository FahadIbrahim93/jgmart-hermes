#!/usr/bin/env python3
"""
JG Mart — Extended behavioral tests.

Tests that complement test_behavior.py by covering:
- Product image correctness (no SVG placeholders in defaults.js)
- Catalog data integrity (prices, categories, image URLs)
- Order flow input validation
- Offline queue behavior
- defaults.js / catalog_data.json cross-consistency
- Security module exports
- PWA service worker cache version
- Delivery fee logic
- i18n keys present in index.html

Run:
    pytest tests/test_extended.py -v
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "src" / "web" / "catalog"
SUPABASE = ROOT / "src" / "web" / "supabase"
MIGRATIONS = SUPABASE / "migrations"


# ── Product image correctness ────────────────────────────────────────────────


class TestProductImages:
    """Verify products have real images, not SVG placeholders."""

    @pytest.fixture
    def defaults_js(self):
        return (CATALOG / "defaults.js").read_text(encoding="utf-8")

    @pytest.fixture
    def catalog_data(self):
        return json.loads(
            (CATALOG / "catalog_data.json").read_text(encoding="utf-8")
        )

    def test_defaults_js_no_svg_placeholders(self, defaults_js):
        """defaults.js must not use images/pXXX.svg placeholders."""
        svg_count = len(re.findall(r"im:'images/p\d+\.svg'", defaults_js))
        assert svg_count == 0, (
            f"defaults.js still has {svg_count} SVG placeholder images; "
            "products should use real Unsplash photos"
        )

    def test_defaults_js_uses_unsplash_images(self, defaults_js):
        """defaults.js products should use Unsplash URLs."""
        unsplash_count = len(
            re.findall(r"im:'https://images\.unsplash\.com/", defaults_js)
        )
        assert unsplash_count >= 60, (
            f"defaults.js has only {unsplash_count} Unsplash images; "
            "expected at least 60"
        )

    def test_catalog_data_uses_http_images(self, catalog_data):
        """catalog_data.json products must use http(s) image URLs."""
        for p in catalog_data["products"]:
            img = p.get("image", "")
            assert img.startswith("http"), (
                f"Product {p['id']} ({p['name']}) has non-HTTP image: {img}"
            )

    def test_catalog_data_no_svg_images(self, catalog_data):
        """catalog_data.json must not use SVG image paths."""
        for p in catalog_data["products"]:
            img = p.get("image", "")
            assert not img.endswith(".svg"), (
                f"Product {p['id']} ({p['name']}) still uses SVG: {img}"
            )

    def test_admin_defaults_use_real_images(self):
        """admin.html DEFAULT_PRODUCTS must not use SVG placeholders."""
        admin = (CATALOG / "admin.html").read_text(encoding="utf-8")
        # Extract DEFAULT_PRODUCTS block
        block = re.search(
            r"const DEFAULT_PRODUCTS\s*=\s*\[(.*?)\];",
            admin,
            re.DOTALL,
        )
        assert block, "DEFAULT_PRODUCTS not found in admin.html"
        svg_count = len(re.findall(r"image:'images/[^']+\.svg'", block.group(1)))
        assert svg_count == 0, (
            f"admin.html DEFAULT_PRODUCTS has {svg_count} SVG placeholders"
        )


# ── Catalog data cross-consistency ───────────────────────────────────────────


class TestCatalogConsistency:
    """Verify defaults.js and catalog_data.json are consistent."""

    @pytest.fixture
    def defaults_products(self):
        text = (CATALOG / "defaults.js").read_text(encoding="utf-8")
        # Extract product objects from defaults.js
        products = []
        for m in re.finditer(
            r"\{id:'([^']+)',nm:'([^']*)',ct:'([^']*)',pr:(\d+)", text
        ):
            products.append(
                {"id": m.group(1), "name": m.group(2), "category": m.group(3),
                 "price": int(m.group(4))}
            )
        return products

    @pytest.fixture
    def catalog_products(self):
        return json.loads(
            (CATALOG / "catalog_data.json").read_text(encoding="utf-8")
        )["products"]

    def test_defaults_has_products(self, defaults_products):
        assert len(defaults_products) >= 60, (
            f"defaults.js has only {len(defaults_products)} products; "
            "expected at least 60"
        )

    def test_all_prices_positive(self, defaults_products):
        for p in defaults_products:
            assert p["price"] > 0, (
                f"Product {p['id']} ({p['name']}) has price {p['price']}"
            )

    def test_all_categories_valid(self, defaults_products):
        valid_cats = {
            "rice_dal", "oil_spices", "vegetables", "fish", "meat",
            "dairy_eggs", "fruits", "fmcg", "beverages", "snacks",
        }
        for p in defaults_products:
            assert p["category"] in valid_cats, (
                f"Product {p['id']} ({p['name']}) has unknown category: {p['category']}"
            )

    def test_no_duplicate_product_ids(self, defaults_products):
        ids = [p["id"] for p in defaults_products]
        assert len(ids) == len(set(ids)), "Duplicate product IDs in defaults.js"

    def test_catalog_data_no_duplicate_names(self, catalog_products):
        names = [p["name"] for p in catalog_products]
        assert len(names) == len(set(names)), "Duplicate product names in catalog_data.json"


# ── Order flow input validation ───────────────────────────────────────────────


class TestOrderFlowValidation:
    """Verify the order flow has proper input validation."""

    def test_security_module_exports(self):
        security = (CATALOG / "security.js").read_text(encoding="utf-8")
        for fn in ("escapeHtml", "validatePhone", "validateBuilding", "validateFlat"):
            assert fn in security, f"security.js must export {fn}"

    def test_index_html_validates_building(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "validateBuilding" in index, "index.html must validate building"
        assert "validateFlat" in index, "index.html must validate flat"
        assert "validatePhone" in index, "index.html must validate phone"

    def test_index_html_escapes_user_input(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "escapeHtml" in index, "index.html must escape user input"

    def test_order_flow_has_offline_queue(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "JG_OFFLINE_QUEUE" in index, "index.html must use offline queue"
        assert "navigator.onLine" in index, "index.html must check online status"

    def test_order_flow_has_error_boundary(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        # The syncOrder function must have try/catch
        assert "catch(err)" in index or "catch(err)" in index, (
            "index.html syncOrder must have try/catch error boundary"
        )

    def test_db_js_has_error_handling(self):
        db = (CATALOG / "db.js").read_text(encoding="utf-8")
        # submitOrder must have try/catch
        assert "catch (error)" in db, "db.js submitOrder must have try/catch"
        assert "JG_LOG.error" in db or "console.error" in db, (
            "db.js must log errors (via JG_LOG.error or console.error)"
        )
        assert "saveOrderToLocalStorage" in db, "db.js must have localStorage fallback"


# ── Delivery fee logic ───────────────────────────────────────────────────────


class TestDeliveryFeeLogic:
    """Verify delivery fee logic is correct in index.html."""

    def test_delivery_fee_zones_exist(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "DEL_FEES" in index, "index.html must define DEL_FEES"
        # Must have at least 3 zones
        assert "c1" in index and "c3" in index and "c4" in index, (
            "DEL_FEES must have c1, c3, c4 zones"
        )

    def test_delivery_fee_calculation(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        # The fee logic: bi>20?c4:bi>13?c3:c1
        assert "bi>20" in index, "Delivery fee must check building > 20"
        assert "bi>13" in index, "Delivery fee must check building > 13"


# ── PWA service worker ───────────────────────────────────────────────────────


class TestPWAServiceWorker:
    """Verify PWA service worker is properly configured."""

    def test_sw_js_exists(self):
        sw = CATALOG / "sw.js"
        assert sw.exists(), "sw.js must exist"

    def test_sw_has_cache_version(self):
        sw = (CATALOG / "sw.js").read_text(encoding="utf-8")
        assert "CACHE" in sw or "cache" in sw, "sw.js must define a cache version"

    def test_sw_has_offline_fallback(self):
        sw = (CATALOG / "sw.js").read_text(encoding="utf-8")
        assert "offline" in sw.lower() or "fallback" in sw.lower(), (
            "sw.js must have offline fallback"
        )


# ── i18n keys ────────────────────────────────────────────────────────────────


class TestI18n:
    """Verify i18n keys are present in index.html."""

    def test_i18n_has_en_and_bn(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "en:{" in index or "en={" in index, "i18n must have English"
        assert "bn:{" in index or "bn={" in index, "i18n must have Bengali"

    def test_i18n_has_order_confirmation(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "ordConfT" in index, "i18n must have order confirmation title"
        assert "ordConfS" in index, "i18n must have order confirmation subtitle"


# ── RPC security ─────────────────────────────────────────────────────────────


class TestRPCSecurity:
    """Verify the order creation RPC is secure."""

    def test_rpc_exists(self):
        rpc_path = MIGRATIONS / "rewrite_create_public_order.sql"
        assert rpc_path.exists(), "rewrite_create_public_order.sql must exist"

    def test_old_rpc_removed(self):
        old_path = MIGRATIONS / "rls_anonymous_orders.sql"
        assert not old_path.exists(), (
            "rls_anonymous_orders.sql must be removed (pricing fraud path)"
        )

    def test_rpc_uses_security_definer(self):
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "SECURITY DEFINER" in sql, "RPC must use SECURITY DEFINER"

    def test_rpc_validates_customer_phone(self):
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "customer phone required" in sql.lower(), (
            "RPC must validate customer phone"
        )

    def test_rpc_rejects_empty_items(self):
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "no items" in sql.lower(), "RPC must reject empty items"

    def test_rpc_computes_total_server_side(self):
        sql = (MIGRATIONS / "rewrite_create_public_order.sql").read_text(
            encoding="utf-8"
        )
        assert "subtotal" in sql.lower(), "RPC must compute subtotal"
        assert "delivery_fee" in sql.lower(), "RPC must compute delivery fee"
        assert "total" in sql.lower(), "RPC must compute total"


# ── Accessibility ────────────────────────────────────────────────────────────


class TestAccessibility:
    """Verify basic accessibility attributes are present."""

    def test_skip_link_exists(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "Skip to content" in index or "skip to content" in index.lower(), (
            "index.html must have a skip-to-content link"
        )

    def test_product_cards_are_keyboard_accessible(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert 'tabindex="0"' in index, "Product cards must be focusable"
        assert 'role="button"' in index, "Product cards must have button role"

    def test_modals_have_aria_attributes(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert 'aria-modal="true"' in index, "Modals must have aria-modal"
        assert 'role="dialog"' in index, "Modals must have dialog role"

    def test_close_buttons_have_aria_labels(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert 'aria-label="Close cart"' in index, "Cart close button needs aria-label"
        assert 'aria-label="Close order history"' in index, (
            "History close button needs aria-label"
        )

    def test_focus_trap_exists(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "Tab" in index and "focusable" in index, (
            "index.html must trap Tab key inside open modals"
        )

    def test_images_have_alt_text(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        # Image templates in JS must include alt text (rendered dynamically)
        img_templates = re.findall(r'<img[^>]+alt="[^"]+"', index)
        assert len(img_templates) >= 3, (
            f"Expected at least 3 image templates with alt text, found {len(img_templates)}"
        )
        # Verify all use the product name as alt text
        for tmpl in img_templates:
            assert 'alt="${p.nm}"' in tmpl or 'alt="${' in tmpl, (
                f"Image template missing dynamic alt text: {tmpl[:80]}"
            )

    def test_images_have_decoding_async(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert 'decoding="async"' in index, "Product images should use decoding=async"


# ── Rate limiting ────────────────────────────────────────────────────────────


class TestRateLimiting:
    """Verify client-side order rate limiting exists."""

    def test_rate_limit_function_exists(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "checkOrderRateLimit" in index, "Missing order rate-limit function"

    def test_rate_limit_blocks_excess_orders(self):
        index = (CATALOG / "index.html").read_text(encoding="utf-8")
        assert "ORDER_RATE_LIMIT_MAX" in index, "Missing rate limit max constant"
        assert "Too many orders" in index, "Missing rate-limit alert message"
