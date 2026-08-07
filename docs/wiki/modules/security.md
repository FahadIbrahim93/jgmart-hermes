# Module: Security

The security module provides sanitization, validation, and authentication helpers.

## Responsibilities

- Escape HTML to prevent XSS on customer-facing surfaces.
- Sanitize HTML (strip `<script>` and event handlers) for admin surfaces.
- Validate phone numbers, building numbers, and flat numbers.
- Manage admin auth (PIN fallback, session expiry).

## Key Files

- [`src/web/catalog/security.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/security.js) — `escapeHtml`, `sanitizeHtml`, `sanitizeUrl`, `validatePhone`, `validateBuilding`, `validateFlat`.
- [`src/web/auth.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/auth.js) — admin auth (PIN, session, `getCurrentUser`, `isAdmin`).
- [`src/web/catalog/admin.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/admin.html) — admin auth UI (PIN fallback).

## Public API

- `JG_SECURITY` — `escapeHtml(str)`, `sanitizeHtml(html)`, `sanitizeUrl(url)`, `validatePhone(phone)`, `validateBuilding(b)`, `validateFlat(f)`.
- `getCurrentUser()` / `isAdmin()` / `signOut()` (from `auth.js`).

## Internal Structure

`escapeHtml` escapes `&<>\"'` — used on customer-facing tables. `sanitizeHtml` strips `<script>` tags and `on*` attributes with regex, plus `javascript:` URIs — used on admin surfaces. `sanitizeUrl` allows `https://`, `http://`, `mailto:`, `tel:`, `#`, `/`.

Admin auth uses a PIN fallback (`DEFAULT_PIN = '1234'`) stored in localStorage, with a 24-hour session expiry. Actual data writes still require a real Supabase-authenticated session with `role IN ('admin','operator')` per RLS.

## Dependencies

- **Used by:** all catalog pages (via `security.js`), admin panel.
- **Uses:** none (standalone).

## Notable Patterns / Gotchas

- **Regex HTML sanitizer.** `sanitizeHtml` uses regex to strip `<script>` and `on*` attributes — a well-known bypass magnet (malformed/nested tags, `<svg onload>`, `data:` URIs not covered). Current usage is limited to admin surfaces already gated by `escapeHtml`, so exposure is contained today — but it's a landmine for the next feature that renders richer user content.
- **Hardcoded PIN.** `DEFAULT_PIN = '1234'` is stored in localStorage in plaintext and printed in the login UI.
- **Static CSP nonce.** Pages use `script-src 'nonce-gscb6Xp2nALPgenhRE7XtA'` — the nonce is static in the source (not per-request), which is a known CSP weakness.