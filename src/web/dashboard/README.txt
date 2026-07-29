# JG Mart Operations Dashboard

Minimal ops dashboard for order overview. Reads orders from catalog `localStorage` until Supabase wiring is complete.

## Access

- Local: open `src/web/dashboard/index.html`
- Default PIN: `1234` (override via `jgmart_admin_pin` in localStorage)

## Next steps

1. Complete Supabase setup: `docs/setup/SUPABASE_SETUP.md`
2. Wire dashboard to `orders` table via `src/web/supabase/client.js`
3. Add Vercel deploy route if hosting separately from catalog
