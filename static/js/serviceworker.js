self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('hangarin-cache-v2').then(function(cache) {
            return cache.addAll([
                '/',
                '/manifest.json',
                '/static/css/style.css',
                '/static/js/theme.js',
                '/static/img/icon-192.png',
                '/static/img/icon-512.png',
                '/static/images/avatar.png',
            ]);
        })
    );
});

self.addEventListener('fetch', function(e) {
    e.respondWith(
        caches.match(e.request).then(function(response) {
            return response || fetch(e.request);
        })
    );
});