# HAProxy

## HAProxy configuration

The [four essential sections to an HAProxy configuration](https://www.haproxy.com/blog/the-four-essential-sections-of-an-haproxy-configuration/) file are:

* `global` define process-wide security and performance tunings
* `defaults` helps reduce duplication, its settings apply to all of the `frontend` and `backend` sections that come after it
* `frontend` defines the IP addresses and ports that clients can connect to
* `backend` defines a group of servers that will be load balanced and assigned to handle requests

## Resilience

Haproxy allows you to combine active health checks, retries and circuit breaking to get full coverage protection for your services.

Acting out real-world failure modes is the best way to test whether your system is resilient. What actually happens when you start killing web server nodes? What is the effect of inducing latency in the network? If a server returns HTTP errors, will downstream clients be affected and, if so, to what degree? Intentionally [injecting faults using chaos engineering](https://www.haproxy.com/blog/haproxy-layer-7-retries-and-chaos-engineering/) techniques, you begin to see exactly how HAProxy should be tuned.

### Active health checks

Adding the `check` parameter to a `server` line in your HAProxy configuration, it pings that server to see if it's up  up and working properly. This can either be an attempt to connect over TCP/IP or an attempt to send an HTTP request and get back a valid response. If the ping fails enough times, HAProxy stops load balancing to that server.

Health checks target a service's IP and port or a specific URL, therefore active health checks monitor a narrow range of the service. They work well for detecting when a service is 100% down. But what if the error happens only when a certain API function is called, which is not monitored by the health checks? The health checks would report that the service is functioning properly, even if 70 or 80% of requests are calling the critical function and failing.

### Automatic retries

Automatic retries is a mechanism built into HAProxy, which let you attempt a failed connection or HTTP request again. When HAProxy receives a request, but can’t establish a TCP connection to the selected backend server, it automatically tries again after an interval set by `timeout connect`. Retrying is an intrinsically optimistic operation: It expects that calling the service a second time will succeed, which is perfect for transient errors such as those caused by a momentary network disruption. Retries do not work as well when the errors are long-lived, such as those that happen when a bad version of the service has been deployed.

With HAProxy 2.0 you can trigger retries on certain events. The `retry-on` directive lets you list other kinds of failures that will trigger a retry and covers both Layer 4 and Layer 7 events. For example, if messages time out after the connection has been established due to network latency or because the web server is slow to respond, retry-on tells HAProxy to trigger a retry.

### Circuit breaker

A circuit breaker is more pessimistic. After errors exceed a threshold, it assumes that the disruption is likely to be long-lived. To protect clients from continuously calling the faulty service, it shuts off access for a specified period of time. The hope is that, given enough time, the service will recover.

Unlike active health checks, a circuit breaker monitors live traffic for errors, so it will catch errors in any part of the service. You can [implement a circuit breaker](https://www.haproxy.com/blog/circuit-breaking-haproxy/#implement-a-circuit-breaker-the-simple-way) to monitor live traffic for detecting errors.