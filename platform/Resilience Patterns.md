# Resilience Patterns

How does a system keep working when a dependency is slow or down?

A slow dependency does more damage than a dead one. A dead one fails fast and the caller moves on. A slow one holds the caller's thread and connection for as long as the caller will wait, new requests pile up behind it, and the caller becomes slow to its own callers. Every pattern below bounds how long you wait, bounds how much you send, or decides what to do instead of calling. The names follow Michael Nygard's *Release It!*.

## Timeouts

Never make a call without a limit on how long you will wait. A timeout turns a slow dependency back into a fast failure. Set connect and read timeouts separately, and shorter than the timeout of whoever is calling you, or your caller gives up first and your work is wasted.

## Retries with backoff and jitter

A retry bets that the failure was brief: a dropped packet, a server mid-restart. It is wrong when the dependency is overloaded, because every retry adds load to the thing already failing. Two rules make it safe. Wait longer between attempts (exponential backoff) and add a random amount to each wait (jitter), so a thousand clients that failed together do not retry together. Brooker's 2015 post shows the jitter matters more than the exponent.

Retry only requests that can be repeated without harm, or make them so with an idempotency key. Count the layers: if the client library, the sidecar and the proxy each make three attempts, one failure becomes twenty-seven requests. Give the whole path a retry budget, a cap on retries as a fraction of first attempts, rather than a count per layer.

## Circuit breakers

A breaker is a state machine around a call. **Closed** is normal: calls go through and outcomes are counted. When failures cross a threshold, an error rate or a run of consecutive failures over a window, the breaker **opens** and calls fail without touching the dependency. After a cool-off it goes **half-open** and lets one probe through. Success closes it; failure opens it for another cool-off.

A timeout bounds one call. A fallback replaces one result with a cached or default one. A breaker stops calling at all, which frees your threads and gives the dependency room to recover. Returning stale data when a call passes 100 ms is a timeout with a fallback; a breaker is what stops you making the attempt for the next thirty seconds. The usual placement is between backend services; at the edge an open breaker turns one slow page into a blank one for everyone.

## Bulkheads

Ship hulls are divided into compartments so one breach does not sink the ship. Give each dependency its own pool of connections or threads, and each tenant or class of traffic its own capacity. Otherwise one slow dependency drains the shared pool and every unrelated call starves.

## Rate limiting and load shedding

Rate limiting protects a service from a caller exceeding an agreed rate. The limit is per key (client, token, IP), usually a token bucket: tokens refill at the agreed rate, each request spends one, and a request with no token gets a 429.

Load shedding is the service protecting itself when total load is too high. Rejecting a request now is cheap; failing it after five seconds in a queue costs both sides the five seconds. Queue wait time is the signal: when a request would wait longer than the caller's timeout, drop it.

## Back-pressure

Back-pressure is the dependency telling the caller to slow down instead of silently falling behind. A 429 or 503 with `Retry-After` is back-pressure. A bounded queue that refuses when full is back-pressure. A consumer that pulls the next message only when it has finished the last one has it built in, which is one reason queues are a good boundary between services of different speeds ([Messaging Fundamentals](../messaging/Messaging%20Fundamentals.md#coupling)). Without it, an unbounded buffer somewhere grows until the process dies.

## Health checks are the input

All of the above needs to know whether the dependency is healthy. An **active** check probes a fixed endpoint on a timer; it finds a server that is fully down and nothing else, since an endpoint that fails on one code path still passes. A **passive** check counts the outcomes of real traffic and sees what callers see. A circuit breaker is a passive check with a state machine attached. In a proxy the two combine: HAProxy's `observe` and `error-limit` mark a server down from live errors, and its active `check` is the probe that brings it back ([Load Balancing and Proxies](Load%20Balancing%20and%20Proxies.md)). Kubernetes splits the active check into a readiness probe that removes a pod from a Service and a liveness probe that restarts it.

## Where each pattern sits

| Pattern | Client library (Polly, resilience4j) | Sidecar or mesh (Envoy, Istio) | Proxy or load balancer (HAProxy, Nginx) |
|---|---|---|---|
| Timeout | Per call, most precise | Per route | `timeout connect`, `timeout server` |
| Retry | Per call, knows idempotency | Per route, policy driven | `retries`, `retry-on` |
| Circuit breaker | Per dependency, in process | Outlier detection ejects hosts | Passive checks mark servers down |
| Bulkhead | Thread or connection pools | Per-upstream connection limits | `maxconn` per server |
| Rate limit | Outbound throttling | Per route | First line, at the edge |
| Load shedding | In the server's own handler | Per-upstream limits | Queue limits, `timeout queue` |
| Back-pressure | Bounded queues, pull consumers | Connection limits | Connection queueing |

The library knows the request, including whether it is idempotent, but costs one dependency per language. The sidecar and proxy know nothing about the request but apply one policy to every service. Most systems use both, which is why retry budgets matter.

## How to rederive this

* Slow is worse than dead because it holds resources; bound every wait.
* A retry adds load to something already failing; back off, add jitter, cap the total.
* A breaker is a state machine with an open state, not a timeout and not a fallback.
* Separate pools so one dependency cannot starve the rest.
* Reject early and tell the caller; an unbounded buffer is where the process dies.

## Sources

* Nygard, *Release It!*, 2nd ed., Pragmatic Bookshelf, 2018 (timeouts, circuit breaker, bulkhead, back-pressure).
* Brooker, "Exponential Backoff and Jitter", AWS Architecture Blog, 2015.
* Beyer et al., *Site Reliability Engineering*, O'Reilly, 2016, ch. 21 "Handling Overload" and ch. 22 "Addressing Cascading Failures" (retry budgets, load shedding).
* HAProxy configuration manual: <https://docs.haproxy.org/>.
* Kubernetes docs, Liveness, Readiness and Startup Probes: <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/>.
