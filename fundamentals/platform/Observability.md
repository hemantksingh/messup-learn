# Observability

Distributed systems give scalability and resilience but add complexity. [Monitoring](https://www.catchpoint.com/observability-vs-monitoring) began as watching a server's CPU and memory; it grew into observing user experience and finding the root cause of slowdowns with traces and logs.

Knowing the `what`, `when` and `why` of something happening in a running system is hard. The question the page answers:

> How is the software behaving for real users, right now?

Reading the codebase gives a mental model of what may happen. It is slow and rarely enough. Observability answers from the system's outputs instead.

## What observable systems provide

Monitoring tells us the overall health of our systems. Observability lets us infer the internal state of something from the outside, without reading its source, so we can respond to outages and *debug the system in production*. An observable system answers three questions from its telemetry alone:

* What is going wrong?
* Why is it going wrong?
* How well is the system performing against the business objectives?

Two principles follow. Know the `what` and `when` from telemetry and alerts before customers tell you. Find the `why` without referring to the code, by putting enough context in the telemetry that the system can be interrogated with observability tooling alone.

## Signals: logs, metrics and traces

Telemetry comes in three signals. They overlap, but [each has a different purpose](https://www.reddit.com/r/devops/comments/9hku3v/prometheus_vs_opentracing):

* Logs: *what happened in my system?* Discrete events with detail, written at the point where something happened.
* Traces: *how are system components interacting with each other?* One trace follows a single request across processes as a tree of timed spans, so it shows latency and bottlenecks end to end.
  * Example tools: AWS X-Ray, Jaeger, Zipkin, Grafana Tempo.
* Metrics: *how does system performance change over time?* Numbers aggregated over time: CPU, memory, error rates, response times. They give the overall health and trend view.
  * Example tools: CloudWatch Metrics, Prometheus; Grafana visualises them but does not store them.

The trade-off between them: metrics are cheap to store, aggregated and kept longest, so they are the basis for alerts and service level objectives. Traces carry the most context per request but are sampled and cost more to collect. Logs sit between. Most systems use all three and correlate them through shared identifiers such as a trace id.

## OpenTelemetry

[OpenTelemetry](https://opentelemetry.io/docs/) (OTel) is the vendor-neutral way to emit all three signals. It defines an API and SDKs for instrumenting code, a wire protocol (OTLP) and a Collector that receives, processes and exports telemetry to whichever backend you choose. Instrumentation libraries in the application export to a local Collector by default; the Collector forwards to Prometheus, Jaeger, Grafana, a cloud service or a commercial vendor. Switching backends is then a Collector configuration change, not a code change.

OTel superseded two earlier projects, OpenTracing and OpenCensus, both now archived. Tooling has followed: Jaeger v2 is built on the OTel Collector and the Jaeger client libraries were retired in favour of the OTel SDKs; Datadog's dd-trace supports the OTel API; Azure Monitor and AWS each ship their own OTel distribution.

## Logging

Error logs tell developers what went wrong in their applications. User event logs give product managers insights on usage. (Jay Kreps' essay [The Log](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) is about a different log, the append-only record behind databases and brokers.)

For application logging in distributed systems:

* **Structured logging**: log JSON or key-value pairs, not free text, so machines can parse and query. Include timestamp, level and context.
* **Centralised logging**: aggregate logs from all services in one place for searching and correlation.
* **Standard log levels**: define INFO, WARN and ERROR once and document when to use each.
* **Contextual information**: include application state, request and response details and user ids so a request can be followed across services. Log at architectural boundaries: entry and exit points such as API endpoints and calls to external services or databases, and the points where business decisions send execution down different paths.
* **Handling errors**:
  * Log failures with the exception stack trace, but distinguish what is logged from what is returned to the user. A stack trace reveals internals: the encryption algorithm, server paths, whether input is sanitised, how objects are referenced, the database brand and version. Log the detail; give the user only enough to recover.
  * Centralise error handling in an exception filter or middleware and let exceptions bubble up to it, for consistent responses and log messages.
  * Follow [exception guidelines](https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions): for example, wrap third-party exceptions in your own when the originals mean nothing to your consumers.

### Centralised log management

Plain text log entries are good for humans to read but not for machines to process. Reading log files by hand across VMs, containers and serverless functions becomes unmanageable. For alerting, auditing and searching, logs need to be **structured** and **centralised**.

**Syslog** is the standard on Unix-like systems. It separates the software that generates messages, the system that stores them and the software that reports on them, and tags each message with a facility code and a severity level. Modern Linux ships `systemd`, whose `journald` collects and stores logs. It is not a Syslog implementation but is compatible: it listens on the same `/dev/log` socket and exposes facility and severity as journald fields.

A **SIEM** is a security application first: real-time threat analysis over logs, automated. A log management system collects logs; it can be used for security but that is not its purpose. Choose by the question you need answered.

### Log shipping

Getting logs off hosts is a small data pipeline (see [Data Pipelines](../data/Data%20Pipelines.md)) with a fixed shape: a **shipper** on each host tails files or reads journald and forwards; an **aggregator** parses, enriches and buffers; a **store** indexes; a dashboard **visualises**.

* Logstash and Fluentd receive Syslog and collect, filter, buffer and route logs between many sources and destinations. On Kubernetes the common shippers are Fluent Bit (the lighter sibling of Fluentd, both CNCF projects) and the OpenTelemetry Collector, which carries logs alongside metrics and traces (see [OpenTelemetry](#opentelemetry)).
* Durability is a setting: Logstash defaults to an in-memory queue, so switch on its persistent on-disk queue if you cannot afford to lose logs on a crash. It does not need Redis in front for that.
* Elastic's Beats (Filebeat, Metricbeat) remain supported, but Elastic steers new deployments to the single Elastic Agent managed through Fleet.
* Logging libraries such as *NLog* and *Serilog* write structured logs through a target-agnostic API: the same logging call can go to console, file, database or cloud with configuration alone.

"ELK" is the Elastic Stack (Elasticsearch, Logstash, Kibana). Its licence changed away from Apache 2.0 in 2021, which produced the OpenSearch fork; check the current licence terms before choosing either.

## Tracing

Call stacks show the flow of execution in a monolith: method A called B, which called C. That breaks when the call crosses a process boundary and is no longer a reference on the local stack. [Distributed tracing](https://learn.microsoft.com/en-us/azure/azure-monitor/app/distributed-trace-data) gathers the timing data needed to troubleshoot latency in microservice architectures.

Tracers live in your applications and record timing and metadata about operations that took place.

* They intercept application calls to record how long a request took and report this **out-of-band**, outside the request pipeline, to the tracing system for storage.
* They show pain points in a request's path through visualisations like flame graphs, which carry error and latency data per span.
* Traces are also data. Span attributes can be queried and aggregated, not just drawn; the OTel Collector's spanmetrics connector derives rate, error and latency metrics from spans.

Two open source backends, both descended from [Google's Dapper](https://research.google.com/pubs/pub36356.html) paper:

* [Zipkin](https://zipkin.io/pages/architecture.html), from Twitter, accepts trace data over HTTP, gRPC or Kafka (Scribe is legacy). The collector validates, stores and indexes it for lookup.
* [Jaeger](https://www.jaegertracing.io/docs/), a CNCF graduated project since 2019. Version 2 is built on the OpenTelemetry Collector; instrument with OTel SDKs, not the retired Jaeger clients. Jaeger exposes its own metrics in Prometheus format.

A service mesh emits traces for the traffic it proxies without application changes (see [Kubernetes](Kubernetes.md)).

## Metrics

Metrics contain the data that inform you about the state of your systems, which lets you see patterns and course correct. Are customers using the new feature? Did traffic drop after that last deployment? If there is an error, how long has it been happening and how many customers were affected?

Individual metrics per resource (network in and out, CPU, volume IO) help, but for laterally scaled web and database tiers an aggregation across all instances is more useful.

[Prometheus](https://prometheus.io/) is an open source metrics and alerting tool, with Grafana for dashboards. Nagios, Icinga and Sensu suit host, network and service checks, the classical sysadmin tasks. To see the internal state of each service (white-box monitoring) Prometheus is the better fit. It works on a **pull model**:

* Client libraries in your application define metrics and expose their current values on an HTTP endpoint, `/metrics`. The Prometheus server scrapes each instance on a schedule and stores the time series. Docker and Kubernetes components expose the same format natively.
* Short-lived batch jobs may not live long enough to be scraped. They push to a [Pushgateway](https://github.com/prometheus/pushgateway), which holds the values for Prometheus to scrape.
* [Exporters](https://prometheus.io/docs/instrumenting/exporters/) translate metrics from systems you cannot instrument (HAProxy, Linux system stats) into the Prometheus format.
* **PromQL** queries the server; Grafana runs those queries to draw dashboards; Alertmanager routes alerts fired by rules.

[PromCat](https://promcat.io/) by Sysdig packages exporters, dashboards and alert rules per integration; [Thanos](https://thanos.io) adds high availability and long-term storage to Prometheus.

**Cardinality**: each distinct combination of label values is a separate time series. A label holding user ids or GUIDs multiplies the series count and can take a Prometheus-style store down. High-cardinality attributes belong on trace spans and log events, which are stored per record; metric labels stay low-cardinality (service, endpoint, status code). The richer the dimensions on a span, the more questions it can answer later, so put the context there.

## Deciding what healthy means

Ideas from Google's [Site Reliability Engineering](https://sre.google/) that this page depends on.

* A **service level indicator** (SLI) is a measurement of one aspect of service from the user's side: the fraction of requests that succeed, the fraction served under 300 ms. A **service level objective** (SLO) is the target for an SLI over a window, such as 99.9% success over 30 days. The **error budget** is the gap between the SLO and perfection. While the budget is intact the team ships freely; when it is spent, reliability work takes priority. This dissolves the tension between "ship more" and "break less", and it tells you which alerts deserve attention: the ones that burn budget.
* **Alert on symptoms, not causes.** Page on what the user experiences, error rate and latency against the SLO, not on CPU being high or a queue being long. Causes belong on dashboards for diagnosis; a symptom alert catches causes you did not predict.
* **Post-mortems** are blameless: action items come from facts about the system, not from who touched it. A **pre-mortem** asks the same questions before the change.
* **Drain and roll back** beats debugging under fire. To roll back you must know the previous state, so record it before changing anything.
* Capacity has to allow for hostile load (DDoS) and routine risk (a router firmware upgrade), not only expected traffic.

Practical points for alerting:

* Know which metrics come for free. Cloud managed services provide most by default; on IaaS such as EC2, CPU comes by default but memory and disk usage need an agent on the instance.
* Avoid noise. Configure sensible log levels. Do not set aggressive thresholds; tune them to prevent false positives, and fire one alert for many errors of the same kind.
* Do not normalise errors. "Expected alerts" hide the genuinely unexpected.
* Make alerts actionable. There is no point in an alert the receiver cannot act on; link it to a runbook.
* Dashboards say what is being looked at and what good and bad look like, and evolve as the product changes.

**Real user monitoring and synthetics.** Synthetics are scripted probes (a browser script or an API call) run from outside on a schedule: black-box monitoring that checks uptime even when no user is active. Real User Monitoring (RUM) is telemetry from actual user sessions, so it reflects real devices, networks and paths. Neither is white-box monitoring, the term for metrics exposed by the system's internals.

## Tooling

Open source: Prometheus for metrics, the Grafana stack (Loki for logs, Tempo for traces, Mimir for metrics, Grafana for dashboards), Jaeger for traces, OpenSearch for log search. Commercial platforms covering all signals: Datadog, Splunk AppDynamics, Dynatrace, New Relic.

## How to rederive this

* Start from the question "how is the software behaving for real users?" and ask what output would answer it: an event (log), a number over time (metric) or a request's path (trace).
* Anything stored per record can carry rich context; anything stored as a time series pays per label combination. That decides where high cardinality goes.
* Pull versus push follows from lifetime: a long-running process can be scraped, a short-lived job must push.
* An alert is worth paging on only if a user could notice the condition; everything else is a dashboard.
* An SLO is just an SLI with a target and a window; the error budget is what is left.

## Sources

* Google, [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/), chapters on monitoring distributed systems and service level objectives.
* [OpenTelemetry documentation](https://opentelemetry.io/docs/).
* [Prometheus documentation](https://prometheus.io/docs/introduction/overview/).
* Sigelman et al., [Dapper, a Large-Scale Distributed Systems Tracing Infrastructure](https://research.google.com/pubs/pub36356.html), Google, 2010.
* Jay Kreps, [The Log: What every software engineer should know about real-time data's unifying abstraction](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying), 2013.
