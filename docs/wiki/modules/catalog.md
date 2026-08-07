# Module: Catalog

The catalog module renders the product shop. It is the customer-facing entry point.

## Responsibilities

- Fetch and display products from Supabase (with JSON fallback).
- Render products grouped by category.
- Manage the cart in `localStorage` (`jgmart_c`).
- Build the WhatsApp order message link.

## Key Files

- [`src/web/catalog/index.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/index.html) — main catalog page (1,602 lines).
- [`src/web/catalog/catalog_data.json`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/catalog_data.json) — static product catalog (65 products, used as fallback).
- [`src/web/catalog/defaults.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/defaults.js) — default product data and delivery fees.
- [`src/web/catalog/nav_template.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/nav_template.html) — shared navigation markup.

## Public API

- `JG_DATA_STORE` (from `data-store.js`) — normalized `localStorage` access for products, orders, cart, address, fees, language.
- `JG_SECURITY` (from `security.js`) — `escapeHtml`, `sanitizeHtml`, `validatePhone`, `validateBuilding`, `validateFlat`.

## Internal Structure

The catalog pages are monolithic: HTML, CSS, and JS are all inline in a single file. Product data is loaded via `db.js:loadProductsFromDB`, which queries Supabase and falls back to `catalog_data.json`. The cart is a `localStorage` array keyed by `jgmart_c`.

## Dependencies

- **Used by:** customer (browser), `order_intake.html` (order form).
- **Uses:** `db.js` (product/order data), `data-store.js` (localStorage), `security.js` (validation/escaping), `order-state.js` (order status).

## Notable Patterns / Gotchas

- **Monolithic files.** `index.html` is 1,602 lines with inline CSS and JS. Every page re-implements its own cart/nav/i18n logic rather than sharing components.
- **Minified variable naming.** The JS uses single-letter variables (`g`, `f`, `b`, `tr`) — hand-optimized or AI-condensed for size, at the cost of readability.
- **No build step.** Pages are plain HTML served as static files; no bundler, no component boundaries.