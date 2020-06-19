# Distributed Databases

Stateless applications can be scaled relatively easily by adding more servers, that means if your website gets more traffic you add more servers. But databases are inherently difficult to scale because they are stateful. Generally you solve this problem by getting a bigger machine that has higher resources and multiple cores, but the laws of physics allow you to fit only so many transistors on a chip. The other way to scale your database is by partitioning the data functionally or via sharding over multiple databases. As compared to a monolithic database, in a distributed database you have suddenly lost

* Secondary indexes
* Foreign key constraints
* Query optimization, possibly in favour of key value lookups
* Joins

All of this work does not just vanish but is now done by your application.

Consistency in the database and distributed systems world can be viewed in terms of

* Consistency in ACID context means application correctness in terms of business behaviour e.g. bank account balance cannot be negative.
* Consistency models
* CAP theorem

## ACID

Application consistency is enforcing the rules that keep the aggregate (group of properties that change together) consistent. e.g. if the quantity of an order changes, the order amount will also need to change for it to be consistent.

Smaller aggregates can perform and scale better, they are also more likely to be transactionally consistent with lesser chances of concurrent conflicts during a commit. If you happen to keep multiple aggregates consistent through a single transaction by folding multiple aggregates into a bigger aggregate, it is time to relook at the use case and assess if it can be fulfilled using eventual consistency.

### Serializability

*Serializability is not about doing one thing at a time but the effect of what you did is like you did one thing at a time.*

Result of executing a set of transactions is equivalent to executing those transactions one at a time, in some serial order. Each transaction might be executed concurrently but, serializability  guarantees the final result will be the same. This allows us to reason about the transactions in a serial order without having to worry about their concurrent execution. That complexity is taken care by the database.

Serializability != serial execution

Serializability comes at a cost - Concurrency control: Locking and coordination

## Consistency models

![consistency-models.png](../Images/consistency-models.PNG "Consistency Models")

### Strict consistency or Linearizability

Reads and writes execute in a total order that matches time. Just like running your code on a single thread in a single processor. Linearization makes things simple because the order in which events happen is **totally ordered**. It's cheaper and a reasonable thing to be doing. Majority of the systems can be linearized.

**Total ordering** is an ordering that defines the exact order of every element in the series.

**Partial ordering** of elements in a series is an ordering that doesn't specify the exact order of every item, but only defines the order between certain key items that depend on each other.

For example if you have three events `{A, B, C}`, then they are totally ordered if they always have to happen in the order `A > B > C`. However, if A must happen before C, but you don't care when B happens, then they are partially ordered. In this case we would say that the sequences `A > B > C, A > C > B, and B > A > C` all satisfy the partial ordering.

Reasons for non-linearization:

* Loosely connected systems (example is Git) When you prefer availability over consistency. For consistency these systems might use **causal consistency** and [conflict resolution](https://www.youtube.com/watch?v=yCcWpzY8dIA&t=506s).
* When you have low latency and high throughput requirements.
* In general, external consistency (linearizability) requires **monotonically increasing timestamps**.

### Eventual consistency

**CAP Theorem** - Eric Brewer, a professor at the University of California, Berkeley, and cofounder and chief scientist at Inktomi proposed Off the three properties of shared data systems only two can be achieved at a given time.

* Consistency - Client perceives that a set of operations has occurred all at once, Consistency here means linearizability.
* Availability - Every operation must terminate in an intended response.
* Partition tolerance - Operations will complete, even if individual components are unavailable.

In large scale distributed-scale systems, network partitions are a given and
partition tolerance is a failure model i.e. sometimes your servers are not going to be able to talk to each other (it may decide to do garbage collection and pause) and sometimes you won't know how long they wont be able to talk to each other. It is not possible to decide if the server is delayed or faulty.

Given that partition tolerance is rarely achievable therefore, there really are 2 choices **consistency** or **availability**

Relaxing consistency will allow the system to remain highly available under partitionable conditions, whereas making consistency a priority means that under certain conditions (while performing a distributed transaction involving a 2 phase commit that involves locks and coordination) the system will not be available.

Do not show the users the same data that they have changed.
Identify transactions that always need to be  consistent.
Stay out of the newspapers.  Avoid globalised widespread failure by compromising the architecture. Localised failure for a certain user is less frequent and can be accommodated as the cost of doing business.

## Google Spanner paper

https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf

[Spanner, True Time & The CAP Theorem](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45855.pdf)

Spanner claims to be a CA system but technically it is a CP system i.e. in case of some partions, Spanner chooses Consistency and forfiets Availability. It does not guarantee 100% availability but rather something like 5 or more "9s" (1 failure in 10^5 or less)

**TrueTime** is a global synchronized clock with bounded non-zero error: it returns a time interval that is guaranteed to contain the clock’s actual time for some time during the call’s execution. Thus, if two intervals do not overlap,
then we know calls were definitely ordered in real time. If the intervals overlap, we do not know the actual order. The TrueTime API uses inputs from GPS & atomic clocks to calculate a bound of time for when an event occurred. Based on this they are able to have **total ordering** in the system.

Spanner gets its *serializability* from locks, but it gets its external consistency (similar to *linearizability*) from TrueTime.

*We believe it is better to have application programmers deal with performance problems due to overuse of transactions as bottlenecks arise, rather than always coding around the lack of transactions.*

### *Overuse of transactions = bottlenecks*

This is not only true across a network on a distributed db (2 phase commit coordination costs) but also across CPU cores on a single multicore db (serialization and cache line transfers costs).
