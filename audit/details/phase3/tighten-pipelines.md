# Tighten report: fundamentals/data/Data Pipelines.md

Word count (code fences excluded, `wc -w`): 1512 before, 983 after. Target 900 to 1000.

The page stops near 990 rather than 900 because every remaining candidate is a fact, an owner sentence or a link that rule 2 protects (listed under "Tempted to cut but kept").

No commit. Only this file edited. fundamentals/platform/Observability.md untouched (its pre-existing working-tree modification is unchanged). No em or en dashes. British spelling kept (modelled). Headings in the same order; "Log data is one kind of pipeline" shortened to "Log data". All four links kept (Asynchronous Messaging x2, Data Platforms, Observability#log-shipping). Sources unchanged. Rederive bullets cut from six to five, each one line. No "> Own view:" block existed.

## What was cut

Restatement
* "The cost of batch is waiting, not scaling" (restated "results are hours or a day old" and "it scales").
* "The pipeline runs from capture to serve, not just the middle" (the bullets already say so).
* "Row formats suit writing and reading whole records" (follows from the row-wise definition).
* "(the row is no longer there to select)" after "misses deletes".
* "so duplicates are harmless" after "overwrite on a key or remember what it has seen".
* Intro: "A data pipeline is the chain of steps that ..." collapsed into the first sentence.
* Stages closing sentence merged with the Kreps sentence; inline "As Jay Kreps argues in" replaced by a parenthetical since Sources carries the cite.

Inferable asides
* Intro examples of producers and consumers (application/device/log; warehouse/model table/search index/other service).
* "Something has to run the steps in order, on time, and cope with failure. That is the orchestrator" (the orchestrator sentence lists exactly those duties).
* Backfill example "to reprocess last month after a bug fix" reduced to "rerun day by day".
* Orchestration "the same input gives the same result on a rerun" (that is the definition of idempotent; the overwrite rule carries it).
* Batch/stream opening: "reads everything since the last run and writes its output" reduced to "over stored data".
* "The trade is latency against throughput and simplicity" (the two following sentences make the point).
* Windows example shortened from a full question to "Card payments per customer per five minutes".
* Watermark gloss shortened ("an estimate that 'all events up to time T have probably arrived'" to "all events up to T have probably arrived").
* Akidau inline attribution ("Akidau's Streaming Systems is built around these choices"); the book stays in Sources.
* Formats: "and every consumer downstream can break" merged into "Schema changes break consumers"; "instead of failing at run time" to "up front".
* "the data mesh section of" before the Data Platforms link.
* Log data: the four-role list kept as a parenthetical, the failure-mode examples (back pressure, duplicates, parse failures) dropped as "the same failure modes" already points at the intro list.

Filler and connectives
* "Every pipeline has the same four stages" to "Four stages".
* "Given that", "The only question is", "for example", "which is what Spark does" to "as Spark does", "The usual way is to", "nothing special" to "just", "In a stream the pipeline must" to "a stream must be", "so it became cheaper to" to "became cheaper".
* Bullet text in the stages list trimmed to the verbs.

Second paragraph of "Formats and schema" (named candidate)
* The compatibility rules (add optional fields, never remove or rename, breaking change is a new version) and the "same idea as any published interface" sentence were dropped; the page now says the rules are the data contract in Data Platforms, with the link.

Product lists
* "(Airflow, Dagster, or a cloud equivalent)" to "(Airflow, Dagster)".
* "usually run through Kafka Connect" dropped from the Debezium sentence.
* "for the common databases" dropped from the Debezium sentence.
* "(warehouse, cache, index)" after "every downstream store".
* "A streaming pipeline" to "Streaming".

Rederive bullets
* Six to five: the rerun bullet and the network bullet merged into "Reruns and duplicates: overwrite on a key and both are harmless." Each bullet cut to one declarative line; the "Ask whether ..." preambles dropped.

Link targets checked: fundamentals/data/Data Platforms.md line 30 carries the data-contract compatibility rules the Formats paragraph now points at; fundamentals/platform/Observability.md has the "## Log shipping" heading for the #log-shipping anchor.

## Tempted to cut but kept
* "None of this is streaming audio or video, which is delivering bytes to a player": it corrects the pre-rewrite page, which conflated stream processing with audio/video streaming.
* "Capture, curate, consume is the same list with store and transform combined": the owner's original framing from the pre-rewrite page.
* The three streaming use-case bullets, verbatim: the owner's examples.
* The two-clocks / watermark / late-data sentence: every bold term is a fact the Akidau source is cited for.
* "as Spark does", "dbt", "Debezium", "Airflow, Dagster": single product names that anchor a concept, so kept even though the lists around them were cut.
* The three polling failures (source load, missed deletes, missed intermediate states), the transactional outbox paragraph, and "Hence data lakes are mostly Parquet and warehouses are columnar inside": facts.
* The Kleppmann "log is the source of truth, downstream stores are derived views" sentence: it is the page's link to the DDIA ch. 11 source; only the book title moved into a parenthetical.
* "Classic ETL ... because warehouse storage and compute were expensive and shared": the causal fact behind the ETL to ELT shift.
