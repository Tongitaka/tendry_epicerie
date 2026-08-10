const CACHE_NAME = 'tendry-v5';
const ASSETS = [
  './',
  './index.html',
  './html5-qrcode.min.js',
  './chart.js'
];

// Fametrahana ireo rakitra ao anaty cache
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

// Fanadiovana ny cache taloha rehefa misy version vaovao (manova finday/mise à jour)
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fampiasana ny cache rehefa offline
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});
