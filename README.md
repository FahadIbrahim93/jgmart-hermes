# jgmart-hermes 🛵

**Hyperlocal grocery delivery PWA for 1,700 families.**  
WhatsApp-native ordering, Supabase backend, 51% margin model. Zero app download friction.

- **Live:** https://jg-mart.vercel.app  
- **Repo:** [FahadIbrahim93/jgmart-hermes](https://github.com/FahadIbrahim93/jgmart-hermes)  
- **Stack:** HTML/CSS/JS PWA · Supabase · Python automation  
- **Stage:** Pre-seed / pilot — 27 buildings, 4 clusters, 82 products

<div align="center">

![JG Mart](https://img.shields.io/badge/JG_Mart-Pre_seed-blue?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL%20%2B%20Auth-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![PWA](https://img.shields.io/badge/PWA-Offline_first-5A0FC8?style=for-the-badge)](https://web.dev/progressive-web-apps/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Native_ordering-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/8801870489448)

</div>

---

## What it is

JG Mart is a revenue-first grocery delivery PWA for Japan Garden City, Dhaka. Built for real families, not portfolio demos:

- **WhatsApp-native ordering** — No app download, no app-store friction
- **Cluster-based routing** — 27 buildings, 4 clusters, optimized delivery
- **Supabase backend** — PostgreSQL + Auth + RPC for order management
- **Offline-first PWA** — Service worker cache v6, works offline
- **Operator dispatch** — Admin panel with Supabase Auth + PIN fallback
- **Business model** — 51% gross margin by removing middlemen

Built with AI-assisted workflow: lint → test → build → deploy pipeline cuts shipping time ~60% while maintaining quality gates.

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

## Business metrics

| Item | Value |
|---|---|
| Stage | Pre-seed / Pilot |
| Families | 1,700 |
| Buildings | 27 |
| Clusters | 4 (C1–C4) |
| Products | 82 items, 10 categories |
| Margin | 51% gross |
| Source | Krishi Market (800m away) |

---

## Quality metrics

- **Validation** — 45/45 HTML, 17/17 Python checks passing
- **Live Site** — 20/20 files returning HTTP 200
- **PWA** — Service worker cache v6, manifest.json
- **CI** — GitHub Actions green on main

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

## Why this repo stands out

1. **Revenue-first** — Built for a real business with 51% margin model, not a portfolio demo
2. **Zero friction** — WhatsApp-native ordering removes app-store barriers
3. **PWA expertise** — Offline-first, service worker caching, manifest-driven install
4. **Full-stack ownership** — From Supabase schema to Python automation to Vercel deploy
5. **Real metrics** — 1,700 families, 27 buildings, 4 clusters, 82 products

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for setup and PR guidelines.  
See [AGENTS.md](./AGENTS.md) for AI coding standards and architecture rules.
