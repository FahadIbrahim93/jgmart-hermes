# JG Mart

**JG Mart** is a hyperlocal grocery delivery platform for Japan Garden City (JGC), Mohammadpur, Dhaka. We source fresh produce from Krishi Market (800m away) and deliver same-day to ~1,700 families across 27 buildings — at wholesale prices, with zero app download friction.

**Live site:** [jg-mart.vercel.app](https://jg-mart.vercel.app)  
**GitHub:** [FahadIbrahim93/jgmart-hermes](https://github.com/FahadIbrahim93/jgmart-hermes)

---

## 🎯 What this is

JG Mart is a revenue-first grocery delivery operation built as a PWA. The business model targets 51% gross margin by removing middlemen and running WhatsApp-native ordering on top of Supabase. This repo is the single source of truth for code, ops docs, brand assets, and investor materials.

---

## 📊 Business metrics

| Item | Value |
|------|-------|
| Stage | Pre-seed / Pilot |
| License | MIT |
| Frontend | Vanilla HTML/CSS/JS PWA |
| Backend | Supabase (PostgreSQL + Auth) |
| Products | 82 items, 10 categories |
| Coverage | 27 buildings, 4 clusters (C1–C4) |
| Live Site | 20/20 files returning 200 |
| Validation | 45/45 HTML, 17/17 Python |
| PWA | Service worker (cache v6), manifest.json |
| Order Flow | WhatsApp (8801870489448) + Supabase RPC |
| Admin | Supabase Auth + PIN fallback |

---

## 🛠️ Tech stack

- **Catalog:** Static HTML PWA deployed on Vercel
- **Database:** Supabase (`src/web/supabase/schema.sql`)
- **Automation:** Python 3.11 scripts
- **CI:** GitHub Actions (validate + deploy catalog on `main`)

---

## 🗂️ Repository map

```
├── MASTER_INDEX.md          # Canonical asset index — start here
├── AGENTS.md                # Rules for AI agents working in this repo
├── docs/origin/             # Origin notes, session reports
├── src/web/catalog/         # Live customer website
├── src/web/supabase/        # Database schema + seed (migration target)
├── src/pitch/               # Investor deck + scripts
├── src/templates/           # Legal, marketing, ops templates
├── src/scripts/automation/  # Python tooling
├── assets/brand/kimi/       # Brand PNGs (print + social)
├── data/trackers/           # CSV/XLSX financial + ops trackers
├── docs/operations/         # Ops playbooks
├── docs/product/PRD.md      # Product requirements
└── _archive/agents/         # Frozen originals (read-only)
```

---

## 🚀 Quick start

```bash
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes
pip install -r requirements.txt
python tests/validate_toolkit.py
```

---

## 📚 Key docs

| Document | Path |
|----------|------|
| Master index | `MASTER_INDEX.md` |
| PRD | `docs/product/PRD.md` |
| Pitch deck | `src/pitch/deck.html` |
| Financial model | `src/pitch/financial_model.md` |
| Supabase setup | `docs/setup/SUPABASE_SETUP.md` |
| Agent rules | `AGENTS.md` |

---

## 🏆 Why this matters

- **Unit-economics clarity:** 51% margin model with real coverage, categories, and order flow
- **WhatsApp-native UX:** Zero app download friction for a low-trust, high-frequency grocery market
- **PWA-first:** Offline-capable catalog with service worker caching
- **Automated validation:** HTML + Python validation in CI before deploy
- **Single source of truth:** Code, ops, brand, and investor materials consolidated in one repo

---

## 📄 License

MIT — see [LICENSE](LICENSE).

Built with hustle. Documented for scale.
