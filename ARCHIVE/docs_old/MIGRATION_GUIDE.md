# JG Mart — LocalStorage to Supabase Migration Guide

> **Purpose:** Migrate existing data from localStorage to Supabase database
> **Last Updated:** 28 July 2026

---

## Overview

If you've been using the old admin panel with localStorage, your data is stored in your browser only. This guide helps you migrate that data to Supabase so it's permanent and accessible from any device.

---

## What Gets Migrated

| Data Type | localStorage Key | Supabase Table |
|-----------|-----------------|----------------|
| Products | `jgmart_prods` | `products` |
| Orders | `jgmart_ords` | `orders`, `order_items` |
| Settings | Various keys | `settings` |
| Admin PIN | `jgmart_admin_pin` | `profiles.role` |

---

## Step 1: Export Data from localStorage

### Using the Old Admin Panel

1. Open the old admin panel: https://jg-mart.vercel.app/admin
2. Login with PIN: `1234`
3. Go to **Settings** tab
4. Click **"Export All Data"**
5. Save the JSON file as `localstorage_backup.json`

### Using Browser DevTools

1. Open browser DevTools (F12)
2. Go to **Application** → **Local Storage**
3. Find these keys:
   - `jgmart_prods` → Copy value
   - `jgmart_ords` → Copy value
   - `jgmart_admin_wa` → Copy value
4. Save to a file:

```json
{
  "products": [...],
  "orders": [...],
  "settings": {
    "whatsapp_number": "8801870489448"
  }
}
```

---

## Step 2: Set Up Supabase

Follow the guide in `docs/SUPABASE_SETUP.md` to:
1. Create Supabase project
2. Run schema.sql
3. Run seed.sql
4. Create admin user
5. Update config.js

---

## Step 3: Run Migration Script

Create a file `migrate_to_supabase.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>JG Mart - Migration Tool</title>
  <style>
    body { font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 20px; }
    .step { margin: 20px 0; padding: 20px; background: #f5f5f5; border-radius: 8px; }
    button { background: #00442D; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 14px; }
    button:disabled { background: #ccc; }
    .success { color: #16a34a; font-weight: 600; }
    .error { color: #c0392b; font-weight: 600; }
  </style>
</head>
<body>
  <h1>JG Mart - LocalStorage → Supabase Migration</h1>

  <div class="step">
    <h3>Step 1: Load Data</h3>
    <p>This will read your localStorage data from the old admin panel.</p>
    <button onclick="loadLocalData()">Load Local Data</button>
    <div id="loadStatus"></div>
  </div>

  <div class="step">
    <h3>Step 2: Preview Migration</h3>
    <p>Review what will be migrated to Supabase.</p>
    <button onclick="previewMigration()" id="previewBtn" disabled>Preview</button>
    <div id="previewStatus"></div>
  </div>

  <div class="step">
    <h3>Step 3: Migrate to Supabase</h3>
    <p>This will insert all data into your Supabase database.</p>
    <button onclick="migrateData()" id="migrateBtn" disabled>Migrate Now</button>
    <div id="migrateStatus"></div>
  </div>

  <script type="module">
    import { supabase } from './src/web/supabase/client.js';

    let localData = null;

    window.loadLocalData = () => {
      try {
        const products = JSON.parse(localStorage.getItem('jgmart_prods') || '[]');
        const orders = JSON.parse(localStorage.getItem('jgmart_ords') || '[]');
        const waNumber = localStorage.getItem('jgmart_admin_wa') || '8801870489448';

        localData = { products, orders, settings: { whatsapp_number: waNumber } };

        document.getElementById('loadStatus').innerHTML =
          `<p class="success">✓ Loaded ${products.length} products, ${orders.length} orders</p>`;
        document.getElementById('previewBtn').disabled = false;
      } catch (e) {
        document.getElementById('loadStatus').innerHTML =
          `<p class="error">✗ Error: ${e.message}</p>`;
      }
    };

    window.previewMigration = async () => {
      if (!localData) return;

      const preview = `
        <p><strong>Products to migrate:</strong> ${localData.products.length}</p>
        <p><strong>Orders to migrate:</strong> ${localData.orders.length}</p>
        <p><strong>Settings to migrate:</strong> 1 (WhatsApp number)</p>
        <p style="margin-top:12px;color:#00442D;font-weight:600;">Ready to migrate!</p>
      `;

      document.getElementById('previewStatus').innerHTML = preview;
      document.getElementById('migrateBtn').disabled = false;
    };

    window.migrateData = async () => {
      if (!localData) return;

      const statusEl = document.getElementById('migrateStatus');
      statusEl.innerHTML = '<p>Migrating...</p>';

      try {
        // Migrate products
        if (localData.products.length > 0) {
          const products = localData.products.map(p => ({
            name: p.nm,
            name_bn: p.name_bn || '',
            category_id: p.ct || 'fmcg',
            price: p.pr || 0,
            unit: p.un || 'piece',
            in_stock: true,
            sort_order: parseInt(p.id?.replace('p', '') || '0')
          }));

          const { error } = await supabase.from('products').insert(products);
          if (error) throw error;

          statusEl.innerHTML += `<p class="success">✓ Migrated ${products.length} products</p>`;
        }

        // Migrate orders
        if (localData.orders.length > 0) {
          const orders = localData.orders.map(o => ({
            order_number: `JG-${o.id || Date.now()}`,
            customer_name: o.customer || 'Customer',
            customer_phone: o.phone || '',
            customer_building: o.building || '',
            customer_flat: o.flat || '',
            items: o.items || [],
            subtotal: o.sub || 0,
            delivery_fee: o.delivery || 0,
            total: o.total || o.sub || 0,
            payment_method: 'cash',
            status: o.status || 'pending',
            created_at: o.date ? new Date(o.date).toISOString() : new Date().toISOString()
          }));

          const { error } = await supabase.from('orders').insert(orders);
          if (error) throw error;

          statusEl.innerHTML += `<p class="success">✓ Migrated ${orders.length} orders</p>`;
        }

        // Migrate settings
        const { error: settingsError } = await supabase
          .from('settings')
          .upsert({ key: 'whatsapp_number', value: localData.settings.whatsapp_number });

        if (settingsError) throw settingsError;
        statusEl.innerHTML += `<p class="success">✓ Migrated settings</p>`;

        statusEl.innerHTML += `<p class="success" style="margin-top:12px;font-size:1.1rem;">🎉 Migration complete!</p>`;
      } catch (error) {
        statusEl.innerHTML += `<p class="error">✗ Error: ${error.message}</p>`;
      }
    };
  </script>
</body>
</html>
```

Save this as `migrate_to_supabase.html` in your catalog folder.

---

## Step 4: Run Migration

1. Open the migration tool: `https://your-site.vercel.app/migrate_to_supabase.html`
2. Click **"Load Local Data"** — this reads your browser's localStorage
3. Click **"Preview"** — review what will be migrated
4. Click **"Migrate Now"** — data is sent to Supabase

---

## Step 5: Verify Migration

1. Go to your Supabase dashboard
2. Click **Table Editor**
3. Check **products** table — should have your old products
4. Check **orders** table — should have your old orders
5. Check **settings** table — should have your WhatsApp number

---

## Step 6: Clean Up

After verifying the migration:

1. **Keep old data as backup** — Don't delete localStorage yet
2. **Update catalog** to use Supabase by default
3. **Deploy new code**
4. **Test thoroughly** — Make sure orders, products, etc. work
5. **Delete old admin panel** — After 1 week of successful operation

---

## Rollback Plan

If something goes wrong:

1. The old admin panel still works at `/admin.html`
2. Your localStorage data is untouched
3. You can switch back to localStorage by setting `USE_SUPABASE = false` in `db.js`

---

## Data Mapping Reference

### Products

| localStorage Field | Supabase Column | Notes |
|-------------------|-----------------|-------|
| `p.nm` | `name` | Product name |
| `p.ct` | `category_id` | Category ID |
| `p.pr` | `price` | Price in BDT |
| `p.un` | `unit` | Unit (piece, kg, etc.) |
| `p.id` | `sort_order` | Used for ordering |

### Orders

| localStorage Field | Supabase Column | Notes |
|-------------------|-----------------|-------|
| `o.id` | `order_number` | Prefixed with `JG-` |
| `o.customer` | `customer_name` | Customer name |
| `o.phone` | `customer_phone` | Phone number |
| `o.building` | `customer_building` | Building name |
| `o.flat` | `customer_flat` | Flat number |
| `o.items` | `items` | JSONB array |
| `o.sub` | `subtotal` | Subtotal |
| `o.delivery` | `delivery_fee` | Delivery fee |
| `o.total` | `total` | Final total |

---

## Support

If you encounter issues:
1. Check browser console for errors
2. Verify Supabase credentials in config.js
3. Ensure schema.sql was run successfully
4. Check Supabase logs in Dashboard → Logs

---

*Last updated: 28 July 2026 | JG Mart — Migration Guide v1.0*
