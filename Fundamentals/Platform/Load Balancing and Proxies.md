# Load Balancing and Proxies

Systems that are expected to grow over time need to be built on top of a scalable architecture. Such an architecture can support growth in users, traffic, or data size with no drop-in performance. It should provide that scale in a linear manner where adding extra resources results in at least a proportional increase in ability to serve additional load. Growth should introduce economies of scale, and cost should follow the same dimension that generates business value out of that system. While cloud computing provides virtually unlimited on-demand capacity, your design needs to be able to take advantage of those resources seamlessly. There are generally two ways to scale an IT architecture: vertically and horizontally.

## Vertical Scaling

Scaling vertically takes place through an increase in the specifications of an individual resource, such as upgrading a server with a larger hard drive or a faster CPU. With Amazon EC2, you can stop an instance and resize it to an instance type that has more
RAM, CPU, I/O, or networking capabilities. This way of scaling can eventually reach a limit, and it is not always a cost-efficient or highly available approach. However, it is very easy to implement and can be sufficient for many use cases especially in the short term.

## Horizontal scaling

Historically load balancers have been deployed as hardware on the edge in the data centre. Hardware load balancers like Citrix NetScaler Application Delivery Controller (ADCs) and F5 require proprietary, rack-and-stack hardware appliances. In order to scale, network load balancer hardware is typically over provisioned — in other words, they are sized to be able to handle occasional peak traffic loads. In addition, each hardware device must be paired with an additional device for high availability in case the other load balancer fails. This means that most load balancers stay idle until peak traffic times.

With a shift in cloud native and microservices architecture running on dynamic runtimes like kubernetes, the supporting application infrastructure needs to be more programmable and maintainable by cross functional teams. Software load balancers bridge the divide between NetOps and DevOps, they are simply installed on standard virtual machines. HAProxy and Nginx can both be used for load balancing your workloads across application servers. Both are covered below.

## Nginx

While Nginx is primarily a webserver it also provides layer 7 load balancing capabilities. Nginx started off as basic reverse proxy, created by *Igor Sysoev* while he was working as a sysadmin at Rambler (Russian equivalent of yahoo). He was looking at ways to improve Apache's performance. Due to the several inherent design choices Apache had the inability to handle more than 10k simultaneous users, commonly known as the **C10k problem**.

Nginx can address many use cases and provides all the tools for delivering your applications reliably with a low resource footprint. As a web server, it serves static content directly and reverse proxies to other application servers accepting TCP connections and making new TCP connections to upstream servers. As a caching engine it handles both static and dynamic content.

* Basic load balancer
* Reverse proxy and HTTP web server
* Serves static content very efficiently and reliably, using relatively little memory
* Set request limit (request rate) - Effective way to protect against DOS by blacklisting IP addresses. Possible to set the IPs in key value store. Also use Fail2ban.

In addition to the above **Nginx Plus** provides commercial load balancing, authentication, access control, application‑aware health checks and more configuration and monitoring options. It can be used alongside or as a replacement for hardware load balancers.

### Nginx and Apache

Apache is an HTTP server designed to serve static web pages. It can serve dynamic content using various technologies such as Java Servlets, JSPs, PHP, CGI, Python or whatever. It spins new threads as the server get busy, therefore ends up using more memory with each new connection. Performance asymptotically slows as you reach your server's limit.

Apache HTTP and Apache Tomcat can be used together through a connector module called `mod_jk`. This allows you to use the Apache HTTP server to serve regular static webpages, and the Tomcat Servlet engine to execute servlets.

Apache runs PHP or Python in  process and utilises *AppArmour* to elevate & downgrade privileges for 3rd party code. Nginx on the other hand runs 3rd party code in a contained environment - *jail* or *container* not in the Nginx process by default. Therefore you get a higher degree of isolation and a better security model with Nginx.

As well as performance, consider which web server you are more familiar with, while opting for one.

### Nginx as an API Gateway

For most microservices‑based applications, it makes sense to implement an [API Gateway](https://www.nginx.com/blog/building-microservices-using-an-api-gateway), which acts as a single entry point into a system. The API Gateway is responsible for request routing, composition, and protocol translation. It provides each of the application’s clients with a custom API. The API Gateway can also mask failures in the backend services by returning cached or default data.

An API gateway restricts access to your backend servers whereas [WAF](https://www.owasp.org/index.php/Web_Application_Firewall) - Web application firewall protects your application logic from layer 7 attacks including SQL injection, XSS, CSRF and more. It works as an intermediary between external users and web applications. While proxies generally protect a client machine’s identity by acting as an intermediary, WAFs protect servers.

Like hardware load balancers, WAFs have traditionally been in the realm of hardware appliances and suffered from the same shortcomings - cost and inflexibility to scale up and down. The Nginx WAF module is based on the widely used open source software **ModSecurity**. ModSecurity is a basic WAF module, if you need performance optimizations there are supported versions of ModSecurity available from F5. Nginx also provides a commercial WAF offering with [Nginx App Protect](https://www.nginx.com/products/nginx-app-protect/)

[IPS](https://www.lanner-america.com/blog/waf-vs-ips-whats-difference/) - Intrusion Prevention System is a layer 3/4 general purpose protection appliance or software. It provides protection from traffic from a wide variety of protocol types, such as DNS, SMTP, TELENT, RDP, SSH and FTP.

API gateways provide utility in dealing with some [specific concerns](https://www.nginx.com/blog/microservices-api-gateways-part-1-why-an-api-gateway) — such as authentication and rate limiting but business logic and process orchestration implemented in middleware, especially where it requires expert skills and tooling can lead to **overambitious API gateway** problems.

#### Access management and security control

* IP Access Control List (ACL) - `Allow` & `Deny` directives can be used to whitelist or blacklist IP addresses or subnet(s). **Failtoban** - dynamically manage blacklists.

* SSL/TLS offload with integration to Let's Encrypt - fully automated, free certificates trusted by 99% of browsers.

* Rate, connection and bandwidth limiting can help mitigate some forms of DDoS.

* HTTP Basic and [Authentication based on Subrequest result](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/) - proxy pass to external authentication service, such as LDAP or OAuth. If the auth server is HTTP based, the authentication setup is straight forward, but if your are going to authenticate against LDAP you'll have to write an HTTP to LDAP converter that generates an LDAP request from an HTTP request, authenticates with LDAP and returns the response as HTTP.

* JWT Token Based authentication - (exclusive to Nginx Plus) JWT Token once received by the client app from the JWT issuer (Identity provider) can be validated & parsed by Nginx. **Identity Propagation** - The relevant identity fields after being parsed, can be passed onto the upstream APIs as standard HTTP headers. Nginx can also perform authorization for certain endpoints that have restricted access e.g. admins, by inspecting the groups present in the token.

* NTLM proxying - (exclusive to Nginx Plus) Nginx interleaves requests across different connections to upstream servers in order to optimize traffic (HTTP2). NTLM requires each request to be sent over a different HTTP connection so that requests from different users are not interleaved on the same connection. By specifying `ntlm` directive Nginx does not interleave requests across connection(s).

### Nginx monitoring

* https://amplify.nginx.com is a SAAS based monitoring tool that provides real time monitoring, alerting and configuration checking - runs a bunch of tools to determine your configuration is safe e.g. SSL configuration. You can use NGINX Amplify for free on up to 5 servers. There is no trial period, so you can monitor those servers, for free, indefinitely.
* https://www.datadoghq.com/blog/how-to-monitor-nginx

### Operating Nginx

Nginx is a master process that reads the configuration and manages worker processes; the workers handle requests with non-blocking I/O, one worker per CPU core as a rule. `ps -ax | grep nginx` lists them.

The configuration file is `nginx.conf`; where it lives depends on how Nginx was installed (`/etc/nginx` for distribution packages, `/usr/local/etc/nginx` for Homebrew, `/usr/local/nginx/conf` for source builds). `nginx -V` prints the compiled-in path.

* Reload configuration without dropping connections: `nginx -t && nginx -s reload`. This re-reads the config and starts new workers; it does **not** load a new binary.
* Upgrade the binary without downtime: send `USR2` to the master to start a new master from the new binary, then `WINCH` and `QUIT` to the old one.
* Requests are matched by `listen` (address and port), then `server_name` (host header), then `location` (path). `default_server` is a parameter on `listen` that catches requests whose host matches no `server_name`.
* Logs default to `/var/log/nginx/access.log` and `/var/log/nginx/error.log`.

## HAProxy

HAProxy or High Availability proxy is the most popular open source software load balancer that provides high availability for TCP-based services. It is written in C and supports SSL termination, persistent connections, health checks, compression and more. It can be used as a load balancer, reverse proxy or application delivery controller

* Fast and lightweight proxy server and load balancer with a small memory footprint and low CPU usage.
  * Haproxy consistently [performs on par or better](https://www.datadoghq.com/blog/monitoring-haproxy-performance-metrics/) in benchmarks against other popular reverse proxies like http-proxy or the Nginx webserver. However Nginx [claim](https://www.nginx.com/blog/nginx-and-haproxy-testing-user-experience-in-the-cloud) to be more performant using *latency percentile distribution* as a metric.
* Protocol agnostic - it can handle anything sent over TCP
  * Haproxy can run in Layer 4 TCP mode and Layer 7 HTTP mode. In Layer 4 TCP mode, HAProxy forwards the RAW TCP packets from the client to the application servers. In the Layer 7 HTTP mode, HAProxy parses HTTP headers before forwarding them to the application servers.
  * Nginx only supports layer 7 HTTP mode. For load balancing services like LDAP, MYSQL if you want to use TCP mode, then you can use Nginx Plus or other web servers like Apache.
  * You can [configure Haproxy and Nginx to work together](https://www.howtoforge.com/tutorial/how-to-setup-haproxy-as-load-balancer-for-nginx-on-centos-7/) as a load balancer and web server.
* Only deals with the network and never touches the file system, therefore it cannot serve static content
* On CentOS 7, HAProxy is available in the default repository which makes it easy to install and configure.

### HAProxy configuration

The [HAProxy configuration file](https://www.haproxy.com/documentation/hapee/latest/onepage/) has [four essential sections](https://www.haproxy.com/blog/the-four-essential-sections-of-an-haproxy-configuration/):

* `global` define process-wide security and performance tunings
* `defaults` helps reduce duplication, its settings apply to all of the `frontend` and `backend` sections that come after it
* `frontend` defines the IP addresses and ports that clients can connect to
* `backend` defines a group of servers that will be load balanced and assigned to handle requests

#### Dynamic configuration

As services are containerised and become ephemeral, keeping your configurations up-to-date becomes a daunting task, especially in service mesh architectures. You can dynamically configure HAProxy using the

* TCP and Unix sockets based [Runtime API](https://www.haproxy.com/blog/dynamic-configuration-haproxy-runtime-api/). Since this is a TCP based API you can communicate with it [using telnet or socat](https://www.youtube.com/watch?v=JjXUH0VORnE). Changes made through the runtime API do not persist i.e. after making a change via the API if haproxy is restarted the changes will be lost.
* REST based [Data plane API](https://www.haproxy.com/blog/new-haproxy-data-plane-api/). This can be [installed](https://www.haproxy.com/documentation/hapee/latest/api/data-plane-api/installation/haproxy-community/) by downloading the Data Plane API binary from the GitHub repository.

### Resilience

Haproxy allows you to combine active health checks, retries and circuit breaking to get full coverage protection for your services.

Acting out real-world failure modes is the best way to test whether your system is resilient. What actually happens when you start killing web server nodes? What is the effect of inducing latency in the network? If a server returns HTTP errors, will downstream clients be affected and, if so, to what degree? Intentionally [injecting faults using chaos engineering](https://www.haproxy.com/blog/haproxy-layer-7-retries-and-chaos-engineering/) techniques, you begin to see exactly how HAProxy should be tuned.

#### Active health checks

Adding the `check` parameter to a `server` line in your HAProxy configuration, it pings that server to see if it's up  up and working properly. This can either be an attempt to connect over TCP/IP or an attempt to send an HTTP request and get back a valid response. If the ping fails enough times, HAProxy stops load balancing to that server.

If you’re load balancing web applications, then instead of monitoring a server based on whether you can make a TCP connection, you can [setup an HTTP based health check](https://www.haproxy.com/blog/using-haproxy-as-an-api-gateway-part-3-health-checks/) to monitor a specific URL.

```sh
backend apiservers
    balance roundrobin
    option httpchk GET /health
    server server1 192.168.50.3:80 check
```

Health checks target a service's IP and port or a specific URL, therefore active health checks monitor a narrow range of the service. They work well for detecting when a service is 100% down. But what if the error happens only when a certain API function is called, which is not monitored by the health checks? The health checks would report that the service is functioning properly, even if 70 or 80% of requests are calling the critical function and failing.

#### Pasive health checks

Active checks are easy to configure and provide a simple monitoring strategy. They work well in a lot of cases, but you may also wish to monitor real traffic for errors, which is known as passive health checking. In HAProxy, a passive health check is [configured](https://www.haproxy.com/blog/using-haproxy-as-an-api-gateway-part-3-health-checks/#passive-health-checks) by adding an `observe` parameter to a `server` line. You can monitor at the TCP or HTTP layer.

Circuit breaker is implemeted using a passive health check. A backend that develops problems should automatically stop receiving traffic.

#### Connection queueing

An early warning sign of a server with deteriorating health is **queue length**. Queue length is the number of sessions in HAProxy that are waiting for the next available connection slot to a server. Rather than simply failing when there are no servers ready to receive connections, HAProxy queues clients until a one becomes available.

Giving feedback to downstream components about the health of a server is known as **backpressure**. It’s a mechanism for letting the client react to early warning signs, such as by backing off

#### Automatic retries

Automatic retries is a mechanism built into HAProxy, which let you attempt a failed connection or HTTP request again. When HAProxy receives a request, but can’t establish a TCP connection to the selected backend server, it automatically tries again after an interval set by `timeout connect`. Retrying is an intrinsically optimistic operation: It expects that calling the service a second time will succeed, which is perfect for transient errors such as those caused by a momentary network disruption. Retries do not work as well when the errors are long-lived, such as those that happen when a bad version of the service has been deployed.

With HAProxy 2.0 you can trigger retries on certain events. The `retry-on` directive lets you list other kinds of failures that will trigger a retry and covers both Layer 4 and Layer 7 events. For example, if messages time out after the connection has been established due to network latency or because the web server is slow to respond, retry-on tells HAProxy to trigger a retry.

#### Circuit breaker

A circuit breaker is more pessimistic. After errors exceed a threshold, it assumes that the disruption is likely to be long-lived. Using retries carelessly could result in creating a Denial of Service (DoS) attack within your own service. As a service fails or performs slowly, multiple clients might repeatedly retry failed requests. That creates a dangerous risk of exponentially increasing traffic targeted at the failing service. To protect clients from continuously calling the faulty service, the circuit breaker shuts off access for a specified period of time. The hope is that, given enough time, the service will recover.

Unlike active health checks, a circuit breaker monitors live traffic for errors, so it will catch errors in any part of the service. You can [implement a circuit breaker](https://www.haproxy.com/blog/circuit-breaking-haproxy/#implement-a-circuit-breaker-the-simple-way) to monitor live traffic for detecting errors.

You can also use the HAProxy [agent-check](http://cbonte.github.io/haproxy-dconv/2.0/configuration.html#5.2-agent-check) that runs independently of a regular health check to trigger the circuit breaker. An agent check allows HAProxy to [guage health with an external agent](https://www.haproxy.com/fr/blog/using-haproxy-as-an-api-gateway-part-3-health-checks/). The external agent is a piece of software (.net e.g. https://github.com/LuccaSA/Haproxy.AgentCheck) running on the server that’s separate from the application you’re load balancing.

#### Rate limiting

Rate Limiters are pretty dumb (they can be complex, but generally dumb). There is a threshold, anything above the threshold is limited. Thresholds are decided based on the capacity of the underlying service or based on your application requirements (like SLA: say 1 user makes 5 API calls max per minute). Sometimes even to thwart DoS.

Circuit breakers are more of resiliency patterns and more intelligent than Rate limiters. They ensure failure to one component of the system does not bring down the entire system by backing off for some time, assuming the backoff interval would suffice for the failure to heal/recover. When the 3rd party does not respond, you trip open the circuit on some percentage of failures and keep trying after some backoff interval. You close the circuit when 3rd party starts to respond again. Helps your system to be responsive and not hog resources when no work is being done downstream.

At what level do you need to have them - As usual, that depends. Generally, Rate limiters are your first line of defense to DDoS, and are implemented at the load balancer/Reverse proxy level. More application-aware thresholds can be placed in your reverse proxy, keeping them abstracted from the application.

Circuit breakers - use then when you making an unreliable call downstream, when the downstream can either take more time than you intend or you want your service to function for some time regardless of the 3rd party's availability. You can also use this to make your application responsive at the expense of the result of 3rd party. For example - if your downstream did not respond within 100ms with live results, you trip your circuit at 100ms and show the use older cached/default results.

You should not enable circuit breaking between your application and end users, since this could lead to a bad user experience. Use it between backend services, such as between proxied microservices.

### Monitoring

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
