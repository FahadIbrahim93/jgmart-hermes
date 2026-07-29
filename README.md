# JG Mart

**JG Mart** is a hyperlocal grocery delivery platform for Japan Garden City (JGC), Mohammadpur, Dhaka. We source fresh produce from Krishi Market (800m away) and deliver same-day to ~1,700 families across 27 buildings — at wholesale prices, with zero app download friction.

**Live site:** [jg-mart.vercel.app](https://jg-mart.vercel.app)  
**GitHub:** [FahadIbrahim93/jgmart-hermes](https://github.com/FahadIbrahim93/jgmart-hermes)

This repository is the **single source of truth** for code, ops docs, brand assets, and investor materials. Consolidated from Hermes (code), Grok (ops playbooks), and Kimi (brand + PRD).

## Quick Start

```bash
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes
pip install -r requirements.txt
python tests/validate_toolkit.py
```

## Status

| Item | Value |
|------|-------|
| Stage | Pre-seed / Pilot |
| License | MIT |
| Frontend | Vanilla HTML/CSS/JS PWA |
| Backend (target) | Supabase (PostgreSQL + Auth) |
| Backend (legacy) | localStorage admin — being replaced |
| Products | 65 items, 10 categories |
| Coverage | 27 buildings, 4 clusters (C1–C4) |

## Repository Map

```
├── MASTER_INDEX.md          # Canonical asset index — start here
├── AGENTS.md                # Rules for AI agents working in this repo
├── IDEA.md                  # Origin note
├── src/web/catalog/         # Live customer website
├── src/web/supabase/        # Database schema + seed (migration target)
├── src/pitch/               # Investor deck + scripts
├── src/templates/           # Legal, marketing, ops templates
├── src/scripts/automation/  # Python tooling
├── assets/brand/kimi/       # Brand PNGs (print + social)
├── data/trackers/           # CSV/XLSX financial + ops trackers
├── docs/operations/         # Grok + Kimi ops playbooks
├── docs/product/PRD.md      # Product requirements
└── _archive/agents/         # Frozen Grok/Kimi originals (read-only)
```

## Stack

- **Catalog:** Static HTML PWA deployed on Vercel
- **Database:** Supabase (`src/web/supabase/schema.sql`)
- **Automation:** Python 3.11 scripts
- **CI:** GitHub Actions (validate + deploy catalog on `main`)

## Key Docs

| Document | Path |
|----------|------|
| Master index | `MASTER_INDEX.md` |
| PRD | `docs/product/PRD.md` |
| Pitch deck | `src/pitch/deck.html` |
| Financial model | `src/pitch/financial_model.md` |
| Supabase setup | `ARCHIVE/docs_old/SUPABASE_SETUP.md` |
| Agent rules | `AGENTS.md` |

## Deployment

Vercel auto-deploys `src/web/catalog` on push to `main` via GitHub Actions. Config: `vercel.json` at repo root.

## For AI Agents

Read `AGENTS.md` and `MASTER_INDEX.md` before creating files. Do not create sibling agent folders (Grok/Kimi/Hermes). All work happens in this repo.

---

*Built with hustle. Documented for scale.*
