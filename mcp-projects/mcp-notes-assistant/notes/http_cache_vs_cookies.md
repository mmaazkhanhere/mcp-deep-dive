---
title: HTTP — Cache vs Cookies
tags: [http, web, caching, cookies]
created: 2025-09-02
updated: 2025-09-02
---

# HTTP — Cache vs Cookies

**Cache**: stores _responses_ to avoid refetching (performance).

- Controlled by headers: `Cache-Control`, `ETag`, `Last-Modified`.

**Cookies**: store small _key-value_ data for the browser (state).

- Sent with requests to the same origin (or allowed scope).
- Used for sessions, prefs, CSRF tokens (carefully).

**Rule of thumb**: cache = **resource reuse**; cookies = **client state**.
