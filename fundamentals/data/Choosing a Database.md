# Choosing a Database

Choose a datastore by the shape of the workload: how you write, how you read, how wrong an answer you can tolerate, how much you can lose. No store removes work. Each one decides which work it does for you (joins, transactions, consistency, durability) and which moves into your application.

## Questions to ask first

* **What is the mix of reads and writes?** A store is usually optimised for one. Reads scale with copies; writes need spreading over machines. Check how the engine handles concurrent writers.
* **Does the data fit on one machine?** In memory, almost anything is fast. On one disk, a single relational server is the simplest answer. Distribute only when it does not fit.
* **What are the access patterns?** A few primary key lookups: a key-value store may be enough. Joins and ad hoc questions: you want a query engine. If you have not partitioned on the keys you query by, you load everything and filter in the application.
* **Do you need authoritative answers, or availability?** Do you need transactions? What is your weird result tolerance? A stale basket count is fine; a stale bank balance is not. Consistency costs coordination, which costs latency and availability ([Consistency Models](../data/Consistency%20Models.md)).
* **How much loss can you tolerate?** Durability means the write is on disk before the server says "committed". Disk is slower than memory, so every store trades here. You could miss some writes to a logging store; you cannot miss an order.
* **What latency and availability do you need?** How many concurrent users? Can you accept downtime?
* **What does the team already run well?** A store you can operate at 3 a.m. beats a better fit nobody can debug.

## Scaling a relational database

A stateless application scales by adding servers. A database is stateful, so that does not work directly. The steps, cheapest first:

1. **Read replicas.** Asynchronous copies of the primary. They scale reads, not writes, and they lag: a client can write to the primary and not see its own write on a replica.
2. **Functional partitioning.** Different tables on different servers (orders here, catalogue there). Often lines up with service boundaries, but it is a data technique, not an architecture.
3. **Sharding.** Rows of one table split across servers by a key. This gives write capacity, and this is where the cost lands. You have lost:
   * secondary indexes across the whole dataset
   * foreign key constraints between shards
   * joins across shards
   * query optimisation, which collapses into key lookups
   * transactions that span shards

   This work does not vanish; your application now does it, or nobody does. Under range partitioning an auto-increment key is an anti-pattern: every new row lands on the last shard. Hashing the key spreads writes but loses range scans.

## Aggregate-oriented stores

Fowler and Sadalage call most NoSQL stores **aggregate-oriented**: the unit of storage is a whole aggregate, a group of data that changes together, not rows spread across tables. An order and its line items are one aggregate and travel together on every read and write. An aggregate lives on one node and needs no join, so it suits a cluster. It also removes the mismatch between objects in code and rows in tables.

The cost shows when you slice the data another way. Revenue by product needs line items from many orders grouped by product, so the root is now the product. A relational database rearranges data with a query. An aggregate store needs a second copy shaped for that question. Schemaless, but the schema is still there, implicit in the code that reads the aggregate.

| Category | Unit stored | Examples |
|---|---|---|
| Key-value | opaque value under a key | Redis, DynamoDB |
| Document | a structured document you can query into | MongoDB, Cosmos DB (multi-model), Couchbase |
| Wide-column | rows with a sparse, flexible set of columns | Cassandra, HBase, Bigtable |
| Graph | nodes and edges | Neo4j, Neptune |

The first three are aggregate-oriented. Graph is Fowler's fourth category but is not: small records, many connections.

An aggregate is a natural transaction boundary; these stores update one aggregate atomically. MongoDB, DynamoDB and Cosmos DB now also offer transactions across several documents or items, at higher latency and with size limits. Design around the aggregate first.

## Consistency is a dial

"NoSQL trades consistency for scale" is a slogan, not a property. Most of these stores default to eventual consistency and let you turn the dial up per operation: Cassandra lets each read and write say how many replicas must agree; DynamoDB offers strongly consistent reads; Cosmos DB has five levels from strong to eventual; MongoDB has read and write concerns up to majority and linearizable. Turning it up costs latency and availability during partitions ([Consistency Models](../data/Consistency%20Models.md)). Check the default.

## Durability

Check what an acknowledgement means: on one node's disk, or on a majority of nodes, before the client hears "ok"? MongoDB by default acknowledges a write once a majority of the replica set has journaled it. Redis is in-memory with two persistence modes. RDB snapshots alone are not durable; everything since the last snapshot is lost on a crash. The append-only file is: `appendfsync everysec` loses at most about a second, `always` fsyncs every write. Redis with snapshots only is a cache; with AOF it is not.

Redis snapshots by forking. The child shares the parent's pages copy-on-write; only pages changed during the save are duplicated, so memory nears 2x only under heavy writes. The real failure is the kernel refusing `fork()` under `vm.overcommit_memory=0`; the Redis docs say set it to `1`. Redis left the BSD licence in 2024 and added AGPLv3 with Redis 8; Valkey is the fork that kept BSD.

## Graph databases

Relational databases do not lack relationships; foreign keys and joins are relationships. What they and aggregate stores lack is cheap multi-hop traversal. Each hop is an index lookup, so "friends of friends who bought this" costs a join per hop and gets worse with depth. A graph database uses **index-free adjacency**: each node holds pointers to its neighbours, so a hop is a pointer follow and cost depends on the part of the graph you touch, not its total size. "Who bought a particular product", not just "what did a customer buy", becomes cheap. Native graph storage is built for this; some products serialise the graph into a general-purpose backend instead. Non-traversal queries (count everything) get harder (Robinson, Webber and Eifrem).

## Distributed SQL

Spanner, CockroachDB and YugabyteDB keep the relational model and SQL, partition rows across nodes, and stay strongly consistent by replicating each partition through consensus. Spanner orders transactions globally with TrueTime, backed by GPS and atomic clocks. You pay in commit latency and transaction size limits. Detail in [Consistency Models](../data/Consistency%20Models.md).

> Own view: if your data can comfortably fit on a single database server, a relational database is a good choice.

## How to rederive this

* Every store does the same jobs: store, find, keep consistent, keep safe. Ask which it does for you and which your application does.
* Split data across machines and anything needing two pieces at once (join, constraint, transaction) crosses a machine boundary. That is the sharding cost list.
* An aggregate lives on one node: cheap to read, atomic to update. Cutting across aggregates needs a second copy or coordination.
* Replicas agreeing before answering costs a round trip and fails under partition. Hence a dial.
* Index lookup per hop versus pointer per hop. That is the graph case.

## Sources

* Sadalage and Fowler, *NoSQL Distilled* (aggregate orientation, the four categories, implicit schema)
* Kleppmann, *Designing Data-Intensive Applications*, ch. 2 (data models), 5 (replication), 6 (partitioning)
* Robinson, Webber and Eifrem, *Graph Databases* (index-free adjacency, native versus non-native storage)
* [MongoDB default write concern](https://www.mongodb.com/docs/manual/reference/mongodb-defaults/)
* [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) and the [Redis FAQ](https://redis.io/docs/latest/develop/get-started/faq/) on fork and `vm.overcommit_memory`
* [Redis licences](https://redis.io/legal/licenses/)
* Brewer, [Spanner, TrueTime and the CAP Theorem](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45855.pdf)
