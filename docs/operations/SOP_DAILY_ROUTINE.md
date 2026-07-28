# Standard Operating Procedure — Daily Routine

## Pre-Launch (6:00–7:00 AM)

| Time | Task | Owner | Tool |
|------|------|-------|------|
| 6:00 | Power on dashboard tablet / laptop | Ops Lead | Tech Dashboard |
| 6:05 | Verify rider attendance | Ops Lead | WhatsApp Group |
| 6:10 | Check inventory levels | Store Manager | `PRODUCT_PRICING.csv` |
| 6:20 | Upload any new product images | Tech | `add_image_urls.py` |
| 6:30 | Review weather / traffic alerts | Ops Lead | Google Maps |
| 6:45 | Send morning huddle message | Ops Lead | WhatsApp Broadcast |
| 6:55 | Final catalog link test | Tech | Catalog URL |

## Launch (7:00–8:00 AM)

| Time | Task | Owner | Tool |
|------|------|-------|------|
| 7:00 | Catalog goes live | System | Vercel |
| 7:05 | First order test order | Ops Lead | WhatsApp |
| 7:10 | Rider dispatch test | Ops Lead | Dashboard |
| 7:30 | Confirm all 3 zones active | Ops Lead | Dashboard |

## Operations (8:00 AM–8:00 PM)

| Time | Task | Owner | Tool |
|------|------|-------|------|
| Every hour | Sync orders to finance | Tech | `sync_bridge.py` |
| 12:00 | Midday rider check-in | Ops Lead | WhatsApp |
| 2:00 | Afternoon stock recheck | Store Manager | Physical count |
| 5:00 | Evening rush preparation | Ops Lead | Extra riders on standby |
| 8:00 | Cutoff for next-day orders | System | Catalog |

## Closing (8:00–9:00 PM)

| Time | Task | Owner | Tool |
|------|------|-------|------|
| 8:00 | Last order dispatch | Ops Lead | Dashboard |
| 8:30 | Generate daily report | Tech | `daily_summary.py` |
| 8:45 | Send ops summary to founder | Tech | WhatsApp |
| 9:00 | Archive daily data | Tech | `drive_sync.py` |

## Quality Checks
- [ ] No order left undelivered after cutoff
- [ ] All rider logs submitted
- [ ] Finance dashboard balanced
- [ ] Next-day inventory prepared

---

*Reference: `04_Operations/OPERATIONS_PLAYBOOK.txt`, `DAILY_START.bat`, `DAILY_END.bat`.*
