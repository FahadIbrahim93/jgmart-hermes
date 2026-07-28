# JG Mart — Supabase Setup Guide

> **Status:** Production-ready | **Last Updated:** 28 July 2026

This guide walks you through setting up Supabase as the backend database and authentication provider for JG Mart.

---

## Table of Contents

1. [What is Supabase?](#1-what-is-supabase)
2. [Create Supabase Project](#2-create-supabase-project)
3. [Run Database Schema](#3-run-database-schema)
4. [Seed Initial Data](#4-seed-initial-data)
5. [Configure Authentication](#5-configure-authentication)
6. [Update App Configuration](#6-update-app-configuration)
7. [Deploy](#7-deploy)
8. [Verify Setup](#8-verify-setup)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. What is Supabase?

Supabase is an open-source Firebase alternative. It provides:
- **PostgreSQL database** — Relational data with real-time subscriptions
- **Authentication** — Email/password, OAuth, magic links
- **Storage** — File uploads for product images
- **Edge Functions** — Serverless API endpoints
- **Realtime** — Live data sync across clients

**Cost:** Free tier includes 500MB database, 1GB storage, 50K monthly active users. Perfect for JG Mart's scale.

**Website:** https://supabase.com

---

## 2. Create Supabase Project

### Step 1: Sign Up

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub or email
4. Verify your email

### Step 2: Create Project

1. Click "New project"
2. Fill in:
   - **Name:** `jgmart-db`
   - **Database Password:** [Save this! You'll need it]
   - **Region:** `Asia Pacific (Singapore)` — closest to Bangladesh
   - **Plan:** Free
3. Click "Create new project"
4. Wait 2-3 minutes for setup

### Step 3: Get API Keys

1. Go to **Settings** (gear icon) → **API**
2. Copy these values:
   - **Project URL:** `https://xxxxxxxxxxxxx.supabase.co`
   - **anon/public key:** `eyJhbGc...` (long string starting with `eyJ`)
   - **service_role key:** `eyJhbGc...` (keep this secret!)

---

## 3. Run Database Schema

### Step 1: Open SQL Editor

1. In your Supabase project, go to **SQL Editor** (left sidebar)
2. Click "New query"

### Step 2: Run Schema

1. Open the file: `src/web/supabase/schema.sql`
2. Copy the entire contents
3. Paste into the SQL Editor
4. Click "Run" (or press Ctrl+Enter)
5. You should see: "Success. No rows returned"

### Step 3: Verify Tables

1. Go to **Table Editor** (left sidebar)
2. You should see these tables:
   - ✅ profiles
   - ✅ categories
   - ✅ products
   - ✅ orders
   - ✅ order_items
   - ✅ customers
   - ✅ partners
   - ✅ settings
   - ✅ audit_log

---

## 4. Seed Initial Data

### Step 1: Run Seed SQL

1. Go back to **SQL Editor**
2. Open the file: `src/web/supabase/seed.sql`
3. Copy the entire contents
4. Paste into SQL Editor
5. Click "Run"

### Step 2: Verify Data

1. Go to **Table Editor** → **categories**
2. You should see 10 categories (Rice & Dal, Vegetables, Fish, etc.)
3. Go to **Table Editor** → **products**
4. You should see 20+ sample products

---

## 5. Configure Authentication

### Step 1: Enable Email Auth

1. Go to **Authentication** → **Providers**
2. Find "Email" in the list
3. Ensure it's **Enabled**
4. Configure:
   - **Confirm email:** OFF (for faster onboarding during beta)
   - **Secure email change:** ON
   - **Double confirm email change:** ON

### Step 2: Create Admin User

**Option A: Via Supabase Dashboard**

1. Go to **Authentication** → **Users**
2. Click "Add user" → "Create new user"
3. Fill in:
   - **Email:** `admin@jgmartbd.com`
   - **Password:** [Your secure password]
   - **Auto Confirm User:** ON
4. Click "Create user"
5. Copy the User UUID (e.g., `123e4567-e89b-12d3-a456-426614174000`)

**Option B: Via SQL**

```sql
-- Create admin user in auth.users
INSERT INTO auth.users (
  id,
  email,
  encrypted_password,
  email_confirmed_at,
  raw_app_meta_data,
  raw_user_meta_data
) VALUES (
  '00000000-0000-0000-0000-000000000001',
  'admin@jgmartbd.com',
  crypt('your-secure-password', gen_salt('bf')),
  NOW(),
  '{"provider":"email","providers":["email"]}',
  '{"full_name":"Fahad Ibrahim","role":"admin"}'
);

-- Create profile
INSERT INTO public.profiles (
  id,
  email,
  full_name,
  role,
  phone
) VALUES (
  '00000000-0000-0000-0000-000000000001',
  'admin@jgmartbd.com',
  'Fahad Ibrahim',
  'admin',
  '8801870489448'
);
```

### Step 3: Test Login

1. Open the admin panel: `https://your-project.vercel.app/admin-new/`
2. Login with `admin@jgmartbd.com` and your password
3. You should see the dashboard

---

## 6. Update App Configuration

### Step 1: Update Supabase Config

Edit `src/web/supabase/config.js`:

```javascript
export const SUPABASE_URL = 'https://xxxxxxxxxxxxx.supabase.co';
export const SUPABASE_ANON_KEY = 'eyJhbGc...';
```

Replace with your actual values from Step 2.3.

### Step 2: Enable Database Mode

In `src/web/catalog/db.js`, ensure:

```javascript
const USE_SUPABASE = true;
```

### Step 3: Deploy

```bash
git add .
git commit -m "feat: enable Supabase database and authentication"
git push origin main
```

---

## 7. Deploy

### Option A: Vercel (Recommended)

1. Go to https://vercel.com/new
2. Import `FahadIbrahim93/jgmart-hermes`
3. **Environment Variables:**
   - `VITE_SUPABASE_URL` = your Supabase URL
   - `VITE_SUPABASE_ANON_KEY` = your Supabase anon key
4. Deploy

### Option B: Netlify

1. Go to https://app.netlify.com/drop
2. Drag the `src/web/catalog/` folder
3. Add environment variables in Site settings

---

## 8. Verify Setup

### Checklist

- [ ] Admin panel loads at `/admin-new/`
- [ ] Login works with email/password
- [ ] Dashboard shows stats
- [ ] Products tab shows seeded products
- [ ] Can add new product
- [ ] Can edit product
- [ ] Can delete product
- [ ] Orders tab works
- [ ] Settings save to database
- [ ] Catalog loads products from database
- [ ] Orders submit to database

### Test Data Flow

1. **Add Product** in Admin → Check Table Editor → Should appear in products table
2. **Submit Order** in Catalog → Check Table Editor → Should appear in orders table
3. **Update Settings** in Admin → Check Table Editor → Should update settings table

---

## 9. Troubleshooting

### "Failed to connect to Supabase"

- Check `SUPABASE_URL` and `SUPABASE_ANON_KEY` in config.js
- Ensure you ran schema.sql and seed.sql
- Check browser console for CORS errors

### "Invalid API key"

- Verify you're using the **anon/public** key, not service_role
- Check that the key hasn't expired

### "Row Level Security policy violation"

- Ensure you're logged in
- Check that the user has the correct role in profiles table
- Verify RLS policies were created in schema.sql

### "Tables not found"

- Re-run schema.sql in SQL Editor
- Check for errors in the SQL output
- Ensure you're in the correct Supabase project

### "Orders not appearing"

- Check that `in_stock = true` for products
- Verify RLS policies allow inserts
- Check browser console for JavaScript errors

---

## Next Steps

1. **Connect custom domain** for admin panel
2. **Enable 2FA** for admin accounts
3. **Set up email templates** in Supabase Auth
4. **Add OAuth providers** (Google, WhatsApp)
5. **Configure backups** in Supabase
6. **Set up monitoring** with Supabase Dashboard
7. **Add Realtime** for live order updates
8. **Enable Storage** for product images

---

## Support

- **Supabase Docs:** https://supabase.com/docs
- **JG Mart GitHub:** https://github.com/FahadIbrahim93/jgmart-hermes
- **WhatsApp:** +8801870489448

---

*Last updated: 28 July 2026 | JG Mart — Supabase Setup Guide v1.0*
