# JG Mart — Deployment Guide

> **Status:** Production-ready | **Last Updated:** 28 July 2026

This guide covers deploying the JG Mart web applications to production. We have two separate apps:

1. **Customer Catalog** — `src/web/catalog/` — Public-facing grocery catalog
2. **Operations Dashboard** — `src/web/dashboard/` — Private business dashboard

---

## Table of Contents

1. [Quick Deploy (5 Minutes)](#1-quick-deploy-5-minutes)
2. [Option A: Deploy Catalog to Vercel](#2-option-a-deploy-catalog-to-vercel)
3. [Option B: Deploy Catalog to Netlify](#3-option-b-deploy-catalog-to-netlify)
4. [Option C: Deploy Dashboard to Vercel](#4-option-c-deploy-dashboard-to-vercel)
5. [Option D: Deploy Both with GitHub Actions](#5-option-d-deploy-both-with-github-actions)
6. [Local Testing](#6-local-testing)
7. [Custom Domain Setup](#7-custom-domain-setup)
8. [Post-Deploy Checklist](#8-post-deploy-checklist)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Quick Deploy (5 Minutes)

### Prerequisites
- GitHub account (you have: `FahadIbrahim93`)
- Vercel account (free tier) OR Netlify account (free tier)
- Your repo: https://github.com/FahadIbrahim93/jgmart-hermes

### Fastest Path

```bash
# 1. Clone the repo
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes

# 2. Install Vercel CLI
npm i -g vercel

# 3. Deploy catalog (public)
vercel --prod --catalog src/web/catalog/

# 4. Deploy dashboard (private)
vercel --prod --dashboard src/web/dashboard/
```

That's it. You'll get two live URLs.

---

## 2. Option A: Deploy Catalog to Vercel

### Step 1: Import Project

1. Go to https://vercel.com/new
2. Click "Import" → Select `jgmart-hermes` repo
3. Configure:
   - **Project Name:** `jgmart-catalog`
   - **Root Directory:** `src/web/catalog`
   - **Build Command:** Leave empty (static site)
   - **Output Directory:** `.`
4. Click "Deploy"

### Step 2: Configure vercel.json

Create `src/web/catalog/vercel.json`:

```json
{
  "version": 2,
  "name": "jgmart-catalog",
  "builds": [
    { "src": "*.html", "use": "@vercel/static" },
    { "src": "*.svg", "use": "@vercel/static" },
    { "src": "images/*", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/", "dest": "/index.html" },
    { "src": "/catalog", "dest": "/index.html" },
    { "src": "/shop", "dest": "/index.html" },
    { "src": "/about", "dest": "/landing.html" },
    { "src": "/menu", "dest": "/menu.html" },
    { "src": "/track", "dest": "/track.html" },
    { "src": "/zone", "dest": "/zone.html" },
    { "src": "/admin", "dest": "/admin.html" },
    { "src": "/manifest", "dest": "/manifest.html" },
    { "src": "/(.*)", "dest": "/404.html" }
  ]
}
```

### Step 3: Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

| Key | Value | Description |
|-----|-------|-------------|
| `WHATSAPP_NUMBER` | `+8801870489448` | Your WhatsApp business number |
| `AOV_BDT` | `800` | Average order value |
| `DELIVERY_FEE_BDT` | `30` | Standard delivery fee |
| `SUBSCRIPTION_PRICE_BDT` | `149` | Monthly subscription price |

### Step 4: Deploy

```bash
vercel --prod
```

**Expected URL:** `https://jgmart-catalog.vercel.app`

---

## 3. Option B: Deploy Catalog to Netlify

### Step 1: Drag & Drop (Fastest)

1. Go to https://app.netlify.com/drop
2. Drag the folder `src/web/catalog/` into the browser
3. Done. You'll get a random URL like `https://random-name.netlify.app`

### Step 2: Git-based Deploy (Recommended)

1. Go to https://app.netlify.com/start
2. Select your `jgmart-hermes` repo
3. Configure:
   - **Base directory:** `src/web/catalog`
   - **Publish directory:** `src/web/catalog`
4. Click "Deploy site"

### Step 3: Configure netlify.toml

Create `src/web/catalog/netlify.toml`:

```toml
[build]
  publish = "."
  command = "echo 'No build needed - static site'"

[[headers]]
  for = "/*"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## 4. Option C: Deploy Dashboard to Vercel

The dashboard is **private** — only you and your team should access it.

### Step 1: Create Private Project

1. Go to https://vercel.com/new
2. Import `jgmart-hermes` repo
3. Configure:
   - **Project Name:** `jgmart-dashboard`
   - **Root Directory:** `src/web/dashboard`
   - **Framework Preset:** Other
4. Click "Deploy"

### Step 2: Password Protection

In Vercel Dashboard → Settings → Password Protection:

```
Enable Password Protection: ON
Password: [your-secure-password]
```

Or use Vercel's built-in access control:

1. Go to Settings → Members
2. Add only your email
3. Set project to "Private"

### Step 3: Deploy

```bash
vercel --prod --catalog src/web/dashboard/
```

**Expected URL:** `https://jgmart-dashboard.vercel.app`

---

## 5. Option D: Deploy Both with GitHub Actions

This is the **recommended** approach. It auto-deploys both apps on every push to `main`.

### Step 1: Get Vercel API Key

1. Go to https://vercel.com/account/tokens
2. Click "Create Token"
3. Name: `jgmart-hermes-deploy`
4. Scope: Full account
5. Copy the token

### Step 2: Add GitHub Secrets

1. Go to https://github.com/FahadIbrahim93/jgmart-hermes/settings/secrets/actions
2. Add these secrets:

| Name | Value |
|------|-------|
| `VERCEL_TOKEN` | Your Vercel API token |
| `VERCEL_ORG_ID` | Your Vercel org ID (from Vercel dashboard) |
| `VERCEL_PROJECT_CATALOG` | `jgmart-catalog` |
| `VERCEL_PROJECT_DASHBOARD` | `jgmart-dashboard` |

### Step 3: Create GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy-catalog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm i -g vercel
      - run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
        working-directory: ./src/web/catalog
      - run: vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }} --yes
        working-directory: ./src/web/catalog

  deploy-dashboard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm i -g vercel
      - run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
        working-directory: ./src/web/dashboard
      - run: vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }} --yes
        working-directory: ./src/web/dashboard
```

### Step 4: Push and Auto-Deploy

```bash
git add .github/workflows/deploy.yml
git commit -m "feat: add auto-deploy workflow for catalog + dashboard"
git push origin main
```

GitHub Actions will automatically deploy both apps within 2-3 minutes.

---

## 6. Local Testing

### Option A: Python HTTP Server

```bash
# Test catalog
cd src/web/catalog
python -m http.server 8000
# Open: http://localhost:8000

# Test dashboard (new terminal)
cd src/web/dashboard
python -m http.server 8001
# Open: http://localhost:8001
```

### Option B: Node HTTP Server

```bash
npx serve src/web/catalog -l 8000
npx serve src/web/dashboard -l 8001
```

### Option C: VS Code Live Server

1. Install "Live Server" extension
2. Right-click `index.html` → "Open with Live Server"

---

## 7. Custom Domain Setup

### For Catalog (Customer-Facing)

**Recommended domain:** `shop.jgmartbd.com` or `order.jgmartbd.com`

1. Buy domain from Namecheap/GoDaddy (≈ ৳1,000/year for `.com`)
2. In Vercel Dashboard → Settings → Domains
3. Add your domain
4. Update nameservers at your registrar:
   ```
   ns1.vercel-dns.com
   ns2.vercel-dns.com
   ```
5. Wait 5-10 minutes for propagation

### For Dashboard (Private)

**Recommended:** Use Vercel's built-in domain with password protection:
```
https://jgmart-dashboard-xyz.vercel.app
```
No custom domain needed for internal tooling.

---

## 8. Post-Deploy Checklist

- [ ] Catalog loads on mobile (test with real phone)
- [ ] WhatsApp deep link opens with correct number (+8801870489448)
- [ ] Product images load (check network tab for 404s)
- [ ] Admin panel accessible (if enabled)
- [ ] Dashboard loads and shows sample data
- [ ] SSL certificate active (https://, not http://)
- [ ] Custom domain configured (if applicable)
- [ ] Password protection enabled on dashboard
- [ ] Google Analytics added (optional)
- [ ] Facebook Pixel added (optional)

---

## 9. Troubleshooting

### Catalog Issues

| Problem | Solution |
|---------|----------|
| Images not loading | Check `assets/images/` path is correct |
| WhatsApp link broken | Verify `WHATSAPP_NUMBER` env var |
| 404 on refresh | Add `_redirects` file with `/* /index.html 200` |
| Slow load times | Enable Vercel Edge Network (automatic) |

### Dashboard Issues

| Problem | Solution |
|---------|----------|
| Charts not rendering | Check Chart.js CDN is loading |
| Data not persisting | Use `localStorage` or connect to Firebase/Supabase |
| Mobile layout broken | Test with Chrome DevTools device emulation |

### General

| Problem | Solution |
|---------|----------|
| Deploy fails | Check GitHub Actions logs |
| Site shows old version | Clear cache, hard refresh (Ctrl+Shift+R) |
| SSL error | Wait 10 minutes, or re-issue cert in Vercel |

---

## 10. Next Steps After Deployment

1. **Test with real users:** Send the catalog URL to 10 beta customers
2. **Collect feedback:** Use the dashboard's feedback tracker
3. **Iterate:** Update prices, products, and design based on feedback
4. **Scale:** Add more products, categories, and features
5. **Monitor:** Set up Google Analytics to track traffic and conversions

---

## Support

- **WhatsApp:** +8801870489448
- **GitHub Issues:** https://github.com/FahadIbrahim93/jgmart-hermes/issues
- **Live Site:** https://jg-mart.vercel.app (existing)

---

*Last updated: 28 July 2026 | JG Mart — Deployment Guide v1.0*
