# Phase 4 report: fundamentals/data/Data Platforms.md (TRIM)

File edited: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/data/Data Platforms.md (only this file). Not committed.

## (a) Question the page answers

How should data be organised across an organisation, and what is the difference between a lake, a warehouse and a lakehouse? Answered up front in two sentences (domain teams own and publish data as a product over a shared platform; warehouse models before loading, lake stores raw files and models later, lakehouse gives lake files warehouse table guarantees), then derived in sections: Big data (the Vs), Operational and analytical planes, Data mesh (with Data contracts and Limitations), Request-response versus event-driven, Lake, warehouse, lakehouse (with comparison table), Processing engines, How to rederive this, Sources.

## (b) Prose word counts

Counted with awk: fences and table rows excluded, headings and the Sources list excluded.

| | Before | After |
|---|---|---|
| Body prose | 2,115 | 1,219 |

Target was 1,000 to 1,200; result is 19 words over, well under the 3,000 ceiling. H1 changed from "Aspects of big data" to "Data Platforms" (filename).

## (c) What was cut and why

Pasted passages (rule 5, audit OPINION rows):
* Kreps "Maslow's hierarchy ... space heater ... In my experience ... completely backwards" (old L13-19), first person was Kreps'. Replaced by one attributed sentence with the LinkedIn link ("in his experience most organisations have holes at the base" is attributed inside the sentence); Observability and Data Pipelines already cite the article.
* Kleppmann DDIA ch. 10 paraphrase (old L70-76, "Databases require you to structure data ... is often valuable than"). Reduced to one attributed sentence ("more valuable than" fixed) plus the owner's "joins across datasets that were previously disparate" point; the byte-sequence observation kept as one sentence.
* Hazelcast glossary paragraph on Lambda versus Kappa (old L62), including Hazelcast Jet (merged into Hazelcast Platform 5.0, STALE). Batch versus stream is owned by Data Pipelines; replaced by one linking sentence.
* Stopford's data dichotomy section (old L53-60, DUPLICATE of Asynchronous Messaging Kafka section). Reduced to the takeaway (flow control moves to receiver, cost is a broker, a retained log lets a domain regenerate its copy) with attribution and a link to ../messaging/Asynchronous%20Messaging.md#kafka. Kafka is not re-explained.

Stale product detail (rule 4):
* Spark "on Hadoop, Mesos, standalone" and "Yarn and Mesos are the two most widely used cluster managers" (old L99, L103). Mesos support was deprecated in Spark 3.2 and removed in 4.0 (SPARK-44442, audit-verified). Now "YARN, Kubernetes or standalone"; the version reason is kept out of the page per rule 4.
* Spark described as an RDD-era engine (old L99-101). Added DataFrames/Spark SQL and Structured Streaming in one sentence.
* "maybe Hadoop/Spark ecosystem" as the data-specialist skill set (old L51). Now "Spark, dbt and Airflow".
* "concept of a data lake is closely tied to Apache Hadoop" (old L82). Now "Originally the lake was HDFS; today it is object storage (S3, ADLS, GCS)".

Catalogue and anecdote (rule 2):
* Hadoop stack section and the hadoop-stack.png embed (old L80-91). MapReduce kept as one correct sentence: input split, map record to key-value pairs, shuffle and sort by key, reduce. Old L88 ("Map: split the data") was WRONG; fixed.
* Facebook MySQL to Hadoop anecdote (old L84), circa 2010, unverified.
* Gartner 85 percent failure figure (old L93), secondary source, undated; dropped rather than attributed.

Wrong claims (rule 4):
* "SQL is completely relational, while your data lakes are completely unstructured" (old L78). Replaced by the lake versus warehouse versus lakehouse section: lakes hold mostly Parquet/ORC/Avro queried with SQL (Trino, Spark SQL); open table formats (Iceberg, Delta, Hudi) add ACID tables, schema evolution and time travel; lakehouse is the merge.
* "relational, PostGres like database" for a warehouse (old L68). Now "columnar, massively parallel (MPP) SQL engine". The audit's suggestion to keep the definition in Data in the Cloud is superseded: that page was DROPPED in Phase 1 (audit/file-triage.md line 108), so this page owns the definition. `grep -rn PostGres fundamentals cloud practice` finds no other copy.
* "too big of OLTP" (old L3). Now "too big for a single OLTP database".

Style (rule 3): four em-dashes and one en-dash removed; American spellings (organization, modeled, decentralized, analyical) corrected; the rhetorical question "So the question is, how can we build reliable data flow" removed.

## (d) What was moved where

Nothing moved to another page. Material that overlapped with other pages was replaced by links:
* Batch versus stream (Lambda/Kappa): Data%20Pipelines.md#batch-versus-stream.
* Row versus columnar formats: Data%20Pipelines.md#formats-and-schema.
* Log-based brokers and retention: ../messaging/Asynchronous%20Messaging.md#kafka.

The owner's compatibility rules and schema registry text (old L30, L39) were gathered under a new `### Data contracts` heading with the bold term **data contract** intact, so the Data Pipelines link text ("the **data contract** in Data Platforms") still lands on matching wording.

Image embed removed: `../../images/hadoop-stack.png` (old L91). The image file itself was left for Phase 5, which deletes rasters.

## (e) Inbound links changed

None. The filename did not change and the only inbound link (fundamentals/data/Data Pipelines.md line 52, `[Data Platforms](Data%20Platforms.md)`) has no fragment, so it still resolves. Verified with `grep -rn "Big%20Data\|Big Data.md\|Data%20Platforms" fundamentals cloud practice README.md`.

Optional link change for whoever next edits Data Pipelines (not done, per "do NOT edit any other page"): the line 52 link could become `Data%20Platforms.md#data-contracts` now that the section exists.

Outbound anchors verified to exist: `## Batch versus stream` (Data Pipelines line 16), `## Formats and schema` (Data Pipelines line 48), `### Kafka` (Asynchronous Messaging line 83).

External links checked with curl (audit/tools/linkcheck-one.sh method): Armbrust CIDR 2021 PDF, Helland CIDR 2005 PDF, both martinfowler.com Dehghani articles, the Confluent data dichotomy post and the Microsoft big data architectures page all return 200. The Kreps LinkedIn URL (engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) returns 404. The same URL is used in Data Pipelines and Observability, so I left it unchanged for consistency and list it below as a cross-page fix for Phase 5's link sweep. LinkedIn moved its engineering blog to www.linkedin.com/blog/engineering/...; that URL answers 400 to curl (bot blocking), so it needs a browser check before replacing all three.

## (f) Diagrams or tables for Phase 5

* Table already added: warehouse versus lake versus lakehouse (storage, schema, transactions, query, data kept). Phase 5 may want to check column wording.
* Diagram candidate: `lakehouse-layers.drawio.svg`, three stacked layers (object storage files, table format metadata, query engines) with the warehouse drawn alongside as engine plus own storage, showing the two converging on the same tables.
* Diagram candidate: `data-mesh-planes.drawio.svg`, operational and analytical planes with a central pipeline team versus domain teams publishing data products over a self-serve platform.
* No replacement is needed for hadoop-stack.png; the Hadoop catalogue is gone.

## (g) Open questions for the owner

1. The Kreps hierarchy-of-needs paragraph is kept as one attributed sentence here and Data Pipelines also cites the same article for "without a complete data flow the analytics have nothing to stand on". Keep both, or drop it here and rely on the Data Pipelines mention?
2. The old page had no `> Own view:` block and I added none. The mesh Limitations section reads like the owner's stance ("understand the trade-offs before adopting"); it is stated neutrally. Should it be marked as Own view?
3. Warehouse examples are BigQuery and Snowflake. Redshift was dropped to keep two names; add it back if the AWS pages should cross-reference it.
4. The Microsoft "big data architectures" link (old L21) is kept as the only vendor link. Happy to drop it if vendor docs should not be cited from a fundamentals page.
5. Sources list Dehghani's 2019 article and the 2020 "Data Mesh Principles and Logical Architecture" article (which named federated computational governance); the 2022 O'Reilly book could be added if the owner has read it.
6. Kreps "The Log" link is dead (404) in this page, Data Pipelines and Observability. Replace all three at once in Phase 5, probably with https://www.linkedin.com/blog/engineering/distributed-systems/the-log-what-every-software-engineer-should-know-about-real-time-datas-unifying after a browser check.
