# JG Mart — Agent Instructions

This file defines how AI agents (Cursor, Grok, Kimi, etc.) should work on this project.

## Source of Truth

- **Repository:** `G:\JGC Mart` (this folder = git root)
- **GitHub:** `FahadIbrahim93/jgmart-hermes`
- **Live site:** https://jg-mart.vercel.app

## Rules

1. **Do not** create sibling folders like `JGC Mart-Grok`, `JG Mart- Kimi`, or `JGC Mart - Hermes`. Those are retired.
2. **Do not** create duplicate `MASTER_INDEX` files. Use `MASTER_INDEX.md` at repo root only.
3. **Do not** use localStorage for new features. Target backend: Supabase (`src/web/supabase/`).
4. **Do not** commit secrets (`.env`, API keys, real customer data).
5. **Check** `MASTER_INDEX.md` before adding new docs or assets.
6. **New files go in:**
   - Code → `src/`
   - Brand images → `assets/brand/`
   - Trackers (CSV) → `data/trackers/`
   - Ops docs → `docs/operations/`
   - Product docs → `docs/product/`

## Tech Stack (locked)

| Layer | Technology |
|-------|------------|
| Frontend | Vanilla HTML/CSS/JS (no Next.js unless explicitly requested) |
| Backend | Supabase (PostgreSQL + Auth) |
| Hosting | Vercel (catalog) |
| Automation | Python 3.11 |

## Workflow

1. Work on a feature branch (`feature/description`)
2. Run `python tests/validate_toolkit.py` before committing
3. Open PR to `main` — CI validates and deploys catalog

## Archived Agent Work

Original Grok and Kimi outputs are frozen in `_archive/agents/`. Import new content from other agents into the proper `docs/`, `assets/`, or `data/` paths — do not edit archives.

## Owner

Fahad Ibrahim — Japan Garden City, Mohammadpur, Dhaka
