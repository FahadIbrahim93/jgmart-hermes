# JG Mart Hermes

**JG Mart** is a neighborhood grocery delivery platform built for hyperlocal communities. We combine WhatsApp-first ordering, real-time inventory tracking, and rider logistics to deliver fresh products within hours.

This repository contains the complete technical, business, and operational foundation for the JG Mart platform.

## Status

> **Production-ready admin system with Supabase backend.** See `docs/SUPABASE_SETUP.md` for setup.

- **Stage:** Pre-seed / Pilot
- **License:** MIT
- **Stack:** Vanilla HTML/JS frontend, Supabase backend (PostgreSQL + Auth)
- **Live:** https://jg-mart.vercel.app (catalog), deploy `src/web/admin-new/` for admin

## Quick Start

```bash
# Clone
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes

# Install Python deps
pip install -r requirements.txt  # when available

# Run validation toolkit
python tests/validate_toolkit.py
```

## Authentication & Admin

The admin panel uses **Supabase authentication** with email/password.

### Setup

1. Create Supabase project: https://supabase.com
2. Run `src/web/supabase/schema.sql` in Supabase SQL Editor
3. Run `src/web/supabase/seed.sql` to seed categories and products
4. Update `src/web/supabase/config.js` with your Supabase URL and anon key
5. Create admin user in Supabase Auth with role `admin`
6. Deploy `src/web/admin-new/` to Vercel/Netlify
7. Access at `/admin-new/` or `/admin/` (redirects)

### Default Roles

- **customer:** Can browse catalog, place orders
- **partner:** Can view assigned orders
- **operator:** Can manage products, orders, customers
- **admin:** Full access to all features

### Old Admin Panel

The old PIN-based admin panel (`/admin`) is deprecated. It now redirects to the new system. Data is still in localStorage until migrated. See `docs/MIGRATION_GUIDE.md`.

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
- **Backend:** Python scripts for data sync and automation
- **Data:** JSON exports, CSV trackers
- **Hosting:** Vercel / Netlify (catalog), TBD (backend)

## Roadmap

1. **Q3 2026:** Complete repo restructure, add tests, set up CI/CD
2. **Q4 2026:** Migrate to structured backend (FastAPI/Flask), add database
3. **Q1 2027:** Launch pilot in 1 neighborhood, onboard 20 partners
4. **Q2 2027:** Scale to 5 neighborhoods, raise seed round

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with hustle. Documented for scale.*
