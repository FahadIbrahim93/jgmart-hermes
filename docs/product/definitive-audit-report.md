# JG Mart — Definitive Codebase Audit & Remediation Plan

**Date:** 2026-08-04
**Scope:** Full repo at `G:\JG Mart`, branch `main` (commit `9b624f4`), 392 files, 6.5MB.
**Source:** `FahadIbrahim93/jgmart-hermes` → live at https://jg-mart.vercel.app
**Method:** Factual review of every source file, Supabase schema/RLS/RPCs, CI workflows, dependency manifests, and the validation harness. This is the single source of truth — not a hypothetical assessment.

---

## Executive Summary

JG Mart is a **capable solo-founder MVP** for hyperlocal grocery delivery in Japan Garden City, Dhaka. The WhatsApp-native, no-app-download flow matches the business model (thin margins, low-friction, ৳800 AOV, 51% margin). The product is aimed correctly — the *implementation* has gaps.

**The one finding that must be fixed before taking real orders:** order pricing is fully client-trusted and written straight into the database. Anyone with the public anon key can call the order RPC directly and insert an order for real products at ৳1 each. This is a direct fraud path, not theoretical.

Everything else is real but lower-severity: a hardcoded admin PIN displayed in the UI, a regex HTML sanitizer, three sources of truth for product data, and a test suite that tests nothing.

---

## Scores (1–10)

| Dimension | Score | Why |
|---|---|---|
| **Security** | **3/10** | Order pricing is fully client-trusted and written straight into the DB via a `SECURITY DEFINER` RPC — the single most serious issue, detailed below. Admin auth has a hardcoded `1234` PIN fallback displayed in the UI. Mitigated somewhat by real RLS on the tables themselves. |
| **Test coverage & reliability** | **2/10** | There are **zero** unit/behavioral tests. `tests/validate_toolkit.py` (the only file in `tests/`) is a static file/link/tag checker, not a test of cart math, order flow, or RLS behavior. CI's `pytest` step is wired as `pytest tests/ -v || echo 'No tests yet'` — it can never fail the build. |
| **Code quality & structure** | **5/10** | Individual functions (e.g. `db.js`) are reasonably clean, with sensible fallback logic and consistent `escapeHtml` use on customer-facing tables. But `index.html` (1,602 lines), `admin.html` (1,222 lines), `order_intake.html` (880 lines) are monolithic HTML+JS+CSS files with minified, single-letter variable naming (`g`, `f`, `b`, `tr`) — clearly hand-optimized or AI-condensed for size, at the cost of readability. |
| **Readability & maintainability** | **4/10** | Same root cause as above. Business logic (pricing, cart state, i18n strings) is interleaved with DOM manipulation in giant template literals. No build step, no bundler, no component boundaries — every page reimplements its own cart/nav/i18n logic independently. |
| **Architecture & modularity** | **4/10** | Three parallel data paths for the same entities: static `catalog_data.json`, `localStorage`, and Supabase, reconciled at runtime via `resolveProductUuid`'s legacy-id-to-UUID mapping. That's real migration debt, not just a fallback — it means product data can silently drift across three sources of truth. RLS design itself (role-based via `profiles.role`) is architecturally sound. |
| **Performance & scalability** | **6/10** | Reasonable for the current scale (82 products, single neighborhood). PWA service worker and offline queue are genuine engineering, not decoration. No pagination on admin order/product tables, no debouncing visible on search-as-you-type — fine at current volume, will not scale past a few hundred orders/products without rework. |
| **Compliance / domain standards** | **4/10** | No visible PCI concerns (cash/WhatsApp-based, no card data touched — good). But there's no rate limiting or CAPTCHA on the public order-creation RPC, no input validation on phone/building beyond client-side regex (server-side `create_public_order` accepts anything), and no audit trail correctness guarantee since `p_total` isn't derived from source data. |
| **Team collaboration readiness** | **5/10** | `AGENTS.md`, `CONTRIBUTING.md`, `CHANGELOG.md` exist, which is more process hygiene than most solo projects bother with. But the repo root is cluttered with overlapping status docs (`MASTER_INDEX.md`, `STATUS_REPORT.md`, `VALIDATION_REPORT.txt`, plus a 1.6MB `ARCHIVE/` and a separate `_archive/agents/` — two different "archive" conventions) that will confuse any second contributor about what's live vs. dead. |
| **Alignment with business objectives** | **7/10** | This is the strongest dimension. The WhatsApp-native, no-app-download flow directly matches the stated business model (thin margins, low-friction hyperlocal delivery), and the zone/slot/pricing config in `config.js` matches the real ops model (clusters, cutoff times, delivery fees). The product is aimed correctly — the *implementation* of that product has the gaps above. |

**Composite: ~4.4/10.** This reads as a fast, capable solo-founder MVP — not a broken toy, but not something that should be taking real customer payments or PII yet without the fixes below.

---

## High-priority issues (ranked by actual risk)

### 1. Order totals are client-supplied and trusted — CRITICAL
`db.js`'s `submitOrder()` sends `subtotal`, `deliveryFee`, `total`, and each line item's `price` straight from the browser cart into `supabase.rpc('create_public_order', ...)`. That RPC (`rls_anonymous_orders.sql`) is `SECURITY DEFINER`, granted to `anon`, and inserts every field verbatim with no recomputation from the `products` table and no check that `total = subtotal + delivery_fee` or that item prices match the catalog.

Anyone with the public anon key (which is, correctly, embedded in the client — that's expected for a publishable key) can call this RPC directly via `curl`, bypassing the UI entirely, and insert an order for real products at ৳1 each, or with items that don't exist. There is nothing server-side stopping this. This is the one finding I'd escalate before anything else — it's a direct path to being defrauded, not a theoretical one.

**Fix:** rewrite `create_public_order` to accept only `item_id` + `qty` per line, look up current price from `products` inside the function, compute subtotal/fee/total server-side from the zone/slot config, and ignore any client-sent price/total fields.

### 2. Admin auth has a hardcoded, displayed default PIN
`admin.html` ships `DEFAULT_PIN = '1234'`, stores it in `localStorage` in plaintext, and prints `Default PIN: 1234` directly in the login UI copy. This is gated somewhat by the fact that actual writes still require a real Supabase-authenticated session with `role IN ('admin','operator')` per RLS — so PIN-only sessions can't mutate protected tables — but it's still a broken, confusing security boundary that will mislead an operator into thinking they have real admin access when they don't, and normalizes "PIN in cleartext, shown on screen" as acceptable.

**Fix:** drop the PIN fallback entirely, or if it must exist for offline ops use, generate a random PIN per deployment via env var, never render it in the DOM, and never let it imply write access it doesn't grant.

### 3. Tests don't test anything, and CI can't fail on them
`tests/validate_toolkit.py` checks that HTML tags are balanced and that files referenced in docs actually exist. That's useful as a docs-linter, but it is being presented (in `package.json`'s `validate` script and the README's Quick Start) as *the* test suite. There is no test asserting cart totals compute correctly, that RLS actually blocks a non-admin write, that the WhatsApp message is built correctly, or that `resolveProductUuid` resolves what it claims to. Compounding this, CI runs `pytest tests/ -v || echo 'No tests yet'` — even if real tests existed and failed, the build would still go green. Same pattern in the security job: `bandit -r src/ -ll || true` — findings are printed, never enforced.

**Fix:** separate "docs validation" from "tests." Write real tests (pytest for the Python automation, Playwright or plain fetch-based tests for the RPC/RLS behavior — Supabase's local dev stack makes this straightforward). Remove the `|| echo` / `|| true` escape hatches from CI once real tests exist, so a red test actually blocks a merge.

### 4. Hand-rolled regex HTML sanitizer
`security.js`'s `sanitizeHtml()` strips `<script>` tags and `on*` attributes with regex. Regex-based HTML sanitization is a well-known bypass magnet (malformed/nested tags, `<svg onload>`, `data:` URIs not covered here, obscure encodings). Current usage looks limited to admin-facing surfaces already gated by `escapeHtml` elsewhere, so exposure looks contained today — but it's a landmine for the next feature that renders richer user content.

**Fix:** either don't accept/render HTML from user input at all (escape everything, which is what most of the codebase already correctly does), or if rich text is genuinely needed, use DOMPurify rather than a hand-rolled filter.

### 5. Three sources of truth for product data
`catalog_data.json` (static file), `localStorage`, and Supabase all hold product data, reconciled at runtime by mapping legacy string IDs (`p001`) to Supabase UUIDs. This works today but is real migration debt: any process that updates one without the others (e.g., editing the JSON but not re-running `sync_catalog_to_supabase.py`) silently desyncs price/stock between what customers see and what's authoritative.

**Fix:** pick Supabase as the single source of truth now that it's live, keep `catalog_data.json` only as a generated offline-fallback artifact (not hand-edited), and delete the legacy-ID mapping layer once all data is migrated.

### 6. Repo hygiene / dead weight
1.6MB `ARCHIVE/` plus a separate `_archive/agents/` (two different "old stuff" conventions), five overlapping root-level status docs (`MASTER_INDEX.md`, `STATUS_REPORT.md`, `VALIDATION_REPORT.txt`, `CHANGELOG.md`, `IDEA.md`). None of this breaks anything, but it's the kind of clutter that makes a second engineer's first day painful — they can't tell what's live without reading everything.

**Fix:** one `ARCHIVE/` (or none — use git history instead), collapse status docs into the README + CHANGELOG, delete the rest.

---

## Concrete improvement plan

**Code-level (do these first, in order):**
1. Rewrite `create_public_order` to price server-side from `products` + zone config; reject the client's price/total fields.
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