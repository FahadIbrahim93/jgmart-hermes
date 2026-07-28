const CACHE = 'jgmart-v1';
const FILES = [
  './',
  './index.html',
  './manifest.json',
  './favicon.svg',
  './landing.html',
  './menu.html',
  './track.html',
  './zone.html',
  './images/placeholder.svg',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      if(e.request.url.match(/\.(jpg|svg|png|css|js|json)$/)){
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
      }
      return res;
    }).catch(() => caches.match('./offline.html')))
  );
});
