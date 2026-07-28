# Deployment Instructions

## Method 1: Vercel (Recommended)

### 1. Connect GitHub to Vercel
1. Go to https://vercel.com/new
2. Import `FahadIbrahim93/jgmart-hermes`
3. Create 2 projects:
   - **Project 1:** `jgmart-catalog` (Root: `src/web/catalog/`)
   - **Project 2:** `jgmart-dashboard` (Root: `src/web/dashboard/`)

### 2. Set Environment Variables

For **jgmart-catalog**:
```
WHATSAPP_NUMBER=+8801870489448
AOV_BDT=800
DELIVERY_FEE_BDT=30
SUBSCRIPTION_PRICE_BDT=149
```

For **jgmart-dashboard**:
```
NODE_ENV=production
```

### 3. Deploy
Click "Deploy" in Vercel dashboard. Auto-deploys on every push to main.

## Method 2: Netlify

### Catalog
1. Go to https://app.netlify.com/drop
2. Drag `src/web/catalog/` folder
3. Done

### Dashboard
1. Go to https://app.netlify.com/drop
2. Drag `src/web/dashboard/` folder
3. Done

## Method 3: GitHub Actions (Auto-Deploy)

### 1. Get Vercel Token
1. Go to https://vercel.com/account/tokens
2. Create token: `jgmart-deploy`
3. Copy token

### 2. Add GitHub Secrets
Go to https://github.com/FahadIbrahim93/jgmart-hermes/settings/secrets/actions
Add:
- `VERCEL_TOKEN` = your token
- `VERCEL_ORG_ID` = your Vercel org ID

### 3. Push to Deploy
```bash
git push origin main
```

GitHub Actions will auto-deploy both apps in 2-3 minutes.

## Expected URLs

- Catalog: `https://jgmart-catalog.vercel.app`
- Dashboard: `https://jgmart-dashboard.vercel.app`

## Post-Deploy

1. Test catalog on mobile
2. Test WhatsApp deep link
3. Verify dashboard loads
4. Set custom domain (optional)
