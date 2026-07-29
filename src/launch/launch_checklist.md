# JG Mart — Launch Readiness Checklist
## Pre-Launch | Week Before | Day Of | Post-Launch

---

## Pre-Launch (1 Week Before)

### Product & Pricing
- [ ] All 65 products have accurate prices in admin panel
- [ ] Product images load correctly in catalog
- [ ] Bengali/English toggle works on all pages
- [ ] Daily Specials banner has placeholder text set
- [ ] Delivery fees match cluster configuration (C1-2: free, C3: ৳20, C4: ৳30)

### Website & Technical
- [ ] All 13 pages load without errors
- [ ] WhatsApp links use correct number: +8801870489448
- [ ] Admin PIN is set and documented (not shared publicly)
- [ ] PWA manifest and service worker are active
- [ ] Offline fallback page works
- [ ] Site health checker shows all green

### Operations
- [ ] 3 riders hired and briefed
- [ ] Rider WhatsApp group created
- [ ] Rider uniforms/bags procured (JG Mart branding)
- [ ] Delivery bags/thermal boxes sourced
- [ ] Payment QR codes printed (bKash + Nagad)
- [ ] Rider route maps printed for each cluster

### Partners & Suppliers
- [ ] Krishi Market vendor agreements confirmed
- [ ] Minimum daily orders committed (৳5,000/day)
- [ ] Vendor contact list saved in phone
- [ ] Backup vendors identified for each category

### Marketing
- [ ] Flyers designed and printed (27 buildings)
- [ ] WhatsApp broadcast message drafted
- [ ] JGC building committee informed
- [ ] Referral discount code activated (50 BDT)
- [ ] Social media accounts created (optional)

---

## Week Before (Final Prep)

### Day -7
- [ ] Run full validation toolkit: `python tests/validate_toolkit.py`
- [ ] Fix any HTML/CSS/JS issues found
- [ ] Test catalog on 3 different devices (iPhone, Android, laptop)
- [ ] Test WhatsApp integration end-to-end
- [ ] Verify admin panel CRUD operations

### Day -5
- [ ] Print 100 flyers for building distribution
- [ ] Prepare rider onboarding packets
- [ ] Set up daily operations spreadsheet
- [ ] Create customer service response templates

### Day -3
- [ ] Conduct rider training session (2 hours)
- [ ] Test delivery route with 1 rider (dry run)
- [ ] Verify payment QR codes work
- [ ] Confirm vendor delivery times

### Day -1
- [ ] Final website check (all pages, all links)
- [ ] Admin panel backup downloaded
- [ ] Rider WhatsApp group activated
- [ ] Emergency contact list distributed

---

## Day Of Launch

### Morning Setup (6:00 AM)
- [ ] Fahad arrives at Krishi Market by 6:30 AM
- [ ] Rider 1 arrives at Krishi Market by 7:00 AM
- [ ] Rider 2 & 3 on standby at JGC
- [ ] First orders confirmed by 7:30 AM
- [ ] WhatsApp broadcast sent by 8:00 AM

### Delivery Execution
- [ ] Morning slot orders delivered by 12:00 PM
- [ ] Rider returns to JGC by 12:30 PM
- [ ] Debrief: what went well, what to fix
- [ ] Evening slot orders confirmed by 3:30 PM
- [ ] Evening deliveries completed by 8:00 PM

### End of Day
- [ ] All orders marked as delivered in admin
- [ ] Daily summary generated
- [ ] Rider payments calculated
- [ ] Next day's vendor orders placed
- [ ] Backup reminder checked

---

## Post-Launch (First Week)

### Daily
- [ ] Check order count by 10:00 AM
- [ ] Verify all deliveries completed by 9:00 PM
- [ ] Respond to WhatsApp messages within 30 minutes
- [ ] Update admin panel with any product changes
- [ ] Note customer feedback for improvements

### End of Week
- [ ] Generate weekly report (orders, revenue, customers)
- [ ] Review rider performance
- [ ] Update product catalog based on demand
- [ ] Plan next week's marketing push
- [ ] Backup all data

---

## Success Metrics (Week 1)

| Metric | Target | Actual |
|--------|--------|--------|
| Orders received | 50+ | ____ |
| Orders delivered | 100% | ____ |
| Customer complaints | 0 | ____ |
| WhatsApp response time | <30 min | ____ |
| Admin panel uptime | 100% | ____ |
| Rider punctuality | 100% | ____ |

---

## Emergency Protocols

### If a rider doesn't show up
1. Call backup rider immediately
2. Merge routes with other rider if possible
3. Notify affected customers via WhatsApp
4. Offer 20 BDT discount for delay

### If vendor can't fulfill order
1. Substitute with equivalent product
2. Notify customer before delivery
3. Refund difference if substitution is cheaper

### If website goes down
1. Switch to manual WhatsApp orders
2. Use admin panel CSV export as backup
3. Fix issue within 2 hours

### If payment fails
1. Accept cash only for that order
2. Process bKash manually later
3. Update customer on payment status
