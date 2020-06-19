# Service bus frameworks

There maybe valid reasons for directly using the raw messaging system (RabbitMQ, Kafka, Azure Service Bus) client APIs, however [service bus frameworks provide an abstraction](https://stackoverflow.com/questions/25953891/why-do-we-need-service-bus-frameworks-like-nservice-bus-masstransit-on-top-of-me) over the underlying transport that may help you get started quickly and prevent writing duplicate code for:

* Transaction management between your domain database operations and queue persistence for message delivery guarantees
    * *exactly once* delivery using a distributed transaction. Distributed transactions [incur a significant overhead and are unreliable](http://www-db.cs.wisc.edu/cidr/cidr2007/papers/cidr07p15.pdf). Not all transports support distributed transactions. NServiceBus utilizes **DTC** to support [2PC XA transaction](https://dzone.com/articles/xa-transactions-2-phase-commit) with MSMQ transport.
    * *at least once* delivery using the [Outbox pattern](https://www.kamilgrzybek.com/design/the-outbox-pattern/). This may result in duplicate message delivery. Message [deduplication](https://en.wikipedia.org/wiki/Data_deduplication#Post-process_versus_in-line_deduplication) is required to achieve [idempotence](http://cap.dotnetcore.xyz/user-guide/en/cap/idempotence/) for redelivered messages that are not naturally idempotent.
    * *at most once* delivery
* Message distribution - Routing published messages to subscribed consumers
* Retry messages that fail to send or execute. Delayed retries to prevent overloading the consumer if it is not responding.
* Polling back off strategy. Polling consumers wait longer before trying to pull messages from a **table as queue** if there are no new messages on the queue.
* [Handling failures gracefully](https://medium.com/codait/handling-failure-successfully-in-rabbitmq-22ffa982b60f) by providing appropriate acknowledgements e.g. RabbitMq commands
    * ack - successfully processed
    * nack - [reject or requeue unprocessed message](https://stackoverflow.com/questions/28794123/ack-or-nack-in-rabbitmq)
    * dead-letter queue - hold messages that cannot be processed after specified number of retries.
* Serialization
* Monitoring, audit and message versioning.
* Support for long running transactions or process managers (sagas)

Service bus frameworks are built on top of multiple messaging systems or transports:

* http://cap.dotnetcore.xyz/user-guide/en/transports/general
* https://docs.particular.net/transports
* https://masstransit-project.com/usage/transports

The frameworks in theory provide reconfiguration of transports with API abstractions, but switching from one transport to the other requires careful consideration of latency, scalability and operational aspects because each transport is very different from the other.