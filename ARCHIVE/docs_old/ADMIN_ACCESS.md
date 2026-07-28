# JG Mart — Admin & Dashboard Access Guide

> **Last Updated:** 28 July 2026

---

## Quick Access

| Panel | URL | Default PIN | Status |
|-------|-----|-------------|--------|
| Admin Panel | `https://jg-mart.vercel.app/admin` | `1234` | ✅ Live |
| Dashboard | Deploy `src/web/dashboard/` separately | `1234` | Ready to deploy |

---

## 1. Admin Panel (Catalog)

### Access URL
```
https://jg-mart.vercel.app/admin
```

### Default PIN
```
1234
```

### How to Login
1. Open the URL above on any device
2. Enter PIN: `1234`
3. Click "Unlock"

### What You Can Do
- **📦 Products:** Add, edit, delete products. Update prices in real-time.
- **📋 Orders:** View and manage customer orders.
- **📊 Stats:** See daily revenue, orders, customers.
- **⚙️ Settings:** Change PIN, update WhatsApp number, manage promos.

### Change Your PIN
1. Login to admin panel
2. Go to **Settings** tab
3. Enter new 4-6 digit PIN
4. Click "Save PIN"

**⚠️ Important:** PIN is stored in your browser's localStorage. Clear browser data = lose PIN (resets to `1234`).

---

## 2. Operations Dashboard

### Access
The dashboard is **NOT yet deployed**. To deploy:

#### Option A: Vercel (Recommended)
1. Go to https://vercel.com/new
2. Import `FahadIbrahim93/jgmart-hermes`
3. Root Directory: `src/web/dashboard`
4. Deploy
5. Access at: `https://jgmart-dashboard.vercel.app`

#### Option B: Local Testing
```bash
cd src/web/dashboard
python -m http.server 8001
# Open: http://localhost:8001
```

### Default PIN
```
1234
```

### Features
- **📊 Overview:** Daily stats, weekly charts, revenue trends
- **📋 Orders:** Order management with status tracking
- **💰 Finance:** P&L, cash flow, partner settlements
- **📈 Daily P&L:** Day-by-day profit/loss tracking
- **📉 Analytics:** Customer behavior, category performance
- **💬 Feedback:** Customer feedback collection
- **💾 Backup:** Export all data as JSON
- **📝 Comm Log:** Communication history with partners

### Security
- PIN protection on all pages
- Session persists in localStorage
- Click "Lock Dashboard" to logout
- No backend required — all data in browser

---

## 3. Security Best Practices

### Change Default PINs
Both admin and dashboard use `1234` by default. **Change immediately after first login.**

### Browser Storage
- PINs are stored in `localStorage`
- Clearing browser data resets PINs to `1234`
- PINs are NOT sent to any server
- Data stays in your browser only

### If You Forget PIN
1. Clear browser data for the site
2. Refresh page
3. Use default PIN: `1234`

### Production Deployment
When deploying to production:
1. Change default PIN in code
2. Use HTTPS only
3. Add password protection at Vercel/Netlify level
4. Consider adding IP whitelist for dashboard

---

## 4. Data Backup

### Admin Panel Data
1. Login to admin panel
2. Go to **Settings** tab
3. Click "Export All Data"
4. Save the JSON file

### Dashboard Data
1. Go to **Backup** page
2. Click "Export All Data"
3. Save the JSON file

### Restore Data
1. Open admin panel or dashboard
2. Go to **Settings** or **Backup**
3. Click "Import Data"
4. Select the JSON file

---

## 5. Troubleshooting

### "Wrong PIN" Error
- Default PIN is `1234`
- Check if you changed it previously
- Clear browser data and use default

### Admin Page 404
- Ensure you're on the live site: https://jg-mart.vercel.app
- Try `/admin.html` instead of `/admin`
- Redeploy catalog if needed

### Dashboard Not Loading
- Check browser console for errors
- Ensure `auth.js` is in the same folder
- Try hard refresh (Ctrl+Shift+R)

### Data Not Persisting
- Check if localStorage is enabled
- Check browser privacy settings
- Try incognito mode to test

---

## 6. Next Steps

1. **Change default PINs** in both admin and dashboard
2. **Deploy dashboard** to Vercel/Netlify
3. **Test on mobile** — admin panel is mobile-optimized
4. **Set up backups** — export data weekly
5. **Add team members** — share PIN with trusted operators only

---

## Support

- **WhatsApp:** +8801870489448
- **GitHub Issues:** https://github.com/FahadIbrahim93/jgmart-hermes/issues

---

*Last updated: 28 July 2026 | JG Mart — Admin Access Guide v1.0*
