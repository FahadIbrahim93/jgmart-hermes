# Module: Data

The data module handles Supabase integration, data models, and row-level security (RLS).

## Responsibilities

- Connect to Supabase (URL + anon key) with environment-based config.
- Load products, categories, and orders from Supabase with JSON/localStorage fallback.
- Enforce RLS policies on all tables.
- Manage the legacy ID-to-UUID mapping for product data.

## Key Files

- [`src/web/supabase/client.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/supabase/client.js) — Supabase client initialization.
- [`src/web/supabase/config.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/supabase/config.js) — config loading (runtime > local > placeholders), `JG_MART_CONFIG` (zones, slots, fees, categories).
- [`src/web/supabase/schema.sql`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/supabase/schema.sql) — base schema (profiles, categories, products, orders, order_items).
- [`src/web/supabase/migrations/`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/supabase/migrations/) — RLS/RPC migrations.
- [`src/web/supabase/seed.sql`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/supabase/seed.sql) — seed data.
- [`src/web/supabase/seed_from_catalog.sql`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/supabase/seed_from_catalog.sql) — seed from `catalog_data.json`.

## Public API

- `isSupabaseConfigured()` — true when real Supabase credentials are configured (not placeholders).
- `JG_MART_CONFIG` — zones, slots, fees, categories, currency, WhatsApp number.

## Data Models

- **profiles** — extends `auth.users`, role-based (`customer`, `operator`, `admin`, `partner`), RLS via `profiles.role`.
- **products** — `id` (UUID), `category_id`, `name`, `price`, `unit`, `in_stock`, `metadata` (legacy_id).
- **categories** — `id` (TEXT), `name`, `name_bn`, `icon`, `sort_order`.
- **orders** — `order_number`, `customer_name`, `customer_phone`, `customer_building`, `customer_flat`, `delivery_slot`, `delivery_date`, `items` (JSONB), `subtotal`, `delivery_fee`, `total`, `payment_method`, `status`.
- **order_items** — `order_id`, `product_id`, `product_name`, `quantity`, `unit_price`, `total`.

## RLS Policies

- `profiles` — users view/update own profile; admins view all.
- `categories` / `products` — viewable by everyone; modify only by `admin`/`operator`.
- `orders` — staff view/update all; `anon` can INSERT via the permissive policy (defense-in-depth for the `SECURITY DEFINER` RPC).
- `order_items` — viewable with the order (customer or staff).

## Notable Patterns / Gotchas

- **Three sources of truth.** Product data lives in Supabase (authoritative), `catalog_data.json` (static fallback), and `localStorage` (cart state). `resolveProductUuid` reconciles them via legacy ID mapping — real migration debt.
- **`SECURITY DEFINER` RPC.** `create_public_order` runs with definer privileges, letting anon insert into `orders`. The permissive RLS policy on `orders`/`order_items` is the defense-in-depth layer.
- **Config loading order.** `config.js` loads in order: runtime (CI/production, `window.__JG_MART_SUPABASE__`) > local (`config.local.js`, gitignored) > placeholders.