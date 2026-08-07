# JG Mart — Wiki

Reference documentation for the JG Mart codebase.

## Overview

JG Mart is a static, single-page progressive web app (PWA) for hyperlocal grocery delivery in Japan Garden City, Dhaka. It has no server — the frontend is a collection of vanilla HTML/CSS/JS files deployed to Vercel, with Supabase (PostgreSQL + Auth) as the backend.

## Contents

- [Architecture](architecture.md) — system architecture, data flow, key design decisions.
- [Getting Started](getting-started.md) — setup, first run, common workflows.
- [Modules](modules/) — per-module deep-dives.

## Module Map

| Module | Purpose |
|---|---|
| [`catalog`](modules/catalog.md) | Catalog pages, product display, cart UI |
| [`orders`](modules/orders.md) | Order submission, tracking, offline queue |
| [`admin`](modules/admin.md) | Admin panel, auth, order management |
| [`data`](modules/data.md) | Supabase integration, data models, RLS |
| [`pwa`](modules/pwa.md) | Service worker, offline caching, manifest |
| [`security`](modules/security.md) | Sanitization, validation, CSP, auth |

## Definitive Audit

See [docs/product/definitive-audit-report.md](../product/definitive-audit-report.md) for the current state of the codebase, scored dimensions, and prioritized remediation plan.