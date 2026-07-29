# JG Mart — Daily Operations SOP
## Standard Operating Procedure for Day-to-Day Operations

---

## 1. Morning Routine (6:00 AM – 9:00 AM)

### Fahad (Founder)
1. **6:00 AM** — Wake up, check WhatsApp for any overnight orders
2. **6:30 AM** — Arrive at Krishi Market
3. **6:30-7:30 AM** — Source products:
   - Buy vegetables for morning slot orders
   - Verify quality (freshness, weight, packaging)
   - Negotiate prices with vendors
   - Pay vendors (cash or bKash)
4. **7:30 AM** — Pack orders by building cluster:
   - C1 (B1-6): Red标签/tag
   - C2 (B7-13): Blue标签/tag
   - C3 (B14-20): Green标签/tag
   - C4 (B21-27): Yellow标签/tag
5. **7:45 AM** — Brief riders:
   - Hand over packed orders
   - Confirm delivery addresses
   - Collect payments (if COD)
   - Issue rider route cards
6. **8:00 AM** — Riders depart for delivery
7. **8:00-9:00 AM** — Process evening slot orders in admin panel

### Rider 1 (Morning Delivery Lead)
1. **7:00 AM** — Arrive at Krishi Market
2. **7:00-7:45 AM** — Load orders into delivery bag/thermal box
3. **7:45 AM** — Depart for C1/C2 cluster (closest buildings)
4. **8:00-11:30 AM** — Deliver orders:
   - Call customer 5 minutes before arrival
   - Verify order items at door
   - Collect payment (COD) or confirm bKash
   - Mark as delivered in admin panel (if possible)
   - Thank customer, ask for referral
5. **11:30 AM** — Return to JGC
6. **11:30 AM-12:00 PM** — Debrief with Fahad

### Rider 2 & 3 (Support)
1. **7:00 AM** — On standby at JGC
2. **8:00 AM** — Assist Rider 1 if needed
3. **9:00 AM** — If no morning support needed, rest/prepare for evening
4. **3:30 PM** — Return for evening slot

---

## 2. Evening Routine (3:00 PM – 9:00 PM)

### Fahad
1. **3:00 PM** — Check admin panel for evening slot orders
2. **3:30 PM** — Confirm cutoff time for evening orders
3. **4:00 PM** — If enough orders, source from Krishi Market:
   - Buy fish, meat, cooked items
   - Buy vegetables for evening
4. **5:00 PM** — Pack evening orders by cluster
5. **5:30 PM** — Brief riders for evening delivery
6. **6:00 PM** — Riders depart for delivery
7. **6:00-8:00 PM** — Monitor delivery progress via WhatsApp
8. **8:00 PM** — All deliveries should be complete
9. **8:30 PM** — End of day debrief with riders

### Riders
1. **3:30 PM** — Arrive at Fahad's location / JGC gate
2. **5:30 PM** — Load evening orders
3. **6:00 PM** — Depart for delivery (prioritize C4 first, then C3, C2, C1)
4. **6:00-8:00 PM** — Deliver orders
5. **8:00 PM** — Return to base
6. **8:00-8:30 PM** — Return empty bags, report issues

---

## 3. Order Management

### Order Flow
1. Customer sends WhatsApp order
2. Fahad confirms order in admin panel
3. Order appears in admin panel with status "Received"
4. Fahad marks as "Picked Up" when rider departs
5. Rider marks as "Delivered" when customer receives
6. Customer can track via track.html

### Order Status Workflow
```
Received → Picked Up → Delivered
    ↓         ↓           ↓
  (auto)   (rider)    (customer)
```

### Order Cancellation
- Customer cancels before 9 AM (morning) or 3:30 PM (evening): full refund
- Customer cancels after cutoff: 50% cancellation fee
- Admin marks as "Cancelled" in panel

---

## 4. Payment Collection

### Cash on Delivery (COD)
- Rider collects exact amount at door
- Rider marks payment as "Cash" in admin
- Fahad collects cash from riders at end of day
- Cash stored in safe/locker

### bKash
- Customer sends payment to: [JG Mart bKash number]
- Customer sends screenshot to WhatsApp
- Rider verifies payment before delivery
- Admin panel updated with transaction ID

### Reconciliation (Daily)
1. Match admin panel payments with rider reports
2. Match bKash transactions with bank statement
3. Record daily revenue in spreadsheet
4. Deposit cash in bank weekly

---

## 5. Inventory Management

### Daily Sourcing
- **Morning:** Vegetables, fruits, dairy, eggs
- **Evening:** Fish, meat, cooked items, snacks

### Stock Levels
- Minimum stock: 2 days of supply
- Reorder trigger: 1 day of supply remaining
- Emergency sourcing: backup vendor phone list

### Waste Management
- Unsold perishables at end of day:
  - Offer 50% discount to staff/riders
  - Donate to building staff if safe
  - Record waste in daily report

---

## 6. Customer Service

### WhatsApp Response Protocol
- Response time target: 30 minutes
- Business hours: 8:00 AM – 10:00 PM
- After hours: Auto-reply with next-day promise

### Common Customer Issues
| Issue | Resolution | Time |
|-------|------------|------|
| Wrong item delivered | Refund or replace within 24h | 30 min |
| Missing item | Refund or add to next order | 30 min |
| Poor quality | Full refund, no questions asked | 15 min |
| Late delivery | 20 BDT credit + apology | 5 min |
| Price dispute | Match advertised price, refund difference | 15 min |

### Escalation
- Unresolved after 24h: Fahad intervenes directly
- Repeated issues: Customer flagged in admin panel

---

## 7. Rider Management

### Daily Briefing (Morning)
1. Review yesterday's performance
2. Highlight today's priorities
3. Confirm routes and addresses
4. Issue cash for change/parking

### Daily Debrief (Evening)
1. Review delivery completion
2. Discuss issues/challenges
3. Collect rider feedback
4. Plan tomorrow's improvements

### Rider Payments
- Daily wage: ৳500/day
- Performance bonus: ৳50 for 100% on-time delivery
- Deductions: Late arrival (-৳50), customer complaint (-৳100)

---

## 8. Daily Reports

### End-of-Day Report (Generated by Python Script)
```json
{
  "date": "2026-07-29",
  "orders_total": 45,
  "orders_delivered": 43,
  "orders_cancelled": 2,
  "revenue": 36100,
  "cost": 18400,
  "net": 17700,
  "customers_served": 38,
  "top_products": ["Rice 5kg", "Onion 1kg", "Chicken 1kg"],
  "issues": ["Rider 2 late by 15 min", "Vendor short on tomatoes"],
  "tomorrow_plan": "Increase vegetable order by 20%"
}
```

### Weekly Report (Sunday)
- Total orders: ____
- Total revenue: ____
- Total customers: ____
- New customers: ____
- Top 5 products: ____
- Issues & improvements: ____

---

## 9. Backup & Data Management

### Daily Backup
1. Export admin panel CSV (orders, products)
2. Copy to USB drive / Google Drive
3. Verify backup file opens correctly
4. Delete backups older than 30 days

### Weekly Backup
1. Full website snapshot
2. Customer data export
3. Financial spreadsheet backup
4. Store in 2 locations (local + cloud)

---

## 10. Emergency Procedures

### Website Down
1. Switch to manual WhatsApp orders
2. Use phone notes for order tracking
3. Fix issue within 2 hours
4. Notify customers of delay

### Rider Absent
1. Call backup rider
2. Merge routes with other rider
3. Notify affected customers
4. Offer 20 BDT discount

### Vendor Shortage
1. Substitute with equivalent product
2. Notify customer before delivery
3. Refund difference if cheaper

### Payment Dispute
1. Verify transaction ID
2. Check bKash statement
3. Resolve within 24 hours
4. Document in admin panel

---

## 11. Quality Standards

### Product Quality
- Freshness: Same day from Krishi Market
- Packaging: Clean, sealed, labeled
- Weight: Accurate within 5%
- Temperature: Cold items in thermal bags

### Delivery Standards
- Punctuality: On time or early
- Uniform: JG Mart branded shirt/bag
- Communication: Call 5 min before arrival
- Courtesy: Polite, professional, helpful

### Customer Experience
- Order confirmation within 5 minutes
- Delivery within promised slot
- No hidden fees
- Easy returns/refunds
