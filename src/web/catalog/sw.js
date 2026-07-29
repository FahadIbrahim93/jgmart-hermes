const CACHE = 'jgmart-v5';
const FILES = [
  './',
  './index.html',
  './landing.html',
  './menu.html',
  './track.html',
  './zone.html',
  './myorders.html',
  './admin.html',
  './manifest.html',
  './healthcheck.html',
  './notify.html',
  './rider.html',
  './offline.html',
  './csp-report.html',
  './404.html',
  './manifest.json',
  './favicon.svg',
  './catalog_data.json',
  './supabase/config.js',
  './defaults.js',
  './security.js',
  './catalog-init.js',
  './db.js',
  './offline-queue.js',
  './data-store.js',
  './sw.js',
  './images/placeholder.svg',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(FILES))
      .then(() => self.skipWaiting())
      .catch(err => console.warn('SW install failed:', err))
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;

  // Skip non-GET requests
  if(req.method !== 'GET') return;

  // Skip cross-origin requests (except fonts, wa.me, and Supabase)
  if(req.url.includes('http') && !req.url.includes('fonts.googleapis.com') && !req.url.includes('wa.me') && !req.url.includes('supabase.co')) {
    return;
  }

  e.respondWith(
    caches.match(req).then(cached => {
      const fetchPromise = fetch(req).then(res => {
        // Cache successful responses
        if(res && res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(req, clone));
        }
        return res;
      }).catch(() => {
        // Return cached version if network fails
        if(cached) return cached;

        // Special handling for navigation requests
        if(req.mode === 'navigate') {
          return caches.match('./offline.html');
        }

        // Return placeholder for images
        if(req.url.match(/\.(jpg|jpeg|png|gif|svg|webp)$/)) {
          return caches.match('./images/placeholder.svg');
        }

        return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
      });

      return cached || fetchPromise;
    })
  );
});

// Listen for skip waiting message
self.addEventListener('message', e => {
  if(e.data && e.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});
