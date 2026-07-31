# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **ZERO AI Visual Overhaul** — Complete redesign of all 8 catalog pages (+4,415 lines)
  - `index.html`: Complete redesign with glassmorphism, new CSS, cart sidebar, order modal
  - `admin.html`: Redesigned with Supabase Auth + PIN fallback, tab navigation, stats cards
  - `landing.html`: Redesigned landing page with new visual style
  - `menu.html`: Redesigned menu page
  - `notify.html`: Redesigned notifications page
  - `rider.html`: Redesigned rider dashboard
  - `track.html`: Redesigned order tracking page
  - `zone.html`: Redesigned zone page
- **Supabase Integration** — Full backend wiring
  - `data-store.js`: Centralized localStorage wrapper across 7 catalog pages
  - `order-state.js`: Order lifecycle state machine
  - `admin-backend.js`: Supabase auth + CRUD for admin panel
  - `db.js`: Supabase database client
  - `offline-queue.js`: Offline order queue when Supabase unavailable
  - `security.js`: CSP headers
  - `catalog-init.js`: Catalog initialization
  - `defaults.js`: Fallback catalog data
  - `config.runtime.js`: Runtime Supabase config
  - `sw.js`: Service worker (PWA, cache version jgmart-v6)
  - `manifest.json`: PWA manifest
- **New Pages**
  - `operator.html`: Operator intake page for order entry
  - `dashboard/index.html`: Dashboard with Supabase auth
- **Supabase Migrations**
  - `fix_profiles_rls.sql`: Profile RLS policy
  - `admin_user_setup.sql`: Admin user creation
  - `rls_anonymous_orders.sql`: Anonymous order creation via SECURITY DEFINER RPC
  - `fix_generate_order_number.sql`: RPC fix for non-JG- prefixed order numbers
- **Python Automation**
  - `sync_catalog_to_supabase.py`: Sync local catalog to Supabase
  - `check_supabase.py`: API smoke test
  - `print_supabase_setup.py`: Prints SQL paths for SQL Editor
- **Validation Toolkit** — `tests/validate_toolkit.py` (45/45 HTML, 17/17 Python)
- **Taskboard** — `taskboard.html` for project tracking
- **Professional repository structure** (v2.0)
  - `.gitignore`, `LICENSE`, `CONTRIBUTING.md`, `README.md`
  - `.github/` workflows, issue templates, PR template
  - `docs/` hierarchy: audit, architecture, business, operations, api
  - `src/`, `assets/`, `data/`, `config/`, `tests/` directories
  - `ARCHIVE/` for legacy files

### Changed
- **Visual Overhaul**: All 8 catalog pages redesigned with consistent glassmorphism, gradient backgrounds, modern CSS
- **Supabase**: 82 products, 10 categories, 0 orders, 0 duplicates — deduplicated
- **Vercel Deploy**: All 20 files now return 200 (was 13/20)
- **Admin Panel**: Replaced PIN-only auth with Supabase Auth + PIN fallback
- **Order Flow**: WhatsApp orders now use `create_public_order` SECURITY DEFINER RPC
- **Reorganized 295 files** from flat numbered folders into semantic structure
- **Moved all Python scripts** to `src/scripts/automation/`
- **Moved web assets** to `assets/` and `src/web/`

### Fixed
- **Vercel Deploy**: Added missing rewrites for 7 files (operator.html, order-state.js, db.js, admin-backend.js, etc.)
- **Supabase RLS**: Fixed anonymous order creation via SECURITY DEFINER RPC
- **Supabase Dedup**: Removed duplicate Green Chili and Katla Fish products
- **generate_order_number RPC**: Fixed to handle non-JG- prefixed order numbers
- **Drive Cleanup**: Purged 5 redundant agent folders (17 MB reclaimed)
- **HTML Validation**: Fixed 6 issues (was 31/37 → now 45/45)
- **Committed `__pycache__`** removed from version control tracking
- **Duplicate master indexes** consolidated into `MASTER_INDEX.md`

### Security
- Plaintext data files audited and flagged in `BRUTAL_HONEST_AUDIT.md`
- Secrets management recommendations documented
- `config.local.js` gitignored (contains real Supabase credentials)
- `config.runtime.js` committed (contains live Supabase credentials for Vercel)

## [0.1.0] - 2026-07-15

### Added
- Initial project structure with numbered folders (00–12)
- Business plan, pitch deck, financial model
- Web catalog, tech dashboard, marketing materials
- Operations playbooks and legal templates

---

**Note:** Earlier versions were tracked in `CHANGELOG.txt`. This file replaces the legacy changelog with a structured format.
