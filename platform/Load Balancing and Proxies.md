# Load Balancing and Proxies

What does a load balancer or reverse proxy do for me, and how do Nginx and HAProxy differ in doing it?

A reverse proxy accepts a client's connection, opens its own connection to a server behind it and relays the traffic. Because it sits in the middle it can choose the server, drop bad requests, cache answers, end the TLS session and hide how many servers there are. A load balancer is a reverse proxy whose main job is the choosing.

## Scaling up or out

There are two ways to add capacity.

**Vertical scaling** is a bigger machine: more CPU, RAM, disk or network for the one resource. In a cloud you stop the instance and resize it. It is the easiest change and often enough for a long time. It has a ceiling, and one machine is never highly available.

**Horizontal scaling** is more machines doing the same job. The instances must be identical and either stateless or sharing state through something outside themselves (a database, a cache, a queue). Clients need one address for many machines, and something must hand each request to a healthy one. That is the load balancer.

## Hardware or software load balancers

Load balancers used to be hardware at the edge of the data centre: NetScaler (for a while Citrix ADC) and F5 BIG-IP appliances, racked in pairs so one could fail. They are sized for peak traffic and idle the rest of the time; how much is wasted is a vendor claim.

Software load balancers such as HAProxy, Nginx and Envoy run on ordinary virtual machines or containers and are configured from files and APIs, so the team that deploys the application can change the routing. Inside Kubernetes an Ingress or Gateway API controller is one of these proxies driven by cluster objects ([Kubernetes](Kubernetes.md)). Cloud providers sell managed load balancers that hide the proxy entirely.

## Layer 4 or layer 7

A **layer 4** load balancer accepts the client's TCP connection, opens a new one to a server and copies the byte stream across without reading it. It does not know the traffic is HTTP, so it can carry anything: databases, LDAP, mail. It routes on address and port only. HAProxy in `mode tcp` and Nginx's `stream` block do this. A proxy still terminates the connection; it does not forward raw packets, which is what a kernel-level balancer such as LVS/IPVS does.

A **layer 7** load balancer parses the protocol, usually HTTP. It can route on host, path and headers, rewrite requests, retry on another server, cache, compress and return its own responses. HAProxy in `mode http` and Nginx's `http` block do this.

Both tools do both layers in their open source versions. Nginx open source has had TCP load balancing through the `stream` module since 2015, and UDP the year after; it was never a Plus-only feature. The real difference is that Nginx is a web server first and serves files from disk, while HAProxy is a proxy only. It can return small fixed responses (`http-request return`) but does not serve a directory.

## What a reverse proxy does for you

All traffic passes the proxy, so anything you want done to every request goes there instead of into each application.

* **TLS termination.** The proxy holds the certificate and speaks TLS to the client; behind it traffic can be plain HTTP inside a private network. An ACME client renews Let's Encrypt certificates automatically ([TLS Certificates](../networking/TLS%20Certificates.md)).
* **Caching and compression.** Cacheable responses are served from the proxy; responses are compressed once, at the edge.
* **Routing.** One hostname fronts many services, split by host or path. This is the API gateway idea: one entry point that routes, authenticates and rate limits. Keep business logic out of it; a gateway that orchestrates processes becomes a monolith in the middle.
* **Access control.** `allow` and `deny` by IP or subnet. Fail2ban watches the logs and bans repeat offenders, usually with a firewall rule.
* **Rate and connection limits.** A first line against denial of service and runaway clients. Where limits should sit is in [Resilience Patterns](Resilience%20Patterns.md).
* **Authentication offload.** Nginx's `auth_request` sends a subrequest to an external authentication service and lets the request through only on a 2xx. For LDAP, nginx publishes a reference HTTP-to-LDAP service.

A gateway restricts who can reach your servers. A web application firewall (WAF) inspects request content for attacks such as injection and cross-site scripting; an intrusion prevention system (IPS) does the same at layers 3 and 4 across many protocols. The NGINX ModSecurity WAF module reached end of life in March 2024; WAF options and DDoS filtering are in [Web Application Risks](../security/Web%20Application%20Risks.md).

## Nginx

Igor Sysoev wrote Nginx while a sysadmin at Rambler to get past Apache's limits, the **C10k problem** of holding ten thousand simultaneous connections. A master process reads the configuration and manages worker processes, one per CPU core as a rule. Each worker runs an event loop and handles thousands of connections with non-blocking I/O, so memory per connection is small and roughly constant.

Apache's behaviour depends on its multi-processing module (MPM). With `prefork` it forks a process per connection; `worker` and `event` use threads, and `event`, the default since 2.4, handles idle keep-alive connections asynchronously, which narrows the gap. Under `prefork` memory grows with every connection and throughput falls away as the box fills.

The other difference is where application code runs. Apache can embed an interpreter (`mod_php`) so PHP runs inside the web server process. Nginx does not embed application interpreters; it proxies to a separate application process (php-fpm, gunicorn, a JVM) over FastCGI, uwsgi or HTTP. That limits what a bug in the application can reach and lets you restart one without the other. Beyond performance, choose the server your team already knows.

Nginx open source covers web serving, reverse proxy, layer 4 and 7 load balancing, caching, `limit_req` and `limit_conn` rate limiting, and passive upstream checks (`max_fails`, `fail_timeout`). Nginx Plus, the commercial build, adds active health checks, JWT validation, a key-value store, session persistence, `least_time` balancing and a live status API.

### Operating Nginx

`ps -ax | grep nginx` lists the master and its workers. The configuration file is `nginx.conf`; where it lives depends on how Nginx was installed (`/etc/nginx` for distribution packages, `/usr/local/etc/nginx` for Homebrew, `/usr/local/nginx/conf` for source builds). `nginx -V` prints the compiled-in path.

* Reload configuration without dropping connections: `nginx -t && nginx -s reload`. This re-reads the config and starts new workers; it does **not** load a new binary.
* Upgrade the binary without downtime: send `USR2` to the master to start a new master from the new binary, then `WINCH` and `QUIT` to the old one.
* Requests are matched by `listen` (address and port), then `server_name` (host header), then `location` (path). `default_server` is a parameter on `listen` that catches requests whose host matches no `server_name`.
* Logs default to `/var/log/nginx/access.log` and `/var/log/nginx/error.log`.

## HAProxy

HAProxy is a widely used open source load balancer written in C. It does TLS termination, health checks, compression and layer 4 or 7 proxying, and is not a web server. Vendor benchmarks put each of HAProxy and Nginx ahead of the other depending on who ran them; treat them as contested marketing.

The configuration has four sections: `global` for process-wide settings, `defaults` for values inherited by everything after it, `frontend` for the addresses and ports clients connect to, and `backend` for the group of servers requests are balanced across.

### Active and passive health checks

Adding `check` to a `server` line makes HAProxy probe that server on an interval, by TCP connect or, with `option httpchk`, by an HTTP request to a URL. After `fall` failed probes the server is marked down; after `rise` good ones it comes back.

```haproxy
backend apiservers
    balance roundrobin
    option httpchk GET /health
    server server1 192.168.50.3:80 check
```

An active check watches one URL, so it tells you when a server is completely down and nothing about the endpoints it does not call.

A **passive** check watches real traffic. `observe layer4` or `observe layer7` on the `server` line, with `error-limit` and `on-error mark-down`, marks the server down once live requests fail often enough. That is a circuit breaker in the proxy: the passive check opens it and the active check bringing the server back is the probe that closes it ([Resilience Patterns](Resilience%20Patterns.md)). An `agent-check` asks an agent on the server to report its state and weight.

### Retries

When HAProxy cannot open a connection to the chosen server it tries again, up to `retries` times (default 3). The wait between attempts is the smaller of `timeout connect` and one second; `timeout connect` itself is how long one attempt may take, not the retry interval. `option redispatch` lets a later attempt go to a different server. From 2.0 `retry-on` extends retries to layer 7 events such as a response timeout or a 5xx. Retrying suits a brief network blip, does nothing for a bad deployment, and is only safe for requests that can be repeated.

### Queueing and back-pressure

`maxconn` on a `server` line caps the connections HAProxy opens to it. Sessions beyond that wait in a queue, bounded by `timeout queue`, rather than failing. Queue length is the earliest sign that a server is falling behind. Passing that signal back so clients slow down is back-pressure, also in Resilience Patterns.

### Runtime API and metrics

The Runtime API is a Unix or TCP socket enabled in `global` with `stats socket`; over it you read server state, change weights or drain a server. Changes made this way are lost on restart. The REST-based Data Plane API writes the configuration file, so its changes persist.

```haproxy
global
    stats socket /var/run/haproxy.sock user haproxy group haproxy mode 660 level admin
```

The built-in stats page shows every server's state and last check result. Since 2.4 the Prometheus exporter is compiled into core; enable it in a `frontend` with `http-request use-service prometheus-exporter if { path /metrics }` and scrape it ([Observability](Observability.md)).

## Nginx and HAProxy side by side

| | Nginx open source | HAProxy |
|---|---|---|
| Serves files from disk | Yes | No |
| Layer 4 proxying | `stream` block | `mode tcp` |
| Layer 7 proxying | `http` block | `mode http` |
| Active health checks | Plus only | `check` |
| Passive health checks | `max_fails`, `fail_timeout` | `observe`, `error-limit` |
| Layer 7 retries | `proxy_next_upstream` | `retries`, `retry-on` |
| Config reload | `nginx -s reload` (new workers) | master-worker mode, `-sf` (new process) |
| Runtime changes without reload | Plus API | Runtime API |
| Metrics | `stub_status`; exporter is separate | stats page, Prometheus exporter in core |

## How to rederive this

* One address for many machines needs something in the middle to choose; that is where every cross-cutting job (TLS, cache, limits) ends up.
* Layer 4 copies bytes and routes on port; layer 7 reads HTTP and routes on host and path. Both proxies do both.
* An event loop keeps per-connection cost flat; a process per connection does not.
* Active checks find a dead server; only watching real traffic finds a broken one.
* Retry once for a blip, never for a bad deploy; bound every wait.

## Sources

* AWS, *Architecting for the Cloud: AWS Best Practices* whitepaper, 2018 (scaling section, paraphrased).
* Nginx docs: <https://nginx.org/en/docs/>, and the changelog entries for the `stream` module.
* Apache MPM docs: <https://httpd.apache.org/docs/2.4/mpm.html>.
* HAProxy configuration manual: <https://docs.haproxy.org/>.
* HAProxy blog: <https://www.haproxy.com/blog/>.
* F5, "NGINX ModSecurity WAF Is Transitioning to End-of-Life", 2022 (end of life March 2024).
