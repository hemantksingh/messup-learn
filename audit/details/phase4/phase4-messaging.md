# Phase 4 report: split of fundamentals/messaging/Asynchronous Messaging.md

Nothing committed. Original removed with `git rm` (staged deletion). Three new pages are untracked in `fundamentals/messaging/`.

## (a) Question each page answers

| Page | Question |
|---|---|
| `fundamentals/messaging/Messaging Fundamentals.md` | Why send a message instead of making a call, and what can I rely on when I do? |
| `fundamentals/messaging/Sagas and Process Managers.md` | How do I keep a business process consistent across services without a distributed transaction? |
| `fundamentals/messaging/Message Brokers.md` | What does a broker do, and how do queue brokers and log brokers differ? |

## (b) Prose word counts (outside code fences, no table rows)

Body prose excludes headings and the `## Sources` list; the second figure includes them.

| Page | Before | After (body prose) | After (incl. headings and Sources) | Target |
|---|---|---|---|---|
| Asynchronous Messaging.md (original) | 2,712 (2,776 with headings) | removed | removed | |
| Messaging Fundamentals.md | | 1,169 | 1,256 | 900 to 1,200 |
| Sagas and Process Managers.md | | 898 | 984 | 700 to 900 |
| Message Brokers.md | | 1,299 | 1,408 | 1,000 to 1,300 |

Original section sizes, for reference: intro 105; consistency 300; at-least-once 211; sagas 516; sagas and distributed transactions 288; implementing sagas 15; choosing a messaging system 113; Kafka 141; Kafka and RabbitMQ 500; MSMQ 122; AMQP 0-9-1 model 144; service bus library 155; persisted background jobs 96.

The total grew from 2,712 to 3,366 because each page now carries its own intro, `## How to rederive this` and `## Sources`, and because three joins had to be written (coupling definitions, queues versus topics, timeouts). Every page is inside its own target.

## (c) What was cut and why

- **Duplicate Helland quote.** It appeared twice in the original (consistency option 2 and the sagas section). Kept once, in Messaging Fundamentals under the XA option; Sagas links to it.
- **Fielding quote** trimmed from two paragraphs to the one-line "rest transaction is an oxymoron" with attribution (pasted passage to short attributed quotation).
- **Rhetorical questions** ("How do you recover in case one of the requests fails?", "what if the payment also needs to be triggered...", "What if the order of the business flow changes?") rewritten as statements.
- **Bare-URL bullets** ("Implementing Sagas", "References") became titled `## Sources` entries on the relevant page. The Wistia video link for Udi Dahan's talk was dropped (the blog post is kept).
- **Product-list filler**: "Open source messaging systems e.g. RabbitMQ, Apache Kafka, Apache ActiveMQ, and NSQ" dropped; the brokers still appear as examples where a concept needs one. "earlier Apache Samza, developed at LinkedIn, and Apache Storm" dropped from stream processors (stale, per audit distsys-1 L85).
- **Vendor-ish sentences** dropped: "Kafka ... provides some database like ACID guarantees" (dubious), "Layered on top of Kafka distributed stream processors provide simple but powerful tools ...", "Such queues are not suitable for long-term data storage" (already implied), "NServiceBus does provide pub-sub capability with MSMQ by using its own persistence" (generalised to "a bus library has to add it with its own subscription store").
- **Grammar and spelling** on owner's sentences where meaning was unchanged: "in case if one node goes down", "behavioral" to "behavioural", "centralized" to "centralised".
- **Owner's `> Own view:` blocks**: none existed in the original, none added.

Every Phase 2 correction is preserved in meaning: per-partition ordering and offset-based redelivery, `__consumer_offsets` since Kafka 0.9, RabbitMQ Streams (3.9) caveat with the classic/quorum scope, heuristic labelled "not a rule" with the RabbitMQ single active consumer and Service Bus sessions caveat, MQTT no longer an acronym, STOMP link to stomp.github.io, AMQP 0-9-1 versus 1.0 incompatible and RabbitMQ 4.0 speaking both, MSMQ marked legacy, Transactional Outbox named, Garcia-Molina origin with NServiceBus usage stated, temporal coupling defined as both parties up at once and the flow-change coupling called ordering coupling.

## (d) What was moved where

| Original section | New home |
|---|---|
| Intro (in-band calls, temporal coupling, REST feeds alternative) | Messaging Fundamentals: intro and `## Coupling` |
| Behavioural and ordering coupling (defined inside the sagas section) | Definitions in Messaging Fundamentals `## Coupling`; worked Order/Payment/Shipment chain stays in Sagas `## Event chains and their coupling` with a link back |
| Domain and message persistence consistency (3 options) | Messaging Fundamentals `## Domain and message persistence consistency`, with the outbox given its own `### The Transactional Outbox` |
| Producers guarantee at least once / consumers implement idempotency | Messaging Fundamentals `## At-least-once delivery and idempotent consumers` |
| Persisted background jobs (Hangfire) | Messaging Fundamentals `## Persisted background jobs` |
| Sagas & Process Managers, Sagas and distributed transactions, Implementing Sagas | Sagas and Process Managers (`## What a saga is`, `## Orchestration versus choreography`, `## Sagas and distributed transactions`, Sources) |
| New: timeouts | Sagas and Process Managers `## Timeouts and long-running processes` (written fresh, kept to the fundamental: a durable wait is a message to yourself) |
| Choosing a messaging system (protocols) | Message Brokers `## Protocols` |
| The AMQP 0-9-1 model | Message Brokers `## The AMQP 0-9-1 model` |
| New: queues versus topics | Message Brokers `## Queues versus topics` (competing consumers versus fan-out; what "topic" means in 0-9-1, Kafka, SNS/SQS) |
| Kafka; Kafka and RabbitMQ | Message Brokers `## Queue brokers versus log brokers` with `### Ordering and redelivery` and `### Which to pick`; the "database inside out" paragraph became `## Stream processors` |
| MSMQ | Message Brokers `## MSMQ (legacy)`, C# sample kept (durability off by default is the lesson) |
| What a service bus library adds (incl. licensing paragraph) | Message Brokers `## What a service bus library adds` |

New paragraph in Messaging Fundamentals, `## REST feeds instead of a broker`, summarises the Atom alternative in one paragraph and links `REST.md#atom-based-pub-sub`; REST.md itself is unchanged and keeps its Atom section for now.

Cross-links: Fundamentals links Brokers, Sagas, Event Sourcing and CQRS, Consistency Models, Data Pipelines, REST. Sagas links Fundamentals (#coupling, #domain-and-message-persistence-consistency) and Brokers (from the timeouts section). Brokers links Fundamentals (#at-least-once-delivery-and-idempotent-consumers), Sagas, Event Sourcing and CQRS, Data Pipelines, cloud/aws/Messaging.md.

## (e) Inbound links changed

| File:line | Before | After |
|---|---|---|
| `fundamentals/data/Data Pipelines.md:46` | `[Asynchronous Messaging](../messaging/Asynchronous%20Messaging.md)` | `[Messaging Fundamentals](../messaging/Messaging%20Fundamentals.md#the-transactional-outbox)` |
| `fundamentals/data/Data Pipelines.md:56` | `[Asynchronous Messaging](../messaging/Asynchronous%20Messaging.md)` | `[Messaging Fundamentals](../messaging/Messaging%20Fundamentals.md#at-least-once-delivery-and-idempotent-consumers)` |
| `fundamentals/data/Consistency Models.md:37` | `[Asynchronous messaging](../messaging/Asynchronous%20Messaging.md)` | `[Asynchronous messaging](../messaging/Messaging%20Fundamentals.md)` |
| `fundamentals/messaging/Event Sourcing and CQRS.md:34` | `[Asynchronous Messaging](Asynchronous%20Messaging.md#domain-and-message-persistence-consistency)` | `[Messaging Fundamentals](Messaging%20Fundamentals.md#the-transactional-outbox)` |
| `fundamentals/messaging/Event Sourcing and CQRS.md:36` | `[Asynchronous Messaging](Asynchronous%20Messaging.md#producers-guarantee-at-least-once-delivery-and-consumers-implement-idempotency)` | `[Messaging Fundamentals](Messaging%20Fundamentals.md#at-least-once-delivery-and-idempotent-consumers)` |
| `fundamentals/platform/Resilience Patterns.md:35` | `[Asynchronous Messaging](../messaging/Asynchronous%20Messaging.md)` | `[Messaging Fundamentals](../messaging/Messaging%20Fundamentals.md#coupling)` |

Note on Resilience Patterns: this file is untracked and appeared during my run (another Phase 4 agent is creating it). It was not on my do-not-edit list so I repointed the link with a one-line `sed`; if that agent rewrites the file from its own buffer the change may be lost, so please have them confirm the link reads `../messaging/Messaging%20Fundamentals.md#coupling`.

**Protected files, changes needed (not made by me):**

- `fundamentals/data/Data Platforms.md:41`: `[Asynchronous Messaging](../messaging/Asynchronous%20Messaging.md#kafka)` must become `[Message Brokers](../messaging/Message%20Brokers.md#queue-brokers-versus-log-brokers)`. This link did not exist at the start of my run; the Data Platforms agent added it.
- `fundamentals/platform/Load Balancing and Proxies.md`: no inbound link to the old page, no change needed.
- `fundamentals/platform/Observability.md`: no inbound link to the old page, no change needed.

Pages the assignment said "may link" but had no inbound link (REST.md, Service Orientation.md, Choosing a Database.md, cloud/aws/Messaging.md): left unedited; the new pages link out to REST and AWS Messaging instead.

`audit/wiki-plan.md` structure block already lists "Messaging Fundamentals · Sagas and Process Managers · Message Brokers"; no edit.

Final check: `grep -rn "Asynchronous%20Messaging\|Asynchronous Messaging" fundamentals cloud practice audit/wiki-plan.md` returns only the Data Platforms line above.

## (f) Diagrams for Phase 5 to draw, tables to build

- `images/persisted-background-jobs.drawio.svg` for Messaging Fundamentals `## Persisted background jobs` (already in the wiki-plan table): web app and separate worker both reading one persisted job store. Replaces `images/hangfire-singleprocess.png` and `images/hangfire-winservice.png`, which are not embedded anywhere now and can be deleted.
- `images/transactional-outbox.drawio.svg` for Messaging Fundamentals `### The Transactional Outbox`: one local transaction writing the domain row and the outbox row, a forwarder (poll or CDC) publishing to the broker and marking rows dispatched, with the crash point before "mark dispatched" labelled "duplicate from here".
- `images/saga-orchestration-vs-choreography.drawio.svg` for Sagas `## Orchestration versus choreography`: the Order/Payment/Inventory/Shipment chain drawn twice, event chain versus saga in the middle, and a compensation arrow on a failed step.
- `images/queue-vs-log-broker.drawio.svg` for Message Brokers `## Queue brokers versus log brokers`: delete-on-ack queue with competing consumers versus partitioned log with per-consumer-group offsets; show the m1/m2 reordering on the queue side and the rewind on the log side.
- Optional table for Message Brokers `## Queues versus topics`: rows RabbitMQ (0-9-1), Kafka, Azure Service Bus, AWS; columns "what a queue is", "what a topic is", "how fan-out is done", "how ordering is done".

No image embeds existed in the original page, so none were removed.

## (g) Open questions for the owner

1. The AMQP protocol bullet still says AMQP was "an open replacement for proprietary messaging middleware". True of 1.0's origin (JPMorgan, 2003), but the 0-9-1/1.0 split makes the sentence loose. Keep, or drop the clause?
2. `## MSMQ (legacy)` keeps the four-line `System.Messaging` C# sample because "durable is not the default" is the lesson. Drop the sample and keep one sentence instead?
3. The `## Which to pick` heuristic attributes ordering to "Kafka is usually a better choice". With RabbitMQ Streams and single active consumer, is that still your view, or should it become a neutral "log brokers order per partition; queue brokers order per single consumer"?
4. The Fielding quotation is attributed to the rest-discuss mailing list without a URL (the archive is gone). Keep as an unlinked attribution, or drop the quote?
5. REST.md still holds the full Atom section and the dated "broker is a single point of failure" argument; Messaging Fundamentals now has the one-paragraph summary. When REST.md is trimmed, the Atom section could move here and REST.md link back. Your call on which page owns it.
6. Two new sections (`## Timeouts and long-running processes`, `## Queues versus topics`) are written by me, not from your notes. Please read them for voice; they are the only paragraphs on the three pages that are not either your sentences or a Phase 2 correction.
