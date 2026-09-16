---
title: "HTTP"
summary: "Why each HTTP version exists: keep alive, multiplexing and QUIC each remove a cost the previous one left on the wire."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "RFC 1945 (HTTP/1.0); RFC 9112 (HTTP/1.1), section 9.3.2 on pipelining"
  - "RFC 9113 (HTTP/2); RFC 7541 (HPACK)"
  - "RFC 9218 (Extensible Priorities); RFC 8297 (103 Early Hints)"
  - "RFC 9000 (QUIC); RFC 9114 (HTTP/3)"
  - "HAProxy, HTTP keep-alive, pipelining, multiplexing and connection pooling"
  - "NGINX, 7 tips for faster HTTP/2 performance; Chrome Developers, Removing HTTP/2 Server Push from Chrome"
tags: [http, http2, http3, quic, multiplexing, head-of-line-blocking]
---
# HTTP

HTTP is a layer 7 protocol. HTTP/1.x and HTTP/2 run over TCP; HTTP/3 runs over QUIC, which runs over UDP. It works in a client-server model and follows the [request-response](https://x.com/kosamari/status/859958929484337152) paradigm. The client sends a request to a server, the server waits till the complete request is received and then replies with a response. The server never starts a message on its own; for the ways round that see [Realtime Web](Realtime%20Web.md).

Each version fixed a cost the previous one left on the wire. One term is needed throughout. **Multiplexing** allows several requests and responses to be sent over a single connection by interleaving them without order dependency i.e. the responses can arrive in a different order to the requests.

## HTTP/1.0

HTTP is a session-less protocol. Each request and response sequence is independent from each other, which means that, on its own, HTTP requires each request to have its own connection. The client establishes a connection, requests an update, gets a response from the server, then closes the connection. Imagine this process being repeated endlessly, by thousands of concurrent users. It is incredibly taxing on the server at scale, and every request pays a TCP handshake before a byte of HTTP moves.

HTTP/1.0 (RFC 1945, 1996) does not support persistent connections by default. To get one the client sends a `Connection: keep-alive` header to indicate to the server that the connection should remain open for any subsequent requests. That is not a hard and fast rule and the server can close the connection after the first response, or any response. The keep-alive mode in HTTP/1.0 is explicit: both the client and server have to announce it. HTTP/1.0 is almost no longer used on the Internet.

## HTTP/1.1

HTTP/1.1 supports persistent connections by default. There is no need to send the `Connection` header to announce support for keep-alive. Each party expects that the peer supports it, although either peer can change this by sending `Connection: close`. A persistent connection can be closed after any full response is sent or after some time when the connection has become idle, to save resources on the server side. [HTTP Keep-Alive](https://www.haproxy.com/blog/http-keep-alive-pipelining-multiplexing-and-connection-pooling/#history-of-keep-alive-in-http) decouples the one-to-one relationship between TCP and HTTP, which is what made HTTP/1.1 scale.

What it did not fix is ordering. Because the connection is persistent, a client can send its next request on the same connection as soon as the previous response has arrived, but only then. **HTTP pipelining** goes one step further: the client sends several requests without waiting for their responses, and the server must return the responses in the same [order](https://www.rfc-editor.org/rfc/rfc9112#section-9.3.2). Either way the connection is ordered and blocking (FIFO), so a slow response holds up everything queued behind it. This is **head-of-line (HOL) blocking**. Pipelining is not used. No browser ships it, and HTTP/2 multiplexing replaced it.

Browsers work round HOL blocking by opening multiple TCP connections in parallel to speed up page loading. Browsers have different limits on maximum concurrent connections per domain but they generally support around 6. Each connection costs a handshake and memory on the server, so fewer connections reused for subsequent requests give better latency and save resources.

### HTTP/1.1 workarounds

With six ordered connections, the number of requests is the bottleneck. So the performance advice for HTTP/1.1 was to make fewer, bigger requests: CSS image sprites (many icons in one image), JS and CSS concatenation (many files in one bundle) and domain sharding (serving assets from `img1.example.com`, `img2.example.com` and so on to get another six connections per hostname).

Under HTTP/2 these [optimisations actually hurt](https://www.f5.com/company/blog/nginx/7-tips-for-faster-http2-performance). Sharding splits requests across several connections, each paying its own TCP and TLS handshake and keeping its own header-compression context, and the server cannot prioritise between requests it does not see together. Sprites and bundles make the browser download bytes the page does not use, and a change to one icon or one function invalidates the cache for the whole bundle. With multiplexing, many small requests on one connection are cheap, so the advice reverses: ship small, cacheable files from one origin.

![Three client-to-server timelines. HTTP/1.1 sends one request and waits for its response before sending the next, so the next request waits behind the previous response (head-of-line blocking). HTTP/2 sends several requests on one TCP connection and the response frames of different streams interleave, but one lost TCP packet stalls all streams. HTTP/3 does the same over independent QUIC streams, so one lost packet stalls only its own stream.](../images/http-multiplexing.drawio.svg "Multiplexing in HTTP/1.1, HTTP/2 and HTTP/3")

## HTTP/2

Built on Google's SPDY protocol. First standardised as RFC 7540 (2015), revised as RFC 9113 (2022). [Supported](https://caniuse.com/http2) by all major browsers.

* **Multiplexing over one TCP connection.** HTTP/2 splits each request and response into frames tagged with a stream ID, so many streams interleave on one connection and the responses can complete in any order. That removes HTTP-level HOL blocking and significantly reduces the number of connections and latency between clients and servers. Connections must persist: the `Connection` header and other hop-by-hop headers are forbidden.

* **Binary framing.** HTTP/1.x is textual; HTTP/2 is binary. Frames are unambiguous to parse and cheap to interleave. The inconvenience is that humans can no longer read the wire for debugging without a tool.

* **Header compression.** Headers are compressed with HPACK, which keeps a table of headers already sent on the connection and sends an index instead of repeating them. Cookies and user-agent strings repeat on every request, so the bandwidth saving is considerable and offsets the minor increase in CPU load.

* **Prioritisation.** Clients can indicate the order in which they want to receive resources, so a browser can ask for the CSS that blocks rendering before the images below the fold. RFC 9113 deprecated the original stream-dependency priority scheme, which servers made little use of. RFC 9218 (Extensible Priorities) replaces it with a simple urgency header for both HTTP/2 and HTTP/3.

* **TLS, effectively required.** HTTP/2 did not change the security requirements of HTTP, but browsers only speak HTTP/2 over TLS (negotiated with ALPN), which makes TLS mandatory for all intents and purposes.

* **Server Push, now historical.** HTTP/2 let the server send resources to the browser cache before they were requested. Pushed resources were only processed by the browser and never reached application code, so this was never a channel for application messages (see [Realtime Web](Realtime%20Web.md)). Servers rarely guessed better than the browser. Chrome 106 disabled it in 2022 and Firefox 132 removed it in 2024. The `103 Early Hints` status (RFC 8297) is the replacement: the server tells the browser what to preload while it is still building the real response, and the browser decides.

What HTTP/2 could not fix is TCP. TCP delivers bytes in order, so when one packet is lost every stream on the connection waits for the retransmission, even streams whose packets all arrived. HOL blocking moved down a layer rather than disappearing. On a lossy link one HTTP/2 connection can be slower than six HTTP/1.1 connections, because a loss on one of the six stalls only that one.

## HTTP/3

HTTP/3 (RFC 9114, 2022) runs over QUIC (RFC 9000, 2021) instead of TCP. QUIC moves multiplexing to the transport protocol i.e. the reliability of receiving HTTP/3 frames for the right resources in the right order is moved down into the transport and leaves UDP just for the packetisation, therefore simplifying HTTP. Because each QUIC stream is delivered independently, a lost packet only stalls the stream it belongs to. This removes the head-of-line blocking across streams that HTTP/2 still has on a single TCP connection.

QUIC also builds in TLS 1.3, so HTTP/3 is always encrypted and the transport and TLS handshakes are one round trip instead of two. It supports 0-RTT connection resumption, where a client returning to a server sends its first request in the first packet. QUIC runs over UDP rather than as a new transport because routers, firewalls and operating systems already pass UDP; a new transport would have taken decades to deploy.

![Three protocol stacks side by side. HTTP/1.1 over optional TLS over TCP over IP, using several TCP connections. HTTP/2 over TLS (effectively required) over TCP over IP, using one TCP connection with many streams. HTTP/3 over QUIC with TLS 1.3 built in, over UDP over IP, using one QUIC connection with independent streams.](../images/http-protocol-stacks.drawio.svg "HTTP protocol stacks")

## How to rederive this

- Start from the cost: a TCP handshake per request. Keep-alive removes it; that is HTTP/1.0 to 1.1.
- A single ordered connection queues; six connections are a workaround, not a fix. Sprites, bundles and sharding exist only to reduce requests on ordered connections.
- Interleave frames tagged by stream and the queue disappears; that is HTTP/2, and it makes the workarounds harmful.
- TCP still delivers in order, so loss stalls every stream. Put the streams in the transport and encrypt from the first packet; that is QUIC and HTTP/3.
- Anything the server sends unasked is either a cache hint (Push, Early Hints) or needs a different transport (Realtime Web).

## Sources

- RFC 1945 (HTTP/1.0): https://www.rfc-editor.org/rfc/rfc1945
- RFC 9112 (HTTP/1.1), section 9.3.2 on pipelining: https://www.rfc-editor.org/rfc/rfc9112
- RFC 9113 (HTTP/2) and RFC 7541 (HPACK): https://www.rfc-editor.org/rfc/rfc9113 and https://www.rfc-editor.org/rfc/rfc7541
- RFC 9218 (Extensible Priorities): https://www.rfc-editor.org/rfc/rfc9218
- RFC 8297 (103 Early Hints): https://www.rfc-editor.org/rfc/rfc8297
- RFC 9000 (QUIC) and RFC 9114 (HTTP/3): https://www.rfc-editor.org/rfc/rfc9000 and https://www.rfc-editor.org/rfc/rfc9114
- HAProxy, HTTP keep-alive, pipelining, multiplexing and connection pooling (source of the persistent-connections explanation): https://www.haproxy.com/blog/http-keep-alive-pipelining-multiplexing-and-connection-pooling/
- NGINX, 7 tips for faster HTTP/2 performance: https://www.f5.com/company/blog/nginx/7-tips-for-faster-http2-performance
- Chrome Developers, Removing HTTP/2 Server Push from Chrome: https://developer.chrome.com/blog/removing-push
