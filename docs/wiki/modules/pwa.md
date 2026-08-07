# Module: PWA

The PWA module provides offline caching, the service worker, and the app manifest.

## Responsibilities

- Cache catalog pages and assets for offline access.
- Serve cached pages when the network is unavailable.
- Provide the app manifest for installability.
- Manage cache versioning and updates.

## Key Files

- [`src/web/catalog/sw.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/sw.js) — service worker (cache version `jgmart-v6`).
- [`src/web/catalog/manifest.json`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/manifest.json) — app manifest.
- [`src/web/catalog/offline.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/offline.html) — offline fallback page.
- [`src/web/catalog/offline-queue.js`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/offline-queue.js) — offline order queue.
- [`src/web/catalog/manifest.html`](https://github.com/FahadIbrahim93/jgmart-hermes/blob/main/src/web/catalog/manifest.html) — manifest page.

## Public API

- `JG_DATA_STORE` (from `data-store.js`) — `clearAll()` for cache/data reset.

## Internal Structure

The service worker caches the catalog pages, assets, and the `catalog_data.json` file. On fetch, it serves the cached version first, then attempts a network fetch to update the cache. If the network fails, it returns the cached page (or `offline.html` for navigation requests). Cache version is `jgmart-v6`.

The offline queue (`offline-queue.js`) stores orders in localStorage when the network is down and replays them when it returns.

## Dependencies

- **Used by:** all catalog pages (via the service worker).
- **Uses:** `data-store.js` (localStorage), `db.js` (order submission).

## Notable Patterns / Gotchas

- **Cache versioning.** The cache is named `jgmart-v6`; updating `sw.js` requires bumping this version to force a cache update.
- **Offline order queue.** Orders are queued in localStorage when the network is down and replayed when it returns.
- **No service worker registration shown.** The SW is listed in the cache but registration (via `navigator.serviceWorker.register`) must be in the page JS — verify it's present in `index.html`.