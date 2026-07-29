# JG Mart — Production Deploy

Live domain: https://jg-mart.vercel.app  
GitHub: https://github.com/FahadIbrahim93/jgmart-hermes

## Current status (honest)

| Check | Status |
|-------|--------|
| Code on `main` | Done |
| CI (validate + black) | Green |
| Actions deploy job | Passes (skips CLI deploy when secrets missing) |
| Live site serving **this repo** | **Not yet** — jg-mart.vercel.app still serves an old single landing page |

Production is not linked to the consolidated repo layout yet. A Vercel login is required once.

## Fix production (pick one)

### Option A — Vercel Dashboard (fastest)

1. Open https://vercel.com/dashboard → project for `jg-mart`
2. **Settings → Git**
   - Connected repo: `FahadIbrahim93/jgmart-hermes`
   - Production branch: `main`
   - **Root Directory: leave empty (`.`)** — do **not** use `src/web/catalog`
3. **Settings → Build & Output**
   - Build Command: empty
   - Output Directory: empty (serve repo as static)
4. **Deployments → Redeploy** latest `main` commit (or push an empty commit)

After that, these must work:
- https://jg-mart.vercel.app/ → catalog
- https://jg-mart.vercel.app/dashboard → ops dashboard
- https://jg-mart.vercel.app/src/web/catalog/defaults.js → 200

### Option B — GitHub Actions CLI deploy

Add repo secrets (Settings → Secrets and variables → Actions):

| Secret | Where to get it |
|--------|-----------------|
| `VERCEL_TOKEN` | https://vercel.com/account/tokens |
| `VERCEL_ORG_ID` | Project Settings → General |
| `VERCEL_PROJECT_ID` | Project Settings → General |

Then re-run workflow: **Deploy to Production**.

### Option C — Local CLI

```powershell
cd "G:\JGC Mart"
npx vercel login
npx vercel link   # select the jg-mart project; root = .
npx vercel --prod
```

## Why Root Directory must be `.`

Catalog JS imports Supabase from `../supabase/`. If Vercel Root Directory is `src/web/catalog`, those modules and `/dashboard` never deploy.

Repo-root `vercel.json` rewrites `/` → `/src/web/catalog/index.html`.
