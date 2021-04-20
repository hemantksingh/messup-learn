# Asynchronous message‑based integration

REST and RPC based integrations are synchronous approaches that result in **in-band** blocking calls between services, therefore scalability and fault tolerance are hindered. They introduce **temporal coupling** i.e. previous calls must succeed before the next one can be made. Asynchronous messaging allows servers to be more stable in case a client crashes after sending the request but before the server sends a response. The server's resources are not tied up waiting until the connection times out. Collaboration between services can be implemented via asynchronous messaging or each service publishing REST based feeds of their events to be consumed by other services.

## Domain and message persistence consistency

Adopting messaging between services requires you to give up on strict consistency and leads you towards eventual consistency. **Durable messaging** adds more stability from regular [store-and-forward messaging](https://docs.particular.net/nservicebus/architecture/principles#messaging-versus-rpc-store-and-forward-messaging) as the messages are persisted to disk locally before attempting to be sent. But this means that your transactional persistence store used by a service to store domain entities and the persistence store backing the messaging infrastructure used for forwarding the messages published by a service must be consistent with each other to ensure **guaranteed message delivery** between services. Options are:

1. Domain model and messaging infrastructure share the same persistence store. This allows changes to the domain and adding new messages within a local transaction.

1. Domain model's persistence and messaging persistence store are controlled under a global XA transaction (two-phase commit). Pat Helland in his paper [Life beyond Distributed Transactions](http://www-db.cs.wisc.edu/cidr/cidr2007/papers/cidr07p15.pdf) says *"Attempts to use distributed transactions are too fragile and perform poorly"*

1. Create a special storage area (e.g. a database table) for messages in the same persistence store that is used by the Domain model. Rather than the messaging mechanism controlling the message store, it is controlled by your service (bounded context). An out-of-band (background process) **event forwarding** mechanism monitors the message store for new messages, publishes them through the messaging mechanism and then marks them as dispatched/published. The message store also has the ability to provide REST-based notification feeds for the messages. The event forwarder must be custom developed in order to send messages through the messaging mechanism and it could fail just before marking a message as dispatched (assuming no global transactions between the message store and the messaging mechanism persistence). When the event forwarder recovers it will end up publishing the messages again. This enforces some constraints on consumers, like the ability to de-duplicate incoming messages.

### Producers guarantee at least once delivery and consumers implement idempotency

* Message Idempotency - Messages fall into 2 categories: those that affect the state of the recipient service and those that do not. The messages that do not cause change to the processing service are naturally idempotent. http://blog.jonathanoliver.com/idempotency-patterns/

* At least once delivery - For reliable message delivery the messaging system will try to redeliver some messages for which it did not receive acknowledgement from the consumer, maybe because the consumer failed just after receiving the message. It does this because its only other recourse is to occasionally lose messages ("at most once messaging"). This results in the application having to deal with message retries and out-of-order arrival of some messages. To ensure idempotency (i.e. guaranteeing that processing of retried messages is harmless)  the recipient service is typically designed to remember that the message has been processed. http://blog.jonathanoliver.com/how-i-avoid-two-phase-commit/

* Deduplication of messages/ Remembering processed messages - To ensure the idempotent processing of messages that are not naturally idempotent, the service must remember a message has been processed previously. This knowledge is state. The state accumulates as messages are processed. To ensure each message is processed at-most-once there must be some unique characteristic of the message e.g. (message id) that is remembered to ensure it will not be processed more than once.

## Sagas & Process Mangers

There are occasions when a business process requires a flow of steps that need to execute in a particular order.

Order -> Payment -> Shipment

In SOA based architectures these steps are often encapsulated as separate services. Asynchronous event based collaboration is often used to decouple the communication between these services by publishing and consuming events.

Order (OrderPlaced) -> Payment (PaymentReceived) -> Order (OrderAccepted) -> Shipment (OrderShipped)

The above approach can still lead to **behavioral coupling** due to the fact that the Payment service needs to know about the OrderPlaced event, what if the payment also needs to be triggered from a different service? Every time a new client for the Payment service is introduced it will require a change to the Payment Service to process the incoming event. Therefore if the publishing service changes the published event, the consuming service needs to change too in order to process that event.

What if the order of the business flow changes? e.g. an inventory check now needs to be performed before shipping the goods.

Order (OrderPlaced) -> Payment (PaymentReceived) -> Order (OrderAccepted) -> Inventory (ItemFetched) -> Shipment (OrderShipped)

The above approach leads to **temporal coupling** and will require a change to the Shipping service as it will now need to process a different event, published from the Inventory service.

[Avoiding puristic event chains](https://www.infoq.com/articles/microservice-event-choreographies?utm_campaign=rightbar_v2&utm_source=infoq&utm_medium=articles_link&utm_content=link_text) is key to reducing such coupling between services and managing complexity in an event driven asynchronous model. The communication between the services can be routed through a centralized component - **saga** that tracks the progress of the overall business process and passes control to the next process or reacts to an event raised by a service.

OrderPlaced -> (Saga) Transformation -> CollectPayment -> Payment

A **saga** is a long lived business transaction or process. It needs to exist when a business process spans more than one service/domain or bounded context. Using a combination of orchestration and choreography for collaboration amongst services a saga can be used for

* **event command transformation** - Sagas listen to events and dispatch commands while services receive commands and publish events
* **handling long running processes** - Sagas use state machine to hold current status of the business process (e.g. an order status)

There is however now the danger of the saga becoming a central monolithic controller that becomes hard to change over a period of time, but if you treat the saga just as a means of keeping track of the status and the order of the business process, you can avoid that knowledge creeping into each individual service. This allows each service to evolve independent of its clients and the business process it supports and move towards a more decoupled design.

### Sagas and distributed transactions

Another approach to implement the business process is to wrap it into a distributed transaction spanning more than one service. This often involves going across a network (e.g. Http requests in RESTful services) and is not reliable because *Networks aren't reliable, they can and will fail.* How do you recover in case one of the requests fails?

Transactions work well when your resources are modelled within the same database. In a relational database consistency and isolation of transactions is handled by a transaction coordinator. If the transactions span more than one resource (for example 2 databases) consistency and isolation is achieved through a 2 phase commit. If you happen to do transactions over Http, it is time to rework your domain model because you are no longer dealing with SQL.

<blockquote>“If you find yourself in need of a distributed transaction protocol, then how can you possibly say that your architecture is based on REST? I simply cannot see how you can get from one situation (of using RESTful application state on the client and hypermedia to determine all state transitions) to the next situation of needing distributed agreement of transaction semantics wherein the client has to tell the server how to manage its own resources.

...for now I consider "rest transaction" to be an oxymoron.” - Roy Fielding</blockquote>

Pat Helland in his paper [Life beyond Distributed Transactions](http://www-db.cs.wisc.edu/cidr/cidr2007/papers/cidr07p15.pdf) says *"Attempts to use distributed transactions are too fragile and perform poorly"*

Sagas are conceptually similar to a distributed transaction coordinator (DTC) but avoid locking transactions across multiple resources. As opposed to a DTC, Sagas offer resilience by compensating state rather than rolling back changes in case of a failure and the changes made to a resource state are visible externally.

### Implementing Sagas

* http://blog.jonathanoliver.com/cqrs-sagas-with-event-sourcing-part-i-of-ii/

* https://blog.bernd-ruecker.com/what-are-long-running-processes-b3ee769f0a27

* Udi Dahan's [Saga Persistence in Event Driven Architecture](http://udidahan.com/2009/04/20/saga-persistence-and-event-driven-architectures/) - https://particular-1.wistia.com/medias/a2h268abx8

## Choosing a messaging system

Open source messaging systems e.g. RabbitMQ, Apache Kafka, Apache ActiveMQ, and NSQ. Underlying messaging protocols

* AMQP - (Advanced Message Queuing Protocol) designed as an open replacement for existing proprietary messaging middleware
* STOMP - (Simple/Streaming Text Oriented Messaging Protocol) more analogous to HTTP https://docs.nats.io/
* MQTT - (Message Queue Telemetry Transport) specifically designed for resource-constrained devices and low bandwidth, high latency networks
* Kafka uses its own binary [protocol](https://kafka.apache.org/protocol) over TCP to allow clients persistent connections for request pipelining.

### Kafka

Kafka is a *log-based message broker* different from AMQP/JMS-style traditional brokers. It combines the durable storage of databases with low-latency notification facilities of messaging. Databases as we know them are global shared mutable state, Kafka provides centralized immutable state based on a distributed append-only log. This allows you to [turn the database inside out](https://martin.kleppmann.com/2015/11/05/database-inside-out-at-oredev.html) and move the data processing (querying) out of the data store into a distributed stream processor (e.g. Apache Samza - developed at LinkedIn, Apache Storm). As opposed to storing your data in a database, running ETL functions and querying it later, you can take the streams of facts as they come in, and functionally process them in real-time. Layered on top of Kafka distributed stream processors provide simple but powerful tools for joining streams and managing large amounts of data reliably.

### Kafka and RabbitMQ

Kafka stores events in categories called topics which are partitioned so that these topics can scale beyond a single server. These partitions are replicated across multiple nodes in case if one node goes down, the data is not going to be lost. RabbitMQ sends messages via exchanges to queues to which consumers bind to retrieve the messages.

Kafka employs a dumb broker and uses smart consumers to read its buffer. This means the onus is on the consumer to keep track of messages that it has read in the past (by tracking their location in each log - consumer state). Kafka cluster retains all published messages - whether or not they have been consumed for a configurable amount of time.

Kafka is a durable message store and provides some database like ACID guarantees. This means clients can "replay" the event stream on demand as opposed to more traditional message brokers like RabbitMQ where even though messages are written to disk, once a message has been delivered, it is removed from the queue and deleted. Such message brokers are not suitable for long-term data storage. However, RabbitMQ is often used with Apache Cassandra to support durable storage and stream history, or with the LevelDB plugin for applications that need an “infinite” queue, but neither feature ships with RabbitMQ itself.

Kafka supports **log compaction** (state snapshots) using key based compaction of messages for content beginning in time. If each message has a key, then of all the messages with the same key, only the most recent one is preserved. The other compaction throws away data after certain amount of time. This works well for events tracking type data e.g. if you want to keep only 2 weeks worth of data.

AMQP or JMS style messaging systems in order to guarantee message delivery, expect an acknowledgement from consumers after they have processed the message. In case the consumer crashes without sending the ack to the broker for message m1, the only option the broker is left with is to retry delivery of m1.  Meanwhile the consumer could recover and process the next message m2. Depending upon when the retry occurs, the consumer could end up receiving m2 and then m1 (on redelivery). This results in **out-of-order arrival** of messages. Fundamentally Kafka does not suffer from this issue as it uses a time ordered event log to store messages.

Therefore for disjointed job queue use case where order of execution of jobs is not important AMQP and JMS style brokers are a good fit e.g.

* send email
* charge credit card

However if the order of the messages is important Kafka is a better choice. e.g. a series of events that occur in sequence:

* user viewed a webpage
* customer purchased a product

#### References

* https://stackoverflow.com/questions/42151544/is-there-any-reason-to-use-rabbitmq-over-kafka
* https://dzone.com/articles/understanding-when-to-use-rabbitmq-or-apache-kafka
* http://kth.diva-portal.org/smash/get/diva2:813137/FULLTEXT01.pdf

### MSMQ

MSMQ (native to Windows) is a store and forward queueing system with queues local to each communicating server. Unlike a centralised message broker (like RabbitMQ) where messages and queues are stored on a central or a clustered server that enables pub-sub, events based pub-sub is not supported in MSMQ because there is no central server. NServiceBus does provide pub-sub capability with MSMQ by using its own persistence for managing publishers and subscribers.

MSMQ is a persistent queueing solution, but not by default. The default is to store messages in memory. To have MSMQ persist messages to disk so they are not lost in case of a server crash you have to specify it on each message.

```csharp
MessageQueue msgQ = new MessageQueue(@".\private$\Orders");
msgQ.DefaultPropertiesToSend.Recoverable = true;
msgQ.Send("This message will be marked as Recoverable");
msgQ.Close();
```