---
title: "HTTP Caching"
summary: "What Cache-Control, ETag and Vary tell browsers and proxies, and when authenticated responses may be cached."
kind: concept
status: current
last_reviewed: 2026-09-16
sources: []
tags: [http, caching, cache-control, etag, reverse-proxy]
---
# HTTP Caching

[HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching) can be done in the browser/client, at the reverse proxy/CDN or at the origin/server. It supports a bunch of headers:

* [Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
  * `public` means the response may be stored by any cache, shared or private, even if the request carried an `Authorization` header. A proxy will not cache a resource if it is marked as `private`, the resource could be specific to a user and is only meant to be cached at the client.
  * `no-cache` option doesn't mean the cache wouldn't store the resource, it can. It just implies that the proxy should verify with the server each time the resource is requested whether the resource is still valid. The server can use an **ETag**, which identifies one representation (version) of the resource (e.g. by performing a hash), or **Last-Modified** to check if the resource has changed.
  * `no-store` option will prevent resources from being stored by the cache at all.
  * `must-revalidate` means that once the response is stale, a cache must revalidate it with the origin before reusing it. It may not serve the stale copy if the origin is unreachable (no stale-on-error). Fresh responses are served as normal. See [RFC 9111 section 5.2.2.2](https://www.rfc-editor.org/rfc/rfc9111#section-5.2.2.2).
  * `proxy-revalidate` Like `must-revalidate`, but only for shared caches (e.g., proxies). Ignored by private caches.
  * `max-age` the resource can be cached for the specified duration in seconds. This works well for independent resources but for mutable content with dependencies [max-age is the wrong choice](https://jakearchibald.com/2016/caching-best-practices/) as it can lead to the inter dependent resources getting out of sync.
* Responses to requests with `Authorization` header are automatically private, and aren't generally cached by shared/public caches e.g. reverse proxies
* `Vary` - Specifies a header value that can be different for different requests. When a cache receives a request that has a `Vary` header field, it must not use a cached response by default unless all header fields specified in the Vary header match in both the original (cached) request and the new request. For example
  * `Vary: Accept-Encoding` specifies `Accept-Encoding` value can be different for different requests e.g. `Accept-Encoding: gzip, deflate, br` A server can set `Vary: Accept-Encoding` to ensure that a separate version of a resource is cached for all requests that specify support for a particular set of encodings. You may want to allow a resource to be cached in uncompressed and (various) compressed forms, and served appropriately to user agents based on the encodings that they support.
  * `Vary: User-Agent` specifies `User-Agent` value can be different for mobile and desktop clients. This can be used for serving different content to desktop and mobile users, but it is widely discouraged: there are so many distinct User-Agent strings that the cache hit rate collapses. Normalise the User-Agent at the edge or use client hints instead.

A cache revalidates a stored response with a **conditional request**. It sends `If-None-Match` with the stored ETag, or `If-Modified-Since` with the stored Last-Modified date. If the representation has not changed, the origin answers `304 Not Modified` with no body and the cache keeps serving its copy. A strong ETag changes whenever the bytes change. A weak ETag (prefixed `W/`) only changes when the meaning changes, so it works for `If-None-Match` but not for byte-range requests.

## Types of Cacheable content

Reverse proxies are great at caching static content like video, images, CSS, HTML, JS - all the big files that do not change often and only between releases.

Caching API data that is continuosuly being updated in the backend especially if it is a big payload for even a short amount of time for high amounts of load can have a significant change in performance. It’s perfectly fine to serve a slightly stale response for content that doesn’t change extremely often, such as daily news feeds, product descriptions, reviews, and comment boards. Even caching this content for five or ten seconds could have a worthwhile impact, depending on the number of users viewing that same data. Caching for a very short period of time is known as **microcaching**.

Caching content at the reverse proxy that is unique to a user, such as API keys, user profile data etc is not advisable because it is meant for that user and only ever going to be requested for that specific user.

| Content | Examples | Cacheability |
|---|---|---|
| Static | Images, CSS, simple HTML | Easy to cache |
| Dynamic | Blog posts, status pages, some API data | Micro-cacheable for seconds |
| User-specific | Shopping cart, account data | Do not cache at shared caches |

### Caching authenticated requests

The rules for caching authenticated responses can be [tricky](https://stackoverflow.com/questions/39060208/authorization-check-for-http-caches). Section 3.5 of [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111#section-3.5) talks about the conditions under which shared caches can store and reuse such responses. They can be cached only when one of the following Cache-Control headers is present: `s-maxage`, `must-revalidate` or `public`.

The default behavior for responses that require authentication is to not be cached by shared proxies. No header is needed for this; it is what happens when none of the three directives above is present.

If you want to override this behavior you can ignore certain Cache-Control headers from the origin server and set your own Cache-Control header before sending the response. This will depend upon the sensitivity of the data, e.g. if you simply use expiration caching with `public` modifier, you run the risk of storing the data specific to a user in a public cache. This may still be okay as long as the request is being validated and authorized by the origin server.

Either of these works:

```http
Cache-Control: public, no-cache
Cache-Control: public, proxy-revalidate
```
