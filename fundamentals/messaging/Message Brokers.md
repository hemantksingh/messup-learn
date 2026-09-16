# Message Brokers

What does a broker do, and how do queue brokers and log brokers differ?

A broker is the store-and-forward middle. Producers hand it messages and carry on; it keeps them until consumers are ready, routes them, fans them out and redelivers those that were not acknowledged. That is what buys the decoupling in [Messaging Fundamentals](Messaging%20Fundamentals.md). Queue brokers (RabbitMQ, Azure Service Bus, SQS) delete a message once it is consumed. Log brokers (Kafka, RabbitMQ Streams) keep an append-only log and let each consumer hold its own position in it.

## Protocols

The protocols under the common brokers:

* **AMQP** (Advanced Message Queuing Protocol), an open replacement for proprietary messaging middleware. AMQP 0-9-1 (the RabbitMQ exchange and queue model) and AMQP 1.0 (the ISO standard used by Azure Service Bus) are different, incompatible protocols; see [The AMQP 0-9-1 model](#the-amqp-0-9-1-model) below.
* **STOMP** (Simple/Streaming Text Oriented Messaging Protocol) more analogous to HTTP, see [stomp.github.io](https://stomp.github.io/).
* **MQTT** (originally MQ Telemetry Transport, no longer an acronym) specifically designed for resource-constrained devices and low bandwidth, high latency networks.
* Kafka uses its own binary [protocol](https://kafka.apache.org/protocol) over TCP to allow clients persistent connections for request pipelining.

## The AMQP 0-9-1 model

What most people mean by "AMQP" is the 0-9-1 model that RabbitMQ made popular. It has three entities: a producer publishes to an **exchange**; **bindings** are rules that say which **queues** an exchange forwards to; consumers read from queues. A binding carries a *binding key*; a message carries a *routing key*; the exchange type decides how the two are compared.

* **Direct**: deliver to queues whose binding key equals the routing key.
* **Fanout**: deliver to every bound queue, ignore keys.
* **Topic**: match the routing key against dotted patterns with `*` and `#` wildcards.
* **Headers**: match on message headers instead of the key (`x-match: all` or `any`).

AMQP **1.0**, the ISO standard used by Azure Service Bus and ActiveMQ, is a different protocol: no exchanges or bindings, just links between nodes. The two are not wire-compatible. RabbitMQ speaks both natively since 4.0.

## Queues versus topics

A **queue** delivers each message to one of its consumers. Several consumers on one queue compete for messages. A **topic** is publish-subscribe: every subscriber gets its own copy of every message.

The word "topic" means something different in each broker. In AMQP 0-9-1 it is an exchange type that routes by pattern, and fan-out is done by binding several queues to one exchange. In Kafka a topic is the partitioned log itself and each consumer group reads the whole of it. On AWS they are separate services, SNS for topics and SQS for queues, see [AWS Messaging](../../cloud/aws/Messaging.md). The common shape is a topic in front and a queue per consumer behind it.

## Queue brokers versus log brokers

Kafka is a *log-based message broker* different from AMQP/JMS-style traditional brokers. It combines the durable storage of databases with low-latency notification facilities of messaging. Databases as we know them are global shared mutable state, Kafka provides centralised immutable state based on a distributed append-only log.

Kafka topics are partitioned to scale beyond a single server, and partitions are replicated so that losing one node loses no data.

Kafka is a dumb broker with smart consumers: the consumer decides how far it has read (its offset in each partition) and when to commit that position. Since Kafka 0.9 (2015) committed offsets are stored broker-side in the `__consumer_offsets` topic rather than in ZooKeeper or the client. Kafka retains messages, consumed or not, for a configured time.

Kafka is a durable message store. This means clients can "replay" the event stream on demand as opposed to more traditional message brokers like RabbitMQ where even though messages are written to disk, once a message has been delivered, it is removed from the queue and deleted. This comparison applies to RabbitMQ's classic and quorum queues. RabbitMQ Streams (3.9, 2021) are an append-only, replayable log with retention policies, much closer to a Kafka topic.

Kafka supports **log compaction** using key based compaction of messages: of all the messages with the same key, only the most recent one is preserved. The other retention policy throws away data after a certain amount of time, e.g. keep only 2 weeks worth.

### Ordering and redelivery

AMQP or JMS style messaging systems, in order to guarantee message delivery, expect an acknowledgement from consumers after they have processed the message. In case the consumer crashes without sending the ack to the broker for message m1, the only option the broker is left with is to retry delivery of m1. Meanwhile the consumer could recover and process the next message m2. Depending upon when the retry occurs, the consumer could end up receiving m2 and then m1 (on redelivery). This results in **out-of-order arrival** of messages. Kafka avoids this within a partition: order is preserved per partition only (choose the partition key accordingly), and redelivery after a consumer crash is by re-reading from the last committed offset, so m1 and m2 are re-processed in order.

### Which to pick

As a heuristic, not a rule: for a disjointed job queue use case where order of execution of jobs is not important, AMQP and JMS style brokers are a good fit e.g.

* send email
* charge credit card

If the order of the messages is important Kafka is usually a better choice (RabbitMQ single active consumer and Azure Service Bus sessions also give ordering). e.g. a series of events that occur in sequence:

* user viewed a webpage
* customer purchased a product

## Stream processors

Because the log is durable and replayable, you can [turn the database inside out](https://martin.kleppmann.com/2015/11/05/database-inside-out-at-oredev.html) and move the data processing (querying) out of the data store into a distributed stream processor (e.g. Kafka Streams, Apache Flink). Instead of storing data, running ETL and querying later, you process the stream of facts as it arrives. The same log is a natural home for an event store, see [Event Sourcing and CQRS](Event%20Sourcing%20and%20CQRS.md); the pipeline side is in [Data Pipelines](../data/Data%20Pipelines.md).

## MSMQ (legacy)

Legacy (Windows and .NET Framework only). MSMQ is a store and forward queueing system with queues local to each communicating server. Unlike a centralised message broker (like RabbitMQ) where messages and queues are stored on a central or a clustered server that enables pub-sub, events based pub-sub is not supported in MSMQ because there is no central server; a bus library has to add it with its own subscription store.

MSMQ persists messages only if asked; the default is in memory. To have MSMQ persist messages to disk so they are not lost in a server crash you have to specify it on each message.

```csharp
MessageQueue msgQ = new MessageQueue(@".\private$\Orders");
msgQ.DefaultPropertiesToSend.Recoverable = true;
msgQ.Send("This message will be marked as Recoverable");
msgQ.Close();
```

## What a service bus library adds

You can drive a broker with its raw client. A bus library (NServiceBus, MassTransit, Rebus, Wolverine, CAP) sits on top and saves you writing the same code again:

* the outbox and idempotent-consumer plumbing that turn at-least-once delivery into "effectively once" (see [Messaging Fundamentals](Messaging%20Fundamentals.md#at-least-once-delivery-and-idempotent-consumers));
* routing of published messages to subscribers;
* retries with back-off, and polling back-off when a queue is quiet;
* acknowledgements and dead-letter queues for messages that keep failing;
* serialisation, message versioning, auditing;
* [sagas and process managers](Sagas%20and%20Process%20Managers.md).

Two cautions. Swapping transports is possible in theory but every broker differs in latency, ordering and operational behaviour, so treat it as a migration. And check the licence: NServiceBus has always been commercial, MassTransit v9 is commercial (v8 stays open source until the end of 2026), Rebus and Wolverine are open source. The MSMQ transport and the distributed transactions it allowed are legacy; MSMQ never came to modern .NET.

## How to rederive this

* A broker is a durable buffer plus a router. Everything else is policy on top.
* Delete on acknowledgement gives a queue. Keep the log and let the reader hold a cursor gives a log; replay follows.
* Ordering costs parallelism: one ordered stream is one consumer at a time, so partition by the key whose order matters.
* Redelivery to competing consumers can reorder; rewinding a cursor cannot.

## Sources

* RabbitMQ, [AMQP 0-9-1 model explained](https://www.rabbitmq.com/tutorials/amqp-concepts) and [Native AMQP 1.0 in RabbitMQ 4.0](https://www.rabbitmq.com/blog/2024/08/05/native-amqp)
* Martin Kleppmann, [Turning the database inside out](https://martin.kleppmann.com/2015/11/05/database-inside-out-at-oredev.html), Oredev 2015
* Apache Kafka, [protocol guide](https://kafka.apache.org/protocol)
* [STOMP specification](https://stomp.github.io/)
* Stack Overflow, [Is there any reason to use RabbitMQ over Kafka](https://stackoverflow.com/questions/42151544/is-there-any-reason-to-use-rabbitmq-over-kafka)
* DZone, [Understanding when to use RabbitMQ or Apache Kafka](https://dzone.com/articles/understanding-when-to-use-rabbitmq-or-apache-kafka)
* KTH thesis comparing message brokers, [full text](http://kth.diva-portal.org/smash/get/diva2:813137/FULLTEXT01.pdf)
