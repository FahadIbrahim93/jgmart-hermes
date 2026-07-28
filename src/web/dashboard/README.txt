JG Mart KPI Dashboard - Usage Instructions
==========================================

GETTING STARTED
---------------
1. Open index.html in any modern web browser (Chrome, Firefox, Edge, Safari).
2. The dashboard will load with pre-populated sample data.
3. All data is automatically saved to your browser's localStorage.

NAVIGATION
----------
Use the left sidebar to switch between sections:
- Dashboard: Overview with KPI cards, charts, and recent data
- Orders: Full orders management with add/edit/delete
- Customers: Customer database with contact info and history
- Partners: Partner/rider performance tracking
- Inventory: SKU management with stock alerts
- Settings: Business settings, data import/export

ENTERING ORDERS
---------------
1. Go to Orders section (sidebar) or click "New Order" on Dashboard
2. Click "+ New Order" button
3. Fill in the form:
   - Customer Name: Name of the customer
   - Building/Cluster: Select from the 27 buildings across 4 clusters
   - Items Count: Number of items in the order
   - Total (BDT): Order total amount
   - Status: Pending, Processing, Out for Delivery, Delivered, or Cancelled
   - Rider: Assigned delivery person (optional)
4. Click "Save Order"

UPDATING INVENTORY
------------------
1. Go to Inventory section
2. Click "+ Add SKU" to add new items
3. Or click "Edit" on existing items to update stock levels
4. Stock status is automatically calculated:
   - Good: Stock above reorder point
   - Low: Stock at or below reorder point
   - Critical: Stock below reorder point AND less than 3 days of sales remaining

EXPORTING DATA
--------------
1. Go to Settings section
2. Click "Export Data" to download a JSON backup file
3. The file will be named: jgmart_backup_YYYY-MM-DD.json

IMPORTING DATA
-------------
1. Go to Settings section
2. Click "Import Data" and select a previously exported JSON file
3. All current data will be replaced with the imported data

LOADING SAMPLE DATA
------------------
1. Go to Settings section
2. Click "Load Sample Data" to reset to demo data
3. Confirm the overwrite when prompted

CLEARING ALL DATA
---------------
1. Go to Settings section
2. Click "Clear All Data" to remove everything except settings
3. Confirm when prompted

DARK/LIGHT MODE
--------------
Click the sun/moon icon in the top-right corner to toggle between dark and light themes.
Your preference is saved automatically.

BUSINESS SETTINGS
----------------
In Settings, you can update:
- Business Name
- Location
- Average Order Value (BDT)
- Commission Rate (%)
- Delivery Fee (BDT)

DEPLOYMENT
----------
This is a static single-page application. To deploy:

VERCEL:
1. Push the 05_Tech_Dashboard folder to a GitHub repository
2. Go to vercel.com and import the repository
3. Vercel will auto-detect the static site and deploy
4. Your dashboard will be live at https://your-project.vercel.app

NETLIFY:
1. Drag and drop the 05_Tech_Dashboard folder onto netlify.com/drop
2. Or connect a Git repository for continuous deployment
3. Your dashboard will be live instantly

GITHUB PAGES:
1. Push the 05_Tech_Dashboard folder to a GitHub repository
2. Go to Settings > Pages in your repository
3. Select the branch and folder (root or /docs)
4. Your dashboard will be live at https://username.github.io/repo-name

DATA PERSISTENCE
---------------
- All data is stored in browser localStorage under the key "jgmart_data"
- Data persists between browser sessions
- To backup: use Export Data in Settings
- To transfer to another device: export JSON, import on new device

JG MART BUSINESS CONTEXT
------------------------
- Founder: Fahad Ibrahim
- Location: Japan Garden City, Mohammadpur, Dhaka
- Model: WhatsApp-based grocery delivery, Krishi Market sourcing
- 4 Clusters: Bldg 1-6 (Cluster 1), Bldg 7-13 (Cluster 2), Bldg 14-20 (Cluster 3), Bldg 21-27 (Cluster 4)
- AOV: 800 BDT | Avg Commission: 11% | Delivery Fee: 30 BDT

TROUBLESHOOTING
--------------
- If charts don't load: Check internet connection (Chart.js and Tailwind CDN required on first load)
- If data disappears: Check if localStorage is enabled in your browser
- If layout breaks: Ensure you're using a modern browser (Chrome 90+, Firefox 88+, Edge 90+)
