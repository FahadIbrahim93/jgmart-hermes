# JG Mart — Master Index

**Version:** 4.1 (consolidated) | **Updated:** July 31, 2026 | **Owner:** Fahad Ibrahim

> Single source of truth for all JG Mart assets. Consolidated from Hermes (code), Grok v2 (ops), Kimi v1 (brand + PRD).  
> **GitHub:** [jgmart-hermes](https://github.com/FahadIbrahim93/jgmart-hermes) | **Live:** [jg-mart.vercel.app](https://jg-mart.vercel.app)

---

## Start Here

| Need | Go to |
|------|-------|
| Product requirements | [`docs/product/PRD.md`](docs/product/PRD.md) |
| Investor pitch | [`src/pitch/deck.html`](src/pitch/deck.html) |
| Live catalog code | [`src/web/catalog/`](src/web/catalog/) |
| Database schema | [`src/web/supabase/schema.sql`](src/web/supabase/schema.sql) |
| Agent rules | [`AGENTS.md`](AGENTS.md) |
| Origin idea | [`IDEA.md`](IDEA.md) |

---

## 1. Web & Tech

| Asset | Path | Source | Status |
|-------|------|--------|--------|
| Customer catalog (live) | `src/web/catalog/index.html` | Hermes | **Production** — Vercel `/` |
| Supabase schema | `src/web/supabase/schema.sql` | Hermes | **Applied** (production DB) |
| Supabase full setup | `src/web/supabase/full_setup.sql` | Hermes | One-shot SQL (schema + seeds) |
| Supabase migrations | `src/web/supabase/migrations/` | Hermes | `fix_profiles_rls`, `admin_user_setup`, `rls_anonymous_orders` |
| Supabase seed | `src/web/supabase/seed.sql` | Hermes | Sample products |
| Admin panel | `src/web/catalog/admin.html` | Hermes | **Supabase Auth** + PIN fallback |
| PWA service worker | `src/web/catalog/sw.js` | Hermes | Production |
| Python automation | `src/scripts/automation/` | Hermes | Active |
| Validation toolkit | `tests/validate_toolkit.py` | Hermes | Active |
| Legacy dashboard | `ARCHIVE/src_web_dashboard/` | Hermes | Archived |
| Ops dashboard | `src/web/dashboard/index.html` | Hermes | Active — Supabase orders when configured |
| Catalog seed SQL | `src/web/supabase/seed_from_catalog.sql` | Hermes | 65 products from catalog_data.json |
| Supabase check script | `scripts/check_supabase.py` | Hermes | API smoke test |
| Supabase setup printer | `scripts/print_supabase_setup.py` | Hermes | Prints SQL paths for SQL Editor |
| Vercel cutover script | `scripts/vercel-cutover.ps1` | Hermes | Link + prod deploy helper |
| Supabase setup guide | `docs/setup/SUPABASE_SETUP.md` | Hermes | Active |
| Production deploy guide | `docs/setup/DEPLOY.md` | Hermes | Active — Vercel root must be `.` |

---

## 2. Brand Assets (Kimi)

| Asset | Path | Use |
|-------|------|-----|
| Brand guidelines | `assets/brand/kimi/01_JG_Mart_Brand_Guidelines.png` | Design reference |
| Logo variations | `assets/brand/kimi/02_JG_Mart_Logo_Variations.png` | Profiles, print |
| Social — product | `assets/brand/kimi/03a_JG_Mart_Social_Product.png` | Daily arrivals |
| Social — referral | `assets/brand/kimi/03b_JG_Mart_Social_Referral.png` | Referral promo |
| Social — delivery | `assets/brand/kimi/03c_JG_Mart_Social_Delivery.png` | Trust building |
| A5 flyer | `assets/brand/kimi/04_JG_Mart_Flyer_A5.png` | Print in buildings |
| WhatsApp catalog | `assets/brand/kimi/05_JG_Mart_WhatsApp_Catalog.png` | Daily 7:30 AM status |
| Business card | `assets/brand/kimi/06_JG_Mart_Business_Card.png` | Networking |
| How to order | `assets/brand/kimi/19_JG_Mart_How_To_Order_Guide.png` | New customers |
| Investor 1-pager (visual) | `assets/brand/kimi/JG_Mart_Investor_1Pager.png` | Email pitch |

---

## 3. Operations (Grok — canonical for launch playbooks)

| Asset | Path | Use |
|-------|------|-----|
| 30-day pilot launch | `docs/operations/grok/JG_Mart_30Day_Pilot_Launch_Playbook.txt` | Launch planning |
| Launch day runbook | `docs/operations/grok/JG_Mart_First_Launch_Day_Runbook.txt` | Launch day |
| Pre-launch checklist | `docs/operations/grok/JG_Mart_PreLaunch_Checklist.txt` | Go/no-go |
| Rider pickup checklist | `docs/operations/grok/JG_Mart_Daily_Pickup_Checklist_Rider.txt` | Daily rider card |
| Rider training card | `docs/operations/grok/JG_Mart_Rider_Training_Card.txt` | Rider onboarding |
| Partner guide v1.2 | `docs/operations/grok/08_JG_Mart_Partner_Guide_v1.2.txt` | Partner onboarding |
| CS scripts v1.1 | `docs/operations/grok/09_JG_Mart_CS_Scripts_v1.1.txt` | Customer service |
| Supplier scorecard | `docs/operations/grok/JG_Mart_Supplier_Negotiation_Scorecard.txt` | Vendor eval |
| Print pack manifest | `docs/operations/grok/JG_Mart_Print_Pack_Manifest.txt` | Materials to print |
| Risk log v1.1 | `docs/operations/grok/JG_Mart_Risk_Log_v1.1.txt` | Risk tracking |
| First order kit | `docs/operations/grok/JG_Mart_Customer_First_Order_Kit.txt` | New customers |

### Operations (Kimi — reference)

| Asset | Path |
|-------|------|
| SOP manual | `docs/operations/kimi/07_JG_Mart_SOP_Manual.txt` |
| Partner guide | `docs/operations/kimi/08_JG_Mart_Partner_Guide.txt` |
| Daily checklist | `docs/operations/kimi/13_JG_Mart_Daily_Checklist.txt` |
| Marketing calendar | `docs/operations/kimi/14_JG_Mart_Marketing_Calendar.txt` |

> **Rule:** For conflicting versions, prefer Grok v1.2+ over Kimi v1.

---

## 4. Financial Trackers

| Asset | Path | Source |
|-------|------|--------|
| Financial tracker | `data/trackers/11_JG_Mart_Financial_Tracker.csv` | Kimi |
| KPI dashboard | `data/trackers/12_JG_Mart_KPI_Dashboard.csv` | Kimi |
| 90-day task board | `data/trackers/10_JG_Mart_90Day_Task_Board.csv` | Kimi |
| Inventory tracker | `data/trackers/16_JG_Mart_Inventory_Tracker.csv` | Kimi |
| Customer database | `data/trackers/17_JG_Mart_Customer_Database.csv` | Kimi |
| Cash float log | `data/trackers/JG_Mart_Cash_Float_Log.txt` | Grok |

---

## 5. Investor Materials

| Asset | Path |
|-------|------|
| HTML pitch deck | `src/pitch/deck.html` |
| One-pager (markdown) | `src/pitch/onepager.md` |
| Financial model | `src/pitch/financial_model.md` |
| Q&A cheatsheet | `src/pitch/qa_cheatsheet.md` |
| Committee script | `src/pitch/committee_script.md` |
| Partner script | `src/pitch/partner_script.md` |
| Grok executive summary | `docs/investor/JG_Mart_Executive_Summary.txt` |
| Grok pitch script | `docs/investor/JG_Mart_Pitch_Script.txt` |
| Grok investor 1-pager | `docs/investor/JG_Mart_Investor_1Pager.txt` |

---

## 6. Templates (Hermes)

| Category | Path |
|----------|------|
| Legal | `src/templates/legal/` |
| Marketing | `src/templates/marketing/` |
| Operations | `src/templates/operations/` |

---

## 7. Archive

| Content | Path |
|---------|------|
| Grok originals | `_archive/agents/grok/` |
| Kimi originals | `_archive/agents/kimi/` |
| Legacy v2 structure | `ARCHIVE/` |
| Old unified index | `ARCHIVE/docs_old/MASTER_INDEX.md` |

---

## External References

| Resource | URL |
|----------|-----|
| Live website | https://jg-mart.vercel.app |
| GitHub repo | https://github.com/FahadIbrahim93/jgmart-hermes |
| Google Drive (backup) | https://drive.google.com/drive/folders/1US62pyiirEfW3iABCigkE7LageZcKYHj |

> Google Drive is a **backup mirror** only. This repo is primary.

---

*Update this file when adding or moving any canonical asset.*
