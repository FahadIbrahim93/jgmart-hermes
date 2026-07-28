# JG Mart Hermes

**JG Mart** is a neighborhood grocery delivery platform built for hyperlocal communities. We combine WhatsApp-first ordering, real-time inventory tracking, and rider logistics to deliver fresh products within hours.

This repository contains the complete technical, business, and operational foundation for the JG Mart platform.

## Status

> **WARNING:** This repository is undergoing a professional restructure (v2.0). The codebase is **not production-ready**. See `docs/audit/BRUTAL_HONEST_AUDIT.md` for the full technical assessment.

- **Stage:** Pre-seed / Pilot
- **License:** MIT
- **Language:** English
- **Stack:** HTML, JavaScript, Python, JSON (legacy); migration to structured stack in progress

## Quick Start

```bash
# Clone
git clone https://github.com/your-org/jgmart-hermes.git
cd jgmart-hermes

# Install Python deps (when requirements.txt is added)
pip install -r requirements.txt

# Run validation toolkit
python tests/validate_toolkit.py
```

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
