# HAProxy

HAProxy or High Availability proxy is the most popular open source software load balancer that provides high availability for TCP-based services. It is written in C and supports SSL termination, persistent connections, health checks, compression and more. It can be used as a load balancer, reverse proxy or application delivery controller

* Fast and lightweight proxy server and load balancer with a small memory footprint and low CPU usage.
  * Haproxy consistently [performs on par or better](https://www.datadoghq.com/blog/monitoring-haproxy-performance-metrics/) in benchmarks against other popular reverse proxies like http-proxy or the Nginx webserver. However Nginx [claim](https://www.nginx.com/blog/nginx-and-haproxy-testing-user-experience-in-the-cloud) to be more performant using *latency percentile distribution* as a metric.
* Protocol agnostic - it can handle anything sent over TCP
  * Haproxy can run in Layer 4 TCP mode and Layer 7 HTTP mode. In Layer 4 TCP mode, HAProxy forwards the RAW TCP packets from the client to the application servers. In the Layer 7 HTTP mode, HAProxy parses HTTP headers before forwarding them to the application servers.
  * Nginx only supports layer 7 HTTP mode. For load balancing services like LDAP, MYSQL if you want to use TCP mode, then you can use Nginx Plus or other web servers like Apache.
  * You can [configure Haproxy and Nginx to work together](https://www.howtoforge.com/tutorial/how-to-setup-haproxy-as-load-balancer-for-nginx-on-centos-7/) as a load balancer and web server.
* Only deals with the network and never touches the file system, therefore it cannot serve static content
* On CentOS 7, HAProxy is available in the default repository which makes it easy to install and configure.

## HAProxy configuration

The [HAProxy configuration file](https://www.haproxy.com/documentation/hapee/latest/onepage/) has [four essential sections](https://www.haproxy.com/blog/the-four-essential-sections-of-an-haproxy-configuration/):

* `global` define process-wide security and performance tunings
* `defaults` helps reduce duplication, its settings apply to all of the `frontend` and `backend` sections that come after it
* `frontend` defines the IP addresses and ports that clients can connect to
* `backend` defines a group of servers that will be load balanced and assigned to handle requests

### Dynamic configuration

As services are containerised and become ephemeral, keeping your configurations up-to-date becomes a daunting task, especially in service mesh architectures. You can dynamically configure HAProxy using the

* TCP and Unix sockets based [Runtime API](https://www.haproxy.com/blog/dynamic-configuration-haproxy-runtime-api/). Since this is a TCP based API you can communicate with it [using telnet or socat](https://www.youtube.com/watch?v=JjXUH0VORnE). Changes made through the runtime API do not persist i.e. after making a change via the API if haproxy is restarted the changes will be lost.
* REST based [Data plane API](https://www.haproxy.com/blog/new-haproxy-data-plane-api/). This can be [installed](https://www.haproxy.com/documentation/hapee/latest/api/data-plane-api/installation/haproxy-community/) by downloading the Data Plane API binary from the GitHub repository.

## Resilience

Haproxy allows you to combine active health checks, retries and circuit breaking to get full coverage protection for your services.

Acting out real-world failure modes is the best way to test whether your system is resilient. What actually happens when you start killing web server nodes? What is the effect of inducing latency in the network? If a server returns HTTP errors, will downstream clients be affected and, if so, to what degree? Intentionally [injecting faults using chaos engineering](https://www.haproxy.com/blog/haproxy-layer-7-retries-and-chaos-engineering/) techniques, you begin to see exactly how HAProxy should be tuned.

### Active health checks

Adding the `check` parameter to a `server` line in your HAProxy configuration, it pings that server to see if it's up  up and working properly. This can either be an attempt to connect over TCP/IP or an attempt to send an HTTP request and get back a valid response. If the ping fails enough times, HAProxy stops load balancing to that server.

If you’re load balancing web applications, then instead of monitoring a server based on whether you can make a TCP connection, you can [setup an HTTP based health check](https://www.haproxy.com/blog/using-haproxy-as-an-api-gateway-part-3-health-checks/) to monitor a specific URL.

```sh
backend apiservers
    balance roundrobin
    option httpchk GET /health
    server server1 192.168.50.3:80 check
```

Health checks target a service's IP and port or a specific URL, therefore active health checks monitor a narrow range of the service. They work well for detecting when a service is 100% down. But what if the error happens only when a certain API function is called, which is not monitored by the health checks? The health checks would report that the service is functioning properly, even if 70 or 80% of requests are calling the critical function and failing.

### Pasive health checks

Active checks are easy to configure and provide a simple monitoring strategy. They work well in a lot of cases, but you may also wish to monitor real traffic for errors, which is known as passive health checking. In HAProxy, a passive health check is [configured](https://www.haproxy.com/blog/using-haproxy-as-an-api-gateway-part-3-health-checks/#passive-health-checks) by adding an `observe` parameter to a `server` line. You can monitor at the TCP or HTTP layer.

Circuit breaker is implemeted using a passive health check. A backend that develops problems should automatically stop receiving traffic.

### Connection queueing

An early warning sign of a server with deteriorating health is **queue length**. Queue length is the number of sessions in HAProxy that are waiting for the next available connection slot to a server. Rather than simply failing when there are no servers ready to receive connections, HAProxy queues clients until a one becomes available.

Giving feedback to downstream components about the health of a server is known as **backpressure**. It’s a mechanism for letting the client react to early warning signs, such as by backing off

### Automatic retries

Automatic retries is a mechanism built into HAProxy, which let you attempt a failed connection or HTTP request again. When HAProxy receives a request, but can’t establish a TCP connection to the selected backend server, it automatically tries again after an interval set by `timeout connect`. Retrying is an intrinsically optimistic operation: It expects that calling the service a second time will succeed, which is perfect for transient errors such as those caused by a momentary network disruption. Retries do not work as well when the errors are long-lived, such as those that happen when a bad version of the service has been deployed.

With HAProxy 2.0 you can trigger retries on certain events. The `retry-on` directive lets you list other kinds of failures that will trigger a retry and covers both Layer 4 and Layer 7 events. For example, if messages time out after the connection has been established due to network latency or because the web server is slow to respond, retry-on tells HAProxy to trigger a retry.

### Circuit breaker

A circuit breaker is more pessimistic. After errors exceed a threshold, it assumes that the disruption is likely to be long-lived. Using retries carelessly could result in creating a Denial of Service (DoS) attack within your own service. As a service fails or performs slowly, multiple clients might repeatedly retry failed requests. That creates a dangerous risk of exponentially increasing traffic targeted at the failing service. To protect clients from continuously calling the faulty service, the circuit breaker shuts off access for a specified period of time. The hope is that, given enough time, the service will recover.

Unlike active health checks, a circuit breaker monitors live traffic for errors, so it will catch errors in any part of the service. You can [implement a circuit breaker](https://www.haproxy.com/blog/circuit-breaking-haproxy/#implement-a-circuit-breaker-the-simple-way) to monitor live traffic for detecting errors.

You can also use the HAProxy [agent-check](http://cbonte.github.io/haproxy-dconv/2.0/configuration.html#5.2-agent-check) that runs independently of a regular health check to trigger the circuit breaker. An agent check allows HAProxy to [guage health with an external agent](https://www.haproxy.com/fr/blog/using-haproxy-as-an-api-gateway-part-3-health-checks/). The external agent is a piece of software (.net e.g. https://github.com/LuccaSA/Haproxy.AgentCheck) running on the server that’s separate from the application you’re load balancing.

### Rate limiting

Rate Limiters are pretty dumb (they can be complex, but generally dumb). There is a threshold, anything above the threshold is limited. Thresholds are decided based on the capacity of the underlying service or based on your application requirements (like SLA: say 1 user makes 5 API calls max per minute). Sometimes even to thwart DoS.

Circuit breakers are more of resiliency patterns and more intelligent than Rate limiters. They ensure failure to one component of the system does not bring down the entire system by backing off for some time, assuming the backoff interval would suffice for the failure to heal/recover. When the 3rd party does not respond, you trip open the circuit on some percentage of failures and keep trying after some backoff interval. You close the circuit when 3rd party starts to respond again. Helps your system to be responsive and not hog resources when no work is being done downstream.

At what level do you need to have them - As usual, that depends. Generally, Rate limiters are your first line of defense to DDoS, and are implemented at the load balancer/Reverse proxy level. More application-aware thresholds can be placed in your reverse proxy, keeping them abstracted from the application.

Circuit breakers - use then when you making an unreliable call downstream, when the downstream can either take more time than you intend or you want your service to function for some time regardless of the 3rd party's availability. You can also use this to make your application responsive at the expense of the result of 3rd party. For example - if your downstream did not respond within 100ms with live results, you trip your circuit at 100ms and show the use older cached/default results.

You should not enable circuit breaking between your application and end users, since this could lead to a bad user experience. Use it between backend services, such as between proxied microservices.

## Monitoring

Keeping an eye on server health status is critical for knowing how many servers are passing the health-check probes that HAProxy sends. HAProxy publishes the up/down status of every server along with the pass/fail result of the most recent health check. For a basic quick view you can [enable the built-in HAProxy stats page](https://www.haproxy.com/blog/using-haproxy-as-an-api-gateway-part-4-metrics/)

You can also fetch the same metrics in a more programmatic way by using the [HAProxy Runtime API](https://www.haproxy.com/blog/dynamic-configuration-haproxy-runtime-api/). First, enable the API by adding a stats socket directive to the global section of your configuration. This exposes the API as a Unix socket located at `/var/run/haproxy.sock` so you can call it from scripts and programs running on the same machine:

```sh
global
    stats socket /var/run/haproxy.sock user haproxy group haproxy mode 660 level admin
```

You can also publish it on an IP address and port of your choosing so that you can access it remotely. In the following example, the API listens at localhost on port 9999:

```sh
global
    stats socket ipv4@127.0.0.1:9999 user haproxy group haproxy mode 660 level admin
```

* [Datadog haproxy dashboard](https://www.datadoghq.com/dashboards/haproxy-dashboard/) allows you to monitor frontend connections between the client and HAProxy, connections between HAProxy and your backend servers, and combined metrics such as error codes and server status.

* HAProxy 2.0 has native support for Prometheus, allowing you to export metrics directly by [enabling the built-in Prometheus endpoint](https://www.haproxy.com/blog/haproxy-exposes-a-prometheus-metrics-endpoint/) on HAProxy. You then [configure Prometheus](https://www.haproxy.com/blog/haproxy-exposes-a-prometheus-metrics-endpoint/#configuring-prometheus) to scrape the `/metrics` path
