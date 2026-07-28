# API Integration Guide

## Overview
JG Mart exposes integration points via WhatsApp Business API, JSON data exports, and webhook-style file drops. This document describes how to connect external systems.

## 1. WhatsApp Business API

### Inbound (Customer → Platform)
- **Format:** WhatsApp Cloud API webhook
- **Payload:** JSON with `from`, `type`, `text.body`
- **Action:** Route to order intake or support flow

### Outbound (Platform → Customer)
- **Template Messages:** Pre-approved for order confirmations, delivery alerts, promos
- **Session Messages:** Free-form within 24-hour customer window
- **Media:** Product images, invoices, maps

### Configuration
```json
{
  "phone_number_id": "YOUR_PHONE_NUMBER_ID",
  "access_token": "YOUR_ACCESS_TOKEN",
  "verify_token": "YOUR_VERIFY_TOKEN",
  "webhook_url": "https://your-domain.com/webhook/whatsapp"
}
```

## 2. Data Export API

### Endpoint
`POST /api/v1/export`

### Request
```json
{
  "type": "orders|finance|analytics",
  "date_from": "2026-07-01",
  "date_to": "2026-07-31",
  "format": "json|csv"
}
```

### Response
```json
{
  "status": "success",
  "download_url": "https://storage.googleapis.com/...",
  "records": 1247,
  "generated_at": "2026-07-31T23:59:00Z"
}
```

## 3. Webhook Drop (Legacy)
- `09_Data_Export/sync_out/` is the legacy drop zone
- New system should poll or receive via webhook instead
- Transition plan: keep both for 30 days, then decommission

## 4. Integration Checklist
- [ ] WhatsApp Business account approved
- [ ] Phone number ID configured
- [ ] Webhook endpoint deployed with HTTPS
- [ ] Verify token set in both Meta and platform
- [ ] Template messages submitted and approved
- [ ] Fallback SMS provider configured (Twilio / MSG91)

## 5. Testing
- Use Meta WhatsApp Cloud API Sandbox
- Test with `validate_toolkit.py` → WhatsApp connectivity check
- Monitor delivery receipts in dashboard

---

*For implementation details, see `src/scripts/automation/` scripts.*
