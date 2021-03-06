# Logging

Application logging requires you to think about

## What to log?

The quality of the design and code structure affects the quality of your logging code. Public APIs with coarse grained interfaces are important logging boundaries. Consider logging

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

## Centralized Log Management

Plain text log entries are really good for humans to read, but not so good for machines to process. Manually reading log files in a distributed architecture with logs from disparate applications that may be running on VMs, containers or serverless infrastructure, quickly becomes unmanageable. In order to be automatically processed for alerting, auditing, searching and efficient sorting, logs need to be **structured** and **centralized** for machine readability.

### Syslog

Standard logging solution on Unix-like systems that allows centralizing of info from the kernel and running programs for auditing, security and monitoring of application behaviour. It has a standard for message logging that allows separation of the software that generates messages, the system that stores them and the software that reports and analyzes them.

Journald - Modern linux distributions are shipped with the service manager `systemd` which introduces `journald` for collecting and storing logs. The journald service is not a Syslog implementation, but it is Syslog compatible since it will listen on the same `/dev/log` socket. It will collect the received logs and allow the user to filter them by facility code and/or severity level using the equivalent journald fields (SYSLOG_FACILITY, PRIORITY)

### SIEM and log management

SIEM systems are security applications first and foremost, while log management systems like Syslog are primarily designed for collecting log data. A log management system can be used for security purposes, but it’s more complicated than what it’s worth. If you want a tool that will help you gather all of your logs in one place, choose a log management system. If you need to use logs to manage security for a large or diverse IT infrastructure, choose a SIEM system.

Another [key differentiation](https://www.n-able.com/blog/siem-vs-log-management) is that SIEM is a fully automated system, while log management is not. SIEM features real-time threat analysis, while log management does not. For MSPs, the solution you choose will largely depend on what you have the means, personnel, and time to accomplish. What’s more important is that you have a system in place to analyze your customers’ logs and are able to craft a cybersecurity plan based on that information.

### Log Collection

Log forwarders like Logstash and Fluentd can receive Syslog messages and ship them to a central log aggregator.

Logging libraries like *nlog* and *serilog* help in writing structured logs and allow log centralisation by providing target agnostic logging APIs e.g. use the same logging interface to push logs to console, file, db, cloud etc with minimal configuration.

## Tracing

[Tracing and metrics](https://opentelemetry.io/docs/) while partially overlap but [each have different purposes](https://www.reddit.com/r/devops/comments/9hku3v/prometheus_vs_opentracing/) and usecases. Depending upon your monitoring requirements, if you need to analyse both metrics and tracing data, then you may decide to [deploy tracing and metrics solutions together](https://developers.redhat.com/blog/2017/07/10/using-opentracing-with-jaeger-to-collect-application-metrics-in-kubernetes) as opposed to a standalone analysis backend.

Debugging distributed microservices poses a challenge in understanding and reasoning about the overall system interactions. Call stacks are used to debug monoliths showing the flow of execution (Method A called Method B, which called Method C), but how do we bug when the call is across a process boundary, not simply a reference on the local stack? This is where [distributed tracing](https://docs.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing) comes in. It helps in gathering timing data needed to troubleshoot latency problems in microservice architectures.

Tracers live in your applications and record timing and metadata about operations that took place. They intercept application calls to record how long a request took to process and asynchronously report this info **out-of-band** (outside the application request pipeline) to the tracing system for storage. 

Adopting an open instrumentation standard like [Opentracing](https://opentracing.io/docs/overview/) and [Opencensus](https://opencensus.io/) (both now part of [Opentelemetry](https://opentelemetry.io/)) allows language agnostic monitoring capabilities.

[Zipkin](http://zipkin.io/pages/architecture.html) is an open source distributed tracing system from Twitter based on [Google's Dapper](https://research.google.com/pubs/pub36356.html) paper and supports various transports like HTTP, Kafka , Scribe for pushing the tracing data to a Zipkin collector. Once the trace data arrives at the Zipkin collector daemon, it is validated, stored, and indexed for lookups by the Zipkin collector.

[Jaeger](https://github.com/jaegertracing/jaeger) is an open source distributed tracing system. Similar to Zipkin, it's been inspired by the Google Dapper paper and complies with OpenTelemetry. By default, [Jaeger exposes tracing metrics in the Prometheus format](https://www.jaegertracing.io/docs/1.17/monitoring/#metrics) so they can be made available to other tools. Jaeger joined CNCF in 2017 and has recently been elevated to CNCF's highest level of maturity, indicating its widespread deployment into production systems.

[Appinsights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing#enable-via-opencensus) also supports distributed tracing through OpenCensus - an open source, vendor-agnostic, single distribution of libraries to allow collecting application **metrics** and **distributed traces**, then transfer the data to a backend of your choice in real time. This data can be analyzed by developers and admins to understand the health of the application and debug problems.

## Metrics

Metrics are a key aspect of observability, along with logging and tracing. They contain the data that inform you about the state of your systems, which in turn allows you to see patterns and make course corrections as needed. Metrics give you essential feedback about how well, or unwell, things are going: Are customers using the new features? Did traffic rates drop after that last deployment? If there’s an error, how long has it been happening and how many customers have likely been affected?

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

## Application monitoring

Ingesting all the log data from different sources only makes sense if you can connect the dots and get meaningful information about the state of your applications. From production monitoring to security concerns, it is critical for businesses to analyze and review their log data for monitoring and observability. Three of the most popular log management platforms are:

* https://www.splunk.com/
* https://www.sumologic.com/
* ELK stack (Elasticsearch, Logstash, and Kibana) with different hosted offerings:
    * https://cloud.elastic.co/
    * https://logit.io/

While Splunk is a one stop solution for all your infrastructure and application monitoring needs, it comes at a price. You may not need all the operation intelligence features that it provides. While the ELK stack provides a rich API for developers to integrate with, Sumo Logic provides a better search facility.

Some other options for application logging and monitoring include:

* https://www.datadoghq.com/
* https://www.graylog.org/
* https://raygun.com/
* [New Relic](https://newrelic.com/)