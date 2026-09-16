# Phase 3 report: Data Pipelines

Files changed (not committed):
- `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/data/Data Pipelines.md` (full rewrite, 1,512 words by `wc -w` including headings, links and source lines; body prose is roughly 1,350; over the 1,200 target but under the one-third ceiling. The nine assigned sections plus Sources make it hard to go lower without dropping a rederivation.)
- `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Observability.md` (appended one `## Log shipping` section at the end of the file, 10 added lines, 0 deletions, nothing else touched).

## (a) Question the page answers

How does data get from where it is produced to somewhere it is useful, and what breaks along the way? The first paragraph answers it: a pipeline is the chain of steps that carries data across the gap between producer and consumer, and what breaks is late arrival, duplicates, loss, schema change, or a rerun that gives a different result.

## (b) Kept from the original

- The owner's capture / curate / consume framing, mapped onto capture, store, transform, serve, with an explicit note that "curate" covered store plus transform.
- The owner's streaming use cases: fraud detection on card transactions, trading systems reacting to price changes, infrastructure monitoring spotting faults.
- The batch versus stream split as the organising fundamental.
- From the Logstash / Beats / Fluentd material: the shipper, aggregator, store, visualise shape and the persistent-queue fact, now in Observability `## Log shipping`.

## (c) Dropped and why

- "fits into the Curate stage": a pipeline spans capture to serve, not one stage. Corrected in the text.
- "directed acyclic graph that is difficult to scale" (audit WRONG, L11): batch DAGs scale by partitioning; the cost is latency. Replaced.
- Media-streaming analogy (audit WRONG, L20): stream processing is about events, not delivering bytes to a player. Replaced with a card-payments-per-five-minutes example and one sentence saying the analogy does not apply.
- "military and intelligence systems" example: no fundamental behind it, dropped from the list.
- Hortonworks DataFlow link (audit STALE, L3), YouTube and Medium links: catalogue links, not fundamentals.
- The entire Logstash / Filebeat / Beats / Eland / Elasticsearch-for-data-science section (L22-45): observability tooling and vendor-blog paste (Logz.io opinion "one of the best log file shippers", audit L30), Eland "brand new" (STALE, L45), ML jobs "experimental" (STALE, L45). What survives is the five facts in the brief, in Observability.
- The Logstash versus Fluentd comparison (L47-55): self-contradicting on persistent queues (L28 vs L53, audit INCONSISTENT and WRONG), "needs Redis" (WRONG), JVM/Ruby memory argument (STALE; Java execution engine since 7.0). Replaced by the corrected bullets in `## Log shipping`.
- Both images (`elastic-log-shippers.jpg`, `logstash-fluentd-comparison.png`): removed from the page and not embedded in Observability, per the assignment.

## (d) Added, with sources

- Four stages capture, store, transform, serve: Reis and Housley, *Fundamentals of Data Engineering* (their lifecycle is generation, storage, ingestion, transformation, serving; collapsed to four verbs here). "Without reliable data flow the analytics on top have nothing to stand on" is attributed to Jay Kreps, "The Log" (2013), named inline and linked in Sources rather than pointing at the unattributed paste in Data Platforms.
- Batch as a pure function of fixed input, scaled by partitioning; DAG of steps: Kleppmann, DDIA ch. 10.
- Event time versus processing time, windows, watermarks, late data (drop, correct, or hold): Akidau, Chernyak and Lax, *Streaming Systems*.
- ETL versus ELT and why cheap, separately billed warehouse compute made ELT and dbt the default: Reis and Housley; general industry knowledge, no version or price stated.
- Orchestration (Airflow, Dagster), retries, backfills, idempotent steps by overwriting the output partition rather than appending, and "read the period as a parameter, not now": Reis and Housley; Airflow's own design (execution date as the run parameter). Stated as a derivation, not a product claim.
- Polling misses deletes and intermediate states; log-based CDC reads the WAL/binlog; Debezium via Kafka Connect; downstream stores as derived views: Kleppmann, DDIA ch. 11.
- Outbox pattern implemented with CDC: linked to the existing description in Asynchronous Messaging; Debezium documents the outbox event router.
- Row versus columnar formats (JSON, CSV, Avro versus Parquet, ORC), why columnar wins for analytics (read only needed columns, better compression): Kleppmann DDIA ch. 3 (column-oriented storage) and ch. 4 (encoding, Avro schema evolution).
- Schema evolution rules and data contracts: DDIA ch. 4; cross-linked to the data mesh compatibility bullet in Data Platforms.
- At-least-once plus idempotent sink as practical exactly-once: linked, not re-explained (Asynchronous Messaging).
- Observability `## Log shipping`: Logstash persistent queues since 5.x (Logstash 5.1 release notes; audit-verified); Elastic Agent and Fleet as the recommended path over standalone Beats (Elastic docs, GA 7.14); Fluent Bit and OpenTelemetry Collector as common Kubernetes shippers (CNCF, OpenTelemetry docs); Elastic Stack licence change in 2021 and the OpenSearch fork (Elastic and AWS announcements, January and April 2021). The current licence is deliberately not stated; the text says to check.

No `> Own view:` blocks were added: the original page carried no owner stance, and inventing one would misattribute.

## (e) Diagrams for Phase 5

- No images are embedded in Data Pipelines. A useful new diagram would be `data-pipeline-stages.drawio.svg`: capture, store, transform, serve as four boxes, with batch (scheduled DAG) and stream (windows on an unbounded input) drawn as the two paths between capture and serve, and CDC shown as the capture arrow reading the database log. Optional.
- `images/elastic-log-shippers.jpg`: removed from Data Pipelines, not re-embedded. The wiki plan already maps it (with the orphan `images/elastic-stack.jpeg`) to a vendor-neutral `log-pipeline.drawio.svg` (shipper, aggregator, store, visualise) to embed under Observability `## Log shipping`.
- `images/logstash-fluentd-comparison.png`: removed, not re-embedded; the wiki plan lists it for deletion (stale vendor comparison). Nothing references either image now.

## (f) Open questions for the owner

1. `## Log shipping` was appended at the very end of Observability, after `## Site reliability engineering`, because the assignment said append and nothing else. Logically it belongs under `## Logging` next to the existing `### Log collection` (line 89), which it partly overlaps (Logstash and Fluentd as forwarders). Phase 4's TRIM of Observability should move it there and fold `### Log collection` into it. The anchor `#log-shipping` works from either place.
2. The page names a few tools (Spark, dbt, Airflow, Dagster, Debezium, Kafka Connect, Parquet, Avro) as examples of each idea. The wiki plan discourages catalogues; these are one or two per concept and no versions, but the owner may want to cut further.
3. Data Platforms (not in my scope) still carries the stale Lambda/Kappa/Hazelcast Jet paragraph and the Hadoop-centric lake section. Data Pipelines now says batch and stream are two paths with different trade-offs and does not mention Lambda or Kappa at all; when Data Platforms is trimmed, the two pages should agree on where that discussion lives.
4. Word count is above target (about 1,350 words of prose against 1,200). If the owner wants it shorter, the candidates are the second paragraph of Formats and schema (contracts, already covered in Data Platforms) and the Log data section (could become one sentence plus the link).

Neither page refers to its own earlier version or to the audit; the corrected facts are stated plainly so the text reads as reference, not as history.
