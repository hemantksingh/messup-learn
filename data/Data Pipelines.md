---
title: "Data Pipelines"
summary: "How data moves from where it is produced to where it is wanted: batch or stream, ETL or ELT, CDC and idempotent steps."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "Kleppmann, Designing Data-Intensive Applications, ch. 10 and 11"
  - "Kreps, The Log: What every software engineer should know about real-time data's unifying abstraction (2013)"
  - "Reis and Housley, Fundamentals of Data Engineering"
  - "Akidau, Chernyak and Lax, Streaming Systems"
tags: [data-pipelines, etl, streaming, batch, change-data-capture, orchestration]
---
# Data Pipelines

Data is produced in one place and wanted in another; a pipeline carries it across the gap and reshapes it on the way. What breaks: data arrives late, twice or not at all, changes shape without warning, or a rerun gives a different result. Pipeline design is deciding up front how each is handled.

## The stages

Four stages, whatever the tools:

* **Capture** (ingest): export, read the change log, or receive events.
* **Store**: land it cheap and durable (object storage, a raw table) before doing anything clever.
* **Transform**: filter, join, clean, aggregate.
* **Serve**: expose it to a query engine, dashboard or model.

Capture, curate, consume is the same list with store and transform combined. Most failures are in the dull capture and store stages, and without a complete data flow the analytics on top have nothing to stand on (Kreps, "The Log").

![Four stage boxes left to right: Capture (ingest), Store (object storage, raw table), Transform (filter, join, clean, aggregate) and Serve (query engine, dashboard, model). A source database feeds Capture through an arrow labelled CDC: read the change log, from its write-ahead log or binlog. The row itself is the batch path, with the Store to Transform arrow labelled batch: scheduled DAG over stored data. A second arrow runs beneath from Capture straight to Transform labelled stream: each event as it arrives, windows over an unbounded input. Caption: batch input is fixed when the job starts so a failed job is rerun; a stream never finishes so it is cut into windows with event time, processing time, a watermark and a late-data rule.](../images/data-pipeline-stages.drawio.svg "Pipeline stages with the batch and stream paths")

## Batch versus stream

A batch job runs on a schedule over stored data, so results are hours or a day old. Streaming handles each event as it arrives, so results are seconds old.

Batch input is fixed when the job starts, so output is a pure function of input and a failed job is rerun. It scales: the job is a directed acyclic graph (DAG) of steps and each step partitions its input across machines, as Spark does.

Streaming is for results whose value decays quickly:

* fraud detection on a stream of card transactions
* trading systems reacting to price changes
* infrastructure monitoring spotting faults as they appear

Streaming is harder because the input never finishes. "Card payments per customer per five minutes" is a group-by in batch; a stream must be cut into **windows**, with two clocks: **event time** (when the payment happened) and **processing time** (when it reached the pipeline). Events arrive out of order and late, so the pipeline needs a **watermark** (all events up to T have probably arrived) to close a window, and a rule for **late data**: drop it, emit a correction, or hold the window open. None of this is streaming audio or video, which is delivering bytes to a player.

## ETL versus ELT

Extract, transform, load; the question is whether the transform happens before or after the data lands. Classic **ETL** transformed on the way in because warehouse storage and compute were expensive and shared, so only clean, modelled data was loaded. Cloud warehouses separate the two and bill compute by use, so loading raw and transforming in SQL became cheaper: **ELT**, now the default. dbt does this step: versioned, tested SQL run as a DAG. The raw layer stays untouched, so a wrong transformation is fixed by rerunning, not re-extracting.

## Orchestration

The orchestrator (Airflow, Dagster) holds the DAG, starts each step when its upstreams finish, retries, alerts when retries run out, and records what ran.

Each step must be **idempotent**: overwrite the output partition for the period (the day's folder or rows) rather than append. Then a **backfill** is just the same DAG rerun day by day. A step that appends, or reads "now" instead of taking the period as a parameter, can be neither retried nor backfilled.

## Change data capture

Polling (select rows whose `updated_at` is newer than last time) loads the source, misses deletes and misses the intermediate state of a row that changed twice between polls.

**Change data capture** (CDC) instead reads the write-ahead log or binlog, the stream the database uses for replication: every insert, update and delete, in order, with almost no load on the source. Debezium publishes each change as an event. Kleppmann (*Designing Data-Intensive Applications* ch. 11): the log is the source of truth and every downstream store is a derived view kept current by consuming it.

CDC is also the plumbing behind the **transactional outbox** in [Messaging Fundamentals](../messaging/Messaging%20Fundamentals.md#the-transactional-outbox): event and state change are written in one transaction and CDC publishes the outbox rows, so they cannot disagree.

## Formats and schema

Data at rest is **row-wise** (JSON, CSV, Avro: all fields of one record together) or **column-wise** (Parquet, ORC: all values of one field together). Columnar wins for analytics: a query touches few columns of many rows, so the engine reads only those, and similar values compress far better. Hence data lakes are mostly Parquet and warehouses are columnar inside.

Schema changes break consumers. Formats with an explicit schema (Avro, Parquet, Protobuf) let a reader check compatibility up front; the rules for changing one safely are the **data contract** in [Data Platforms](Data%20Platforms.md).

## Delivery guarantees

A network hop can lose a message or deliver it twice. Practical exactly-once is **at-least-once delivery plus an idempotent sink**: retry until acknowledged; the destination overwrites on a key or remembers what it has seen. The reasoning is in [Messaging Fundamentals](../messaging/Messaging%20Fundamentals.md#at-least-once-delivery-and-idempotent-consumers) and applies to a warehouse table.

## Log data

Shipping application logs is a pipeline like any other (shipper, aggregator, store, dashboard) with the same failure modes; the tooling is in [Observability, log shipping](../platform/Observability.md#log-shipping).

## How to rederive this

* Start from the gap: produced here, needed there. Get it, keep it, shape it, expose it.
* Complete input: batch, a pure function. Unbounded input: streaming; choose windows, a clock and a late-data rule.
* Warehouse billed per query: transform after loading.
* Getting changes out: polling misses deletes; the log has every change in order; the outbox is CDC on an events table.
* Reruns and duplicates: overwrite on a key and both are harmless.

## Sources

* Martin Kleppmann, *Designing Data-Intensive Applications*, ch. 10 (batch) and ch. 11 (streams, CDC, derived data).
* Jay Kreps, [The Log: What every software engineer should know about real-time data's unifying abstraction](https://www.linkedin.com/blog/engineering/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) (2013).
* Joe Reis and Matt Housley, *Fundamentals of Data Engineering* (ingest, store, transform, serve; ETL versus ELT; orchestration).
* Tyler Akidau, Slava Chernyak and Reuven Lax, *Streaming Systems* (event time, windows, watermarks, late data).
