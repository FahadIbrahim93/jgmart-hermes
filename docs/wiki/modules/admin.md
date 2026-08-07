# Module: Admin

The admin module provides the operator/admin panel for managing products and orders.

## Responsibilities

- Authenticate admin operators (Supabase sign-in or PIN fallback).
- Display and manage products (CRUD via Supabase).
- Display and manage orders (status transitions, bulk actions, print manifest).
- View analytics (dashboard).

## Key Files

- [`src/web/catalog/admin.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/admin.html) — admin panel (1,222 lines).
- [`src/web/catalog/admin-backend.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/admin-backend.js) — admin Supabase backend (fetchProducts, fetchOrders, signIn, signOut).
- [`src/web/auth.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/auth.js) — shared auth module (PIN, session, `getCurrentUser`, `isAdmin`).

## Public API

- `JG_ADMIN_BACKEND` (from `admin-backend.js`) — `enabled`, `signIn`, `signOut`, `fetchProducts`, `fetchOrders`.
- `getCurrentUser()` / `isAdmin()` (from `auth.js`) — session and role checks.

## Internal Structure

Admin auth supports two paths: Supabase sign-in (when configured) and a PIN fallback (`DEFAULT_PIN = '1234'`). PIN-only sessions are stored in localStorage with `pinOnly: true` and a 24-hour expiry. Actual data writes still require a real Supabase-authenticated session with `role IN ('admin','operator')` per RLS — PIN-only sessions can't mutate protected tables.

The admin panel fetches products and orders from Supabase (falling back to localStorage), renders them in tables, and allows status transitions and bulk actions.

## Dependencies

- **Used by:** admin operators (browser).
- **Uses:** Supabase client, `auth.js`, `security.js` (escaping), `order-state.js` (status transitions).

## Notable Patterns / Gotchas

- **Hardcoded PIN.** `DEFAULT_PIN = '1234'` is stored in localStorage in plaintext and printed in the login UI (`Default PIN: 1234`). This is a confusing security boundary — it implies write access it doesn't grant (RLS still blocks protected writes), but normalizes "PIN in cleartext, shown on screen" as acceptable.
- **Monolithic admin page.** `admin.html` is 1,222 lines with inline CSS and JS, minified variable naming, and interleaved business logic.
- **No pagination.** Admin order/product tables have no pagination — fine at current volume, will not scale past a few hundred rows.