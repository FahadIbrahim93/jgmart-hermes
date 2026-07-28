# JG Mart Hermes

**JG Mart** is a neighborhood grocery delivery platform built for hyperlocal communities. We combine WhatsApp-first ordering, real-time inventory tracking, and rider logistics to deliver fresh products within hours.

This repository contains the complete technical, business, and operational foundation for the JG Mart platform.

## Status

> **✅ All 37 HTML pages pass validation. Supabase Auth integrated. Zero hardcoded credentials.**

- **Stage:** Pre-seed / Pilot
- **License:** MIT
- **Stack:** Vanilla HTML/JS frontend, Supabase backend (PostgreSQL + Auth)
- **Catalog:** https://jg-mart.vercel.app
- **Validation:** `python tests/validate_toolkit.py` — 37/37 HTML ✅, 12/12 Python ✅

## Quick Start

```bash
# Clone
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes

# Install Python deps (optional — only for validation scripts)
pip install -r requirements.txt

# Run validation toolkit (verifies all HTML, Python, cross-references)
python tests/validate_toolkit.py

# Serve locally
cd src/web/catalog && python -m http.server 8080
cd src/web/dashboard && python -m http.server 8081
```

## Authentication

All admin and dashboard pages use **Supabase Auth** with email/password.

### Quick Setup (2 ways)

**Option A — Via In-App UI (easiest):**
1. Open `admin.html` → Settings tab → **🔌 Supabase Connection**
2. Paste your Supabase Project URL and Anon Key
3. Click Save → Reload

**Option B — Via localStorage:**
```js
localStorage.setItem('jgmart_supabase_url', 'https://your-project.supabase.co');
localStorage.setItem('jgmart_supabase_anon_key', 'eyJhbGciOi...');
```

### When Supabase is not configured

All auth pages fall back to **Demo Mode** — accepts any email/password combo. No configuration required to browse the codebase.

### Supabase Project Setup

1. Create project at https://supabase.com
2. Run `src/web/supabase/schema.sql` in SQL Editor
3. Run `src/web/supabase/seed.sql` to seed initial data
4. See `docs/SUPABASE_SETUP.md` for full guide

### Pages using Supabase Auth

| Page | Auth |
|------|------|
| `src/web/dashboard/*.html` | `auth.js` (Supabase Auth, auto-wired) |
| `src/web/catalog/admin.html` | `auth.js` (Supabase Auth via shared module) |

### Roles

- **customer:** Browse catalog, place orders
- **partner:** View assigned orders
- **operator:** Manage products, orders, customers
- **admin:** Full access to all features

## Repository Structure

```
├── .github/              # CI/CD, issue templates, PR template
├── .gitignore
├── LICENSE               # MIT License
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── docs/
│   ├── audit/           # Technical audits
│   ├── architecture/    # System design
│   ├── business/        # Plans, financials, pitch decks
│   ├── operations/      # SOPs, manuals, protocols
│   └── api/             # Integration guides
├── src/
│   ├── web/             # Catalog, dashboard, templates
│   ├── scripts/         # Automation, deployment
│   └── templates/       # Legal, marketing, ops templates
├── assets/              # Brand, images, documents
├── data/                # Exports, samples, backups
├── config/              # Deployment configs
├── tests/               # Validation and test suite
└── ARCHIVE/             # Legacy files (read-only)
```

## Documentation

| Document | Location | Description |
|----------|----------|-------------|
| Business Plan | `docs/business/BUSINESS_PLAN.md` | Full business strategy |
| Executive Summary | `docs/business/EXECUTIVE_SUMMARY.md` | One-page investor summary |
| Financial Model | `docs/business/FINANCIAL_MODEL.md` | 6-month projections |
| Pitch Deck | `docs/business/PITCH_DECK.md` | Slide deck summary |
| Operations Manual | `docs/operations/OPERATIONS_MANUAL.md` | Daily procedures |
| System Architecture | `docs/architecture/SYSTEM_ARCHITECTURE.md` | Technical design |

| Supabase Setup | `docs/SUPABASE_SETUP.md` | Database + auth setup guide |
| Migration Guide | `docs/MIGRATION_GUIDE.md` | LocalStorage → Supabase migration |
| Admin Access | `docs/ADMIN_ACCESS.md` | Admin panel usage guide |
| Deployment Guide | `docs/DEPLOYMENT_GUIDE.md` | Deploy catalog + dashboard |
| Tutorial | `docs/TUTORIAL.md` | How-to for all user types |

## Business Inquiries

- **Investors:** Use the [investor inquiry issue template](.github/ISSUE_TEMPLATE/investor_inquiry.md) or email investors@jgmart.example
- **Partners:** See `docs/operations/PARTNER_AGREEMENT.md`
- **Press:** See `docs/business/PRESS_KIT.md` (coming soon)

## Tech Stack (Current)

- **Frontend:** Vanilla HTML/CSS/JS (web catalog + dashboard)
- **Auth:** Supabase Auth (email/password) with localStorage session persistence
- **Backend:** Python scripts for data sync and automation
- **Data:** JSON product catalogs (`catalog_data.json`, `order_intake_data.json`), CSV trackers
- **Hosting:** Vercel / Netlify (catalog + dashboard)
- **Validation:** Custom toolkit (`python tests/validate_toolkit.py`) — 37 HTML, 12 Python

## Roadmap

1. **Q3 2026:** Complete repo restructure, add tests, set up CI/CD
2. **Q4 2026:** Migrate to structured backend (FastAPI/Flask), add database
3. **Q1 2027:** Launch pilot in 1 neighborhood, onboard 20 partners
4. **Q2 2027:** Scale to 5 neighborhoods, raise seed round

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with hustle. Documented for scale.*
