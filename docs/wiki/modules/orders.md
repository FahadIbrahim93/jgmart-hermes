# Module: Orders

The orders module handles order submission, tracking, and the offline queue.

## Responsibilities

- Submit orders to Supabase via the `create_public_order` RPC.
- Generate order numbers via the `generate_order_number` RPC.
- Track order status with validated transitions.
- Queue orders offline when the network is unavailable.

## Key Files

- [`src/web/catalog/db.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/db.js) — order submission (`submitOrder`), product UUID resolution, localStorage fallback.
- [`src/web/catalog/order_intake.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/order_intake.html) — order form (880 lines).
- [`src/web/catalog/order-state.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/order-state.js) — order status constants and transition validation.
- [`src/web/catalog/offline-queue.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/offline-queue.js) — offline order queue.
- [`src/web/catalog/track.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/track.html) — order tracking page.
- [`src/web/catalog/notify.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/notify.html) — WhatsApp notification templates.

## Public API

- `db.js:submitOrder(orderData)` — normalizes input, calls the `create_public_order` RPC, saves to localStorage, returns `{ success, order }`.
- `db.js:resolveProductUuid(legacyOrUuid)` — maps legacy catalog IDs (`p001`) to Supabase UUIDs.
- `JG_ORDER_STATE` (from `order-state.js`) — `STATUSES`, `LABELS`, `ALLOWED_NEXT`, `canTransition`, `apply`.

## Internal Structure

`submitOrder` normalizes the order input (accepting both camelCase and legacy field names), generates an order number via RPC, calls `create_public_order` (a `SECURITY DEFINER` function), inserts line items into `order_items`, and saves a copy to localStorage. If Supabase is unreachable, it falls back to localStorage-only.

Order status transitions are validated against `ALLOWED_NEXT` (e.g. `pending` → `confirmed`/`cancelled`), preventing invalid state changes.

## Dependencies

- **Used by:** `index.html`, `order_intake.html`, `track.html`, `admin.html`.
- **Uses:** Supabase client (`client.js`), `config.js` (zone/slot config), `security.js` (validation).

## Notable Patterns / Gotchas

- **Client-trusted pricing.** `submitOrder` sends `subtotal`, `deliveryFee`, `total`, and each item's `price` from the browser cart into the RPC. The RPC inserts these verbatim with no server-side recomputation — a direct fraud path (see audit report item #1).
- **Legacy ID mapping.** `resolveProductUuid` maps legacy string IDs (`p001`) to Supabase UUIDs via an in-memory index. This is migration debt from the three-source-of-truth model.
- **Offline queue.** Orders are queued in localStorage when the network is down and replayed when it returns.