# JG Mart — Tutorial & How-To Guide

> **For:** Customers, Partners, Operations Team, Developers, Investors
> **Last Updated:** 28 July 2026

---

## Table of Contents

1. [For Customers: How to Order](#1-for-customers-how-to-order)
2. [For Partners: How to Join](#2-for-partners-how-to-join)
3. [For Operations: Daily Routine](#3-for-operations-daily-routine)
4. [For Developers: How to Contribute](#4-for-developers-how-to-contribute)
5. [For Investors: How to Evaluate](#5-for-investors-how-to-evaluate)
6. [Video Tutorial Scripts](#6-video-tutorial-scripts)
7. [FAQ](#7-faq)

---

## 1. For Customers: How to Order

### Step 1: Open the Catalog

Open this link on your phone:
```
https://jg-mart.vercel.app
```

Or scan the QR code from your building's flyer.

### Step 2: Browse Products

- Scroll through categories: Staples, Vegetables, Fish, Meat, FMCG, Fruits
- Tap any product to see details
- Tap "Add to Cart" to add items

### Step 3: Checkout via WhatsApp

1. Tap the cart icon (top-right)
2. Review your order
3. Tap "Checkout via WhatsApp"
4. Enter your building and flat number
5. Select delivery slot: 11AM-1PM or 6PM-8PM
6. Tap "Send Order"

WhatsApp opens automatically with your order message sent to +8801870489448.

### Step 4: Confirm & Pay

You'll receive a confirmation message with:
- Exact total
- bKash number for payment
- Delivery time

Pay via bKash or choose Cash on Delivery (COD).

### Step 5: Receive Delivery

Your order arrives within 2 hours at your door.

---

## 2. For Partners: How to Join

### What We Need

We partner with Krishi Market shops in these categories:
- Rice, Dal, Oil (wholesale grain shops)
- Vegetables (vegetable vendors)
- Fish (fish stalls)
- Meat/Chicken (butcher shops)
- FMCG (grocery shops)
- Milk, Eggs (dairy shops)

### Requirements

1. Shop must be within 2km of Japan Garden City
2. Must have WhatsApp Business
3. Must confirm orders within 15 minutes
4. Must allow pickup between 10:00-11:00 AM and 5:30-6:30 PM
5. Must agree to weekly cash settlement
6. Minimum 3-month commitment

### How to Apply

1. **Visit Krishi Market** (Tajmahol Road, Mohammadpur)
2. **Talk to our team** — Look for JG Mart branded bags or ask at the hub
3. **WhatsApp us:** +8801870489448 with:
   - Shop name
   - Category (rice, veg, fish, etc.)
   - Sample price list
   - Shop location

### Commission Structure

| Category | Commission |
|----------|-----------|
| Staples (rice, dal, oil) | 5-7% |
| Perishables (veg, fish, meat) | 12-15% |
| FMCG | 10-12% |
| Milk, Eggs | 8-10% |

### What You Get

- More customers without delivery cost
- Weekly cash payments
- JG Mart branded bags (free)
- WhatsApp order notifications
- Performance bonuses for on-time delivery

---

## 3. For Operations: Daily Routine

### Morning (6:00 AM - 10:00 AM)

1. **6:00 AM** — Wake up, check overnight WhatsApp orders
2. **6:15 AM** — Send "Today's Availability" to all partners
3. **6:30 AM** — Partners reply with unavailable items
4. **7:00 AM** — Update "Available Today" catalog
5. **7:30 AM** — Post WhatsApp catalog image with prices
6. **8:00 AM** — Customer orders begin via WhatsApp
7. **9:00 AM** — Order cutoff for 11AM-1PM delivery
8. **9:15 AM** — Split orders by partner, send to shops
9. **9:30 AM** — Partners confirm or flag issues
10. **10:00 AM** — Rider pickup begins from Krishi Market

### Midday (10:00 AM - 2:00 PM)

1. **10:00 AM** — Rider collects from all partners
2. **11:15 AM** — Sort at hub, load delivery bags
3. **11:30 AM** — Deliver 11AM-1PM slot
4. **12:00 PM** — Collect payments (COD/bKash)
5. **1:00 PM** — Update orders to "Delivered" in system
6. **2:00 PM** — Lunch break, prepare for evening slot

### Evening (3:00 PM - 10:00 PM)

1. **3:00 PM** — Order cutoff for 6PM-8PM delivery
2. **3:15 PM** — Split orders, send to partners
3. **3:30 PM** — Partners confirm
4. **4:00 PM** — Rider pickup begins
5. **5:15 PM** — Sort at hub, load bags
6. **5:30 PM** — Deliver 6PM-8PM slot
7. **7:00 PM** — Collect payments
8. **8:00 PM** — Update orders to "Delivered"
9. **9:00 PM** — End-of-day reconciliation
10. **10:00 PM** — Update inventory tracker, backup data

### Weekly (Every Sunday)

1. Complete Weekly Review template
2. Review Risk Log
3. Pay partners weekly settlement
4. Update KPI Dashboard
5. Plan next week's marketing

---

## 4. For Developers: How to Contribute

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Code editor (VS Code recommended)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/FahadIbrahim93/jgmart-hermes.git
cd jgmart-hermes

# 2. Install dependencies
pip install -r requirements.txt  # when available
npm install

# 3. Set up pre-commit hooks
pip install pre-commit
pre-commit install

# 4. Run tests
pytest tests/

# 5. Start local servers
# Catalog
cd src/web/catalog && python -m http.server 8000

# Dashboard (new terminal)
cd src/web/dashboard && python -m http.server 8001
```

### Project Structure

```
jgmart-hermes/
├── src/
│   ├── web/
│   │   ├── catalog/       ← Customer-facing grocery catalog
│   │   └── dashboard/     ← Operations dashboard
│   ├── scripts/
│   │   └── automation/    ← Python scripts
│   └── templates/
│       ├── legal/         ← Legal document templates
│       ├── marketing/     ← Marketing materials
│       └── operations/    ← Operational templates
├── assets/
│   ├── brand/             ← Logos, brand guidelines
│   ├── images/            ← Product images
│   └── documents/         ← DOCX, PDF, PPTX, XLSX
├── data/
│   ├── exports/           ← Data exports
│   ├── sample/            ← Sample data
│   └── backups/           ← Backup files
├── docs/                  ← Documentation
└── tests/                 ← Test suite
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Code Standards

- **Python:** PEP 8, `black`, `flake8`
- **JavaScript:** Prettier
- **HTML:** Valid HTML5, WCAG 2.1 AA accessible
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`)

---

## 5. For Investors: How to Evaluate

### What to Review

1. **Business Plan:** `docs/business/BUSINESS_PLAN.md`
2. **Financial Model:** `assets/documents/JG_Mart_Financial_Model.xlsx`
3. **Pitch Deck:** `assets/documents/JG_Mart_Investor_Pitch_Deck.pptx`
4. **Executive Summary:** `docs/business/EXECUTIVE_SUMMARY.md`
5. **Operations Manual:** `docs/operations/OPERATIONS_MANUAL.md`
6. **Audit:** `docs/audit/BRUTAL_HONEST_AUDIT.md` (we're transparent about gaps)

### Key Metrics

| Metric | Value |
|--------|-------|
| Market | 1,700 families, 27 buildings, 4 clusters |
| Avg Order Value | 800 BDT |
| Commission | 11% blended |
| Delivery Fee | 30 BDT |
| Contribution Margin | 51% |
| Seed Ask | 250,000 BDT |
| Target (Month 6) | 350 customers, 1,050 orders/month |

### Live Proof

- **Website:** https://jg-mart.vercel.app
- **GitHub:** https://github.com/FahadIbrahim93/jgmart-hermes
- **WhatsApp:** +8801870489448

### Due Diligence

We encourage investors to:
1. Review the brutal honest audit (`docs/audit/`)
2. Test the live catalog
3. Visit Krishi Market (800m from JGC)
4. Talk to our beta customers
5. Review the financial model assumptions

---

## 6. Video Tutorial Scripts

### Customer Tutorial (30 seconds)

> "Hi! Welcome to JG Mart. Open this link on your phone, browse our fresh groceries, add items to cart, and checkout via WhatsApp. We deliver in 2 hours at Krishi Market prices. That's it — no app, no login, no hassle."

### Partner Tutorial (60 seconds)

> "Hi! We're JG Mart, a grocery delivery service for Japan Garden City. We partner with Krishi Market shops. If you have a shop in rice, vegetables, fish, meat, or FMCG, WhatsApp us at +8801870489448. We handle delivery and customers; you just fulfill orders. Weekly cash payments, no credit risk. Let's grow together."

### Developer Tutorial (5 minutes)

> "Welcome to the JG Mart developer community. This repo contains our complete business toolkit — web apps, automation scripts, legal templates, and operational docs. To contribute: clone the repo, install dependencies, run tests, and submit a PR. We follow PEP 8, Conventional Commits, and WCAG accessibility standards. Check CONTRIBUTING.md for details."

---

## 7. FAQ

### Customers

**Q: How much is delivery?**
A: 30 BDT per order. Free for JG Mart Premium subscribers (149 BDT/month).

**Q: What are the delivery slots?**
A: 11AM-1PM (order by 9AM) and 6PM-8PM (order by 3PM).

**Q: Can I pay via bKash?**
A: Yes. We accept bKash and Cash on Delivery.

**Q: What if an item is out of stock?**
A: We'll call you immediately with alternatives. You can approve or cancel.

**Q: Do you deliver to my building?**
A: We deliver to all 27 buildings in Japan Garden City. Delivery fees vary by cluster.

### Partners

**Q: How much commission do you take?**
A: 5-15% depending on category. Staples: 5-7%, Perishables: 12-15%.

**Q: When do I get paid?**
A: Weekly, every Sunday, for the previous week's orders.

**Q: What if I can't fulfill an order?**
A: Notify us 30 minutes before cutoff. No penalty if communicated early.

**Q: Do I need a website or app?**
A: No. We communicate via WhatsApp. Just confirm orders and prepare for pickup.

### Developers

**Q: Can I use this code for my own delivery business?**
A: Yes, under MIT License. Please attribute JG Mart.

**Q: How do I add a new product category?**
A: Edit `src/web/catalog/catalog_data.json` and `src/web/dashboard/` data files.

**Q: Is there a backend?**
A: No. This is a static site with WhatsApp integration. Data is stored in JSON files.

### Investors

**Q: What's the competitive moat?**
A: Chaldal has no Mohammadpur warehouse. We're 800m from Krishi Market. Zero inventory risk, community insider advantage.

**Q: What's the burn rate?**
A: ~62,000 BDT/month at Month 3, scaling to ~56,250 BDT/month at Month 6.

**Q: When do you break even?**
A: Month 2 (conservative) or Month 1 (aggressive).

**Q: What's the use of funds?**
A: 40% marketing, 30% working capital, 20% equipment, 10% legal/misc.

---

## Quick Links

| Purpose | Link |
|---------|------|
| Customer Catalog | https://jg-mart.vercel.app |
| GitHub Repo | https://github.com/FahadIbrahim93/jgmart-hermes |
| WhatsApp Orders | https://wa.me/8801870489448 |
| Business Plan | `docs/business/BUSINESS_PLAN.md` |
| Financial Model | `assets/documents/JG_Mart_Financial_Model.xlsx` |
| Pitch Deck | `assets/documents/JG_Mart_Investor_Pitch_Deck.pptx` |

---

*Last updated: 28 July 2026 | JG Mart — Tutorial & How-To Guide v1.0*
