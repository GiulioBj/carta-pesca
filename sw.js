/* Carta di pesca - Copyright (c) 2026 Giulio Bojan (GiulioBj). Tutti i diritti riservati. Vedi il file LICENSE. */
/* Rete prima di tutto, così la pagina è sempre l'ultima pubblicata; senza rete uso la copia salvata dei file del sito. */
const CACHE='cartapesca-v1';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['./','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png'])).catch(()=>{}))});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  const r=e.request;
  if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
  e.respondWith(fetch(r).then(res=>{if(res.ok){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp))}return res}).catch(()=>caches.match(r,{ignoreSearch:true}).then(m=>m||Response.error())));
});
