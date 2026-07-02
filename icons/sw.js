const CACHE = 'adbmanager-v1';
const ASSETS = [
  '/autodefesa-painel-2/',
  '/autodefesa-painel-2/index.html',
  '/autodefesa-painel-2/painel_os.html',
  '/autodefesa-painel-2/painel_pagamentos.html',
  '/autodefesa-painel-2/painel_indisponibilidade.html',
  '/autodefesa-painel-2/painel_faturamento.html',
  '/autodefesa-painel-2/icons/icon-192.png',
  '/autodefesa-painel-2/icons/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
