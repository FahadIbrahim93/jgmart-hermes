JG MART — WEB CATALOG
======================

WHAT IS THIS?
-------------
A customer-facing, mobile-optimized grocery catalog for JG Mart.
Customers browse products on their phones and place orders directly via WhatsApp.
No backend required — just open index.html in any browser.

FILES
-----
1. index.html      — The customer-facing website (single file, embedded CSS + JS)
2. catalog_data.json — Product catalog data (20+ products across 8 categories)
3. README.txt      — This file

HOW TO USE
----------
1. Open index.html in any modern web browser (Chrome, Safari, Firefox).
   You can double-click the file or drag it into a browser window.
2. Browse products by category. Click "Add to Cart" to collect items.
3. Click the cart icon (top-right) to review your order.
4. Click "Checkout via WhatsApp", enter your building/flat, select a delivery slot, and submit.
5. WhatsApp will open with a pre-filled order message sent directly to JG Mart (+8801870489448).

HOW TO UPDATE PRICES DAILY
---------------------------
1. Open catalog_data.json in any text editor.
2. Find the product you want to update and change its "price" field.
3. Save the file. The website reads from this file on every load — no rebuild needed.

Example:
   "price": 120   <-- change this number

HOW TO ADD A NEW PRODUCT
------------------------
1. Open catalog_data.json.
2. Add a new object to the "products" array following this structure:

{
  "id": "p026",                          <-- unique id, use next number
  "name": "Product Name",
  "category": "vegetables",              <-- must match a category id
  "price": 50,
  "unit": "kg",                          <-- kg, liter, piece, dozen, 100g, etc.
  "wholesale_price": 42,
  "partner_id": "part001",
  "partner_name": "Krishi Market",
  "commission_pct": 10,
  "stock_status": "in_stock",            <-- "in_stock" or "out_of_stock"
  "image_emoji": "🥬",
  "description": "Short description here"
}

3. Save. The product appears automatically in the catalog.

HOW TO CHANGE THE WHATSAPP NUMBER
----------------------------------
In index.html, search for:
   CONFIG.whatsappNumber: '8801870489448'
Replace with the new number (without the + sign).

Also update the floating WhatsApp button href (search for wa.me/8801870489448).

HOW TO UPDATE DELIVERY ZONES / FEES
------------------------------------
1. In index.html, search for "CONFIG" and edit the delivery fee logic in the 
   getCartTotals() function.
2. To update the displayed zones, edit the HTML in the "Delivery Zones Info" section.
   Or, better yet, read from catalog_data.json delivery_zones array (you can extend the JS).

HOW TO DEPLOY
-------------
This is a static site. You can deploy it to any static hosting service:

OPTION A — Netlify / Vercel / Cloudflare Pages
   - Create a free account.
   - Upload these 2 files (index.html + catalog_data.json).
   - The site is live in seconds.

OPTION B — GitHub Pages
   - Create a repo, push index.html and catalog_data.json.
   - Enable Pages in repo settings.
   - Your site is live at https://<username>.github.io/<repo>/

OPTION C — Shared Hosting / cPanel
   - Upload both files to public_html/ on your hosting.
   - Visit your domain to see the catalog.

CATEGORIES (Do NOT rename these IDs)
-------------------------------------
rice_dal       Rice & Dal
oil_spices     Oil & Spices
vegetables     Vegetables
fish           Fish
meat           Meat
dairy_eggs     Dairy & Eggs
fruits         Fruits
fmcg           FMCG

PARTNERS
--------
part001  Krishi Market
part002  City Traders
part003  Fresh Catch BD
part004  Halal Meats
part005  Green Dairy
part006  Daily Needs BD
part007  National Foods

CUSTOMIZATION TIPS
------------------
- Colors: Change "jg-green" values in the Tailwind config inside index.html.
- Hero text: Edit the <h1> in the Hero section of index.html.
- Delivery slots: Edit CONFIG.deliverySlots in the JS section.
- Categories: Add/remove category tabs in renderCategories() function.
- Products: Update catalog_data.json — the site auto-refreshes.

TROUBLESHOOTING
---------------
Q: Products don't show up.
A: Make sure catalog_data.json is in the same folder as index.html.

Q: WhatsApp link doesn't work on desktop.
A: WhatsApp Web must be installed or you must be logged in at web.whatsapp.com.

Q: Images look broken.
A: The catalog uses emoji as product images. This is intentional — no external images to load.
   If you want real photos, replace image_emoji with <img src="..."> in the product card template.

SUPPORT
-------
For website issues: contact Fahad Ibrahim
For order issues: WhatsApp +8801870489448
