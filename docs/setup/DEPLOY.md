# JG Mart — Production Deploy

Live domain: https://jg-mart.vercel.app  
GitHub: https://github.com/FahadIbrahim93/jgmart-hermes

## Current status (31 July 2026)

| Check | Status |
|-------|--------|
| Code on `main` | Synced after wrap-up commit |
| CI (validate + black) | Green on push |
| Live site serving **this repo** | **Yes** — root deploy (`vercel.json` rewrites) |
| Catalog at `/` | **Yes** — 65 products from defaults / Supabase |
| `/dashboard` | 200 — ops dashboard |
| `/admin` | 200 — admin panel |
| `/defaults.js` | 200 (rewrite → catalog `defaults.js`) |
| Supabase schema + RLS | **Applied** — `full_setup.sql` + `fix_profiles_rls.sql` |
| Supabase products in DB | ~84 rows (duplicate seed possible — see below) |
| GitHub Actions CLI deploy | **Optional** — needs `VERCEL_TOKEN` secret |
| Supabase runtime on Vercel | **Pending** — add `SUPABASE_URL` + `SUPABASE_ANON_KEY` secrets |
| Admin Auth user + profile | **Verify manually** — see `admin_user_setup.sql` |
| E2E (live order → DB) | **Not verified** in automation |

### Still manual

1. Add GitHub Actions secrets (below) so CI can write `config.runtime.js` on deploy.
2. Create admin user in Supabase Auth → run `migrations/admin_user_setup.sql`.
3. Submit one test order on live catalog and confirm row in Supabase `orders`.
4. If product count is wrong (84 vs 65), dedupe or re-seed once — both `seed.sql` and `seed_from_catalog.sql` may have run.

## GitHub Actions secrets

Add at https://github.com/FahadIbrahim93/jgmart-hermes/settings/secrets/actions

| Secret | Value |
|--------|-------|
| `VERCEL_TOKEN` | https://vercel.com/account/tokens |
| `VERCEL_ORG_ID` | `team_dQhygReHfUO67Sajlaz6X4gJ` |
| `VERCEL_PROJECT_ID` | `prj_cNHDDA56pUQIbuq2tuT2hBlmelfV` |
| `SUPABASE_URL` | Project URL (Settings → API) |
| `SUPABASE_ANON_KEY` | Anon/public key (not service_role) |

Without `VERCEL_TOKEN`, the deploy job skips and Vercel Git Integration (or manual CLI) still serves production.

## Deploy options

### Option A — Vercel Dashboard (Git integration)

1. Open https://vercel.com/dashboard → project `jg-mart`
2. **Settings → Git**
   - Repo: `FahadIbrahim93/jgmart-hermes`
   - Production branch: `main`
   - **Root Directory: empty (`.`)** — not `src/web/catalog`
3. **Build & Output** — Build Command and Output Directory both empty (static repo)
4. Push to `main` or Redeploy latest commit

Verify:

- https://jg-mart.vercel.app/
- https://jg-mart.vercel.app/dashboard
- https://jg-mart.vercel.app/admin
- https://jg-mart.vercel.app/defaults.js

### Option B — GitHub Actions CLI deploy

Set all secrets above, then run workflow **Deploy to Production** (or push to `main`).

### Option C — Local CLI

```powershell
cd "G:\JGC Mart"
npx vercel login
npx vercel link   # select jg-mart; root = .
npx vercel --prod
```

Helper script: `scripts/vercel-cutover.ps1`

## Why Root Directory must be `.`

Catalog modules import Supabase from `../supabase/`. If Vercel Root Directory is `src/web/catalog`, `/dashboard`, Supabase client paths, and root rewrites break.

Repo-root `vercel.json` maps `/` → `/src/web/catalog/index.html` and short paths for catalog assets.

## Local Supabase config

- Copy `src/web/supabase/config.local.example.js` → `config.local.js` (gitignored).
- Production: `config.runtime.js` from CI secrets or manual copy of `config.runtime.example.js` (gitignored).
