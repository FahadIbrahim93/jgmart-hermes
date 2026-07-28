JG MART — WEB CATALOG
======================

WHAT IS THIS?
-------------
Customer-facing web pages for JG Mart, a hyperlocal grocery delivery platform.
Customers browse products, add to cart, and place orders via WhatsApp.
All pages are static HTML/CSS/JS — no build step or backend required.


DATA FLOW ARCHITECTURE
----------------------

The product catalog uses TWO separate data sources for different pages:

┌──────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                │
│  catalog_data.json  ────→  index.html  (main shopping page)    │
│                     ────→  menu.html   (printable price menu)   │
│                     ────→  admin.html  (product management)     │
│                                                                │
│  order_intake_data.json ──→  order_intake.html  (order form)   │
│                                                                │
└──────────────────────────────────────────────────────────────────┘

catalog_data.json (65 products, 10 categories)
─────────────────────────────────────────────────
The MAIN product catalog used by the shopping, menu, and admin pages.
Each product has: id, name, category, price, unit, emoji, rating, reviews, image path

Pages that use it:
  • index.html     — Main catalog browser (shop by category, search, cart, WhatsApp checkout)
  • menu.html      — Printable price list (organised by category for print/PDF)
  • admin.html     — Admin panel (edit prices, manage products, view orders/analytics)

order_intake_data.json (63 items, 7 categories)
─────────────────────────────────────────────────
A SEPARATE product catalog for the order intake form.
Uses different product names, pricing, and category structure
from the main catalog. This was intentionally designed as
a distinct ordering interface with its own product selection.

Pages that use it:
  • order_intake.html  — Dedicated order intake form with customer info fields


HOW PRODUCT LOADING WORKS
-------------------------

All four catalog pages use the same pattern:

  1. Page loads → check localStorage for cached product data
  2. If cached data exists → use it immediately (fast, no network)
  3. If no cached data → fetch from the appropriate .json file
  4. On successful fetch → save to localStorage for next visit
  5. On fetch failure → use a small hardcoded fallback set

This means:
  • First visit = one HTTP request for the .json file
  • Subsequent visits = instant load from localStorage
  • To refresh the cache (e.g. after price updates), clear localStorage
    or rename the storage keys


FILES IN THIS DIRECTORY
-----------------------

PAGE FILES:
  index.html           — Main catalog browser (shop, cart, WhatsApp checkout)
  menu.html            — Printable price list for customers
  order_intake.html    — Order intake form with full product selection
  admin.html           — Admin panel (manage products, orders, analytics)
  landing.html         — Marketing landing page
  track.html           — Order tracking page
  zone.html            — Delivery zone info page
  manifest.html        — Delivery manifest (printable, rider-facing)
  myorders.html        — Customer order history
  healthcheck.html     — System health page
  nav_template.html    — Navigation template
  jsonld-snippets.html — Structured data snippets for SEO

DATA FILES:
  catalog_data.json       — Main product catalog (65 products, 10 categories)
  order_intake_data.json  — Order intake product catalog (63 items, 7 categories)

ASSETS:
  images/              — Product images (p001.jpg through p065.jpg)
  manifest.json        — PWA manifest
  sw.js                — Service Worker (offline support)
  favicon.svg          — Site favicon

CONFIG FILES:
  vercel.json          — Vercel deployment config
  netlify.toml         — Netlify deployment config
  robots.txt           — Search engine crawling rules
  sitemap.xml          — SEO sitemap
  _redirects           — URL redirect rules


HOW TO USE (Store Operators)
----------------------------
1. Open index.html in any modern browser (Chrome, Safari, Firefox).
   You can double-click the file or drag it into a browser window.
2. Browse products by category. Tap items to see details.
3. Add items to cart, then tap the WhatsApp button to check out.
4. Enter your building/flat details and send the order message.

For the order intake form: open order_intake.html
- Fill in customer details, add items by tapping +/-, and send via WhatsApp.

For the admin panel: open admin.html
- **Supabase Auth** — login with email/password (if configured) or demo mode (any credentials if Supabase not set up)
- Edit prices inline, add/remove products, view orders and analytics.
- Settings tab includes **🔌 Supabase Connection** to enter credentials without editing code.
- Click **🚪 Logout** in the top-right to sign out.

For the printable menu: open menu.html → click "Print Menu" or "Save PDF"


HOW TO CHANGE THE WHATSAPP NUMBER
---------------------------------
The WhatsApp number is hardcoded in multiple files. Search and replace:
- In index.html:  wa.me/8801870489448  (appears twice)
- In order_intake.html:  WHATSAPP_NUMBER = '8801870489448'
- In the JS config section of index.html:  CONFIG.whatsappNumber


HOW TO UPDATE PRODUCTS
----------------------

For main catalog (index.html, menu.html, admin.html):
  1. Open catalog_data.json in any text editor
  2. Find the product by its "id" field (e.g. "p001")
  3. Edit the fields: "pr" (price), "nm" (name), "de" (description), etc.
  4. Save the file — the changes take effect on next page load

For order intake (order_intake.html):
  1. Open order_intake_data.json
  2. Navigate to the relevant category (e.g. "rice", "veggies", "fishmeat")
  3. Edit the "name", "price", or "unit" fields
  4. Save the file

PRICE UPDATE WORKFLOW (Daily):
  1. Get today's wholesale prices from Krishi Market partners
  2. Open catalog_data.json
  3. Update relevant prices (the "pr" field for each product)
  4. Deploy the updated file to hosting


HOW TO ADD A NEW PRODUCT
------------------------

In catalog_data.json, add a new object to the "products" array:

    {
      "id": "p066",
      "nm": "Product Name",
      "ct": "vegetables",
      "pr": 50,
      "un": "kg",
      "em": "🥬",
      "rt": 4,
      "rv": 0,
      "de": "Short description",
      "im": "images/p066.jpg"
    }

Fields:
  id  — Unique identifier (p + zero-padded number)
  nm  — Product name (English)
  ct  — Category ID (must match one of: rice_dal, oil_spices, vegetables, fish,
        meat, dairy_eggs, fruits, fmcg, beverages, snacks)
  pr  — Price in BDT (integer)
  un  — Unit (kg, L, pc, doz, 100g, 200g, 250g, 500g, bunch)
  em  — Emoji representation (shown if image is missing)
  rt  — Rating (1.0–5.0)
  rv  — Number of reviews / order count
  de  — Short description
  im  — Image path relative to this directory

In order_intake_data.json, add to the relevant category's item array:

    { "name": "Product Name", "unit": "/kg", "price": 50 }


CATEGORIES (catalog_data.json)
------------------------------
rice_dal       Rice & Dal
oil_spices     Oil & Spices
vegetables     Vegetables
fish           Fish
meat           Meat
dairy_eggs     Dairy & Eggs
fruits         Fruits
fmcg           Household
beverages      Drinks
snacks         Snacks

CATEGORIES (order_intake_data.json)
-----------------------------------
rice           Rice & Dal
oil            Oil & Spices
veggies        Vegetables
fishmeat       Fish & Meat
dairy          Dairy & Eggs
fruits         Fruits
fmcg           FMCG


HOW TO DEPLOY
-------------
All files are static — deploy to any static hosting:

  Netlify:     Deploy the entire src/web/catalog/ directory
  Vercel:      Same — point it to src/web/catalog/
  GitHub Pages: Push and enable Pages from the repo settings

The vercel.json and netlify.toml files handle SPA routing.


TROUBLESHOOTING
---------------
Q: Products don't show up.
A: Make sure catalog_data.json is in the same folder as index.html.
   Open browser DevTools → Console tab to see any load errors.
   Check localStorage for "jgmart_prods" — clear it and reload.

Q: Prices are old / not updating.
A: Clear localStorage (Application tab in DevTools → Local Storage →
   right-click → Clear All) and reload the page.

Q: Images look broken.
A: Some products use emoji fallback (shown via onerror handler).
   The images/ folder contains JPG files for ~75% of products.
   Missing images display the product emoji instead.

Q: WhatsApp link doesn't work.
A: WhatsApp Web must be open or installed.
   Test on a mobile device for the most reliable experience.


SUPPORT
-------
Website issues:  Contact Fahad Ibrahim
Order issues:    WhatsApp +8801870489448
