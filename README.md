# JG Mart Hermes

**JG Mart** is a hyperlocal grocery delivery platform built for Japan Garden City (JGC), Mohammadpur, Dhaka. We source fresh produce from Krishi Market (800m away) and deliver same-day to 1,700 families across 27 buildings — at wholesale prices, with zero app download friction.

This repository contains the production website, operational tools, investor pitch package, and automation scripts.

## Live Website

- **Catalog:** `src/web/catalog/index.html`
- **Admin:** `src/web/catalog/admin.html`
- **Deploy:** Vercel / Netlify static deploy from repo root (`vercel.json`, `netlify.toml`)

## Status

- **Stage:** Pre-seed / Pilot
- **License:** MIT
- **Stack:** Vanilla HTML/CSS/JS, localStorage persistence, Python automation
- **Products:** 65 items across 10 categories
- **Coverage:** 27 buildings, 4 delivery clusters (C1–C4)

## Quick Start

```bash
# Clone
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes

# Run validation toolkit
python tests/validate_toolkit.py
```

## Website Structure

```
src/web/catalog/
├── index.html          # 65-product catalog (main entry)
├── landing.html        # Customer-facing about/features page
├── menu.html           # Printable menu card (24 products)
├── track.html          # Order status lookup
├── zone.html           # Delivery zones & fees
├── myorders.html       # Customer order history
├── admin.html          # PIN-protected admin panel
├── manifest.html       # Delivery manifest print page
├── healthcheck.html    # Site health checker
├── 404.html            # Custom error page
├── sw.js               # PWA service worker
├── manifest.json       # PWA manifest
└── images/             # Product + category images
```

## Admin Panel

The admin panel uses **PIN authentication** with localStorage persistence.

- Default PIN: configured in `admin.html`
- Manages products, prices, orders, promo banners, CSV export, backup reminders
- Data stored in `jgmart_prods`, `jgmart_orders`, `jgmart_promo` localStorage keys

## Operational Tools

| Tool | Path | Purpose |
|------|------|---------|
| Daily Summary | `src/scripts/automation/daily_summary.py` | Generate daily box-drawing reports |
| WhatsApp Summary | `src/scripts/automation/daily_whatsapp_summary.py` | Broadcast message generator |
| Image Cache | `src/scripts/automation/cache_images.py` | Download product images locally |
| Sync Bridge | `src/scripts/automation/sync_bridge.py` | Central data export/import |
| Placeholder Gen | `src/scripts/automation/generate_placeholders.py` | SVG category placeholders |

## Pitch Package

Ready-to-use materials for investor, partner, and committee meetings:

- `src/pitch/deck.html` — 12-slide HTML pitch deck
- `src/pitch/onepager.md` — Investor one-pager
- `src/pitch/partner_script.md` — Krishi Market vendor pitch script
- `src/pitch/committee_script.md` — JGC building committee pitch script
- `src/pitch/qa_cheatsheet.md` — Objection handling Q&A
- `src/pitch/deck_notes.md` — Speaker notes + timing guide
- `src/pitch/financial_model.md` — Unit economics + projections
- `src/pitch/RESEARCH_BRAINSTORM.md` — Audience research + competitive analysis

## Business Model

| Metric | Value |
|--------|-------|
| Average Order Value | ৳800 |
| Contribution Margin | 51% |
| Seed Ask | ৳250,000 |
| Equity Offered | 15% |
| Pre-Money Valuation | ৳1.67M |
| Runway | 6 months |
| Break-Even | Month 5 |

## Delivery Zones

| Cluster | Buildings | Delivery Fee |
|---------|-----------|--------------|
| C1 | B1–B6 | Free |
| C2 | B7–B13 | Free |
| C3 | B14–B20 | ৳20 |
| C4 | B21–B27 | ৳30 |

## Deployment

### Vercel
1. Connect repo to Vercel
2. Root directory: `.` (repo root)
3. Vercel auto-detects `vercel.json`
4. Deploy triggers on push to `main`

### Netlify
1. Connect repo to Netlify
2. Build command: empty (static)
3. Publish directory: `src/web/catalog`
4. Netlify auto-detects `netlify.toml`

## Documentation

| Document | Location |
|----------|----------|
| Changelog | `CHANGELOG.md` |
| Contributing | `CONTRIBUTING.md` |
| Operations | `src/scripts/automation/` |
| Validation | `tests/validate_toolkit.py` |

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with hustle. Documented for scale.*
