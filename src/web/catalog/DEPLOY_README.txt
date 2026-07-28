╔═══════════════════════════════════════════════════════════════════════════╗
║     JG MART — DEPLOYMENT INSTRUCTIONS                                    ║
║     For Vercel or Netlify                                                ║
╚═══════════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════
QUICK DEPLOY (5 minutes)
═══════════════════════════════════════════════════════════════════════════

OPTION A: VERCEL (Recommended)
─────────────────────────────────
1. Go to https://vercel.com/new
2. Sign up with GitHub/GitLab/email
3. Choose "Deploy without Git" → drag this folder
   OR
   Import from Git: push this folder to a repo, then import it

4. Vercel auto-detects the project — just click "Deploy"
5. Your catalog goes live at: https://jgmart.vercel.app (or your custom name)

OPTION B: NETLIFY (Alternative)
─────────────────────────────────
1. Go to https://app.netlify.com/drop
2. Drag this entire '06_Web_Catalog' folder onto the browser
3. Your site goes live instantly at a netlify.app URL
4. The _redirects and netlify.toml files handle routing

═══════════════════════════════════════════════════════════════════════════
WHAT GETS DEPLOYED
═══════════════════════════════════════════════════════════════════════════

This "06_Web_Catalog" folder contains everything needed:

  index.html       → Main catalog (65 products, cart, checkout)
  landing.html     → About/explainer page
  menu.html        → Printable menu card
  zone.html        → Delivery zone info
  track.html       → Order status tracker
  admin.html       → Password-protected admin panel
  manifest.html    → Delivery manifest for riders
  myorders.html    → Customer order history
  404.html         → Custom error page
  sw.js            → Service worker (offline support)
  manifest.json    → PWA manifest (install on phone)
  vercel.json      → Vercel deployment config
  netlify.toml     → Netlify deployment config
  _redirects       → Netlify 404 redirects
  images/          → Product images (50 JPEGs + 25+ SVGs + placeholder)

Total: 8+ HTML pages · 65 products · All images · Full offline support

═══════════════════════════════════════════════════════════════════════════
IMPORTANT NOTE: localStorage
═══════════════════════════════════════════════════════════════════════════

When you deploy to a new domain, localStorage starts EMPTY.
This means:
- Products will show but from the embedded default data
- Orders and customer data will NOT transfer

TO MIGRATE DATA:
  1. Open the OLD site → admin.html → Export All Data
  2. Open the NEW deployed site → admin.html → Settings → Import Data
  3. Upload the exported JSON file

OR just start fresh — the embedded 65 products will appear automatically.

═══════════════════════════════════════════════════════════════════════════
CUSTOM DOMAIN
═══════════════════════════════════════════════════════════════════════════

1. Buy a domain (e.g. jgmart.bd, jgc-groceries.com) from:
   - Bangladesh registrars: bdserver.com, instra.net
   - International: Namecheap, GoDaddy, Porkbun

2. In Vercel dashboard → Project → Domains → Add your domain
3. Update your domain's DNS nameservers to point to Vercel
4. Wait 5-30 minutes for DNS propagation

Your site will be live at your custom domain with HTTPS automatically.

═══════════════════════════════════════════════════════════════════════════
AFTER DEPLOYMENT CHECKLIST
═══════════════════════════════════════════════════════════════════════════

[ ] Open the live URL → verify catalog loads
[ ] Test search and category filter
[ ] Add a product to cart → send WhatsApp → verify message
[ ] Open admin.html → login with PIN 1234 → verify products load
[ ] Change a product price in admin → verify it updates in catalog
[ ] Open track.html → paste an order ID → verify it works
[ ] Open menu.html → click Print → verify print layout
[ ] Open zone.html → verify all 27 buildings shown
[ ] On phone: add to home screen → verify PWA installs
[ ] Share a link with a friend → verify it works

═══════════════════════════════════════════════════════════════════════════
THE WEBSITE IS READY
═══════════════════════════════════════════════════════════════════════════

8 pages · 65 products · Full cart & checkout · PWA installable
Admin panel · Order tracking · Delivery zones · Printable menus
All images · Offline support · 404 page · Clean URLs

Just drag to Vercel → it goes live. 5 minutes. 🚀
