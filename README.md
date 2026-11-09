# jgmart-hermes 🛵

**Grocery PWA prototype / pilot concept for Japan Garden City, Dhaka.**  WhatsApp-native ordering, Supabase backend, offline-first. Pilot target: roughly 1,700 families across 27 buildings in 4 clusters.

- **Live:** https://jg-mart.vercel.app
- **Repo:** [FahadIbrahim93/jgmart-hermes](https://github.com/FahadIbrahim93/jgmart-hermes)
- **Stack:** HTML/CSS/JS PWA · Supabase · Python automation
- **Stage:** Prototype / pilot concept (not a live business)

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20%2B%20Auth-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![PWA](https://img.shields.io/badge/PWA-Offline_first-5A0FC8?style=for-the-badge)](https://web.dev/progressive-web-apps/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Native_ordering-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/8801870489448)

</div>

---

## What it is

JG Mart is a grocery delivery PWA prototype for Japan Garden City, Dhaka. It is a pilot concept, not an operating business. Figures below are pilot targets or financial models, not verified results.

- **WhatsApp-native ordering** — No app download, no app-store friction
- **Cluster-based routing** — 27 buildings, 4 clusters, optimized delivery (pilot plan)
- **Supabase backend** — PostgreSQL + Auth + RPC for order management
- **Offline-first PWA** — Service worker cache v6, works offline
- **Operator dispatch** — Admin panel with Supabase Auth + PIN fallback
- **Business model** — 51% gross margin model (a financial model, not a reported result)

Built with an AI-assisted workflow: lint → test → build → deploy pipeline. The "~60% cuts shipping time" figure is a target from that pipeline, not a verified result.

---

## Tech highlights

| Area | Implementation |
|---|---|
| **Frontend** | Vanilla HTML/CSS/JS PWA, zero dependencies |
| **Backend** | Supabase (PostgreSQL + Auth + RPC) |
| **Automation** | Python 3.11 scripts for ops and validation |
| **CI/CD** | GitHub Actions (validate + deploy on main) |
| **PWA** | Service worker cache v6, manifest.json, offline-first |
| **Order flow** | WhatsApp API (8801870489448) + Supabase RPC |
| **Admin** | Supabase Auth + PIN fallback |

---

## Pilot plan (targets, not results)

| Item | Value | Note |
|---|---|---|
| Stage | Prototype / pilot | Not live |
| Families (pilot target) | ~1,700 | Planning figure |
| Buildings | 27 | Pilot plan |
| Clusters | 4 (C1–C4) | Pilot plan |
| Products | 82 items, 10 categories | Catalog plan |
| Margin model | 51% gross | Financial model, not reported |
| Source | Krishi Market (800m away) | Planned supply |

---

## Getting started

```bash
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes/src/web/catalog
# Serve with any static server, or deploy to Vercel
```

```bash
# Validate HTML
python src/scripts/automation/validate_html.py

# Validate Python scripts
python -m py_compile src/scripts/automation/*.py
```

See [MASTER_INDEX.md](./MASTER_INDEX.md) for the canonical asset index.

---

## Architecture

- **Customer site** — Static HTML PWA in `src/web/catalog/`
- **Database** — Supabase schema in `src/web/supabase/schema.sql`
- **Automation** — Python scripts in `src/scripts/automation/`
- **Brand assets** — PNGs in `assets/brand/kimi/`
- **Ops docs** — Playbooks in `docs/operations/`
- **Investor materials** — Pitch deck in `src/pitch/`

---

## What this repo shows

1. **Prototype scope** — A grocery PWA concept, not a live business or portfolio demo of completed client work
2. **Zero friction** — WhatsApp-native ordering removes app-store barriers
3. **PWA techniques** — Offline-first, service worker caching, manifest-driven install
4. **Full-stack ownership** — From Supabase schema to Python automation to Vercel deploy

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for setup and PR guidelines.  
See [AGENTS.md](./AGENTS.md) for AI coding standards and architecture rules.
