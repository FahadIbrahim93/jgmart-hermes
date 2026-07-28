# System Architecture

## Overview
JG Mart Hermes is a **hyperlocal grocery delivery platform** designed for low-bandwidth environments and WhatsApp-first customer interactions.

```
┌─────────────────────────────────────────────────────────────┐
│                      Customer Layer                         │
│  WhatsApp ↔ Web Catalog ↔ Progressive Web App               │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Application Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Order Intake │  │  Inventory   │  │  Rider Dispatch  │  │
│  │  (HTML/JSON)  │  │  (JSON sync) │  │  (WhatsApp API)  │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  JSON Exports│  │  CSV Trackers│  │  Local Backups   │  │
│  │  (09_Data)   │  │  (12_Tmpl)   │  │  (GDrive Sync)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Hosting Layer                            │
│  Vercel (Catalog) + Netlify (Dashboard) + Local Python       │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Web Catalog (`src/web/catalog/`)
- Static PWA built with vanilla HTML/CSS/JS
- Product browsing with category filters
- Cart and checkout via WhatsApp message generation
- Offline support via Service Worker (`sw.js`)
- Hosted on Vercel with edge caching

### 2. Tech Dashboard (`src/web/dashboard/`)
- Operational metrics: orders, finance, analytics, P&L
- Built as standalone HTML pages with JSON data injection
- Backup and restore functionality
- Hosted on Netlify

### 3. Automation Scripts (`src/scripts/automation/`)
- `validate_toolkit.py` — Pre-flight checks before launch
- `auto_deploy.py` — Deployment automation
- `daily_summary.py` — End-of-day WhatsApp report generation
- `drive_sync.py` — Google Drive backup synchronization
- `cache_images.py` / `add_image_urls.py` — Asset optimization

### 4. Data Sync (`data/`)
- `exports/` — Import/export bundles for analytics
- `sample/` — Test fixtures
- `backups/` — Periodic JSON snapshots

## Data Flow

1. **Customer** browses catalog → adds items → clicks "Order on WhatsApp"
2. **WhatsApp API** sends message to merchant phone
3. **Merchant** confirms order manually or via dashboard
4. **Rider** receives dispatch via WhatsApp
5. **Delivery** confirmed → status updated in dashboard
6. **Finance** record written to JSON export for daily reconciliation

## Infrastructure

| Component | Current | Target |
|-----------|---------|--------|
| Frontend Hosting | Vercel / Netlify | Vercel (unified) |
| Backend | Local Python scripts | FastAPI / Flask on Render/Railway |
| Database | JSON files | PostgreSQL (Supabase/Neon) |
| Auth | None | Clerk / Supabase Auth |
| Payments | Cash / Bank transfer | Razorpay / Stripe (India) |
| Notifications | WhatsApp Business API | WhatsApp + Email fallback |

## Security Architecture

- No secrets in repo (`.env` gitignored)
- API keys managed via environment variables
- CORS restricted to known domains
- Input validation on all forms (client + server)
- Rate limiting on public endpoints (future)

## Performance Targets

| Metric | Current | Target |
|--------|---------|--------|
| Catalog Load | ~3s (unoptimized) | <1.5s (Lighthouse 90+) |
| Dashboard Load | ~2s | <1s |
| Time to First Byte | N/A | <200ms |
| Offline Support | Partial (SW) | Full (PWA) |

---

*This document is living. Update when architecture decisions change.*
