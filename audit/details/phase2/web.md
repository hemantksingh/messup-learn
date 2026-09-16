# Phase 2 corrections: fundamentals/web and apis (HTTP, HTTP Caching, REST, API Styles)

Applied 2026-09-16. Nothing committed. Only the four assigned files were touched by this task (other files in the working tree, including `Rendering Patterns.md` in the same folder, were modified by parallel agents). All four still have exactly one H1, every code fence has a language tag and no em-dashes were added.

## fundamentals/web and apis/HTTP.md

- was: "HTTP is a layer 7 protocol that is transmitted over a TCP connection" → now: "HTTP/1.x and HTTP/2 run over TCP; HTTP/3 runs over QUIC, which runs over UDP."
- was: "currently supported by nearly two-thirds of all web browsers in use" → now: "First standardised as RFC 7540 (2015), revised as RFC 9113 (2022). Supported by all major browsers." (caniuse link kept)
- was: HTTP/2 prioritization bullet presented as current → now: added "RFC 9113 (2022) deprecated the original HTTP/2 stream-dependency priority scheme; RFC 9218 (Extensible Priorities) replaces it for both HTTP/2 and HTTP/3."
- was: one-sentence HTTP/3 section → now: names HTTP/3 (RFC 9114, 2022) over QUIC (RFC 9000, 2021), explains that a lost packet only stalls its own stream (no cross-stream head-of-line blocking), and notes QUIC builds in TLS 1.3 and supports 0-RTT.
- was: "HTTP 1.0 is very old (almost 25 years old)" → now: "HTTP/1.0 is from 1996 (RFC 1945)".
- was: "Because HTTP 1.1 relies on persistent connections, you can use it to send multiple queries in a row and expect responses in the same order. This is called HTTP pipelining" (link to RFC 2616 sec 8) → now: persistent connections (sequential reuse) and pipelining (send without waiting, ordered responses) are separate sentences; "Pipelining is unused in practice. No browser ships it, and HTTP/2 multiplexing replaced it." Link now points at RFC 9112 section 9.3.2.
- was: "RSockets" → now: "RSocket".
- was: "WebSockets have an extremely lightweight footprint on servers" (unattributed Ably claim) → now: attributed to Ably and labelled a trade-off, with an in-page link to the Scaling persistent connections section.
- was: "making HTTP a uni-directional protocol" → now: "making HTTP a client-initiated, half-duplex protocol".
- was: origin based security model attributed to the single TCP connection → now: removed from that bullet; a new handshake bullet says the `Origin` header is what the server uses to apply the origin based security model.
- was: "Sec-WebSocket-Key: key (to ensure anti-tampering of the connection)" → now: "(proves the peer speaks WebSocket and defeats caching intermediaries; it is not a security feature)". Sec-WebSocket-Accept wording adjusted to match.
- was: "many more browsers support Websockets than SSE" → now: removed.
- was: two conflicting sentences ("HTTP/2 provides efficient HTTP based bidirectional communication" vs "HTTP/2 is not a replacement for push technologies") → now: one statement: HTTP/2 streams are bidirectional at the frame level, but browsers expose no API for server-initiated application messages, so HTTP/2 does not replace WebSockets or SSE.
- was: "HTTP/2 introduces Server Push" as current → now: marked historical (Chrome 106 disabled it in 2022, Firefox 132 removed it in 2024) with `103 Early Hints` (RFC 8297) named as the replacement for preloading.
- was: "A server can handle 65,536 sockets per single IP address, however the quantity can be extended by adding additional network interfaces" → now: sentence deleted; the "number of concurrent connections is not the primary problem ... kernel tuning and enough memory" point kept.
- was: two `docs.microsoft.com/...?view=aspnetcore-5.0` links → now: versionless `learn.microsoft.com` links. Typo "endpooints" fixed on the same line.
- was: "Websockets ... do not use the HTTP protocol, therefore your load balancer needs to work in TCP mode" → now: "either as L4 (TCP) passthrough or as an L7 proxy that supports Upgrade; nginx, HAProxy, Envoy and the cloud L7 load balancers all do. L7 gives you routing and TLS termination."
- was: SignalR section describing classic ASP.NET SignalR ("Forever frame (for Internet Explorer only)", "based on the ASP.NET framework. This makes it unsuitable for Non Windows platforms") → now: describes ASP.NET Core SignalR (WebSockets, SSE, Long polling; versionless learn.microsoft.com link), states it has been cross-platform since 2018, and marks the .NET Framework SignalR (Windows only, Forever Frame) as legacy.
- was: "### Streamdata.io" section (five lines, "Server-Sent Event over WebSockets") → now: section removed; one generic sentence at the end of the Server-Sent Events section: streaming proxies (Streamdata.io, acquired by Axway in 2019, was one) sit in front of a polling API and push changes as SSE. The double-parenthesis link was already single-paren in the current file, so nothing to fix there.
- was: image alt texts `http-v-HTTP/2.jpg` and `http-stacks.PNG` → now: descriptive alt text for both, written after viewing the images (sequential vs concurrent request timeline; the three protocol stacks).

## fundamentals/web and apis/HTTP Caching.md

- was: "`public` means a resource can be cached at the server" → now: "`public` means the response may be stored by any cache, shared or private, even if the request carried an `Authorization` header."
- was: "`must-revalidate` doesn't necessarily mean 'must revalidate', it means the local resource can be younger than the provided max-age" → now: once stale, a cache must revalidate with the origin before reuse and may not serve the stale copy if the origin is unreachable (no stale-on-error); fresh responses unaffected; links RFC 9111 section 5.2.2.2.
- was: "ETag which uniquely identifies the resource" → now: "ETag, which identifies one representation (version) of the resource".
- added: one paragraph on conditional requests after the header list: `If-None-Match` / `If-Modified-Since`, `304 Not Modified`, strong vs weak (`W/`) validators.
- was: `Accept-Encoding: gzip,deflate,sdch` → now: `Accept-Encoding: gzip, deflate, br`.
- was: `Vary: User-Agent` "is useful for serving different content to desktop and mobile users" → now: caveat added that it is widely discouraged because the cache hit rate collapses; normalise at the edge or use client hints.
- was: "Section 14.8 of RFC 2616" → now: "Section 3.5 of RFC 9111" with the rfc-editor link.
- was: `Cache-Control: private, s-maxage=0` shown as "the default" → now: fence removed; sentence explains no header is needed, the default applies when none of the three directives is present.
- was: two fences tagged `sh` (one containing `# or`) → now: one `http` fence with the two `Cache-Control` lines and the prose "Either of these works:". Stray spaces in `public ,no-cache ` fixed.
- was: alt text `cacheable-content.jpg` → now: descriptive alt text written after viewing the image (static / dynamic / user content spectrum).

## fundamentals/web and apis/REST.md

- was: H1 "What is REST" → now: "REST".
- was: "URI (Universal resource Identifier)" → now: "URI (Uniform Resource Identifier)".
- added: short Richardson Maturity Model paragraph (levels 0-3) after the "Why bother with REST?" bullets, with the Fowler link, since API Styles no longer explains it.
- was: "POST - Resource created acknowledgement with the resource state, the newly created URI in the response body and Http status code - 201" → now: 201 Created with the new URI in the `Location` header; representation in the body optional.
- was: "A PATCH request can be idempotent, which helps prevent collisions" → now: "PATCH is not idempotent by nature. To prevent lost updates ... make the request conditional with `If-Match` and the ETag the client last saw."
- was: DELETE "405 Method Not Allowed If the resource cannot be deleted, for example ... already been dispatched" (409 used for the same case under PUT) → now: 409 Conflict for the business-state refusal; one sentence explains 405 is for resources that never support DELETE and must carry `Allow`.
- added: after the ad hoc PATCH example, one paragraph naming JSON Patch (RFC 6902, `application/json-patch+json`) and JSON Merge Patch (RFC 7396, `application/merge-patch+json`).
- was: "This request is going to replace the resource state regardless of what the state originally was" placed between the PATCH and PUT examples → now: moved after the PUT example and starts "This PUT request".
- was: "become temporarily available" → now: "become temporarily unavailable".
- was: "Atom trades scalability for latency" / "The tradeoff is scalability for latency" → now: "Atom trades latency for scalability" / "Middleware trades scalability for latency".
- was: "AMQP and JMS style messaging brokers are based on a centralised server ... single point of failure" stated as fact → now: attributed to *REST in Practice* (2010); the qualifier (JMS is an API, clustered or partitioned brokers such as Kafka, RabbitMQ quorum queues and Pulsar are now the norm) replaces the closing "Clustering is often utilized" sentence.
- was: `sh` fences around HTTP requests, `javascript` fences around JSON link objects → now: `http` and `json`.
- was: no trailing newline → now: trailing newline added.

## fundamentals/web and apis/API Styles.md

- was: H1 "Synchronous request/response‑based integration" (U+2011) → now: "API Styles" (ASCII only).
- was: two paragraphs re-defining REST plus the only mention of the Richardson Maturity Model → now: one paragraph plus a link to [REST](REST.md), which now holds RMM. HTTP examples and the JSON:API subsection kept.
- was: `GET /avatars HTTP/1.1` with a JSON body → now: shown as the `HTTP/1.1 200 OK` response, with prose stating the GET request has no body.
- was: three untagged fences → now: `http`. GraphQL query/result fences retagged `sh` → `graphql` / `json`.
- was: `` ` application/vnd.api+json` `` (leading space) → now: `` `application/vnd.api+json` ``.
- was: HN commenter's opinion in first person, "e.g. Swagger" → now: attributed to "One commenter in that thread", "OpenAPI (formerly Swagger)".
- was: "RPC spans the transport layer (TCP) and the application layer in the OSI model" and a sentence ending "which happens to be either" → now: "RPC sits above the transport layer (TCP): the session and presentation layers in OSI terms, or simply the application layer in TCP/IP terms" and the sentence completes with "either an interface definition language file (Thrift IDL, protobuf, WSDL) or a type shared through a common platform (Java RMI, .NET Remoting)".
- was: ".Net Remoting" → now: ".NET Remoting (legacy, .NET Framework only)".
- was: "SOAP uses UDDI - XML based registry for service description and discovery and WSDL for interface definition" → now: contracts are WSDL; UDDI was optional and is defunct (OASIS committee closed 2008).
- was: "Ensuring data types of XML payloads in XML-RPC is tough. In XML you layer meta data on top" → now: XML-RPC uses explicit type tags (`<int>`, `<string>`); SOAP types with XML Schema; the verbosity point kept for SOAP.
- was: "HTTP verbs and the error codes are ignored" → now: "it uses only POST and maps outcomes coarsely to 200 or 500 (a SOAP Fault is a 500)".
- was: "Browsers don't fully support HTTP/2, making REST and JSON the primary way to get data into browser apps" → now: browsers support HTTP/2, but page JavaScript cannot control HTTP/2 framing or read trailers, so gRPC-Web (Envoy or ASP.NET Core proxy), the Connect protocol, or gRPC JSON transcoding (.NET 7+) are used.
- added (gRPC DUPLICATE): one sentence linking gRPC over UDS/named pipes to [Local IPC](../networking/Local%20IPC.md).
- was: "RPC may be a better fit if you are writing your API in a functional language" unattributed → now: "The Smashing Magazine article above suggests ...".
- was: "GraphQL uses sparse fieldsets" → now: "GraphQL uses field selection (the JSON:API equivalent is sparse fieldsets)".
- was: "Queries always return a HTTP status code of 200" → now: field errors still return 200 with a top-level `errors` key; under the GraphQL-over-HTTP spec (2023 onwards, `application/graphql-response+json`) request-level errors may return 4xx, though many servers still return 200 for everything.
- business-layer image alt text: already descriptive from the audit baseline fix; no change needed.

## Deliberately skipped

- CLASSIFY findings that move sections between pages: SignalR to Rendering Patterns, Streamdata.io generalisation as a separate page, HTTP.md split into protocol vs realtime transports, REST.md Atom/event-feed section move to Asynchronous Messaging. All left for a later phase as instructed. The Atom section stays in REST.md with only its factual fixes applied.
- HTTP.md H1 "HTTP based communication" (Low BROKEN, filename mismatch): not a typo and not in the assigned list, so untouched.
- HTTP Caching "gaps" (s-maxage, immutable, stale-while-revalidate, stale-if-error, Age, Expires, heuristic freshness): new content, not corrections; out of scope for this phase.
- Typos on lines with no finding (HTTP.md "perferred"; API Styles "Die to", "devloves", "Andrioid", "REST APIS"): left alone per the "do not rewrite paragraphs with no finding against them" rule. Only "endpooints" was fixed, because that line was already being edited for the versionless link.
- The old HTTP.md L47 RFC 2616 section 8 link was updated to RFC 9112 as part of the pipelining rewrite; the L15 pipelining sentence in the HTTP 1.x section was left unchanged because it is accurate.
- Web verification: not performed. Every replacement fact (RFC numbers and years, browser versions, acquisition year, SignalR release year, OASIS closure) was supplied by the task or by the audit rows with inline sources.
