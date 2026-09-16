---
title: "Data Platforms"
summary: "How to organise data across an organisation: data mesh and data contracts, and lake versus warehouse versus lakehouse."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "Dehghani, How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh (2019); Data Mesh Principles and Logical Architecture (2020)"
  - "Helland, Data on the Outside versus Data on the Inside (CIDR 2005)"
  - "Stopford, The Data Dichotomy (Confluent, 2016)"
  - "Kreps, The Log (2013)"
  - "Kleppmann, Designing Data-Intensive Applications, ch. 10"
  - "Armbrust et al., Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics (CIDR 2021)"
tags: [data-platforms, data-mesh, data-lake, data-warehouse, lakehouse, data-contracts]
---
# Data Platforms

How should data be organised across an organisation, and what is the difference between a lake, a warehouse and a lakehouse? Short answer: the teams that produce data own it and publish it as a product over a shared platform. A warehouse models data before loading, a lake stores raw files and models later, a lakehouse gives the lake's files the warehouse's table guarantees.

## Big data

Big data is data that is too big (100s of TB to PB) or moves too fast to be processed by conventional means, that is too big for a single OLTP database. Three Vs: **Volume**: the data does not fit on one machine. **Velocity**: the rate at which data comes in and how fast the output is needed; the tighter the feedback loop the greater the advantage, and results often go straight into a product, for example Facebook recommendations. **Variety**: the data arrives in formats outside your control, and a common job is to take unstructured input and extract meaning from it; fixed relational schemas are not always a natural fit. The mechanism for all three is the same: partition a big dataset into smaller ones and send each chunk to a separate node in a cluster to be processed in parallel.

## Operational and analytical planes

Traditional [big data architectures](https://docs.microsoft.com/en-us/azure/architecture/data-guide/big-data/) move data from the operational plane (producers) to the analytical plane (consumers) via a [data pipeline](Data%20Pipelines.md). This creates silos: data engineers have little knowledge of the domain, and domain teams produce data without considering how it is used externally, so quality, accuracy and freshness suffer.

Kreps ([The Log](https://www.linkedin.com/blog/engineering/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying)) describes a hierarchy of needs: capture all the relevant data in one place and model it uniformly before building processing, and processing before visualisation and prediction; in his experience most organisations have holes at the base and try to jump to the top.

## Data mesh

Zhamak Dehghani's data mesh brings the two planes together by applying the practices of the operational plane (microservices, DevOps) to analytical data. Four principles:

* **Domain driven decentralised ownership**. Move from monolithic ownership of data to ownership within domain teams, and from technology driven architecture (ingestion, ETL, pipelines) to domain driven data.
* **Data as a product**, not a by-product. Think from the point of view of the customers of your data. A domain's internal state is encapsulated, but its shared state, Helland's [data on the outside](https://www.cidrdb.org/cidr2005/papers/P12.pdf), is easy to consume: clear SLAs on quality, freshness and availability, documented with lineage, schema, usage examples and quality metrics.
* **Self serve infrastructure as a platform**. Apply infrastructure as code and platform thinking to data operations. The platform is agnostic to the domains and provides the cross cutting parts: storage, one pipeline with a well defined API for adding data rather than many point to point pipelines, a catalogue, a schema registry, access control and lineage.
* **Federated computational governance**. Domain teams, not central gatekeepers, define data quality, security and ownership. The rules are embedded in the platform tooling and enforced when something is built, deployed or accessed.

### Data contracts

A **data contract** is the published schema of a shared dataset or event plus the rules for changing it:

* Adding an optional field is backwards and forwards compatible: existing consumers keep working and old producers stay readable.
* Removing a required field, renaming a field or changing its type (date to string) is a breaking change. Publish it as a new versioned message or event.
* A **schema registry** holds every schema and its history and enforces the rule at runtime: a producer presents the schema of a new message and the produce succeeds only if it matches the last one or satisfies the compatibility rule for the channel. Consumers fetch schemas by id rather than carrying them in every payload.

### Limitations

These can be resolved, but understand the trade-offs before adopting a mesh:

* If domains keep their own interpretations of data belonging to other domains, copies diverge and governance gets hard.
* Data specialists, people who know lakes, ETL, stream processing, warehouses and tools such as Spark, dbt and Airflow, are now needed in every domain team.

## Request-response versus event-driven

Stopford's [data dichotomy](https://www.confluent.io/blog/data-dichotomy-rethinking-the-way-we-treat-data-and-services) is the tension between business services that manage operational data and data services that provide business intelligence. Event driven architectures decouple better than request-response because flow control moves from sender to receiver, increasing each service's autonomy. The cost is a message broker. If that broker is a distributed log that retains events long term, a domain can keep a local historic copy in a database of its choice and regenerate it from the log at will: messaging that is also storage, without shared mutable state. How log-based brokers do this is in [Asynchronous Messaging](../messaging/Message%20Brokers.md#queue-brokers-versus-log-brokers).

## Lake, warehouse, lakehouse

A **data warehouse** stores structured, frequently queried data in a columnar, massively parallel (MPP) SQL engine reached over ODBC/JDBC. Data is modelled **up front**: schema and query patterns are decided before loading into the engine's own storage format. BigQuery and Snowflake are examples.

A **data lake** stores files. A file is just a byte sequence, so it can hold database records, text, images or sensor readings. Originally the lake was HDFS; today it is object storage (S3, ADLS, GCS). Most of what lands there is structured or semi-structured columnar files (Parquet, ORC, Avro; see [formats](Data%20Pipelines.md#formats-and-schema)) queried with SQL through engines such as Trino or Spark SQL. The schema is applied on read. Kleppmann (*Designing Data-Intensive Applications* ch. 10) argues that making data available quickly, even raw and awkward, is often more valuable than deciding the ideal model first. The idea is the same as a warehouse: bringing data from across a large organisation into one place enables joins across datasets that were previously separate.

A plain lake has no atomic writes, updates or deletes, no schema enforcement and no consistent view while a job is writing. **Open table formats** (Apache Iceberg, Delta Lake, Apache Hudi) add these as a metadata layer over the files: a directory of Parquet becomes an ACID table with schema evolution and time travel, readable by many engines. Lake storage plus a table format plus warehouse-style engines is the **lakehouse**. Warehouses now read the same tables, so the two are merging.

| | Warehouse | Lake | Lakehouse |
|---|---|---|---|
| Storage | Engine's own columnar format | Files in object storage | Files in object storage plus a table format |
| Schema | On write, modelled up front | On read | On write per table, evolves in place |
| Transactions | ACID | None across files | ACID via table metadata |
| Query | Engine's SQL | Any engine that reads the files | Any engine that speaks the table format |
| Data kept | Curated, structured | Everything, raw | Raw and curated in one store |

## Processing engines

Hadoop came first. HDFS pooled the disks of a cluster into one replicated store and MapReduce ran the computation where the data lived. A MapReduce job splits the input, maps each record to key-value pairs, shuffles and sorts by key, then reduces each key's values to an aggregate. Object storage replaced HDFS and Spark replaced MapReduce.

Hadoop was a child of the cheap storage era; Spark is a child of the memory and network era. It keeps working sets in memory, exposes DataFrames and Spark SQL rather than raw map and reduce, and runs the same code over a stream with Structured Streaming. A **cluster manager** distributes resources between applications; Spark runs on YARN (the Hadoop scheduler), Kubernetes or standalone. Batch versus streaming is decided in [Data Pipelines](Data%20Pipelines.md#batch-versus-stream).

## How to rederive this

* A pipeline between teams that do not talk is where data quality is lost.
* Treat shared data as an interface: a schema, compatibility rules, a registry to enforce them.
* Warehouse: model first, load clean. Lake: land raw, model later. Each is a bet on how well you know the questions in advance.
* A lake is files; add a metadata layer that gives ACID tables and you have a lakehouse.

## Sources

* Zhamak Dehghani, [How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh](https://martinfowler.com/articles/data-monolith-to-mesh.html) (2019) and [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) (2020).
* Pat Helland, [Data on the Outside versus Data on the Inside](https://www.cidrdb.org/cidr2005/papers/P12.pdf) (CIDR 2005).
* Ben Stopford, [The Data Dichotomy](https://www.confluent.io/blog/data-dichotomy-rethinking-the-way-we-treat-data-and-services) (Confluent, 2016).
* Jay Kreps, [The Log](https://www.linkedin.com/blog/engineering/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) (2013).
* Martin Kleppmann, *Designing Data-Intensive Applications*, ch. 10.
* Michael Armbrust et al., [Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics](https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf) (CIDR 2021).
