# Logging

Plain text log entries are really good for humans to read, but not so good for machines to process. Manually reading log files in a distributed architecture with logs from disparate applications that may be running on VMs, containers or serverless infrastructure, quickly becomes unmanageable. In order to be automatically processed for alerting, auditing, searching and efficient sorting, logs need to be **structured** and **centralised** for machine readability.

Logging libraries like *nlog* and *serilog* help in writing structured logs and allow log centralisation by providing target agnostic logging APIs e.g. use the same logging interface to push logs to console, file, db, cloud etc with minimal configuration.

## Tracing

Tracers live in your applications and record timing and metadata about operations that took place. They intercept application calls to record how long a request took to process and asynchronously report this info **out-of-band** (outside the application request pipeline) to the tracing system for storage.

[Zipkin](http://zipkin.io/pages/architecture.html) is an open source distributed tracing system from Twitter based on [Google's Dapper](https://research.google.com/pubs/pub36356.html) paper and supports various transports like HTTP, Kafka , Scribe. It helps gather timing data needed to troubleshoot latency problems in microservice architectures. Adopting an open instrumentation standard like [Opentracing](https://opentracing.io/docs/overview/) allows language agnostic monitoring capabilities as opposed to native instrumentation with Application Performance Management (APM) service like *AppInsights*

## Application monitoring

Ingesting all the log data from different sources only makes sense if you can connect the dots and get meaningful information about the state of your applications. From production monitoring to security concerns, it is critical for businesses to analyze and review their log data for monitoring and observability. Three of the most popular log management platforms are:

* https://www.splunk.com/
* https://www.sumologic.com/
* ELK stack (Elasticsearch, Logstash, and Kibana) with different hosted offerings:
    * https://cloud.elastic.co/
    * https://logit.io/

While Splunk is a one stop solution for all your infrastructure and application monitoring needs, it comes at a price. You may not need all the operation intelligence features that it provides. While the ELK stack provides a rich API for developers to integrate with, Sumo Logic provides a better search facility.

Some other options for application logging and monitoring include:

* https://prometheus.io/ - Open source monitoring for containerised applications with Grafana integration for visualization
* https://www.datadoghq.com/
* https://www.graylog.org/
* https://raygun.com/
* [New Relic](https://newrelic.com/)

## Container monitoring

* Metrics Server - Prometheus is the most popular metrics server for containerised applications. Prometheus metrics format is used by the server to store and read the metrics. Docker runtime itself provides metrics in Prometheus format.
* Metrics Visualizer - Used to build the dashboard by querying the metrics server. You can query the server using Prometheus query language - PromQL and plug those queries into Grafana.
* Metrics provider - run in each container and on each docker host. Client libraries are available for adding instrumentation to your application code.

## Logging and exception handling

### What to log?

The quality of the design and code structure affects the quality of your logs. Public Apis with coarse grained interfaces are important logging boundaries. However, identifying where to log in fragmented APIs that expose internal state can be a tricky. Logging application state (generally held in DTOs in statically typed languages) at various stages can be useful for debugging purposes.

### When to log?

Consider logging at the following stages within your application.

* Entry and exit points of the application. (API endpoints, Outgoing network calls, DB interactions).
* Boundaries where crucial business decisions are made in the code and the execution flow can take multiple paths.
* Error and failure situations with the exception stack trace. It is crucial to understand what is returned as part of the response to the end user. A stack trace can reveal the internals of your application like
  
    * what encryption algorithm you use
    * what some existing paths on your application server are
    * whether you are properly sanitizing input or not
    * how your objects are referenced internally
    * what version and brand of database is behind your front-end

This makes it easy for an attacker to understand the inner workings of your application and makes it vulnerable for attacks. Therefore log as much information as possible in the logs for failures but give away just enough information back to the user for them to recover from failures.

### Exception guidelines

According to [Microsoft design guidelines for exceptions](https://msdn.microsoft.com/en-us/library/ms229014(v=vs.80).aspx)

* Controlling application flow through exceptions is another form of GOTO statement. Exceptions are exceptional scenarios, therefore throwing exceptions should be a decision made with a lot of consideration.

* Distinguish between recoverable situations and failures (exceptions). If there is a known situation that can be recovered from, without the end user receiving an exception, you should make an effort to handle it and return an appropriate error message with a recovery mechanism rather than just an exception failure.

* Consider throwing framework exceptions rather than custom exceptions where ever possible.

* Handle exceptions at entry points to your application, unless there is a specific behaviour like a retry operation is intended.

* Try catch finally blocks are like Transaction. Catch/finally should leave the application in a consistent state no matter what happens in the try block.

* Use interception to wrap 3rd party libraries and manage their exceptions by declaring your own if the underlying exception wouldn't be meaningful to your consumer's app. However, always ensure to specify the inner exception while wrapping the exception. This allows capturing the full stack trace and can help in debugging code.

```csharp
public void SendMessages()
{
    try
    {  
        EstablishConnection();
    }
    catch (System.Net.Sockets.SocketException e)
    {
        throw new CommunicationFailureException(
            "Cannot access remote computer.", e);
    }
}
```

### Checked exceptions

Violate the Open/Closed principle. If the handling of the exception (catch) is 3 levels above, then either a an explicit throw or catch must be declared at each level between the method invocation with the checked exception and the top level handler.