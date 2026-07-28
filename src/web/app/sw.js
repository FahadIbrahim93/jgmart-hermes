/**
 * JG Mart — Service Worker
 * =========================
 * 
 * NOTE: Service workers ONLY register on pages served over HTTPS (or localhost).
 * They DO NOT work with file:// protocol. This file is ready for deployment
 * to Vercel, Netlify, or any HTTPS host. When testing locally, use:
 *   - npx serve .        (serves on http://localhost:3000)
 *   - python -m http.server 8080
 *   - Vercel/Netlify dev server
 * 
 * Cache version: sw_v1 — bump to sw_v2, sw_v3 etc to force a full refresh.
 */

const CACHE_VERSION = 'sw_v1';
const STATIC_CACHE = `jgmart-static-${CACHE_VERSION}`;
const OFFLINE_URL = 'offline.html';

// ─── PRE-CACHE MANIFEST (installed on activation) ───────────────────────────
const PRE_CACHE_FILES = [
  // Root HTML pages
  'index.html',
  'ops.html',
  'data.html',
  'field_ops.html',
  'start.html',
  'health.html',
  // Core CSS
  'theme.css',
  // 05_Tech_Dashboard HTML pages
  '05_Tech_Dashboard/index.html',
  '05_Tech_Dashboard/analytics.html',
  '05_Tech_Dashboard/backup.html',
  '05_Tech_Dashboard/commlog.html',
  '05_Tech_Dashboard/dailypnl.html',
  '05_Tech_Dashboard/finance.html',
  '05_Tech_Dashboard/orders.html',
  // 06_Web_Catalog HTML pages
  '06_Web_Catalog/index.html',
  '06_Web_Catalog/order_intake.html',
  // PWA assets
  'manifest.json',
  'offline.html',
  'favicon.svg',
  '02_Brand_Assets/logo_icon.svg'
];

// ─── STATIC FILE EXTENSIONS (cache-first strategy) ──────────────────────────
const STATIC_EXTENSIONS = [
  '.html', '.css', '.js', '.json',
  '.svg', '.txt', '.csv', '.xlsx',
  '.py', '.bat'
];

// ─── API ROUTE PATTERNS (network-first strategy — placeholder for future use)
const API_PATTERNS = [
  /\/api\//,
  /\/api\./,
  /\.json$/ // treat JSON data files as API-like when they're dynamic
];

/* ═══════════════════════════════════════════════════════════════════════════
   INSTALL — Pre-cache critical files & activate immediately
   ═══════════════════════════════════════════════════════════════════════════ */
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker v1');

  // Skip waiting — activate immediately so new SW takes over right away
  self.skipWaiting();

  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Pre-caching critical files');
        return cache.addAll(PRE_CACHE_FILES).catch((err) => {
          // Some files may 404 if the project directory structure doesn't
          // include all expected files yet — that's non-fatal.
          console.warn('[SW] Pre-cache warning (non-fatal):', err.message);
        });
      })
  );
});

/* ═══════════════════════════════════════════════════════════════════════════
   ACTIVATE — Clean up old caches
   ═══════════════════════════════════════════════════════════════════════════ */
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker v1');

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => {
            // Delete any cache not matching the current version
            return name.startsWith('jgmart-') && name !== STATIC_CACHE;
          })
          .map((name) => {
            console.log('[SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    }).then(() => {
      // Take control of all pages immediately
      return self.clients.claim();
    })
  );
});

/* ═══════════════════════════════════════════════════════════════════════════
   FETCH — Determine strategy: Cache-first vs Network-first
   ═══════════════════════════════════════════════════════════════════════════ */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle requests from our own origin
  if (url.origin !== self.location.origin) {
    return;
  }

  const pathname = url.pathname;

  // ── API / dynamic requests: Network-first ──
  if (isApiRequest(request, pathname)) {
    event.respondWith(networkFirstWithFallback(request, pathname));
    return;
  }

  // ── Static assets: Cache-first ──
  if (isStaticAsset(request, pathname)) {
    event.respondWith(cacheFirstWithFallback(request, pathname));
    return;
  }

  // ── Navigation requests (HTML pages): Cache-first, fallback to offline page
  if (request.mode === 'navigate') {
    event.respondWith(navigationStrategy(request));
    return;
  }

  // ── Everything else: Network-only with optional caching ──
  event.respondWith(networkOnly(request));
});

/* ═══════════════════════════════════════════════════════════════════════════
   STRATEGY IMPLEMENTATIONS
   ═══════════════════════════════════════════════════════════════════════════ */

/**
 * Cache-first: Serve from cache if available, else fetch & cache.
 * Ideal for static assets that rarely change between versions.
 */
async function cacheFirstWithFallback(request, pathname) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    // Network failed — try to serve offline fallback for HTML, or just fail
    if (request.mode === 'navigate' || pathname.endsWith('.html')) {
      return caches.match(OFFLINE_URL);
    }
    // For non-HTML static assets that aren't cached, we can't help
    return new Response('Offline', { status: 503 });
  }
}

/**
 * Network-first: Try the network, fall back to cache, then offline page.
 * Used for API calls and dynamic data.
 */
async function networkFirstWithFallback(request, pathname) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    const cached = await caches.match(request);
    if (cached) {
      return cached;
    }
    // If it's a navigation request underneath, show offline page
    if (request.mode === 'navigate' || pathname.endsWith('.html')) {
      return caches.match(OFFLINE_URL);
    }
    return new Response(JSON.stringify({ error: 'offline' }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

/**
 * Navigation strategy: Cache-first for HTML pages, offline fallback.
 */
async function navigationStrategy(request) {
  const cached = await caches.match(request);
  if (cached) {
    return cached;
  }

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, response.clone());
    }
    return response;
  } catch (err) {
    return caches.match(OFFLINE_URL);
  }
}

/**
 * Network-only: No caching, no fallback.
 */
async function networkOnly(request) {
  try {
    return await fetch(request);
  } catch (err) {
    return new Response('Offline', { status: 503 });
  }
}

/* ═══════════════════════════════════════════════════════════════════════════
   HELPER FUNCTIONS
   ═══════════════════════════════════════════════════════════════════════════ */

function isStaticAsset(request, pathname) {
  // Check by file extension
  const ext = pathname.substring(pathname.lastIndexOf('.')).toLowerCase();
  if (STATIC_EXTENSIONS.includes(ext)) {
    return true;
  }
  return false;
}

function isApiRequest(request, pathname) {
  // Check if URL matches any API pattern
  for (const pattern of API_PATTERNS) {
    if (pattern.test(pathname)) {
      return true;
    }
  }
  return false;
}

/* ═══════════════════════════════════════════════════════════════════════════
   MESSAGE HANDLER — Allows runtime cache clearing from the page
   ═══════════════════════════════════════════════════════════════════════════ */
self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'clearCache') {
    caches.delete(STATIC_CACHE).then(() => {
      console.log('[SW] Cache cleared by user action');
      if (event.ports && event.ports[0]) {
        event.ports[0].postMessage({ status: 'done' });
      }
    });
  }
});
