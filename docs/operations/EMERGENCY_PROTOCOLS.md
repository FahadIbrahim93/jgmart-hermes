# Emergency Protocols

## 1. Rider Accident or Breakdown
1. Stop dispatch for affected zone immediately
2. Contact rider via WhatsApp / phone
3. If injury: call ambulance + notify family
4. If vehicle breakdown: arrange replacement rider or customer pickup
5. Notify customer of delay via WhatsApp template
6. File incident in `RISK_LOG` (see `15_JG_Mart_Risk_Log.txt`)
7. Insurance claim initiated within 24 hours

## 2. Store Stock-Out at Peak
1. Ops lead notified via WhatsApp alert
2. Pause listing of out-of-stock item in catalog
3. Offer substitute or refund via `CUSTOMER_TERMS_OF_SERVICE.txt`
4. If bulk stock-out: redirect orders to nearest partner store
5. Update customer with ETA for restock

## 3. Payment Gateway Failure
1. Default to Cash on Delivery for all orders
2. Display banner on catalog: "Payments temporarily offline"
3. Tech notified to restart payment service
4. If >2 hours: escalate to founder
5. Log downtime in `SYSTEM_TEST.txt`

## 4. Customer Complaint Escalation
**Level 1 (0–2 hours):** WhatsApp support bot / human agent
**Level 2 (2–6 hours):** Ops manager personal call
**Level 3 (6–24 hours):** Founder介入 + compensation offer
**Level 4 (24+ hours):** Legal review if NPS threshold breached

## 5. WhatsApp API Outage
1. Fallback to SMS for critical notifications
2. Use email backup for order confirmations
3. Rider dispatch via phone call
4. Document outage duration and customer impact
5. Contact WhatsApp Business support if >1 hour

## 6. Data Loss / Backup Failure
1. Immediately halt new data writes
2. Restore from last known good backup (`BACKUP_MANIFEST.txt`)
3. Verify data integrity via `validate_toolkit.py`
4. Notify stakeholders of partial data loss window
5. Review backup automation (`drive_sync.py`) for root cause

## 7. Fire / Natural Disaster
1. Activate `BUSINESS_CONTINUITY_KIT.txt`
2. Evacuate personnel first, data second
3. Notify customers of service suspension
4. Coordinate with local authorities
5. Resume from remote backup within 48 hours if safe

---

*Review these protocols quarterly and after every incident.*
