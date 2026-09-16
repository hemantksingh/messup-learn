# Audit: Distributed Systems (batch 1)

Repo: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn`. Audit date 2026-09-16. Read-only; line numbers from `cat -n`.

Files: AMQP.md, Asynchronous Messaging.md, Concurrency Models.md, Consistency Models.md, Continuous Deployment.md, Event Sourcing.md, HTTP Caching.md, HTTP.md (all under `Distributed Systems/`).

---

## Distributed Systems/AMQP.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 3 | WRONG | "Advanced Message Queueing Protocol standard defines the following AMQP entities" (Exchange, Bindings, Queue) | Exchanges and bindings are AMQP **0-9-1** concepts (the RabbitMQ dialect). AMQP **1.0** (the OASIS/ISO/IEC 19464 standard used by Azure Service Bus, ActiveMQ, Qpid) has no exchanges or bindings; it defines links, nodes, containers, sessions. The note presents the 0-9-1 model as "the AMQP standard". | Retitle/introduce as "AMQP 0-9-1 (RabbitMQ) model"; add a short paragraph on AMQP 1.0 and that the two are not wire-compatible. | High |
| 3 | STALE | Whole file frames RabbitMQ as an AMQP 0-9-1 broker only | RabbitMQ 4.0 (Sept 2024) made AMQP 1.0 a core, always-on protocol and 1.0 clients can now manage queues/exchanges/bindings ([RabbitMQ: Native AMQP 1.0](https://www.rabbitmq.com/blog/2024/08/05/native-amqp)). | Add one line noting RabbitMQ speaks 0-9-1, 1.0, MQTT and STOMP natively since 4.0. | High |
| 9 | WRONG | "A queue binds to the exchange with a routing key (address for the queue)" | Conflates the **binding key** (set on the binding) with the **routing key** (set on the message). The routing key is not "the address for the queue". | "A queue is bound to an exchange with a *binding key*; the exchange compares a message's *routing key* against binding keys." | Medium |
| 19 | BROKEN | "**Headers** - When matching requires more than one attribute, routing key is ignored." | Fragment; does not say what headers exchanges match on (message headers, with `x-match: all/any`). | Complete the bullet. | Medium |
| (whole) | CLASSIFY | 19-line file covering only exchange types | Too thin to stand alone; the sibling Asynchronous Messaging.md L76-82 already introduces AMQP/STOMP/MQTT and Servicebus Frameworks.md covers ack/nack/DLQ. | Merge into Asynchronous Messaging.md as an "AMQP 0-9-1 routing model" subsection, or expand to cover default exchange, DLX, prefetch/QoS, publisher confirms, AMQP 1.0. | High |

---

## Distributed Systems/Asynchronous Messaging.md (last commit 2021-04-21)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | "# Asynchronous message‑based integration" | H1 contains a U+2011 non-breaking hyphen (bytes `E2 80 91`) instead of ASCII `-`; `grep "message-based"` will not match. H1 also does not match filename "Asynchronous Messaging". | Replace with ASCII hyphen; consider H1 "Asynchronous Messaging". (Same character appears in Synchronous Messaging.md H1.) | High |
| 3 | INCONSISTENT | "temporal coupling i.e. previous calls must succeed before the next one can be made" | Standard meaning of temporal coupling is that both parties must be available at the same time. L39 then uses "temporal coupling" for a third meaning (an ordering change in the business flow requiring a consumer change). Two different in-file definitions, neither standard. | L3: "temporal coupling: caller and callee must both be up at the same time". L39: call this ordering/behavioural coupling. | Medium |
| 13 | DUPLICATE | Out-of-band "event forwarding" from a message table in the domain store | This is the **Outbox pattern**, described without naming it. Servicebus Frameworks.md L7 names and links it; Event Sourcing.md L35-40 covers the same at-least-once/dedup consequence. | Name it "Transactional Outbox" and cross-link the three files. | High |
| 23 | BROKEN | "## Sagas & Process Mangers" | Spelling error in heading ("Managers"). | Fix heading. | High |
| 41-50 | OPINION | "routed through a centralized component - **saga**" | Presents the NServiceBus/Udi Dahan usage (saga = orchestrating process manager) as the definition. Garcia-Molina's saga is a sequence of local transactions with compensations and can be choreographed or orchestrated; L45 half-acknowledges this. | State that "saga" here means the orchestrator-style saga (a.k.a. process manager) and that choreographed sagas exist. | Medium |
| 79 | WRONG | "STOMP ... more analogous to HTTP https://docs.nats.io/" | Link points to NATS documentation, which is unrelated to STOMP. | Link to https://stomp.github.io/ ; if NATS is wanted, add it as its own bullet. | High |
| 80 | STALE | "MQTT - (Message Queue Telemetry Transport)" | OASIS states MQTT is no longer an acronym (originally "MQ Telemetry Transport" after IBM MQ). Minor. | "MQTT (originally MQ Telemetry Transport; no longer an acronym)". | Medium |
| 78 | STALE | "AMQP - designed as an open replacement for existing proprietary messaging middleware" | No 0-9-1 vs 1.0 distinction; see AMQP.md L3. Azure Service Bus (AMQP 1.0) is never mentioned anywhere in this file despite being the third broker named in Servicebus Frameworks.md. | Add 0-9-1 vs 1.0 note and an Azure Service Bus bullet (queues/topics/subscriptions, sessions for ordering, duplicate detection). | High |
| 85 | STALE | "distributed stream processor (e.g. Apache Samza - developed at LinkedIn, Apache Storm)" | Kafka Streams, ksqlDB and Apache Flink are the mainstream choices now; Storm is largely legacy. | Add Kafka Streams / Flink. | Medium |
| 93 | STALE | "traditional message brokers like RabbitMQ ... once a message has been delivered, it is removed ... not suitable for long-term data storage" | RabbitMQ **Streams** (added in 3.9, July 2021 - date Unverified, three months after this commit) are an append-only, replayable, non-destructive log with retention policies, directly addressing this. | Add: "RabbitMQ 3.9+ Streams provide a Kafka-like replayable log; the classic queue comparison below applies to classic/quorum queues only." | High |
| 93 | WRONG | "RabbitMQ is often used with Apache Cassandra to support durable storage ... or with the LevelDB plugin" | Not a recognised RabbitMQ deployment pattern; appears copied from a vendor blog. No official LevelDB plugin exists for RabbitMQ. | Remove or cite. | Medium |
| 97 | WRONG | "Fundamentally Kafka does not suffer from this issue as it uses a time ordered event log" | Kafka guarantees order **only within a partition**; across partitions of a topic there is no ordering. Also, a Kafka consumer that crashes re-reads from its last committed offset, so m1 and m2 are both re-processed in order - the fix is offset-based, not "time ordered". | "Kafka preserves order per partition (choose the partition key accordingly); redelivery is by re-reading from the committed offset." | High |
| 99-107 | OPINION | "for disjointed job queue ... AMQP ... good fit ... if order is important Kafka is a better choice" | Reasonable rule of thumb, but stated as fact. RabbitMQ single-active-consumer / quorum queues and Azure Service Bus sessions also give ordering. | Label as heuristic. | Medium |
| 115-126 | STALE | MSMQ section incl. `System.Messaging` C# sample | MSMQ is Windows-only legacy; `System.Messaging` exists only in .NET Framework (not .NET Core / .NET 5+). NServiceBus moved MSMQ to a separate transport package. Still true, but a reader in 2026 needs the "legacy" label. | Prefix with "Legacy (Windows / .NET Framework only)". | High |
| 91 | WRONG | "the onus is on the consumer to keep track of messages that it has read" | Partially: since Kafka 0.9 committed offsets are stored broker-side in `__consumer_offsets`; the consumer *decides* when to commit but the broker stores them. | Clarify. | Medium |

---

## Distributed Systems/Concurrency Models.md (last commit 2021-07-27)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 5, 7 | WRONG | "## Communicating Sequential Processing (CSP)" | Hoare's CSP is "Communicating Sequential **Processes**". Error is in an H2 heading and repeated in the link text on L7. | Fix both. | High |
| 13, 16 | OPINION | "Go is the result of rethinking system programming from the ground up, creating a lean, mean, and compiled solution"; "you'll want to use it for nearly everything you used command line interpreters for, thereby replacing your bash, scripts, Python" | Marketing copy / personal recommendation presented as fact. | Label as opinion or trim to the CSP-relevant facts (goroutines, channels). | High |
| 17 | STALE | "drawback - primarily for backend services without support for scripting in the browser" | Go has had a WebAssembly target since Go 1.11 (Aug 2018), before this commit. | Reword: "not a natural fit for browser scripting, though Wasm compilation exists". | Medium |
| 19 | STALE | "Nested callbacks are inevitable and can cause complexity" (Node.js) | Promises/`async`-`await` (Node 8, 2017) and `worker_threads` (stable Node 12, 2019) predate this commit; "inevitable" and "single process" are outdated. | Update: event loop + async/await; worker_threads and cluster for multi-core. | High |
| 47 | WRONG | "Concurrency describes multiple computations occurring simultaneously. Parallelism is concurrency but applied to achieving a single goal" | Inverts the standard distinction (Pike, and the linked SO answer): concurrency = *dealing with* many things at once (structure, interleaving; may run on one core); parallelism = *doing* many things at once (simultaneous execution). | Use the standard definitions. | High |
| 53 | WRONG | "Long lived actors hold some state ... aka **process managers**" | "Process manager" is an EIP messaging pattern (Hohpe & Woolf), not a synonym for a stateful actor. Creates confusion with Asynchronous Messaging.md L23 ("Sagas & Process Managers"). | Remove "aka process managers" or say "can implement process managers". | Medium |
| 59-60 | BROKEN | `[asynchronous vs synchronous](https://www.infoq.com/...campaign=qcon` newline `)` | Markdown link URL split across two lines; renders broken. | Join onto one line. | High |
| 77, 83 | STALE | akka "snapshot" docs; "http://doc.akka.io/docs/akka/2.0.1/" | Akka 2.0.1 docs are from 2012. Also Akka relicensed to BSL 1.1 in Sept 2022; the Apache-licensed fork is **Apache Pekko** - relevant to anyone acting on this reading list. | Link current Akka docs and mention Pekko. | High |

Gap (not a table row): the assignment asked to check .NET async/await, ThreadPool and TPL claims. **There are none in this file** - C# appears only in L3 as a "shared memory + threads" language. For a .NET-oriented notes repo this is a gap, not an error; suggest a short ".NET" subsection (TPL, async/await is not multithreading, `Channel<T>` as CSP, Orleans virtual actors).

---

## Distributed Systems/Consistency Models.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | "# Distributed Databases" | H1 does not match filename "Consistency Models". File is ~60% consistency models, ~40% distributed-DB scaling/Spanner. | Rename H1 to "Consistency Models" and move L3-10 (loss of indexes/joins when sharding) to NoSql.md, or split. | High |
| 36 | BROKEN | `![consistency-models.png](../Images/consistency-models.PNG ...)` | `Images/` contains both `consistency-models.png` and `consistency-models.PNG` (identical size). Alt text names `.png`, src names `.PNG`. Case-sensitive filesystems / git renames will bite. | Delete one copy, reference it consistently, give a descriptive alt. | High |
| 38 | WRONG | "### Strict consistency or Linearizability" | Strict consistency (every read returns the most recent write by absolute global time) is *stronger* than linearizability and unachievable without a perfect global clock. Linearizability only requires each op to appear to take effect atomically at some instant between its invocation and response. | Heading "Linearizability"; define it properly. | High |
| 40 | INCONSISTENT | "It's cheaper and a reasonable thing to be doing. Majority of the systems can be linearized." | Contradicts L51 (non-linearisable systems chosen "when you have low latency and high throughput requirements", i.e. linearizability is costly). "Cheaper" than what is unstated. Unattributed talk notes. | Rewrite: linearizability is simplest to reason about but costs latency/availability (coordination). | Medium |
| 52 | WRONG | "In general, external consistency (linearizability) requires **monotonically increasing timestamps**" | Not a general requirement; single-leader replication or consensus (Raft/Paxos) gives linearizability without synchronised timestamps. It is Spanner's specific approach (TrueTime). | "Spanner achieves external consistency via TrueTime timestamps; others use consensus/leader." | Medium |
| 54 | BROKEN | "### Eventual consistency" | Section content is the CAP theorem; eventual consistency itself is never defined anywhere in the file. | Rename to "CAP theorem"; add a real EC definition (and read-your-writes, monotonic reads, causal). | High |
| 60 | WRONG | "Partition tolerance - Operations will complete, even if individual components are unavailable." | Partition tolerance (Gilbert & Lynch) is that the system keeps operating despite arbitrary message loss between nodes. "Components unavailable" is node failure, not partition. | Fix definition. | Medium |
| 65 | WRONG | "Given that partition tolerance is rarely achievable therefore, there really are 2 choices" | Inverted. Partitions are *unavoidable* (as L62 correctly says), so P is not optional; the trade is C vs A **during a partition**. Also contradicts L62 -> INCONSISTENT. | "Since partitions will happen, the real choice is how the system behaves during one: refuse (CP) or diverge (AP)." Add Brewer 2012 / Kleppmann caveat that "2 of 3" is misleading. | High |
| 69 | WRONG | "Do not show the users the same data that they have changed." | Garbled; presumably "**do** show users the data they just changed" (read-your-writes). As written it says the opposite. | Fix and name the guarantee. | Medium |
| 69-71 | OPINION | "Stay out of the newspapers. Avoid globalised widespread failure by compromising the architecture." | Unattributed conference-talk notes presented as guidance. | Attribute the source talk or label as notes. | Medium |
| 84 | WRONG | "external consistency (similar to *linearizability*)" | Spanner's external consistency **is strict serializability** (serializability + real-time order), which is linearizability generalised to multi-object transactions. "Similar to" undersells the one place where the file could connect its two definitions. | "External consistency = strict serializability = serializable + linearizable ordering of transactions." | High |
| 73-79 | DUPLICATE | Spanner / CAP paper discussion | NoSql.md L71 also cites the same Spanner-and-CAP paper. | Keep Spanner detail here; make NoSql.md link to it. | Medium |

Gap (not a table row): the assignment asked specifically about linearizability vs serializability vs strict serializability. The file defines serializability (L24-32) and linearizability (L38-40) in separate sections and never states the relationship (linearizability = single-object/real-time; serializability = multi-object/any order; strict serializability = both). An agent using this as reference would not learn that distinction from this file.

---

## Distributed Systems/Continuous Deployment.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | "# Separate Deployment from Release" | H1 does not match filename "Continuous Deployment"; the file is not about continuous deployment (no pipeline, no automation) but about decoupling deploy from release. | Rename file to `Deploy vs Release.md` or fold into DevOps notes (below). | High |
| (whole) | CLASSIFY | Entire file | Release-engineering / DevOps practice, not a distributed-systems topic. `Cloud and Infrastructure/DevOps/Overview.md` L56 already lists "separate application build, deployment and release" as a principle; this file is the expansion of that bullet. **Not** a fit for `Tools/CICD.md`, which is a (very stale) CI vendor comparison table (VSTS/AppVeyor/Jenkins/Bamboo). | Move content under DevOps/Overview.md as a subsection, delete this file. | High |

Gap (not a table row): L13-20 ("Enable your feature for: Segment of users / Random selected percentage / All") describes **feature flags/toggles**, canary and percentage rollouts without naming any of them, so a search for those terms finds nothing. Suggest naming the patterns (feature toggle, canary, dark launch, ring-based rollout) and citing Fowler/Hodgson.

---

## Distributed Systems/Event Sourcing.md (last commit 2022-06-29)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | (blank line before `# Event Sourcing`) | File starts with an empty line; some tooling that reads the first line as the title will miss the H1. | Remove blank first line. | Low |
| 6-15 | OPINION | "Complete Build ... Temporal Query ... Event Replay ... Subversion uses complete rebuilds" | Near-verbatim, unattributed quotation of Martin Fowler's *Event Sourcing* bliki (2005). Not wrong, but a knowledge base should attribute quoted material. | Add "(Fowler, 2005)" and link. | High |
| 7 | OPINION | "the key to Event Sourcing is that we guarantee that changes to all domain aggregates are initiated by event objects" | Fowler's 2005 framing. Modern practice (Young, Vernon) says *commands* initiate changes and *events* record them - as L29 of this same file says ("Commands are in imperative tense. Events are something that has happened"). Mildly INCONSISTENT. | "all changes are *recorded as* events". | Medium |
| 25 | WRONG | "A snapshot is a memorisation of left fold" | Technical term is **memoization**. | Fix. | High |
| 29 | WRONG | "Since events are never updated there is no primary key on the EventLog table" | Event stores normally key on (stream/aggregate id, version) precisely to enforce optimistic concurrency on append; "no primary key" is not what the linked Greg Young article recommends. | "No updates/deletes; unique key on (AggregateId, Version) for optimistic concurrency." | Medium |
| 35 | OPINION | "Having the Event Store act as a queue removes the latency ... avoid distributed transactions like DTC" | Greg Young's argument; also note the practical caveat that using the store as the queue requires consumers to track position (i.e. it is the Outbox/CDC idea again). | Attribute; cross-link Outbox in Asynchronous Messaging.md L13. | Medium |
| 37-40 | DUPLICATE | "at least once delivery require the event handlers to be idempotent / able to deduplicate" | Third copy of the same point: Asynchronous Messaging.md L15-21 and Servicebus Frameworks.md L7. | Keep one canonical section and link. | High |

Gap (not a table row): CQRS is never mentioned by name - the linked source is `cqrs.wordpress.com` and "projections"/"read models" are described, but the term appears nowhere in the repo except inside a URL. Snapshots, event versioning/upcasting and EventStoreDB (renamed Kurrent, 2025 - Unverified) are also absent. Suggest a CQRS paragraph and cross-link.

---

## Distributed Systems/HTTP Caching.md (last commit 2021-09-28)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 6 | WRONG | "`public` means a resource can be cached at the server" | `public` means the response may be stored by **any** cache, including shared caches (proxy/CDN) - it says nothing about "the server". It also overrides the default non-storability of `Authorization` responses. | "`public`: storable by any cache, shared or private, even if the request had `Authorization`." | High |
| 9 | WRONG | "`must-revalidate` doesn't necessarily mean 'must revalidate', it means the local resource can be younger than the provided `max-age`, so only revalidate if the content has expired." | Garbled. `must-revalidate` means: once the response is **stale**, a cache MUST NOT reuse it without successful revalidation with the origin (no stale-on-error / stale-while-disconnected). Fresh responses are unaffected either way. | Rewrite per RFC 9111 §5.2.2.2. | High |
| 14 | STALE | "`Accept-Encoding: gzip,deflate,sdch`" | SDCH was removed from Chrome in 2017; `br` (Brotli) and now `zstd` are what modern clients send. | `gzip, deflate, br`. | High |
| 15 | OPINION | "`Vary: User-Agent` ... useful for serving different content to desktop and mobile" | Widely discouraged: UA cardinality makes the cache nearly useless; MDN and CDN vendors recommend against it (use client hints or normalise UA at the edge). | Add caveat. | Medium |
| 29 | STALE | "Section 14.8 of RFC 2616" | RFC 2616 was obsoleted by RFC 7234 (2014, i.e. before this commit) and then RFC 9111 (June 2022). The rule quoted (shared cache may store `Authorization` responses only with `s-maxage`, `must-revalidate` or `public`) is still correct (RFC 9111 §3.5). | Cite RFC 9111 §3.5. | High |
| 33-35 | WRONG | "The default behavior ... `Cache-Control: private, s-maxage=0`" | There is no "default header"; the default is simply absence of an explicit storage permission. The example combines `private` (shared caches must not store) with `s-maxage` (applies only to shared caches) - contradictory directives. | Drop the example or explain it is what a proxy might synthesise. | Medium |
| 33, 39 | BROKEN | code fences tagged ` ```sh ` containing HTTP headers | Language tag is wrong (not shell). | Use ` ```http `. | Low |
| 7 | WRONG | "ETag which uniquely identifies the resource (e.g. by performing a hash)" | An ETag identifies a specific *representation/version* of the resource, not the resource. Strong vs weak (`W/`) validators and `If-None-Match`/`If-Modified-Since` -> 304 are never explained though the assignment names them as key. | Fix wording; add a conditional-request paragraph. | Medium |
| 25 | BROKEN | `![cacheable-content.jpg](...)` | Alt text is the filename. | Descriptive alt. | Low |

Gaps (not table rows): no coverage of `s-maxage`, `immutable`, `stale-while-revalidate` / `stale-if-error` (RFC 5861), `Age`, `Expires`, heuristic freshness, or `Clear-Site-Data`. REST.md L82 also has a paragraph on cacheability of verbs that should link here.

---

## Distributed Systems/HTTP.md (last commit 2021-08-23)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | "# HTTP based communication" | H1 does not match filename "HTTP". Minor. | Align one with the other. | Low |
| 3 | INCONSISTENT | "HTTP is a layer 7 protocol that is transmitted over a TCP connection" | The same file's L31-33 describes HTTP/3 over QUIC/UDP. | "HTTP/1.x and /2 run over TCP; HTTP/3 over QUIC (UDP)." | High |
| 21 | STALE | "currently supported by nearly two-thirds of all web browsers in use" | HTTP/2 support is ~97%+ of browsers in 2026; HTTP/2 spec itself was revised (RFC 7540 -> RFC 9113, June 2022). | Remove the percentage or make it dated. | High |
| 27 | STALE | "HTTP/2 also introduces resource prioritization ... clients can now indicate the order" | RFC 9113 (2022) deprecated the HTTP/2 stream-dependency priority scheme; RFC 9218 "Extensible Priorities" replaces it for HTTP/2 and HTTP/3. | Note deprecation and RFC 9218. | High |
| 31-33 | STALE | HTTP/3 section ("QUIC moves multiplexing to the transport protocol") | Correct in substance, but omits that QUIC (RFC 9000, May 2021 - before this commit) and HTTP/3 (RFC 9114, June 2022) are standardised, that QUIC mandates TLS 1.3, and the key benefit (no transport-level head-of-line blocking across streams, 0-RTT). | Expand with RFC numbers and the HOL-blocking point that L23 sets up. | High |
| 43 | STALE | "HTTP 1.0 is very old (almost 25 years old)" | Relative date; RFC 1945 is from 1996 (30 years in 2026). | "RFC 1945, 1996". | High |
| 47 | WRONG | "Because HTTP 1.1 relies on persistent connections, you can use it to send multiple queries in a row and expect responses in the same order. This is called **HTTP pipelining**" | Persistent connections alone allow *sequential* reuse; pipelining is specifically sending requests *without waiting* for responses. More importantly, pipelining is disabled in every major browser (Firefox removed the pref in 2017; Chrome never shipped it) - it should be labelled as effectively dead. | Split the two concepts; add "pipelining is unused in practice; HTTP/2 multiplexing replaced it". | High |
| 55 | BROKEN | "RSockets" | Protocol is "RSocket". | Fix. | Medium |
| 75 | INCONSISTENT | "making HTTP a uni-directional protocol" | L5 defines bidirectional as "send data in both directions over a channel", which HTTP request/response does. HTTP is client-initiated / half-duplex, not unidirectional. | "client-initiated, half-duplex". | Medium |
| 77 | WRONG | "Single TCP connection ... This allows browsers to apply *origin based security model*" | Non sequitur: the origin model comes from the `Origin` header in the WebSocket handshake, not from using one TCP connection. | Move the origin point to the handshake paragraph. | Medium |
| 83 | WRONG | "Sec-WebSocket-Key: key (to ensure anti-tampering of the connection)" | RFC 6455 §1.3: the key/accept exchange exists to prove the server understands WebSocket and to defeat caching intermediaries; it is explicitly **not** a security or anti-tampering mechanism. | "proves the peer is a WebSocket server, not a security feature". | High |
| 102 | STALE | "many more browsers support Websockets than SSE" | Untrue by 2020 (Chromium Edge shipped SSE in Jan 2020; IE is EOL June 2022). Both are universally supported. | Remove. | High |
| 100 vs 104 | INCONSISTENT | L100 "HTTP/2 provides efficient HTTP based bidirectional communication" vs L104 "HTTP/2 is not a replacement for push technologies" | The two sentences pull in opposite directions without explaining that HTTP/2 streams are bidirectional at the frame level but browsers expose no API for server-initiated application messages. | Merge into one accurate statement. | Medium |
| 104 | STALE | "HTTP/2 introduces Server Push which enables the server to proactively send resources to the client cache" | Server Push is dead in browsers: disabled by default in Chrome 106 (Sept 2022) ([Chrome Developers](https://developer.chrome.com/blog/removing-push)) and removed in Firefox 132 (Oct 2024). `103 Early Hints` (RFC 8297) is the replacement; HTTP/3 implementations largely never shipped push. | Mark as historical; mention Early Hints. | High |
| 108 | WRONG | "A server can handle 65,536 sockets per single IP address, however the quantity can be extended by adding additional network interfaces" | Classic misconception. The 65,535 port limit applies to *ephemeral source ports per (client IP, server IP:port)* i.e. to a **client** connecting to one destination. A server listening on one port distinguishes connections by the full 4-tuple and can hold millions, bounded by file descriptors/memory - as L108's own second half and L110 then say. | Delete the 65,536 sentence; keep the kernel-tuning point. | High |
| 112, 116 | STALE | links `?view=aspnetcore-5.0` | .NET 5 reached end of support May 2022. | Link version-less docs. | High |
| 114 | WRONG | "Websockets work on top of TCP and do not use the HTTP protocol, therefore your load balancer needs to work in TCP mode" | L7 proxies (nginx, HAProxy, Envoy, ALB, Azure App Gateway) all proxy WebSocket by honouring the `Upgrade` handshake - L95 of this same file describes exactly that behaviour, so this is also INCONSISTENT. TCP/L4 mode is *an* option, not a requirement. | "Either L4 passthrough or an L7 proxy that supports Upgrade; L7 gives you routing/TLS termination." | High |
| 118-131 | STALE | SignalR: "Forever frame (for Internet Explorer only)"; "SignalR currently is based on the ASP.NET framework. This makes it unsuitable for Non Windows platforms." | Describes classic ASP.NET SignalR. **ASP.NET Core SignalR** (May 2018, three years before this commit) is cross-platform, dropped Forever Frame, and is what Blazor Server uses (Tools/Web Frameworks.md L157). The "unsuitable for non-Windows" claim was already false when written. | Rewrite for ASP.NET Core SignalR; note classic SignalR as legacy. | High |
| 133-139 | STALE | "Streamdata.io is a Proxy as a Service" | Streamdata.io was acquired by Axway in March 2019 and productised as AMPLIFY Streams ([Axway press release](https://www.axway.com/en/company/media/2019/press-release-axway-acquires-streamdataio-advance-event-driven-apis-its)); the standalone service and blog no longer exist as described. Was already stale at commit time. | Replace with a generic "SSE proxy / API streaming gateway" paragraph or drop. | High |
| 137 | WRONG | "uses Server-Sent Event over WebSockets as the Push protocol" | SSE is a plain-HTTP response stream; it does not run "over WebSockets". The linked article is "SSE *vs* WebSockets". | "uses SSE as the push protocol (chosen over WebSockets)". | High |
| 137 | BROKEN | `[Server-Sent Event over WebSockets]((https://streamdata.io/...))` | Double parentheses -> malformed link. | Fix. | High |
| 118-139 | CLASSIFY | "### SignalR" and "### Streamdata.io" sections | Product/vendor sections nested under "## Persistent connections" in a protocol note. SignalR is a .NET framework topic (fits Tools/Web Frameworks.md, which already mentions it). | Move SignalR to Tools/Web Frameworks.md; drop or generalise Streamdata.io. | Medium |
| 17, 35 | BROKEN | `![http-v-HTTP/2.jpg]`, `![http-stacks.PNG]` | Alt text is the filename (and L17 alt does not even match the src). | Descriptive alt. | Low |
| 71 | OPINION | "WebSockets have an extremely lightweight footprint on servers" | Vendor (Ably) marketing claim; L108-114 of the same file argue the opposite (connection-resource pressure). | Label as trade-off. | Medium |

---

## File classification

| File | H1 title | Kind (reference / cheatsheet / conceptual-essay / opinion / index) | Status (current / partially-stale / stale / archive-candidate) | Audience | Suggested tags (3-6) | One-line summary (<=25 words) | Consolidation note |
|---|---|---|---|---|---|---|---|
| Distributed Systems/AMQP.md | AMQP | reference | partially-stale | backend devs using RabbitMQ | amqp, rabbitmq, message-broker, exchange, routing | Lists AMQP 0-9-1 entities and the four exchange types; nothing on AMQP 1.0. | Merge into Asynchronous Messaging.md (as "AMQP 0-9-1 routing") or expand substantially. |
| Distributed Systems/Asynchronous Messaging.md | Asynchronous message‑based integration | conceptual-essay | partially-stale | architects / backend devs | at-least-once, idempotency, outbox, saga, kafka, rabbitmq | Why async messaging, guaranteed delivery via outbox, sagas vs distributed transactions, Kafka vs RabbitMQ, legacy MSMQ. | Canonical home for messaging; absorb AMQP.md; cross-link Servicebus Frameworks.md and Event Sourcing.md for the duplicated idempotency section; add Azure Service Bus. |
| Distributed Systems/Concurrency Models.md | Concurrency models | conceptual-essay | partially-stale | backend devs | concurrency, csp, actors, erlang, go, akka | Shared-memory threads vs CSP (Go) vs actors (Erlang/Akka); concurrency vs parallelism; when actors fit. | Keep; fix CSP name, invert concurrency/parallelism, add .NET (TPL/async/Orleans) and Pekko note. Arguably belongs in Computer Theory/ rather than Distributed Systems/. |
| Distributed Systems/Consistency Models.md | Distributed Databases | conceptual-essay | partially-stale | architects / DB engineers | consistency, linearizability, serializability, cap-theorem, spanner | ACID vs consistency models vs CAP, serializability and linearizability, Spanner/TrueTime notes. | Rename H1; move sharding-loss paragraph (L3-10) to NoSql.md; add strict-serializability bridge and real eventual-consistency definition. |
| Distributed Systems/Continuous Deployment.md | Separate Deployment from Release | cheatsheet | archive-candidate | dev leads / DevOps | feature-toggles, release-management, canary, devops | Deploy vs release distinction and staged feature enablement (segments, percentage, all). | Misfiled: fold into Cloud and Infrastructure/DevOps/Overview.md (L56) and delete. Not a match for Tools/CICD.md (stale vendor comparison). |
| Distributed Systems/Event Sourcing.md | Event Sourcing | conceptual-essay | current | architects / backend devs | event-sourcing, cqrs, projections, event-store, idempotency | Event sourcing as append-only log with projections, functional (left-fold) view, event store design and at-least-once consequences. | Attribute Fowler/Young; name CQRS; drop duplicated idempotency bullets in favour of a link. |
| Distributed Systems/HTTP Caching.md | HTTP Caching | reference | partially-stale | web/backend devs | http, caching, cache-control, etag, vary, cdn | Cache-Control directives, Vary, what to cache at a reverse proxy, caching authenticated responses. | Keep as the caching reference; fix `public`/`must-revalidate`, cite RFC 9111, add conditional requests and s-maxage/stale-while-revalidate; link from REST.md L82. |
| Distributed Systems/HTTP.md | HTTP based communication | conceptual-essay | partially-stale | web/backend devs | http2, http3, quic, websockets, sse, signalr | HTTP/1.x vs /2 vs /3, persistent connections, long polling, WebSockets, SSE, scaling persistent connections, SignalR. | Split: protocol evolution (HTTP/1-3) vs realtime transports (WS/SSE/long-poll); move SignalR to Tools/Web Frameworks.md; drop Streamdata.io; retire Server Push and 65k-socket claims. |

---

## Cross-file observations

1. **Idempotency / at-least-once is written three times.** Asynchronous Messaging.md L15-21, Event Sourcing.md L37-40 and Servicebus Frameworks.md L7 each explain "at-least-once => idempotent handlers + dedup by message id". Asynchronous Messaging.md L13 additionally describes the Outbox pattern without naming it while Servicebus Frameworks.md names it. Pick one canonical section (Asynchronous Messaging.md) and link the others.

2. **AMQP is presented as one thing.** AMQP.md and Asynchronous Messaging.md L78 never distinguish 0-9-1 (RabbitMQ classic model: exchanges/bindings) from 1.0 (ISO standard: links/nodes; Azure Service Bus, ActiveMQ Artemis, now RabbitMQ 4 core). An agent asked "does Azure Service Bus have exchanges?" would be misled. Azure Service Bus itself appears in the repo only as a name in Servicebus Frameworks.md.

3. **RabbitMQ vs Kafka comparison is pre-Streams.** The "RabbitMQ deletes on delivery / not for storage" framing (Asynchronous Messaging.md L93-107) predates RabbitMQ Streams (3.9) and quorum queues; the Kafka ordering claim (L97) omits "per partition". This is the highest-value correction in the messaging set because it drives technology choice.

4. **Consistency vocabulary is split and never joined.** Consistency Models.md defines serializability (under "ACID") and linearizability (under "Consistency models") but never states that strict serializability = both, that CAP's "C" = linearizability (it does say this, L58, good) and that Spanner's "external consistency" = strict serializability. NoSql.md L44 mentions BASE and L71 Spanner/CAP separately. Suggest one "Consistency" page owning: ACID-C vs distributed-C, linearizability, serializability, strict serializability, eventual/causal/read-your-writes, CAP (with the "2-of-3 is misleading" caveat) and PACELC.

5. **Continuous Deployment.md is misfiled.** It is a DevOps practice note (deploy != release, staged enablement). `Cloud and Infrastructure/DevOps/Overview.md` L56 already carries the same principle as a bullet; the note should become that bullet's expansion. `Tools/CICD.md` was skimmed: it is a 2017-era vendor comparison (VS Team Services - renamed Azure DevOps in 2018 - vs AppVeyor, Jenkins vs Bamboo, with prices) and is itself an archive candidate; it is not a home for this content.

6. **HTTP.md mixes three topics**: HTTP protocol evolution (1.x/2/3), realtime transport patterns (long-poll, WS, SSE, scaling), and .NET/vendor products (SignalR, Streamdata.io). Suggested split: `HTTP.md` (protocol; add QUIC/HTTP/3 detail, Early Hints, retire Server Push and pipelining), `Realtime Web Transports.md` (WS/SSE/long-poll/scaling), and move SignalR to Tools/Web Frameworks.md where Blazor already references it.

7. **Terminology collisions an agent would trip on**: "process manager" is used as a stateful-actor synonym (Concurrency Models.md L53) and as a saga/EIP pattern (Asynchronous Messaging.md L23); "temporal coupling" has two in-file meanings in Asynchronous Messaging.md; "strict consistency" is equated with linearizability in Consistency Models.md.

8. **Non-ASCII hyphen in H1s**: Asynchronous Messaging.md (and Synchronous Messaging.md) use U+2011 in the title, defeating plain-text search for "message-based".

9. **.NET concurrency**: the assignment asked to check async/await, ThreadPool and TPL claims. None exist in this file set; Concurrency Models.md treats C# only as a "shared memory with threads" language. For a repo that is otherwise .NET-heavy (MSMQ, SignalR, NServiceBus, MailboxProcessor) this is a notable gap.

10. **Images**: `Images/consistency-models.png` and `.PNG` are duplicate files; all four images referenced in this set use the filename as alt text.

Sources consulted for High-severity currency checks: [RabbitMQ: Native AMQP 1.0 (4.0)](https://www.rabbitmq.com/blog/2024/08/05/native-amqp), [Chrome Developers: Remove HTTP/2 Server Push](https://developer.chrome.com/blog/removing-push), [Axway acquires Streamdata.io (2019)](https://www.axway.com/en/company/media/2019/press-release-axway-acquires-streamdataio-advance-event-driven-apis-its).
