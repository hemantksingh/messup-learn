# Browser Security Model

A page can send a request almost anywhere and embed almost anything, but it can only read what came from its own origin. That is the same-origin policy. Cookies are older and looser: the browser attaches them to every request that matches their host and path, whoever started it. Web Storage is newer and locked to the origin.

## Origins and sites

An **origin** is scheme + host + port. `https://mybank.com`, `http://mybank.com`, `https://mybank.com:8443` and `https://login.mybank.com` are four origins.

A **site** is the registrable domain, eTLD+1. `login.mybank.com` and `cdn.mybank.com` are one site. The public suffix list decides what counts as a TLD, so `alice.github.io` and `bob.github.io` are different sites. Current browsers also compare the scheme.

The same-origin policy and Web Storage are origin-scoped. Cookie `Domain` and `SameSite` are site-scoped. Cookies ignore the port.

## The same-origin policy

JavaScript on one page may read another page or response only if both have the same origin. Code from `https://mybank.com` may read `https://mybank.com`'s data; `https://evil.example.com` never may.

The policy **restricts reading cross-origin responses, not embedding them**. Images, stylesheets and scripts load across origins through their tags (fonts excepted), but the page cannot read them: a cross-origin `<script>` runs with its source opaque, and a cross-origin image displays but taints any canvas it is drawn into. A cross-origin `fetch()` is sent, but the response is withheld unless the server opts in.

Those requests still carry the user's cookies for the target site. That is the basis of [Cross Site Request Forgery](Cross%20Site%20Request%20Forgery.md): the attacker only needs the authenticated request to happen, not to read the response.

## CORS relaxes it

The server that owns a response decides who may read it. The browser adds an `Origin` request header; the server answers with `Access-Control-Allow-Origin` naming the origins allowed to read.

```http
Access-Control-Allow-Origin: *                    # any origin may read; not allowed with credentials
Access-Control-Allow-Origin: https://foo.example   # only this origin may read
Access-Control-Allow-Credentials: true             # allow the read when cookies were sent
Access-Control-Allow-Methods: POST, GET, OPTIONS   # methods permitted
Access-Control-Allow-Headers: X-PINGOTHER, Content-Type
Access-Control-Max-Age: 86400                      # preflight cache time
```

For anything a plain form could not send (a method other than GET, HEAD or POST, a header outside the safelist, a Content-Type other than form encodings or `text/plain`) the browser first sends a **preflight**: an `OPTIONS` request with `Access-Control-Request-Method` and `Access-Control-Request-Headers`, and sends the real request only if the answer permits it. A form POST with cookies never preflights.

CSP and the same-origin policy sit at opposite ends of a request. If `foo.com` wants to talk to `bar.com`:

1. The `foo.com` response may carry a Content-Security-Policy that stops the page issuing the request at all.
2. If not, the request goes to `bar.com` with whatever `bar.com` cookies the browser holds.
3. `bar.com` responds. The same-origin policy stops `foo.com` reading it unless `Access-Control-Allow-Origin` names `foo.com`.

COOP, COEP and CORP are in [Security Headers](Security%20Headers.md).

## Cookies

HTTP is stateless. A cookie is a small piece of data the server hands the browser, returned on later requests, so the server can tell two requests came from the same browser. Uses: session management (logins, shopping carts), personalisation, tracking.

### Set-Cookie

```http
Set-Cookie: <name>=<value>[; Expires=<date>][; Max-Age=<seconds>][; Domain=<domain>][; Path=<path>][; Secure][; HttpOnly][; SameSite=Strict|Lax|None][; Partitioned]
```

- `Expires` or `Max-Age`: without either, the cookie lasts the browser session. `Max-Age` wins if both are present.
- `Domain`: absent, the cookie is host-only. `Domain=mybank.com` sends it to that host and every subdomain. A server can only name itself or a parent within its site.
- `Path`: the URL prefix it is returned to. Not a security boundary.
- `Secure`: sent only over HTTPS. An HTTP page cannot set or overwrite it.
- `HttpOnly`: hidden from `document.cookie`, so script injected by XSS cannot read it.
- `SameSite`: below.
- `Partitioned`: also keyed by the top-level site, so an embed gets a separate jar per embedding site.

The `Cookie` request header carries only `name=value`, no attributes.

### Limits

RFC 6265 requires at least 50 cookies per domain and at least 4096 bytes per cookie. The 4 KB is per cookie, not the whole jar. An oversize `Set-Cookie` is rejected, not truncated. Current browsers cap around 150 to 180 per domain. Store an identifier in the cookie and the data on the server.

### SameSite

- `Strict`: never on a cross-site request. Arriving from an email link, the user appears logged out.
- `Lax`: on top-level navigations with a safe method (a GET link or redirect). Not on cross-site subresources, iframes or POSTs, so the classic CSRF form post fails.
- `None`: everywhere. Only accepted with `Secure`.

Chromium has treated an unlabelled cookie as `Lax` since Chrome 80 (February 2020). For two minutes after it is set, an unlabelled cookie is also sent on top-level cross-site POSTs (the "Lax+POST" exception). Firefox and Safari do not default to Lax. Set the attribute explicitly.

Two gaps in `Lax`. A request from a compromised `cdn.mybank.com` to `login.mybank.com` is same-site and carries the cookie. Any state change reachable by a top-level GET is still forgeable.

### Prefixes and cookie tossing

`Domain` is site-wide and the `Cookie` header has no attributes. So a page on a forgotten `evil.mybank.com` can set `session=attacker; Domain=mybank.com`, and the browser sends it to `login.mybank.com` alongside, or instead of, the real cookie. The server cannot tell them apart. This is cookie tossing.

A cookie named `__Host-session` is only accepted with `Secure`, `Path=/` and no `Domain`, so it is host-only by construction and a subdomain cannot plant it. `__Secure-` only requires `Secure`; it stops an HTTP page overwriting the cookie but not tossing.

### Session fixation

Tossing is one way to plant a session id before the victim logs in. Session fixation is the general attack: the attacker plants an id they know, the victim logs in, and the server binds the identity to that id. Fix: issue a fresh session id at login and at any privilege change, and never accept an id the server did not generate.

## Third-party cookies today

A cookie is third-party when it belongs to a site other than the one in the address bar. An advertiser's script embedded on many sites gets its own cookie back from each and knows which URL you are on. It cannot read the embedding site's cookies, but its own are enough to follow you across sites.

Safari has blocked third-party cookies since 2020 (Intelligent Tracking Prevention). Firefox has partitioned them since 2022 (Total Cookie Protection): a different jar on every site. Chrome ran a one per cent deprecation trial in January 2024, switched to a user-choice plan in July 2024, and dropped that too in April 2025. It offers opt-in partitioning via `Partitioned` (CHIPS) and the Storage Access API, which lets an embed ask for its cookies.

## Web Storage

`localStorage` and `sessionStorage` are key-value stores scoped to the origin, not the domain: `https://mybank.com` and `https://login.mybank.com` have separate stores.

There is no `HttpOnly` for storage. Any script on the origin reads all of it, so a [Cross Site Scripting](Cross%20Site%20Scripting.md) payload lifts a token from `localStorage` in one line.

| | Cookies | localStorage |
|---|---|---|
| Scope | Host or site (`Domain`), port ignored | Origin (scheme, host, port) |
| Size | About 4 KB per cookie | Roughly 5 to 10 MB per origin |
| Sent to the server | On every matching request | Never |
| Expiry | Session, or `Expires` / `Max-Age` | Until cleared; `sessionStorage` per tab |
| Script access | Unless `HttpOnly` | Always |

The deciding question is who needs the data. A session identifier is for the server: an `HttpOnly`, `Secure`, `SameSite` cookie. A UI preference is for the client: storage.

## How to rederive this

- Which principal is the rule about: origin (same-origin policy, Web Storage) or site (`Domain`, `SameSite`)?
- Reading or sending? The same-origin policy blocks reads and CORS unblocks them. Cookies are about sending; only `SameSite` limits that.
- CSRF: sending is allowed and cookies ride along. XSS token theft: any script on the origin reads its storage.
- Cookie tossing: `Domain` is site-wide and the `Cookie` header has no attributes. `__Host-` restores the origin boundary.

## Sources

- MDN: Same-origin policy, CORS, HTTP cookies, Web Storage API.
- RFC 6265 and the RFC 6265bis draft.
- web.dev: "SameSite cookies explained", "Schemeful Same-Site".
- Chrome Privacy Sandbox announcements, July 2024 and April 2025.
- OWASP Session Management Cheat Sheet.
