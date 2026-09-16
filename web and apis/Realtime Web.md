---
title: "Realtime Web"
summary: "How a server pushes data to a browser: polling, long polling, WebSockets and Server-Sent Events, and how they scale."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "RFC 6455, The WebSocket Protocol, sections 1.3 and 10.2"
  - "WHATWG HTML Standard, Server-sent events"
  - "NGINX, WebSocket proxying; InfoQ, WebSocket and HTTP/2 coexist"
  - "Stack Overflow, resources held for 1,000,000 open WebSockets"
  - "Ably, WebSockets vs HTTP"
  - "ASP.NET Core SignalR introduction and scaling (Microsoft Learn)"
tags: [websockets, server-sent-events, long-polling, realtime, http]
---
# Realtime Web

In [HTTP](HTTP.md) the request is always initiated by the client and the response is produced by the server. That makes HTTP a client-initiated, half-duplex protocol: the server cannot start a message, and only one side talks at a time. A chat app, a stock ticker or a monitoring dashboard needs the opposite. These are the ways a server gets data to a browser that did not just ask for it.

* **Bidirectional** means you can send data in both directions over a channel. HTTP is bidirectional, but only in request-response pairs.

* **Full duplex** implies that client and server can send data in both directions *at the same time* without waiting for a response. Phone lines are an example of full duplex while a walkie-talkie is half-duplex.

## Polling and long polling

Polling is the client asking on a timer. It is

* Not responsive - you cannot be sure that the requested data has changed
* Not efficient - results in wastage of CPU and bandwidth to transfer stale data

Long polling is where the server elects to hold a client connection open for as long as possible, delivering a response only after data becomes available or a timeout has been reached. After receiving the response the client immediately sends a new long-polling request, which emulates real-time delivery over plain HTTP. It works everywhere HTTP works, which is why it survives as the fallback transport.

Its weakness is the path in between. A request crosses gateways and reverse proxies that each have their own idea of how long a connection is allowed to stay open. If it stays open too long something may kill it, maybe even when it was doing something important.

## WebSockets

WebSockets are the usual choice for realtime, ongoing communication. The protocol (RFC 6455) provides:

* Bi-directional protocol - either client or server can send a message to the other party
* Full-duplex communication - client and server can talk to each other independently at the same time over a long running TCP connection
* Single TCP connection - after upgrading the HTTP connection at the start, client and server communicate over that same TCP connection throughout the lifecycle of the WebSocket connection

A WebSocket is thin message framing over a TCP connection. It is a different protocol from HTTP, but the handshake is compatible with HTTP: it uses the HTTP Upgrade facility to switch the connection from HTTP to WebSocket. The client sends an HTTP GET:

```http
GET /chat HTTP/1.1
Host: example.com
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
Origin: https://app.example.com
```

* `Origin` is the page's origin. The server uses it to apply the browser's *origin based security model* and decide whether to accept the connection. The same-origin policy and CORS do not apply to WebSockets, so a server that ignores `Origin` accepts connections from any page. See [Browser Security Model](../security/Browser%20Security%20Model.md#origins-and-sites).
* `Sec-WebSocket-Key` proves the peer speaks WebSocket and defeats caching intermediaries. It is not a security feature.

The server replies with status `101 Switching Protocols`, `Upgrade: websocket`, `Connection: Upgrade` and a `Sec-WebSocket-Accept` derived from the client's key so the client can confirm the server understood the WebSocket handshake. From then on either side sends WebSocket frames at any time. The scheme is `ws://` or, preferably, `wss://` (WebSocket over TLS).

HTTP compatibility lets WebSockets fit existing infrastructure: they use the standard ports 80 and 443, so existing firewall rules apply. Proxies need two things to [support WebSocket](https://www.f5.com/company/blog/nginx/websocket-nginx):

* Upgrade is hop-by-hop, so when a proxy intercepts an Upgrade request from a client it needs to send its own Upgrade request to the backend server, including the appropriate headers.
* The connections are long lived, as opposed to the typical short-lived HTTP connections, so the proxy needs to let them stay open rather than closing them because they seem idle.

After the handshake, WebSocket frames flow over the same TCP connection without HTTP. A load balancer can handle them either as L4 (TCP) passthrough or as an L7 proxy that supports Upgrade; nginx, HAProxy, Envoy and the cloud L7 load balancers all do. L7 gives you routing and TLS termination. See [Load Balancing and Proxies](../platform/Load%20Balancing%20and%20Proxies.md).

## Server-Sent Events

Server-Sent Events (SSE) are a one-way push from server to client. The client-side code (`EventSource`) handles incoming events almost identically to WebSockets, but you cannot send events from the client to the server.

SSE is sent over traditional HTTP: a normal response with content type `text/event-stream` that the server keeps open and appends to. It needs no special protocol or server implementation, passes through any proxy that streams responses, and every current browser supports it. WebSockets need full-duplex connections and a WebSocket-aware server. SSE also has features WebSockets lack by design: automatic reconnection, event IDs so the client can resume from the last one it saw (`Last-Event-ID`), and named event types.

Since everything SSE does can also be done with WebSockets, WebSockets get more attention. If the client only listens, SSE is the simpler transport. An SSE proxy can sit in front of a polling API, cache responses and push changes to clients as events without any server-side changes.

## HTTP/2 does not replace push transports

HTTP/2 streams are bidirectional at the frame level, but browsers expose no API for server-initiated application messages, so [HTTP/2 is not a replacement for WebSockets or SSE](https://www.infoq.com/articles/websocket-and-http2-coexist/). HTTP/2 Server Push only filled the browser cache and is now historical (see [HTTP](HTTP.md#http2)). What HTTP/2 does change is cost: SSE over HTTP/1.1 uses one of the browser's six connections per stream, while over HTTP/2 many SSE streams share one connection.

## Scaling persistent connections

Standard HTTP clients use ephemeral connections that close when the client goes idle and reopen later. Long-lived connections like WebSockets stay open even when the client goes idle, so a high-traffic app holds one connection per user for the whole session. The same applies to gRPC and AMQP clients.

The [number of concurrent connections is not the primary problem](https://stackoverflow.com/questions/17448061/how-many-system-resources-will-be-held-for-keeping-1-000-000-websocket-open). A server distinguishes connections by the full four-tuple (client address and port, server address and port), so one listening port can hold millions. The limits are file descriptors, one per connection and set by `ulimit`, and memory: kernel socket buffers plus whatever state the application keeps per client. The real issue is the workload required to process and respond to messages once the server has received the data. Mostly idle connections that send small chunks infrequently can run past a million on one machine; busy ones cannot. Even then you hit networks, server systems and libraries not configured for that many connections.

Two things follow. Heavy use of connection-related resources by WebSockets can starve other web apps hosted on the same server, so it may make sense to run realtime applications on their own dedicated servers. And once one machine cannot cope you add servers, so a message for a user may need to reach a server that user is not connected to. That means load balancing the connections, a backplane (a pub/sub channel such as Redis) to synchronise messages across servers, and client state that survives a reconnect to a different server.

## SignalR

[ASP.NET Core SignalR](https://learn.microsoft.com/en-us/aspnet/core/signalr/introduction) is a library that provides a simple API for server-to-client remote procedure calls (RPC) that call functions in the client from the server. It abstracts the transports above: it negotiates WebSockets where available and falls back to Server-Sent Events, then long polling, so the application has one code path across clients. For scale-out it uses a [backplane](https://learn.microsoft.com/en-us/aspnet/core/signalr/scale) (Redis) or the Azure SignalR Service, a managed proxy that holds all the client connections while each server keeps a small, constant number of connections to the service. ASP.NET Core SignalR has been cross-platform since its release in 2018. The original ASP.NET SignalR for .NET Framework (Windows only, with an extra Forever Frame transport for Internet Explorer) is legacy.

## How to rederive this

- HTTP only answers questions, so either ask more often (polling), ask and wait (long polling), or change protocol (WebSocket) or keep one response open forever (SSE).
- A WebSocket starts as HTTP so it can use ports 80 and 443 and existing proxies; `Origin` is the only thing standing between it and any page on the web.
- Choose by direction: client must send on the same channel, WebSocket; client only listens, SSE.
- A held connection costs a file descriptor and memory, not a port. Ports run out on the client side, never on the listener.
- Two servers means a message can land on the wrong one; that is why every scale-out design has a backplane.

## Sources

- RFC 6455 (The WebSocket Protocol), section 1.3 on the handshake and section 10.2 on origin: https://www.rfc-editor.org/rfc/rfc6455
- WHATWG HTML Standard, Server-sent events: https://html.spec.whatwg.org/multipage/server-sent-events.html
- NGINX, WebSocket proxying: https://www.f5.com/company/blog/nginx/websocket-nginx
- InfoQ, WebSocket and HTTP/2 coexist: https://www.infoq.com/articles/websocket-and-http2-coexist/
- Stack Overflow, resources held for 1,000,000 open WebSockets: https://stackoverflow.com/questions/17448061/how-many-system-resources-will-be-held-for-keeping-1-000-000-websocket-open
- Ably, WebSockets vs HTTP (the "WebSockets are usually the better choice for ongoing communication" position): https://ably.com/topic/websockets-vs-http
- ASP.NET Core SignalR introduction and scaling: https://learn.microsoft.com/en-us/aspnet/core/signalr/introduction and https://learn.microsoft.com/en-us/aspnet/core/signalr/scale
