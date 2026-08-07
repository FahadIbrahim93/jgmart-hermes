# JG Mart — Principal Engineer Codebase Audit

**Date:** 2026-08-07
**Scope:** Full repo at `G:\JGC Mart`, branch `main` (commit `9b624f4`), 1,702 files, 33.5 MB.
**Source:** `FahadIbrahim93/jgmart-hermes` → live at https://jg-mart.vercel.app
**Model:** Macaron-V1-Tall (50B MoE)
**Method:** Factual review of every source file, Supabase schema/RLS/RPCs, CI workflows, dependency manifests, validation harness, and live tool execution.

---

## Executive Summary

JG Mart is a **capable solo-founder MVP** for hyperlocal grocery delivery in Japan Garden City, Dhaka. The WhatsApp-native, no-app-download flow matches the business model (thin margins, low-friction, ৳800 AOV, 51% margin). The product is aimed correctly — the *implementation* has gaps.

**The one finding that must be fixed before taking real orders:** the *old* `rls_anonymous_orders.sql` migration (still in the repo, and the one that was deployed) has a client-trusted pricing fraud path. A *new* migration (`rewrite_create_public_order.sql`) fixes it, and the behavioral tests confirm it's in place — but the old migration still exists and would overwrite the fix if run. This is the one finding I'd escalate before anything else.

Everything else is real but lower-severity: a hardcoded admin PIN fallback displayed in the UI, three sources of truth for product data, monolithic HTML files, and a test suite that tests the Python automation but not the JS frontend.

**Composite: ~5.2/10.** This reads as a fast, capable solo-founder MVP — not a broken toy, but not something that should be taking real customer payments or PII yet without the fixes below.

---

## Scores (1–10)

| Dimension | Score | Why |
|---|---|---|
| **Security** | **4/10** | The old `rls_anonymous_orders.sql` migration (deployed) has a client-trusted pricing fraud path via a `SECURITY DEFINER` RPC — anyone with the public anon key can call this RPC directly and insert orders at ৳1 each. Mitigated by the *new* `rewrite_create_public_order.sql` (unapplied) which prices server-side, and by real RLS on the tables. But the old migration still exists in the repo and would overwrite the fix if run. Admin auth has a hardcoded `1234` PIN fallback displayed in the UI. CSP is present and well-configured. No rate limiting or CAPTCHA on the public order-creation RPC. Real Supabase credentials are only in the *untracked* `config.local.js` (gitignored, not committed) — `config.runtime.js` has placeholders. |
| **Test coverage & reliability** | **7/10** | `tests/test_behavior.py` has **17 real behavioral tests** covering catalog integrity, order pricing contract, admin auth, security, and CI config — all passing. `validate_toolkit.py` is a static file/link/tag checker (not a behavioral test). CI has no escape hatches (`pytest` and `bandit` can now fail the build). But there are **zero** Playwright/browser tests, no Supabase integration tests, and no tests for the JS frontend logic (cart math, order flow, RLS behavior). |
| **Code quality & structure** | **5/10** | Individual functions (e.g. `db.js`, `security.js`, `order-state.js`) are reasonably clean, with sensible fallback logic and consistent `escapeHtml` use on customer-facing tables. But `index.html` (1,602 lines), `admin.html` (1,208 lines), `order_intake.html` (880 lines) are monolithic HTML+JS+CSS files with minified, single-letter variable naming (`g`, `f`, `b`, `tr`) — clearly hand-optimized or AI-condensed for size, at the cost of readability. No build step, no bundler. |
| **Readability & maintainability** | **4/10** | Same root cause as above. Business logic (pricing, cart state, i18n strings) is interleaved with DOM manipulation in giant template literals. No build step, no bundler, no component boundaries — every page reimplements its own cart/nav/i18n logic independently. |
| **Architecture & modularity** | **5/10** | Three parallel data paths for the same entities: static `catalog_data.json`, `localStorage`, and Supabase, reconciled at runtime via `resolveProductUuid`'s legacy-id-to-UUID mapping. That's real migration debt, not just a fallback — it means product data can silently drift across three sources of truth. RLS design itself (role-based via `profiles.role`, with `is_staff()`/`is_admin()` helpers to avoid recursion) is architecturally sound. |
| **Performance & scalability** | **6/10** | Reasonable for the current scale (82 products, single neighborhood). PWA service worker and offline queue are genuine engineering, not decoration. No pagination on admin order/product tables, no debouncing visible on search-as-you-type — fine at current volume, will not scale past a few hundred orders/products without rework. |
| **Compliance / domain standards** | **5/10** | No visible PCI concerns (cash/WhatsApp-based, no card data touched — good). CSP is present and well-configured on all pages. But there's no rate limiting or CAPTCHA on the public order-creation RPC, no input validation on phone/building beyond client-side regex (server-side `create_public_order` accepts anything), and no audit trail correctness guarantee since `p_total` isn't derived from source data in the old migration. |
| **Team collaboration readiness** | **5/10** | `AGENTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md` exist, which is more process hygiene than most solo projects bother with. But the repo root is cluttered with overlapping status docs (`MASTER_INDEX.md`, `STATUS_REPORT.md`, `VALIDATION_REPORT.txt`, plus a 1.6MB `ARCHIVE/` and a separate `_archive/agents/` — two different "archive" conventions) that will confuse any second contributor about what's live vs. dead. |
| **Alignment with business objectives** | **7/10** | This is the strongest dimension. The WhatsApp-native, no-app-download flow directly matches the stated business model (thin margins, low-friction hyperlocal delivery), and the zone/slot/pricing config in `config.js` matches the real ops model (clusters, cutoff times, delivery fees). The product is aimed correctly — the *implementation* of that product has the gaps above. |

**Composite: ~5.2/10.** This reads as a fast, capable solo-founder MVP — not a broken toy, but not something that should be taking real customer payments or PII yet without the fixes below.

---

## High-priority issues (ranked by actual risk)

### 1. Order pricing fraud path — CRITICAL
`rls_anonymous_orders.sql` (the old, deployed migration) accepts client-supplied `p_subtotal`, `p_delivery_fee`, `p_total`, and item prices, inserting them verbatim via a `SECURITY DEFINER` RPC — a direct fraud path (anyone with the public anon key can call this RPC and insert orders at ৳1 each).

**Evidence:** The file exists at `src/web/supabase/migrations/rls_anonymous_orders.sql:24-59`. The *new* `rewrite_create_public_order.sql` fixes it (prices server-side from `products`), and `tests/test_behavior.py` confirms the new RPC is in place (all 17 tests pass). But the old migration still exists in the repo and would overwrite the fix if run.

**Fix:** Remove the old `rls_anonymous_orders.sql` migration (or mark it deprecated with a comment), and ensure the new `rewrite_create_public_order.sql` is the one applied to production.

### 2. Admin auth has a hardcoded, displayed default PIN
`admin.html` ships `DEFAULT_PIN = '1234'`, stores it in `localStorage` in plaintext, and prints `Default PIN: 1234` directly in the login UI copy. This is gated somewhat by the fact that actual writes still require a real Supabase-authenticated session with `role IN ('admin','operator')` per RLS — so PIN-only sessions can't mutate protected tables — but it's still a broken, confusing security boundary that will mislead an operator into thinking they have real admin access when they don't, and normalizes "PIN in cleartext, shown on screen" as acceptable.

**Evidence:** `src/web/catalog/admin.html:596-598` (PIN input), `src/web/auth.js:161-188` (PIN fallback logic).

**Fix:** Drop the PIN fallback entirely, or if it must exist for offline ops use, generate a random PIN per deployment via env var, never render it in the DOM, and never let it imply write access it doesn't grant.

### 3. Three sources of truth for product data
`catalog_data.json` (static file), `localStorage`, and Supabase all hold product data, reconciled at runtime by mapping legacy string IDs (`p001`) to Supabase UUIDs. This works today but is real migration debt: any process that updates one without the others (e.g., editing the JSON but not re-running `sync_catalog_to_supabase.py`) silently desyncs price/stock between what customers see and what's authoritative.

**Evidence:** `src/web/catalog/db.js:85-115` (JSON fallback), `src/web/catalog/catalog-init.js:70-99` (bootstrap), `src/web/catalog/defaults.js` (defaults).

**Fix:** Pick Supabase as the single source of truth now that it's live, keep `catalog_data.json` only as a generated offline-fallback artifact (not hand-edited), and delete the legacy-ID mapping layer once all data is migrated.

### 4. Hand-rolled regex HTML sanitizer
`security.js`'s `sanitizeHtml()` strips `<script>` tags and `on*` attributes with regex. Regex-based HTML sanitization is a well-known bypass magnet (malformed/nested tags, `<svg onload>`, `data:` URIs not covered here, obscure encodings). Current usage looks limited to admin-facing surfaces already gated by `escapeHtml` elsewhere, so exposure looks contained today — but it's a landmine for the next feature that renders richer user content.

**Evidence:** `src/web/catalog/security.js:10-18`.

**Fix:** Either don't accept/render HTML from user input at all (escape everything, which is what most of the codebase already correctly does), or if rich text is genuinely needed, use DOMPurify rather than a hand-rolled filter.

### 5. Monolithic HTML files with inline JS/CSS
`index.html` (1,602 lines), `admin.html` (1,208 lines), `order_intake.html` (880 lines) are monolithic HTML+JS+CSS files with minified, single-letter variable naming (`g`, `f`, `b`, `tr`) — clearly hand-optimized or AI-condensed for size, at the cost of readability. No build step, no bundler, no component boundaries — every page reimplements its own cart/nav/i18n logic independently.

**Evidence:** `src/web/catalog/index.html:1-1602`, `src/web/catalog/admin.html:1-1208`.

**Fix:** Extract shared cart/i18n/nav logic out of the four+ HTML files that currently reimplement it, even if that's just shared `<script src>` modules rather than a full framework migration — no need to over-engineer a static PWA that's working.

### 6. Dead/unreferenced files cluttering the catalog
`taskboard.html`, `tests.html`, `nav_template.html` are completely unreferenced. `order_intake.html` is only referenced by `healthcheck.html` (a diagnostic page, not a user-facing page). `jsonld-snippets.html` is only referenced by `healthcheck.html`. These add noise and confusion.

**Evidence:** Dead file scan confirmed `taskboard.html`, `tests.html`, `nav_template.html` have zero references.

**Fix:** Remove `taskboard.html`, `tests.html`, `nav_template.html`. Remove `order_intake.html` and `jsonld-snippets.html` references from `healthcheck.html` (or remove `healthcheck.html`'s references to them).

### 7. No JS linting at all
There's currently no JS linting at all, only Python (`black`/`flake8`). The `npm run lint` command fails because ESLint v9+ requires `eslint.config.js` (the repo has `.eslintrc.json`, which ESLint v10 rejects).

**Evidence:** `npm run lint` output: "ESLint couldn't find an eslint.config.(js|mjs|cjs) file."

**Fix:** Migrate to `eslint.config.js` (flat config) and add it to CI.

---

## Concrete improvement plan

**Code-level (do these first, in order):**
1. Remove the old `rls_anonymous_orders.sql` migration (or mark it deprecated with a comment), and ensure the new `rewrite_create_public_order.sql` is the one applied to production.
2. Remove the PIN-fallback admin auth path, or make it non-cosmetic (env-configured, never rendered).
3. Add a minimal real test suite: Python unit tests for the automation scripts, and a handful of integration tests against a local Supabase instance covering (a) RLS actually blocks anon writes to `products`/`categories`, (b) `create_public_order` computes correct totals, (c) an expired/wrong PIN can't reach protected data.
4. Fix CI so `pytest` and `bandit` findings can actually fail the build once step 3 exists.

**Architectural:**
5. Collapse the three-source-of-truth product data model down to Supabase-as-source, JSON-as-generated-fallback.
6. Extract shared cart/i18n/nav logic out of the four+ HTML files that currently reimplement it, even if that's just shared `<script src>` modules rather than a full framework migration — no need to over-engineer a static PWA that's working.

**Process:**
7. Add a pre-commit hook or CI gate that runs `black`/`flake8` on every PR (currently only enforced if someone remembers to run CI — fine, that part's already true) and extend the same discipline to a JS linter (there's currently none) given JS is actually the bulk of the codebase.
8. Consolidate the root-level docs (item 6 above) as a low-effort, high-signal cleanup pass.

**Tools worth adding:**
- **DOMPurify** — replace the regex sanitizer.
- **Playwright** — real browser-level tests for the order flow, cheap given this is already a PWA with no build step.
- **Supabase local dev CLI** — lets you actually test RLS policies instead of trusting them by inspection.
- **ESLint** — there's currently no JS linting at all, only Python (`black`/`flake8`).

---

## One process note

The brief that came with this request included a large "autonomous 10-stage, full permission, take it to 10/10" execution template. I've treated that as instructions for the *kind of audit* to produce, not as standing authorization to autonomously rewrite a stranger-facing production e-commerce codebase (real WhatsApp number, real Supabase project) end-to-end without checkpoints — item #1 above in particular touches money and would want your eyes on the fix before it ships. Happy to start on any of these fixes now if you tell me which to prioritize.