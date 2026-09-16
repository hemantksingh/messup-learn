---
title: "Messaging Fundamentals"
summary: "Why send a message instead of making a call, which coupling it removes, and how the outbox and idempotent consumers make delivery reliable."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "Pat Helland, Life beyond Distributed Transactions, CIDR 2007"
  - "Jonathan Oliver, Idempotency patterns; How I avoid two-phase commit"
  - "Particular Software, Messaging versus RPC, store-and-forward messaging"
  - "Kamil Grzybek, The Outbox pattern"
  - "Webber, Parastatidis and Robinson, REST in Practice (2010), on Atom feeds for events"
tags: [messaging, coupling, transactional-outbox, idempotency, at-least-once]
---
# Messaging Fundamentals

Why send a message instead of making a call, and what can I rely on when I do?

REST and RPC based integrations are synchronous approaches that result in **in-band** blocking calls between services, therefore scalability and fault tolerance are hindered. Asynchronous messaging allows servers to be more stable in case a client crashes after sending the request but before the server sends a response. The server's resources are not tied up waiting until the connection times out. Collaboration between services can be implemented via asynchronous messaging or each service publishing REST based feeds of their events to be consumed by other services. Which broker carries the messages is a separate question, see [Message Brokers](Message%20Brokers.md).

## Coupling

A call couples two services in more than one way. Messaging removes one kind and leaves the others for you to design around.

* **Temporal coupling**: caller and callee must both be up at the same time for the call to succeed. A message removes it. The producer writes to a queue and carries on; the consumer reads when it is running. A queue is a buffer in time.
* **Behavioural coupling**: the consumer knows which event to react to and what to do about it. If the Payment service acts on `OrderPlaced`, every new client of Payment means a change to Payment, and a change to the event means a change to every consumer.
* **Ordering coupling**: a change in the order of business steps forces a consumer change. If an inventory check now has to happen before shipping, the Shipping service must listen for a different event from a different service.

The last two come from how a business process is spread over services and are the subject of [Sagas and Process Managers](Sagas%20and%20Process%20Managers.md).

## Domain and message persistence consistency

Adopting messaging between services requires you to give up on strict consistency and leads you towards [eventual consistency](../data/Consistency%20Models.md). **Durable messaging** adds more stability from regular [store-and-forward messaging](https://docs.particular.net/nservicebus/architecture/principles#messaging-versus-rpc-store-and-forward-messaging) as the messages are persisted to disk locally before attempting to be sent. But this means that your transactional persistence store used by a service to store domain entities and the persistence store backing the messaging infrastructure used for forwarding the messages published by a service must be consistent with each other to ensure **guaranteed message delivery** between services. If the domain change commits and the message is lost, or the message goes out and the domain change rolls back, the two stores disagree. Options are:

1. Domain model and messaging infrastructure share the same persistence store. This allows changes to the domain and adding new messages within a local transaction. An event store that also serves as the queue is one way to get this, see [Event Sourcing and CQRS](Event%20Sourcing%20and%20CQRS.md).

2. Domain model's persistence and messaging persistence store are controlled under a global XA transaction (two-phase commit). The coordinator becomes a lock held across the network. Pat Helland in his paper [Life beyond Distributed Transactions](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf) says *"Attempts to use distributed transactions are too fragile and perform poorly"*.

3. Create a special storage area (e.g. a database table) for messages in the same persistence store that is used by the Domain model. This is the **Transactional Outbox** pattern.

### The Transactional Outbox

Rather than the messaging mechanism controlling the message store, it is controlled by your service (bounded context). The domain change and the outbox row commit in one local transaction. An out-of-band (background process) **event forwarding** mechanism monitors the message store for new messages, publishes them through the messaging mechanism and then marks them as dispatched/published. The forwarder can poll the table or read the database's change log, which is [change data capture](../data/Data%20Pipelines.md).

![Transactional outbox: the service writes the domain row and the outbox row into its own database in one local transaction; a forwarder, polling the table or reading the change log (CDC), reads new outbox rows, publishes them to the broker and marks them dispatched; a crash marker between publish and mark is labelled duplicate from here, consumer must be idempotent, and the broker delivers to the consumer at least once](../images/transactional-outbox.drawio.svg "Transactional outbox and event forwarder")

The event forwarder could fail just before marking a message as dispatched (assuming no global transactions between the message store and the messaging mechanism persistence). When it recovers it will publish the messages again. So the outbox gives at-least-once delivery, and that enforces some constraints on consumers, like the ability to de-duplicate incoming messages.

## At-least-once delivery and idempotent consumers

Producers guarantee at least once delivery and consumers implement idempotency.

* **At least once delivery**: for reliable message delivery the messaging system will try to redeliver some messages for which it did not receive acknowledgement from the consumer, maybe because the consumer failed just after receiving the message. It does this because its only other recourse is to occasionally lose messages ("at most once messaging"). This results in the application having to deal with message retries and out-of-order arrival of some messages.

* **Message idempotency**: messages fall into 2 categories: those that affect the state of the recipient service and those that do not. The messages that do not cause change to the processing service are naturally idempotent. "Set balance to 50" is idempotent; "add 10 to balance" is not.

* **Deduplication, or remembering processed messages**: to ensure the idempotent processing of messages that are not naturally idempotent, the service must remember a message has been processed previously. This knowledge is state. The state accumulates as messages are processed. There must be some unique characteristic of the message (e.g. a message id) that is remembered to ensure it will not be processed more than once. Store the id in the same transaction as the domain change, otherwise a crash between the two puts you back where you started.

"Exactly once" in vendor material means this combination: at-least-once transport plus an idempotent consumer. The network never delivers exactly once; the consumer makes duplicates harmless.

## REST feeds instead of a broker

A service can publish its events as a time-ordered feed (Atom) that consumers poll, each keeping its own position. Polling moves the guaranteed delivery responsibility from the middleware to the consumer, and because the feed is ordered there is no out-of-order arrival. It trades latency for scalability and needs no broker. It suits reference data and events that may take seconds or hours to arrive, not low-latency notifications. See [Atom based pub-sub](../web%20and%20apis/REST.md#atom-based-pub-sub) in REST.

## Persisted background jobs

The same idea explains why "run it in the background" libraries such as Hangfire are reliable when `Task.Run` is not: the call is **serialised and written to a store** (SQL Server, Redis) and a worker dequeues and executes it with retries. If the process dies the job is still in the store. Whether the worker runs inside the web application or as a separate service is a hosting choice; in-process under IIS needs the application pool kept alive. On modern .NET the Generic Host with a `BackgroundService` is the standard way to host such a worker. The job store is a queue and the worker is a consumer, so a job may run twice: make it idempotent.

![A web application serialises the call and writes it as a job to a persisted job store, a database such as SQL Server or Redis. A worker dequeues, runs and retries the job; it is drawn twice, dashed inside the web process and solid in a separate worker process, because where it runs is a hosting choice. If the process dies the job is still in the store; the store is a queue and the worker a consumer, so a job may run twice and must be idempotent](../images/persisted-background-jobs.drawio.svg "Persisted background jobs")

## How to rederive this

* Two stores with a network between them: a crash can separate any two writes, so share one transaction or accept a retry.
* A retry means a duplicate, so the consumer must recognise a message it has seen. That needs an id and a place to remember it.
* A message removes the need for both parties to be up at once. It does nothing about who knows about whom.
* Polling an ordered feed is messaging with the consumer holding the cursor.

## Sources

* Pat Helland, [Life beyond Distributed Transactions](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf), CIDR 2007
* Jonathan Oliver, [Idempotency patterns](http://blog.jonathanoliver.com/idempotency-patterns/) and [How I avoid two-phase commit](http://blog.jonathanoliver.com/how-i-avoid-two-phase-commit/)
* Particular Software, [Messaging versus RPC, store-and-forward messaging](https://docs.particular.net/nservicebus/architecture/principles#messaging-versus-rpc-store-and-forward-messaging)
* Kamil Grzybek, [The Outbox pattern](https://www.kamilgrzybek.com/design/the-outbox-pattern/)
* Webber, Parastatidis and Robinson, *REST in Practice* (2010), on Atom feeds for events
