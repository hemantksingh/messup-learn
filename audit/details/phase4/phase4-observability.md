# Phase 4 report: fundamentals/platform/Observability.md (TRIM)

File edited: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Observability.md`. No other file touched. Not committed.

## (a) Question the page answers

How do I see what a running system is doing, and how do I decide what "healthy" means?

Section order: intro and the two principles; Signals (logs, metrics, traces); OpenTelemetry; Logging (structured logging, error handling, centralised log management with Syslog/journald and a one-sentence SIEM distinction, Log shipping); Tracing; Metrics (Prometheus pull model, cardinality); Deciding what healthy means (SLI/SLO/error budget, alert on symptoms, SRE bullets, alerting practice, RUM vs synthetics); Tooling (one paragraph); How to rederive this; Sources.

## (b) Prose word counts

Counted with `awk` excluding code fences and table rows, headings and the Sources list included (the same count both times).

| | Before | After |
|---|---|---|
| Observability.md | 4,666 | 2,297 |

## (c) What was cut and why

- **Pasted first-person team guideline (old lines 138 to 276, "Principles" and "Best practices").** About 1,500 words, first person, Datadog-specific (Monitors, SLOs, RUM, dd-trace, 15-day and 15-month retention windows), unattributed. Kept only the neutral fundamentals, rewritten in the third person: the two principles (know what and when before customers do; find why without the code), SLI/SLO/error budget (merged with the Phase 1 SRE section, defined once), alert on symptoms not causes (attributed to Google SRE), high cardinality belongs on spans and events not metric labels (with the reason: one time series per label combination), traces are data not just flame graphs (rewritten without the "prefer traces over metrics" absolute), don't normalise errors, actionable alerts with a runbook, self-contained dashboards, and the owner's own pre-guideline bullets on default metrics vs agent, noise and thresholds. Dropped as opinion or vendor practice: "Prefer traces over metrics", "Don't settle on aggregations", "Index valuable telemetry data", "Agree on our top-level tags", "Define a component's service boundary", "Ingest native metrics from 3rd parties", "Be keen and curious observers", "Proactively monitor production", "Surface insights", "Minimize time to acknowledge", "Use dashboards as focal points", "Decide on the metrics that matter", squad references.
- **Pasted intro sentences.** `git show 3198692` (the commit that added the guideline) shows the intro's "We provide value to customers ... so we would like to answer the question", the "extrapolate a mental model" sentence, the blockquote question and the "What do observable systems provide?" block arrived with the same paste (the commit text names the employer). Rewritten in third person; the blockquote question is reworded rather than quoted. The one "us/our" sentence kept ("Monitoring tells us the overall health ... infer the internal state from the outside") predates the paste and is the owner's.
- **APM vendor survey (old "Application monitoring").** Splunk, Sumo Logic, ELK hosted offerings, logit.io, Raygun, TechBeacon and Gartner links, and the comparative opinion ("Splunk is a one stop solution ... Sumo Logic provides a better search facility") all removed. Replaced by one neutral paragraph: open source (Prometheus, Grafana stack, Jaeger, OpenSearch) and commercial (Datadog, Splunk AppDynamics, Dynatrace, New Relic).
- **Three OpenTelemetry explanations** (Tracing line 104, Best practices line 211, "### OpenTelemetry" at the end) consolidated into one `## OpenTelemetry` section right after Signals. OpenTracing and OpenCensus stated as archived predecessors; Jaeger v2 on the OTel Collector with client libraries retired; dd-trace supports the OTel API; Azure Monitor and AWS ship their own distributions. The AWS-managed-Prometheus blog link went.
- **"Considerations" list** under the signals: five bullets of generic comparison text (combining both, complexity, tooling support) compressed to one trade-off paragraph.
- **Application Insights bullet** (OpenCensus-based, stale): removed; covered by "Azure Monitor ships its own OTel distribution".
- **SIEM vs log management second paragraph**: pasted MSP-oriented vendor blog text (n-able) removed; distinction kept as three sentences.
- **PromCat**: spelling fixed, four bullets reduced to one clause. Sysdig blog link and 2017 Red Hat OpenTracing-with-Jaeger link removed; the metrics-from-traces idea is now the OTel Collector spanmetrics connector.
- **Stack trace disclosure sub-list**: five bullets folded into one sentence.
- **Kreps "unified logging layer"** paragraph reduced to one attributed parenthetical noting it is a different "log" (see open questions).
- **Datadog-hosted flame graph link** removed (term kept, no link); the Datadog names that remain are the two the brief asked for (dd-trace supports the OTel API; Datadog in the tool list).
- **Anycast global load balancer bullet** from the merged SRE notes: dropped, it answers neither page question (see (g)).

## (d) What was moved where

- Phase 1 `## Site reliability engineering` merged into `## Deciding what healthy means` together with the guideline's SLI/SLO/error-budget paragraph and the owner's alerting bullets. SLI is now defined (it was not before), then SLO, then error budget, once.
- Phase 3 `## Log shipping` moved under `## Logging` as `### Log shipping` and merged with the owner's `### Log collection` (Logstash/Fluentd, NLog/Serilog). The heading `Log shipping` was kept deliberately so the existing inbound anchor keeps resolving.
- OpenTelemetry moved from the tail of the page to a section directly after Signals.
- Owner's "Principles" folded into two sentences at the end of the intro section.
- Elastic Stack licence note stays as one sentence at the end of Log shipping.

## (e) Inbound links changed

None changed; none needed.

- `fundamentals/data/Data Pipelines.md:60` links to `../platform/Observability.md#log-shipping`. The `### Log shipping` heading survives, so the anchor resolves.
- The in-page `[OpenTelemetry](#opentelemetry)` link resolves to the new `## OpenTelemetry` section.
- `Kubernetes.md` is now linked from Tracing (service mesh emits traces); `Data Pipelines.md` linked from Log shipping (unchanged).
- No page in `fundamentals`, `cloud`, `practice` or `README.md` references the old filename.

## Corrections landed (audit distsys-2 rows)

RUM is not white-box (rewritten: white box = internals-exposed metrics, RUM = user-side telemetry, synthetics = black-box probes); "Pomcat" -> PromCat; Example Tool lines indented as sub-bullets with Grafana marked as visualiser and Tempo added; Zipkin transports HTTP, gRPC, Kafka (Scribe legacy); OpenTracing/OpenCensus archived, adopt OTel; Jaeger versionless docs link, graduated 2019, v2 on OTel Collector; AppInsights/OpenCensus removed; dd-trace OpenTracing claim removed; Datadog retention windows removed; "Traces will always provide more context" removed; high-cardinality advice qualified; Elastic Stack licence/OpenSearch note; Splunk AppDynamics naming; unattributed vendor comparison dropped; .NET Framework 2.0 exception guideline link replaced with the versionless learn.microsoft.com page; 2017 OpenTracing/Jaeger link replaced by spanmetrics; Fluent Bit and OTel Collector added to shippers; Logstash "since 5.x" and Jaeger 1.17 version pins removed. Stray "I" (old line 102) and "configured. to" (old line 143) gone with their sentences. Two rhetorical questions in the owner's text turned into statements; the "three questions" list and the per-signal questions were kept because they are the framing the telemetry answers, not padding.

## (f) Diagrams and tables for Phase 5

- `log-pipeline.drawio.svg` (already assigned to this page in `audit/wiki-plan.md`): shipper on each host -> aggregator -> store -> dashboard. Embed under `### Log shipping`. Name Beats, Fluent Bit and the OTel Collector only in the page text.
- New candidate: `prometheus-pull-model.drawio.svg`: application `/metrics` endpoints and exporters scraped by the Prometheus server, Pushgateway for short-lived jobs, PromQL to Grafana and Alertmanager. Embed under `## Metrics`.
- New candidate: `otel-collector.drawio.svg`: app with OTel SDK -> OTLP -> Collector -> several backends. Embed under `## OpenTelemetry`.
- Small table candidate for `## Signals`: signal, question it answers, storage shape (per record vs time series), cost, retention. Would replace the trade-off paragraph.
- No image embeds existed on the page before; none removed.

## (g) Open questions for the owner

1. The Kreps essay link is kept as a one-line aside. Its "log" is the append-only data structure (Kafka, replication), not application logging; it may belong in Messaging Fundamentals or Data Pipelines instead of here.
2. The anycast global load balancer bullet from the merged SRE.md was dropped. `Load Balancing and Proxies.md` does not mention anycast; if the fact is wanted it needs a home there.
3. The reddit thread (prometheus vs opentracing) is still linked for "each signal has a different purpose". It is a discussion thread, not a source; happy to remove it.
4. The catchpoint.com "monitoring vs observability" link in the intro is a vendor blog. Kept because the owner's sentence leans on it; could be dropped without changing the text.
5. The two principles (know what and when; find why without the code) came from the pasted guideline but are stated neutrally. If the owner holds them as a position, they are candidates for a `> Own view:` block, but only in the owner's own words; none exist in git history.
6. Nagios/Icinga/Sensu vs Prometheus (white-box) sentence is the owner's and kept; confirm the "classical sysadmin tasks" framing is still wanted.
