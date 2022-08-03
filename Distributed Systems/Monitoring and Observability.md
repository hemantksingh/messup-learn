# Monitoring and Observability

While event driven distributed systems provide scalability and resilience, they also introduce complexity. Understanding the `what`, `when` and `why` something happens in the system is hard. We provide value to customers as they use our software systems. So we would like to answer the question:

> How is your software doing when exercised by real users?

We can extrapolate a mental model of what may happen by reading the codebase. This is rarely efficient or even, enough. This is where observable software systems come in handy. With observability, we can understand how our software is working. And we do this by evaluating its outputs.

## What do observable systems provide ?

Monitoring enables us to understand the overall health of our systems, observability allows us to infer the internal state of something from the outside. How do we know that our application is working well and doing what it is supposed to do without having to look inside or access its source code?With observable systems we are able to answer the following questions by querying the telemetry outputs of our systems:

* What is going wrong?
* Why is it going wrong?
* How well is the system performing against our business objectives?

As outlined in the [observability pyramid](https://medium.com/geekculture/monitoring-microservices-part-1-observability-b2b44fa3e67e) observability empowers us with detailed insights into the behavior of our systems through `telemetry data` such as `traces`, `metrics`, and `logs`. While all of them partially overlap, [each has a different purpose](https://www.reddit.com/r/devops/comments/9hku3v/prometheus_vs_opentracing).

## Logging

Logs answer the question - *what happened in my system*?

Error logs tell developers what went wrong in their applications. User event logs give product managers insights on usage. If the CEO has a question about the next quarter’s revenue forecast, the answer ultimately comes from payment/CRM logs.

Apache Kafka Architect Jay Kreps starts with the question - "What is the log?" and has written about [storing and processing log data](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying). For steps before storing and processing data you need a [unified logging layer](https://www.oreilly.com/content/the-log-the-lifeblood-of-your-data-pipeline/) - a pluggable architecture that can take data input from various sources and output the data to multiple destinations.

### What to log?

Building applications requires you to think about what to log? The quality of the design and code structure affects the quality of your logging code. Public APIs with coarse grained interfaces are important logging boundaries. Consider logging

* Entry and exit points of the application e.g. API endpoints, outgoing network calls, DB interactions.
* Boundaries where crucial business decisions are made in the code and the execution flow can take multiple paths.
* Application state (generally held in DTOs in statically typed languages) at various stages can be useful for debugging purposes.
* Error and failure situations with the exception stack trace. It is crucial to understand what is returned as part of the response to the end user. A stack trace can reveal the internals of your application like
  
  * what encryption algorithm you use
  * what some existing paths on your application server are
  * whether you are properly sanitizing input or not
  * how your objects are referenced internally
  * what version and brand of database is behind your front-end

This makes it easy for an attacker to understand the inner workings of your application and makes it vulnerable for attacks. Therefore log as much information as possible in the logs for failures but give away just enough information back to the user for them to recover from failures.

Centralize error handling and logging within your application to provide consistent error responses and formatted log messages. In an HTTP API this can be done in an exception filter or middleware

* Allow application to bubble up all exceptions up to the exception filter or middleware
* Use [exception guidelines](https://msdn.microsoft.com/en-us/library/ms229014(v=vs.80).aspx) for exception handling e.g. define your own exceptions to wrap 3rd party library exceptions if they aren't going to mean anything to the consumers of your app

### Centralized log management

Plain text log entries are really good for humans to read, but not so good for machines to process. Manually reading log files in a distributed architecture with logs from disparate applications that may be running on VMs, containers or serverless infrastructure, quickly becomes unmanageable. In order to be automatically processed for alerting, auditing, searching and efficient sorting, logs need to be **structured** and **centralized** for machine readability.

#### Syslog

Standard logging solution on Unix-like systems that allows centralizing of info from the kernel and running programs for auditing, security and monitoring of application behaviour. It has a standard for message logging that allows separation of the software that generates messages, the system that stores them and the software that reports and analyzes them.

Journald - Modern linux distributions are shipped with the service manager `systemd` which introduces `journald` for collecting and storing logs. The journald service is not a Syslog implementation, but it is Syslog compatible since it will listen on the same `/dev/log` socket. It will collect the received logs and allow the user to filter them by facility code and/or severity level using the equivalent journald fields (SYSLOG_FACILITY, PRIORITY)

#### SIEM and log management

SIEM systems are security applications first and foremost, while log management systems like Syslog are primarily designed for collecting log data. A log management system can be used for security purposes, but it’s more complicated than what it’s worth. If you want a tool that will help you gather all of your logs in one place, choose a log management system. If you need to use logs to manage security for a large or diverse IT infrastructure, choose a SIEM system.

Another [key differentiation](https://www.n-able.com/blog/siem-vs-log-management) is that SIEM is a fully automated system, while log management is not. SIEM features real-time threat analysis, while log management does not. For MSPs, the solution you choose will largely depend on what you have the means, personnel, and time to accomplish. What’s more important is that you have a system in place to analyze your customers’ logs and are able to craft a cybersecurity plan based on that information.

### Log collection

Log forwarders like Logstash and Fluentd can receive Syslog messages and ship them to a central log aggregator. They can collect, filter, buffer and output logs across multiple sources and destinations.

Logging libraries like *nlog* and *serilog* help in writing structured logs and allow log centralisation by providing target agnostic logging APIs e.g. use the same logging interface to push logs to console, file, db, cloud etc with minimal configuration.

## Tracing

With tracing the question you're looking to answer is - *How are system components interacting with each other*?

Debugging distributed microservices poses a challenge in understanding and reasoning about the overall system interactions. Call stacks are used to debug monoliths showing the flow of execution (Method A called Method B, which called Method C), but how do we bug when the call is across a process boundary, not simply a reference on the local stack? This is where [distributed tracing](https://docs.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing) comes in. It helps in gathering timing data needed to troubleshoot latency problems in microservice architectures.

Tracers live in your applications and record timing and metadata about operations that took place. 
* They intercept application calls to record how long a request took to process and asynchronously report this info **out-of-band** (outside the application request pipeline) to the tracing system for storage.
* They can help in identifying pain points in a request's execution path using visualizations like [flame graphs](https://www.datadoghq.com/knowledge-center/distributed-tracing/flame-graph/#what-is-a-flame-graph) that include error and latency data to help developers identify and fix bottlenecks in their applications. I


Adopting an open instrumentation standard like [Opentracing](https://opentracing.io/docs/overview/) and [Opencensus](https://opencensus.io/) (both now part of [Opentelemetry](https://opentelemetry.io/)) allows language agnostic monitoring capabilities.

* [Zipkin](http://zipkin.io/pages/architecture.html) is an open source distributed tracing system from Twitter based on [Google's Dapper](https://research.google.com/pubs/pub36356.html) paper and supports various transports like HTTP, Kafka , Scribe for pushing the tracing data to a Zipkin collector. Once the trace data arrives at the Zipkin collector daemon, it is validated, stored, and indexed for lookups by the Zipkin collector.

* [Jaeger](https://github.com/jaegertracing/jaeger) is an open source distributed tracing system. Similar to Zipkin, it's been inspired by the Google Dapper paper and complies with OpenTelemetry. By default, [Jaeger exposes tracing metrics in the Prometheus format](https://www.jaegertracing.io/docs/1.17/monitoring/#metrics) so they can be made available to other tools. Jaeger joined CNCF in 2017 and has recently been elevated to CNCF's highest level of maturity, indicating its widespread deployment into production systems.

* [Appinsights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing#enable-via-opencensus) also supports distributed tracing through OpenCensus - an open source, vendor-agnostic, single distribution of libraries to allow collecting application **metrics** and **distributed traces**, then transfer the data to a backend of your choice in real time. This data can be analyzed by developers and admins to understand the health of the application and debug problems.

## Metrics

Metrics answer the question - *How does the system performance change over time* ?

Metrics contain the data that inform you about the state of your systems, which in turn allows you to see patterns and make course corrections as needed. Metrics give you essential feedback about how well, or unwell, things are going: Are customers using the new features? Did traffic rates drop after that last deployment? If there’s an error, how long has it been happening and how many customers have likely been affected?

[Prometheus](https://prometheus.io/) is an open source monitoring tool focussed on metrics and alerting with Grafana integration for visualization. Tools like Nagios/Icinga/Sensu are suitable for host/network/service monitoring, classical sysadmin tasks. Nagios, for example, is host-based. However, if you want to get internal detail about the state of each of your micro-services (aka whitebox monitoring), Prometheus is a more appropriate tool.

* Metrics Server - Prometheus is the most [popular metrics server for containerised applications](https://sysdig.com/blog/kubernetes-monitoring-prometheus/). Docker runtime itself provides metrics in Prometheus format. Prometheus metrics format is used by the server to store and read the metrics.
* Metrics Visualizer - Used to build the dashboard by querying the metrics server. You can query the server using Prometheus query language - **PromQL** and plug those queries into Grafana.
* Metrics providers/ Metrics sources
  * Set of client libraries for adding instrumentation to your application code. This lets you define and expose internal metrics via an HTTP endpoint `/metrics` on your permanently running application’s instance. When Prometheus scrapes your instance's HTTP endpoint, the client library sends the current state of all tracked metrics to the server.
  * Instrumented services: Occasionally you will need to monitor components which are ephemeral. The [Prometheus Pushgateway](https://github.com/prometheus/pushgateway) allows you to push time series from short-lived service-level batch jobs to an intermediary job which Prometheus can scrape. Since these kinds of jobs may not exist long enough to be scraped, they can instead push their metrics to a Pushgateway. The Pushgateway then exposes these metrics to Prometheus.
  * [Exporters](https://prometheus.io/docs/instrumenting/exporters/) enable exporting existing metrics from third-party systems as Prometheus metrics. This is useful for cases where it is not feasible to instrument a given system with Prometheus metrics directly (for example, [HAProxy exporter for Prometheus](https://www.haproxy.com/blog/haproxy-exposes-a-prometheus-metrics-endpoint/) or Linux system stats).

Implementing a reliable Prometheus monitoring system requires a tight integration between metrics sources (exporters, instrumented services or instrumentation libraries for your applications), Prometheus metrics collection (service discovery, jobs, filtering and relabeling or recording rules), dashboards and alerts. Making all of these different pieces work together is strenuous and requires a significant amount of effort to set up and maintain over time. [Pomcat](https://promcat.io/) by Sysdig brings all the prometheus monitoring resources together including:

* Prometheus and third-party exporters, packaged as container images with deployment manifests for Kubernetes.
* Both Grafana and Sysdig dashboards
* Both AlertManager and Sysdig PromQL alerts definition.
* Recording rules, in order to pre-calculate metrics when you have tons of them.

[thanos.io](https://thanos.io) is an open source, highly available Prometheus setup with long term storage capabilities.

Depending upon your monitoring requirements, if you need to analyse both metrics and tracing data, then you may decide to [deploy tracing and metrics solutions together](https://developers.redhat.com/blog/2017/07/10/using-opentracing-with-jaeger-to-collect-application-metrics-in-kubernetes) as opposed to a standalone analysis backend.

## Principles

There are two core principles when it comes to building observable software systems.

### Aim for knowing the what and when something is happening

At cinch, we don't expect stakeholders or customers to tell us when something is not quite right with our software. By querying our telemetry data in production, we can find out `what` is happening and `when`. We have alerts that notify us when something is not performing as expected.

System instrumentation and alerting are configured. to ensure that engineers are aware of unexpected behaviour before customers are affected by it.

### Aim for finding out the why without referring to the code

It's easy to be happy with knowing the `what` and `when`. We aim to add as much context to our telemetry data as possible. We want to be able to answer the `why` without referring to the codebase.

System instrumentation provides sufficient transparency. Its behaviour can be interrogated and understood using Observability tooling only.

## Best practices

Teams build observable systems. To do this, teams routinely follow good monitoring and observability practices. Below you'll find a collection of practices that align with the observability principles.

### Practice observability-driven development

Observability-driven development encourages us to consider how a system can be transparent from its inception. Thus providing meaningful and actionable insights into its behaviour.

#### Instrument with intent
Instrumentation uses patterns that allow for optimal aggregation. Essentially answering the unknown unknowns. Rather than only the known unknowns when we observe the system.

The benefit of this approach is two-fold:

The component - and as an extension, the software engineer that writes it - knows the most about what is going on during that invocation and the context around it to produce a useful telemetry dataset
All the useful information is applied - and indexed - at creation and ingestion time. No further optimization or transformation of the telemetry data is needced.

#### Instrument code as a primary concern
Instrumenting our code includes creating telemetry data while writing code. Our tooling provide both automated instrumentation and APIs to achieve this.

#### Define a component's service boundary
We aim to have a well-defined service boundary for our services across all our telemetry data. This way, we can query across all Datadog products efficiently.

#### Agree on our top-level tags
All telemetry data can benefit from having defined top-level tags. Some related to software, e.g. service, env, version. Others more business-specific, e.g. `order_id`, `user_id`, `product_id` etc.


#### Index valuable telemetry data

Not all telemetry data is available for a longer period of time. If in doubt, we index the things that matter. This way they are available to query for a longer period of time. Typically, between 15 days (for Indexed Spans) and 15 months (for Span tags converted to Metrics).

#### Aim for high dimensionality

The more dimensions a telemetry data point has, the better. The more key value pairs your telemetry data point has, the richer the dataset. You will will be more likely to understand both the what and the why in any future investigation.

#### Aim for high cardinality

A tag that has high cardinality, is more useful than a low cardinality tag. A key value pair that has GUID values, will offer far more insights than a boolean tag would. An illustrative example is a GUID vehicle_id vs a boolean has_vehicle.

#### Ingest native metrics from 3rd parties

We use 3rd party native metrics where possible. For example, AWS Lambda metrics will provide some good top-level statistics. These that can be used for Dashboards, Monitors, and SLOs.

#### Don't settle on aggregations

Metrics are useful but often omit valuable details. Prefer trace span tags or logs where possible over metrics. This allows us to aggregate in ways that we want.

#### Use traces as data

A common miss perception about traces is that they are useful for the flame graphs. Flame graphs visualize the journey of a certain request. Using traces as contextualized data is more valuable. Traced data often represent invocations of both backend and frontend requests.

#### Prefer traces over metrics

Traces will always provide us with more context over metrics. Metrics will tell you the what, traces will tell you the what and the why.

#### Prefer Real User Monitoring over Synthetics

Browser and API synthetics do provide the traditional uptime health check type monitoring. However, synthetics are part of the so-called 'Black Box Monitoring'. Real User Monitoring (RUM) data - called 'White Box Monitoring' - provides richer data. It is data ceatedr by users. Instead of 'synthetically' created data when using Synthetics.

#### Consider industry standards

Follow industry standards where possible. For example, our recommended tracing library, dd-trace, is OpenTracing compatible. We strive to instrument our code using the OpenTelemetry standard going forwards. OpenTelemetry is a merger between OpenCensus and OpenTracing, and is part of Cloud Native Computing Foundation.

### Optimise for awareness

Observability-driven development and good instrumentation helps to create observable systems. Data is useless without curious people. We need to couple with this with an immense amount of curiosity.

#### Think about customer affecting failure modes

Strive to come up with and understand the various failure modes of our system. Technical failures that may show reliability are good indicators. Prefer to think about failures that may affect customers .

#### Be keen and curious observers

Our software systems produce rich telemetry data all the time. For the system to be observable whether a change is being made to the system or not, we act as keen and curious observers. We do this by routinely utilizing telemetry to understand and rationalize how the system is behaving internally.

#### Proactively monitor production

The more we query our telemetry data, the more familiar we become with our production systems. By doing this,we get better at gaining insights. We spend time with our squad understanding the various metrics.

#### Surface insights

We routinely investigate the various telemetry data. We automate insights into things that matter. We do this by creating Datadog Monitors or SLOs. We surface these insights on our squad's dashboards.

#### Minimize time to acknowledge

Our software is independently deployable by teams. We operate a 'build it, ship it, support it' model. It should be quick to identify the what and the why of an issue in production. We aim to minimise the time to acknowledge an issue by using efficient alert mechanisms.

#### Evolve meaningful monitors and dashboards

Monitors and dashboards are not useful unless they have collective meaning for our domain and software system. Aim to create and evolve meaningful monitors, SLOs and dashboards

#### Monitor what matters

It's easy to fall into the trap of adding an alert for everything we own. We collectively agree on what matters for the service our software is providing. We use Datadog Monitors to get notified about the things that matter.

#### Avoid normalising errors

Beware of the trap of "expected alerts" and "expected errors". Do not normalise errors as this can hide genuine system unexpected behaviour.

#### Continuously evolve dashboards

A team's product aims and goals evolve over time. We evolve dashboards over time alongside the squad's and product's evolution.

#### Use dashboards as focal points

We use dashboards as focal points at stand ups, stand downs or product feature reviews. By doing this we gain insightful feedback from our code running in production. Dashboards serve as a place where all the squad's important queries are collected. They are used collaboratively within the squad and across squads.

Note that we avoid creating dashboards because stakeholders asked for them. Or even to 'dashboard-gaze'.

#### Dashboards are self-contained

Provide contextual information in dashboards to explain what they are looking at. Indicate what "good" or "bad" looks like and what they should expect to see.

#### Decide on the metrics that matter

A domain will always have some metrics that are more important than others. We strive to understand what they are and figure out how to measure them via observability.

####  Contextualize service level

We strive to understand what service our software component is offering. One way to measure this is by using Service Level Indicators. We then use Service Level Objectives to contextualize the service level. Not all alerts from Datadog Monitors are worthy of our attention. Having an error budget helps us understand when an alert requires real attention.

* Distinguish between metrics available by default e.g. cloud managed services will provide most metrics by default, however for IAAS e.g. in EC2 instances CPU utilization may come up by default but memory utilization and disk usage will require installing an agent on the instance.
* Avoid information overload and noise
  * Configure appropriate logging levels within your application
  * Avoid configuring aggressive alerts. Adjust your alarm threshold to prevent false positives. Only trigger a single alert for multiple errors of the same kind.
* Configure actionable alerts. There is no point informing someone about an issue if they do not know how to deal with the issue. Depending upon the type of issue the alerting notification can have a link to a wiki article or a run book to fix the problem at hand.

## Application monitoring

Ingesting all the telemetry data from different sources only makes sense if you can connect the dots and get meaningful information about the state of your applications. From performance monitoring to security monitoring, it is critical for businesses to analyze and review their telemetry data for monitoring and observability. Three of the most popular log management platforms are:

* https://www.splunk.com/
* https://www.sumologic.com/
* ELK stack (Elasticsearch, Logstash, and Kibana) [Elastic APM agents](https://www.elastic.co/guide/en/apm/agent/dotnet/current/intro.html) automatically measures the performance of your application and tracks errors. The agent auto-instruments and records events, like HTTP requests and database queries. ELK is available in different hosted offerings:
    * https://cloud.elastic.co/ 
    * https://logit.io/

While Splunk is a one stop solution for your infrastructure, security and application monitoring needs, it comes at a price. You may not need all the operational intelligence that it provides. The ELK stack provides a rich API for developers to integrate with, Sumo Logic provides a better search facility.

You can consider [open source APM options](https://techbeacon.com/enterprise-it/5-open-source-apm-tools-compared) or [APM vendors listed by Gartner](https://www.gartner.com/reviews/market/application-performance-monitoring):

* https://www.appdynamics.com/
* https://www.dynatrace.com/
* https://newrelic.com
* https://www.datadoghq.com/
* https://raygun.com/

### OpenTelemetry

With the rise of many different APM (Application Performance Monitoring) vendors, developers want flexibility in choosing vendor backends to visualize their metrics, such as Grafana, Splunk, Amazon CloudWatch, Azure Monitor and others. This flexibility also drives a need for unity within the realm of observability. The [OpenTelemetry](https://opentelemetry.io/docs/) project aims to provide that support by defining a new open standard—the OpenTelemetry Protocol (OTLP) for collecting traces, metrics, and logs. The OpenTelemetry Collector (OTel Collector) can be deployed as an agent on each host within an environment and configured to send telemetry data to the user’s desired back-end(s). OpenTelemetry instrumentation libraries should then be added to each application. By default, these instrumentation libraries are configured to export their data to a locally running Collector. Optionally, a pool of Collector instances can be deployed in a region.

AWS has built its own [AWS-supported distribution of OpenTelemetry](https://aws.amazon.com/blogs/opensource/building-a-reliable-metrics-pipeline-with-the-opentelemetry-collector-for-aws-managed-service-for-prometheus/) to integrate with AWS managed Prometheus
