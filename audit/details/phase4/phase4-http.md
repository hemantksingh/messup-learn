# Phase 4 report: split HTTP.md into HTTP.md and Realtime Web.md

Files edited (not committed):

- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/web and apis/HTTP.md (rewritten in place)
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/web and apis/Realtime Web.md (new)

No other file was edited. Load Balancing and Proxies.md and Observability.md were not touched.

## (a) Question each page answers

- **HTTP** (H1 `HTTP`): how has HTTP changed from 1.0 to 3, and what did each change fix? Sections run chronologically: HTTP/1.0 (per-request connections, explicit keep-alive) → HTTP/1.1 (persistent by default, pipelining, HOL blocking, ~6 connections, the sprites/concatenation/sharding workarounds and why HTTP/2 makes them harmful) → HTTP/2 (multiplexing, binary framing, HPACK, deprecated priorities and RFC 9218, TLS de facto, Server Push historical and 103 Early Hints, residual TCP HOL blocking) → HTTP/3 (QUIC, RFC 9000/9114, independent streams, TLS 1.3 built in, 0-RTT).
- **Realtime Web** (H1 `Realtime Web`): how does a server push to a browser when HTTP is client-initiated? Sections: polling and long polling → WebSockets (Upgrade handshake, Origin, Sec-WebSocket-Key not a security feature, proxies, L4 passthrough or L7 with Upgrade) → Server-Sent Events → HTTP/2 does not replace push transports → scaling persistent connections → SignalR (one paragraph).

## (b) Prose word counts

Method: words in lines outside code fences, excluding table rows and image embed lines. "Body" additionally excludes `## How to rederive this` and `## Sources`, which the old page did not have. Same script for before and after.

| Page | Before | After (body) | After (body + rederive bullets) | Target |
|---|---|---|---|---|
| HTTP.md (whole page at HEAD) | 2,689 | | | |
| of which protocol material (old lines 1-57) | 1,100 | 1,258 | about 1,380 | 1,000 to 1,300 |
| of which realtime material (old lines 58-133) | 1,589 | 1,292 | about 1,400 | 1,000 to 1,300 |

Both pages are within the 1,000 to 1,300 target on body prose, sit around 1,400 with the mandated rederive bullets, and are far under the 3,000 ceiling. The Sources sections (URL lines, about 80 to 110 words each) are not counted.

HTTP.md grew by about 160 words because the brief asked for the "why" behind each change (why the HTTP/1.1 workarounds hurt under HTTP/2, why TCP HOL blocking survives HTTP/2, what Early Hints does instead of Push), and the Server Push paragraph moved in from the realtime half.

## (c) What was cut and why

Vendor text:
- Ably's "thin transport layer ... as close to raw as possible, bar a few abstractions" passage (old line 79) reduced to one plain sentence.
- Ably's "HTTP-based techniques tend to be much more resource intensive on servers" claim and the "that is a trade-off rather than a free win" rebuttal (old line 71) dropped; the trade-off is stated once, neutrally, in the scaling section. Ably remains in Sources as the origin of the "WebSockets are the usual choice" position.
- Streamdata.io / Axway name removed from the SSE proxy sentence (kept generic, as instructed).
- SignalR reduced from a section with a transport list and two marketing paragraphs ("shields you from having to worry about updates to WebSocket", "consistent interface across versions") to one paragraph. Azure SignalR Service sentence (old line 119) folded into it as the scale-out example.

Pasted passages:
- Stack Overflow answer near-verbatim (old line 113, "If the incoming connections are spread out over a long period ...") rewritten into two sentences and attributed in Sources.
- Ably scaling passage (old line 115, "the list goes on and on") rewritten as the backplane / client-state / load-balancing sentence.

Catalogue:
- The six-item list of protocols using long-lived TCP connections (WebSockets, SSE, HTTP/2, gRPC, RSocket, AMQP; old lines 49-56) reduced to "The same applies to gRPC and AMQP clients" in the scaling section.
- gRPC / HTTP/2 L7 load-balancing sentence with the ASP.NET gRPC performance link (old line 115) dropped; it is about gRPC, which API Styles owns.

Restatement and filler:
- Old line 23 repeated the HOL-blocking explanation from line 15 word for word; kept once, in HTTP/1.1.
- "In practice" (once) and "essentially" (twice) removed; "optmizations", "perferred" typos gone; American spellings (standardized, optimizations, prioritization) and em/en dashes replaced.
- Stack Overflow "confusion regarding bidirectional and full duplex in HTTP/2" link dropped; the page now states the point directly.

Audit findings confirmed absent from the result: 65,536-sockets misconception (replaced by four-tuple, file descriptors and memory); "load balancer needs TCP mode" (L4 or L7 with Upgrade); SignalR Windows-only (cross-platform since 2018, classic marked legacy); Server Push presented as current (historical, Early Hints); pipelining as a live optimisation (dead); "many more browsers support WebSockets than SSE" (both universal); Sec-WebSocket-Key as anti-tampering (not a security feature); origin model attributed to the single TCP connection (attributed to the Origin header); HTTP described as unidirectional (client-initiated, half-duplex).

No `> Own view:` block on either page; the source page had none.

## (d) What moved where

HTTP.md → Realtime Web.md:
- Bidirectional and full-duplex definitions (old lines 5-7); multiplexing stays in HTTP.md.
- Long polling (old lines 58-67), WebSockets (69-97), Server-Sent Events (99-107), Scaling persistent connections (109-119), SignalR (121-133), the HTTP/2-is-not-a-push-replacement sentence and the InfoQ link (105).
- The nginx WebSocket proxying link, the Stack Overflow 1M-connections link, the ASP.NET Core SignalR links (now version-less).

Within HTTP.md:
- "Persistent connections" (old lines 37-47) moved from after HTTP/3 to become the HTTP/1.0 and HTTP/1.1 sections.
- Server Push and 103 Early Hints (old line 105) moved from the SSE section into the HTTP/2 section.
- The HTTP/1.x workarounds are now their own H3 under HTTP/1.1 with the reason they hurt under HTTP/2.

New text added for joins and fixes only: why sharding, sprites and bundles hurt under HTTP/2; TCP-level HOL blocking as the setup for HTTP/3; one-round-trip handshake and why QUIC sits on UDP; HPACK named; the WebSocket handshake as an `http` fenced example; SSE `text/event-stream`, `EventSource`, `Last-Event-ID`; the four-tuple, `ulimit` and socket-buffer memory in the scaling section; the backplane (Redis) for scale-out; SSE streams sharing one HTTP/2 connection.

Both images stay in HTTP.md with the Phase 2 alt text: `../../images/http-v-http2.jpg` (after the workarounds section) and `../../images/http-stacks.PNG` (after HTTP/3). No embed was removed.

## (e) Inbound links changed

`grep -rn "HTTP.md" fundamentals cloud practice` finds two inbound links, both to protocol material that stayed in HTTP.md and neither using an anchor:

- fundamentals/web and apis/Web Performance.md:44 `[HTTP](HTTP.md)` (HTTP/1.1 vs 2 vs 3 round trips): unchanged, still correct.
- fundamentals/networking/TLS.md:11 `[HTTP](../web%20and%20apis/HTTP.md)` (QUIC builds in TLS 1.3): unchanged, still correct.

No page in fundamentals, cloud or practice linked `HTTP.md#long-polling`, `#websockets`, `#server-sent-events`, `#scaling-persistent-connections` or `#signalr`, so no anchor moved. Network Layers, API Styles, Local IPC and Load Balancing and Proxies do not link HTTP.md at all.

Links added:
- HTTP.md → `Realtime%20Web.md` (intro and Server Push bullet).
- Realtime Web.md → `HTTP.md` (intro), `HTTP.md#http2` (Server Push), `../security/Browser%20Security%20Model.md#origins-and-sites` (Origin header; the H2 "Origins and sites" exists at line 5 of that page), `../platform/Load%20Balancing%20and%20Proxies.md` (L4 vs L7 handling of WebSockets).

All relative link targets and both image paths verified to exist on disk.

Changes needed in files I was told not to edit (for the agents editing them):
- **fundamentals/platform/Load Balancing and Proxies.md**: nothing is broken. Suggested: where the page covers L4 vs L7 or HAProxy's "persistent connections" (line 83 today), add `See [Realtime Web](../web%20and%20apis/Realtime%20Web.md#websockets) for proxying WebSocket Upgrade and long-lived connections.` The page currently has no WebSocket or Upgrade content.
- **fundamentals/platform/Observability.md**: nothing needed.
- Out of my scope but worth a one-line link when that page is next touched: fundamentals/web and apis/Rendering Patterns.md:161 (Blazor Server holds a SignalR connection per user) could link `Realtime%20Web.md#scaling-persistent-connections`.
- Realtime Web is a new page. It needs an index line in README.md and frontmatter when Phase 5 generates the index; nothing to do now.

## (f) Diagrams and tables for Phase 5

- Redraw `images/http-v-http2.jpg` (already on the audit's REDRAW list) as `.drawio.svg`: HTTP/1.1 one request then wait, versus HTTP/2 frames interleaved on one connection. Consider adding a third lane for HTTP/3 showing one lost packet stalling one stream only; the text now makes that the point of HTTP/3.
- Redraw `images/http-stacks.PNG` (already on the REDRAW list): protocol stacks HTTP/1.1 over TCP (TLS optional), HTTP/2 over TLS over TCP, HTTP/3 over QUIC (TLS 1.3 inside) over UDP.
- New for Realtime Web: a sequence diagram of the WebSocket Upgrade handshake (GET with Upgrade, Origin, Sec-WebSocket-Key; 101 with Sec-WebSocket-Accept; then frames both ways), optionally beside an SSE timeline (one GET, response held open, events appended, auto-reconnect with Last-Event-ID).
- Optional table for Realtime Web: transport comparison (direction, protocol on the wire, proxy requirements, reconnection, browser API) for long polling, WebSocket and SSE. The page states these in prose today.

## (g) Open questions for the owner

1. HTTP.md is 1,258 words of body prose, about 160 more than the protocol half of the old page, because the brief asked for the reason behind each change. The extra sentences (why the workarounds hurt, TCP HOL blocking, why QUIC uses UDP) are mine, not the owner's. Confirm they read as yours or cut them back.
2. The old page opened with "HTTP based communication" as H1 and defined bidirectional, full duplex and multiplexing together. I split them: multiplexing stays in HTTP, the other two open Realtime Web. Happy with that, or do you want all three on one page?
3. The Ably "WebSockets are the better choice for ongoing communication" line survives as a neutral "usual choice" sentence with Ably named in Sources. If you hold that as your own view, say so and it can become an `> Own view:` line in your words.
4. SignalR is now one paragraph in Realtime Web, as the brief asked. The audit had suggested moving it to Rendering Patterns (where Blazor Server mentions it) instead. Either works; say if you prefer the move.
5. The sentence "SSE over HTTP/1.1 uses one of the browser's six connections per stream, while over HTTP/2 many SSE streams share one connection" is new. It is correct but not from your notes; drop it if it feels like textbook.
