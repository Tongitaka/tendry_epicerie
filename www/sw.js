const CACHE_NAME = 'tendry-v2';
const ASSETS = [
  './',
  './index.html',
  './html5-qrcode.min.js',
  './chart.js'
];

// Fametrahana ireo rakitra ao anaty cache
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

// Fampiasana ny cache rehefa offline
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => res || fetch(e.request))
  );
});