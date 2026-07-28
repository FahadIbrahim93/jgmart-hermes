# JG Mart — Authentication & Database Setup Verification

> **Last Updated:** 28 July 2026

Use this checklist to verify your Supabase setup is complete and working.

---

## Pre-Flight Checklist

### Files Created

| File | Purpose | Status |
|------|---------|--------|
| `src/web/supabase/config.js` | Supabase credentials | ✅ Created |
| `src/web/supabase/client.js` | Browser Supabase client | ✅ Created |
| `src/web/supabase/schema.sql` | Database schema | ✅ Created |
| `src/web/supabase/seed.sql` | Sample data | ✅ Created |
| `src/web/auth.js` | Unified auth module | ✅ Created |
| `src/web/admin-new/index.html` | New admin panel | ✅ Created |
| `src/web/catalog/db.js` | Catalog DB integration | ✅ Created |
| `src/web/catalog/admin.html` | Old panel redirect | ✅ Created |
| `docs/SUPABASE_SETUP.md` | Setup guide | ✅ Created |
| `docs/MIGRATION_GUIDE.md` | Data migration guide | ✅ Created |
| `docs/ADMIN_ACCESS.md` | Access instructions | ✅ Created |

---

## Setup Verification

### 1. Supabase Project Created
- [ ] Project created at https://supabase.com
- [ ] Project name: `jgmart-db`
- [ ] Region: Asia Pacific (Singapore)
- [ ] API keys copied

### 2. Database Schema Applied
- [ ] Opened Supabase SQL Editor
- [ ] Ran `src/web/supabase/schema.sql`
- [ ] No errors in SQL output
- [ ] Tables visible in Table Editor:
  - [ ] profiles
  - [ ] categories
  - [ ] products
  - [ ] orders
  - [ ] order_items
  - [ ] customers
  - [ ] partners
  - [ ] settings
  - [ ] audit_log

### 3. Seed Data Loaded
- [ ] Ran `src/web/supabase/seed.sql`
- [ ] Categories table has 10 rows
- [ ] Products table has 20+ rows
- [ ] Settings table has 10 rows

### 4. App Configuration Updated
- [ ] Edited `src/web/supabase/config.js`
- [ ] Set `SUPABASE_URL` to your project URL
- [ ] Set `SUPABASE_ANON_KEY` to your anon key
- [ ] Saved file

### 5. Admin User Created
- [ ] Created user in Supabase Auth
- [ ] Email: `admin@jgmartbd.com`
- [ ] Password: [secure password]
- [ ] Created profile in `profiles` table with role `admin`

### 6. Code Deployed
- [ ] Committed changes to Git
- [ ] Pushed to GitHub
- [ ] Deployed to Vercel/Netlify
- [ ] Environment variables set:
  - [ ] `VITE_SUPABASE_URL`
  - [ ] `VITE_SUPABASE_ANON_KEY`

---

## Functional Verification

### Admin Panel

- [ ] Navigate to `/admin-new/` or `/admin/`
- [ ] Redirects to new admin panel (not showing old PIN login)
- [ ] Login page appears
- [ ] Can switch between Sign In / Sign Up modes
- [ ] Can login with admin@jgmartbd.com
- [ ] Dashboard loads with stats
- [ ] Products tab shows seeded products
- [ ] Can add new product
- [ ] Can edit existing product
- [ ] Can delete product
- [ ] Orders tab loads
- [ ] Customers tab loads
- [ ] Partners tab loads
- [ ] Settings can be updated
- [ ] Logout works

### Catalog

- [ ] Catalog loads products
- [ ] Products display correctly
- [ ] Categories filter works
- [ ] Add to cart works
- [ ] Checkout via WhatsApp works
- [ ] Orders are submitted successfully

### Database

- [ ] New products appear in Supabase `products` table
- [ ] New orders appear in Supabase `orders` table
- [ ] Settings updates appear in `settings` table
- [ ] Profile is created on signup

---

## Security Verification

- [ ] Admin panel requires login (not publicly accessible)
- [ ] Non-admin users cannot access admin features
- [ ] Passwords are hashed (Supabase handles this)
- [ ] RLS policies are active (check Supabase dashboard)
- [ ] API keys are not exposed in client code
- [ ] HTTPS is enforced in production

---

## Performance Verification

- [ ] Admin panel loads in < 2 seconds
- [ ] Product list loads in < 1 second
- [ ] Order submission completes in < 2 seconds
- [ ] No console errors in browser DevTools
- [ ] No CORS errors
- [ ] Images load correctly

---

## Migration Verification (if applicable)

- [ ] Exported data from old admin panel
- [ ] Created `migrate_to_supabase.html`
- [ ] Ran migration tool
- [ ] Verified data in Supabase tables
- [ ] Catalog shows migrated products
- [ ] Orders history is preserved

---

## Known Limitations

| Limitation | Workaround | Priority |
|------------|-----------|----------|
| No real-time updates | Refresh page to see new data | Medium |
| No image upload | Use external URLs for product images | Medium |
| No email notifications | Manual WhatsApp follow-up | Low |
| No SMS OTP | Use email magic links | Low |
| No backup automation | Export from Supabase dashboard weekly | Medium |

---

## Next Steps

1. **Connect custom domain** to admin panel
2. **Enable 2FA** for admin accounts
3. **Set up email templates** in Supabase Auth
4. **Add OAuth providers** (Google, WhatsApp)
5. **Configure backups** in Supabase
6. **Add Realtime** for live order updates
7. **Enable Storage** for product images
8. **Add payment integration** (bKash API)
9. **Set up monitoring** with Supabase Dashboard
10. **Create staging environment** for testing

---

## Support

If verification fails:
1. Check browser console for errors
2. Verify Supabase credentials in config.js
3. Ensure schema.sql was run successfully
4. Check Supabase logs in Dashboard → Logs
5. Review `docs/SUPABASE_SETUP.md` troubleshooting section

---

*Last updated: 28 July 2026 | JG Mart — Verification Checklist v1.0*
