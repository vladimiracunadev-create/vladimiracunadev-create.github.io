const CACHE_NAME = 'vladi-portfolio-v4';
const OFFLINE_URL = './offline.html';

const APP_SHELL = [
    './',
    './index.html',
    './offline.html',
    './manifest.webmanifest',
    './assets/favicon.svg',
    './assets/icons/icon.svg'
];

const NETWORK_FIRST_PATHS = new Set([
    '/',
    '/index.html',
    '/styles.css',
    '/app.js',
    '/pwa.js',
    '/manifest.webmanifest'
]);

function toRelativePath(url) {
    const parsed = new URL(url);
    let pathname = parsed.pathname || '/';

    if (pathname === '') {
        pathname = '/';
    }

    return pathname;
}

async function networkFirst(request, fallbackUrl) {
    const cache = await caches.open(CACHE_NAME);

    try {
        const response = await fetch(request);
        if (response && response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cached = await cache.match(request);
        if (cached) {
            return cached;
        }

        if (fallbackUrl) {
            const offline = await cache.match(fallbackUrl);
            if (offline) {
                return offline;
            }
        }

        throw error;
    }
}

async function cacheFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    if (cached) {
        return cached;
    }

    const response = await fetch(request);
    if (response && response.ok) {
        cache.put(request, response.clone());
    }
    return response;
}

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') {
        return;
    }

    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) {
        return;
    }

    const relativePath = toRelativePath(event.request.url);

    if (event.request.mode === 'navigate') {
        event.respondWith(networkFirst(event.request, OFFLINE_URL));
        return;
    }

    if (NETWORK_FIRST_PATHS.has(relativePath)) {
        event.respondWith(networkFirst(event.request));
        return;
    }

    event.respondWith(cacheFirst(event.request));
});
