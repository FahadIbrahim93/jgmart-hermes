# JG Mart — Product Requirements Document

**Version:** 1.0 (consolidated)  
**Owner:** Fahad Ibrahim  
**Market:** Japan Garden City, Mohammadpur, Dhaka  
**Source:** Extracted from Kimi PRD session; updated for current web catalog + Supabase migration path

## 1. Product Overview

### Problem

~1,700–2,900 families in Japan Garden City spend 1–2 hours traveling to Krishi Market for groceries. Existing apps are slow, expensive, and impersonal. Local shops lack delivery infrastructure.

### Vision

Be the fastest, most trusted grocery delivery for JGC residents — Krishi Market prices, same-day delivery, WhatsApp-native ordering (no app download).

### 90-Day Success Metrics

| Metric | Target |
|--------|--------|
| Active customers | 350 |
| Orders per month | 1,050 |
| On-time delivery | >95% |
| Repeat rate | >40% |
| Net profit | >৳70,000/mo |

## 2. Users

| Persona | Need | Pain point |
|---------|------|------------|
| Busy parent | Quick milk, eggs, vegetables | No time for market trips with children |
| Young professional | Rice, oil, snacks | Shops close early; apps are slow |
| Senior resident | Heavy items (rice, oil) | Cannot carry from market |
| Partner shop | More sales without delivery cost | No tech, no riders |

## 3. MVP Scope

**Not building a native app for MVP.** Channel stack: WhatsApp + web catalog + ops dashboard.

### In scope

| Feature | Description |
|---------|-------------|
| WhatsApp ordering | Customer sends list; operator confirms total |
| 2-slot delivery | Morning (by 12PM) and evening (by 8PM) |
| Web catalog | 65+ SKUs, PWA at [jg-mart.vercel.app](https://jg-mart.vercel.app) |
| COD + bKash | Cash or mobile money on delivery |
| Referral program | ৳100 credit per successful referral |

### Out of scope (MVP)

Mobile app, payment gateway integration, real-time GPS tracking, 1000+ SKUs, 24/7 delivery.

## 4. Technical Direction

| Layer | Current | Target |
|-------|---------|--------|
| Frontend | Vanilla HTML/JS catalog PWA | Same (keep simple) |
| Backend | localStorage (legacy admin) | **Supabase** (PostgreSQL + Auth) |
| Ops | Google Sheets + Python scripts | Supabase + dashboard |
| Comms | WhatsApp Business | WhatsApp Business API (later) |

Schema: `src/web/supabase/schema.sql`

## 5. Operational Workflow

```
Customer (WhatsApp or web catalog)
    → Operator confirms order
    → Split by partner shop
    → Rider pickup from Krishi Market
    → Sort at hub → Deliver in slot
    → Update status + collect payment
```

## 6. Partner Requirements

1. Within 2km of JGC; prefer Krishi Market vendors
2. Confirm orders via WhatsApp within 15 minutes
3. Wholesale + agreed commission pricing
4. Pickup windows: 10:00–11:00 AM and 5:30–6:30 PM

## 7. Risks

| Risk | Mitigation |
|------|------------|
| Partner fails to deliver | Backup shops per category; penalty clause |
| Rider attrition | Dual coverage; per-order bonus |
| Low adoption | Free delivery months 1–3; block-by-block launch |

## 8. Roadmap

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| MVP launch | Weeks 1–4 | 100 customers, 3 partners, 1 rider, Cluster C1 |
| Systemize | Months 2–3 | 3 clusters, delivery fees, part-time ops manager |
| Scale | Months 4–6 | Subscriptions, 6 partners, 2 riders, 550 customers |

## 9. Canonical References

- **Repo index:** `MASTER_INDEX.md`
- **Investor materials:** `src/pitch/`
- **Ops playbooks:** `docs/operations/grok/` (Grok), `docs/operations/kimi/` (Kimi)
- **Brand assets:** `assets/brand/kimi/`
- **Trackers:** `data/trackers/`
