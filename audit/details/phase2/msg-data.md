# Phase 2 corrections: messaging, computing, data, rendering (2026-09-16)

Six files edited, nothing committed, no other file touched. Each edit was an exact-string replacement asserted to match once. Verified after editing: exactly one H1 per file, no U+2011 left, every code fence tagged, no em-dashes added, every in-page anchor and relative link target exists.

## fundamentals/messaging/Asynchronous Messaging.md

- was: `# Asynchronous message‑based integration` (U+2011 hyphen) → now: `# Asynchronous Messaging`
- was: "temporal coupling i.e. previous calls must succeed before the next one can be made" → now: "temporal coupling: caller and callee must both be up at the same time for the call to succeed"
- was: second use "The above approach leads to **temporal coupling**" (ordering change in the business flow) → now: "**ordering coupling** (a change in the order of business steps forces a consumer change)"
- was: outbox described without a name ("An out-of-band (background process) **event forwarding** mechanism...") → now: prefixed "This is the **Transactional Outbox** pattern."
- was: Helland quote appeared twice (option 2 of the persistence list and under "Sagas and distributed transactions") → now: one copy kept under Sagas and distributed transactions; the list item points at it with an in-page anchor
- was: `## Sagas & Process Mangers` → now: `## Sagas & Process Managers`
- was: saga presented only as a central coordinator → now: added that "saga" on this page means the orchestrator style (process manager) as used by NServiceBus and Udi Dahan; the original saga (Garcia-Molina and Salem, 1987) is a sequence of local transactions with compensations and can also be choreographed
- was: STOMP bullet linked https://docs.nats.io/ → now: https://stomp.github.io/
- was: "MQTT - (Message Queue Telemetry Transport)" → now: "MQTT - (originally MQ Telemetry Transport, no longer an acronym)"
- was: AMQP bullet with no 0-9-1 vs 1.0 distinction → now: one line that 0-9-1 (RabbitMQ exchange and queue model) and 1.0 (ISO standard, Azure Service Bus) are different, incompatible protocols, linking to `#the-amqp-0-9-1-model`
- was: "distributed stream processor (e.g. Apache Samza - developed at LinkedIn, Apache Storm)" → now: "Kafka Streams, Apache Flink; earlier Apache Samza ... and Apache Storm"
- was: "the onus is on the consumer to keep track of messages that it has read" → now: consumer decides its offset and when to commit; since Kafka 0.9 (2015) committed offsets are stored broker-side in `__consumer_offsets`
- was: "Such message brokers are not suitable for long-term data storage. However, RabbitMQ is often used with Apache Cassandra ... or with the LevelDB plugin ..." → now: Cassandra/LevelDB sentence deleted; added that the comparison applies to classic and quorum queues and that RabbitMQ Streams (3.9, 2021) are an append-only replayable log with retention
- was: "Fundamentally Kafka does not suffer from this issue as it uses a time ordered event log" → now: order is preserved per partition only (choose the partition key accordingly); redelivery after a crash is by re-reading from the last committed offset, so m1 and m2 are re-processed in order
- was: "Therefore for disjointed job queue ... AMQP and JMS style brokers are a good fit" / "Kafka is a better choice" stated as fact → now: "As a heuristic, ..." and "Kafka is usually a better choice (RabbitMQ single active consumer and Azure Service Bus sessions also give ordering)"
- was: MSMQ section with no status → now: opens "Legacy (Windows and .NET Framework only)."
- Phase 1 appended sections ("The AMQP 0-9-1 model", "What a service bus library adds", "Persisted background jobs") left untouched.

## fundamentals/messaging/Event Sourcing and CQRS.md

- was: file started with a blank line, H1 `# Event Sourcing` → now: no leading blank, H1 `# Event Sourcing and CQRS`
- was: Fowler bliki passage unattributed → now: "The following is paraphrased from Martin Fowler's [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) bliki entry (2005)."
- was: "changes to all domain aggregates are initiated by event objects" → now: "every change to a domain aggregate is recorded as an event object", with a parenthesis that Fowler's 2005 wording was "initiated by" and that in current practice commands initiate and events record, matching the later section
- was: "A snapshot is a memorisation of left fold" → now: "memoization of the left fold"
- was: "Since events are never updated there is no primary key on the EventLog table" → now: events are never updated or deleted, but the table needs a unique key on (aggregate id, version) for optimistic concurrency on append
- was: "Building Event Storage" notes unattributed → now: "Notes from Greg Young's article of that name."
- was: "Having the Event Store act as a queue ... avoide distributed transactions" with no cross-reference → now: typo fixed, plus one sentence that consumers track their own position and this is the same idea as the Transactional Outbox, linking to `Asynchronous%20Messaging.md#domain-and-message-persistence-consistency`
- was: two bullets re-explaining idempotent handlers and deduplication → now: one sentence linking to `Asynchronous%20Messaging.md#producers-guarantee-at-least-once-delivery-and-consumers-implement-idempotency`
- was: CQRS never named → now: `## CQRS` paragraph: command model and query models, term is Greg Young's, projections are the read models, either can be used without the other

## fundamentals/messaging/Service Orientation.md

- was: "a business capaility is synonymous with a business domain or **bounded context**" → now: "a business capability usually maps to a subdomain; **bounded contexts** are the model and language boundaries you draw inside it (often one to one, not always)"
- was: `### 1st law of distributed computing - Do not distribute` → now: `### First Law of Distributed Object Design: don't distribute your objects`, body opens "This is Martin Fowler's law from *Patterns of Enterprise Application Architecture* (2002)."
- was: "Business management in 1950s was done by people passing files..." stated as history → now: prefixed "A useful analogy:"
- was: "According to **Nginx** the least time algorithm has yielded most valuable results" → now: labelled a vendor claim, not independently measured; `least_time` is NGINX Plus only
- was: "centralised service like **Apache zookeeper** as an address/naming registry ... service meshes like **Consul** and **Istio**" → now: Kubernetes Service and DNS as the registry, Consul and etcd outside it, ZooKeeper historical, Istio and Linkerd as meshes that sit on top of discovery
- was: "transmitted via stateful events" → now: "transmitted via event-carried state transfer (events that carry the changed data with them)"
- was: no trailing newline → now: trailing newline

## fundamentals/computing/Concurrency Models.md

- was: `## Communicating Sequential Processing (CSP)` and the same in the link text → now: "Communicating Sequential Processes" in both
- was: six sentences of Go marketing (rethinking system programming, "lean, mean", "you'll want to use it for nearly everything ... replacing your bash, scripts, Python") → now: Go designed at Google from 2007, goroutines are the processes and channels the message-passing primitive (synchronous when unbuffered); Kubernetes, Docker and Prometheus are written in Go; bullets now cover goroutines, channels (unbuffered channel as the CSP rendezvous), static typing and single binary
- was: "drawback - primarily for backend services without support for scripting in the browser" → now: not a natural fit for browser scripting, though a WebAssembly target has existed since Go 1.11 (2018)
- was: Node.js "still relies on a single process ... Nested callbacks are inevitable" → now: callbacks were the original style; promises and `async`/`await` (Node 8, 2017) replaced them; `worker_threads` (stable Node 12, 2019) and `cluster` for more than one core
- was: "Concurrency describes multiple computations occurring simultaneously. Parallelism is concurrency but applied to achieving a single goal." → now: concurrency is dealing with many things at once (structure, may interleave on one core); parallelism is doing many things at once (simultaneous execution on more than one core); a concurrent program may or may not run in parallel
- was: "Long lived actors hold some state ... aka **process managers**" → now: "aka process managers" removed
- was: InfoQ link URL split across two lines → now: one line, tracking parameters dropped
- was: `http://doc.akka.io/docs/akka/snapshot/scala/remoting.html` and `http://doc.akka.io/docs/akka/2.0.1/` → now: `https://doc.akka.io/libraries/akka-core/current/remoting-artery.html` and `https://doc.akka.io/libraries/akka-core/current/`, with a note that Akka moved to the Business Source License in September 2022 and Apache Pekko (https://pekko.apache.org/) is the Apache-licensed fork of Akka 2.6 (all four URLs fetched, 200)
- also: file had no trailing newline; one added (not a listed finding, no content change)

## fundamentals/data/Machine Learning.md

- was: "This method didn't catch on until recently because there wasn't enough data" → now: three things were missing: enough data, enough compute (GPUs) and algorithms that train well at scale
- was: `y = mx + b` re-explained in the intro, "supply new data to the model to see if the new data matches this known pattern" → now: "fitting a line to points (see [Linear regression](#linear-regression) below)" and "supply a new `x` to the model to predict `y`"
- was: unattributed automation-ethics paragraph ("Being fully efficient, always doing what you are told ... inhumane things") → now: deleted (no source to attribute)
- was: data science vs ML distinction stated as fact → now: "One framing (from Analytics Vidhya): ..."
- was: "f(x) = x 2" → now: `` `f(x) = x²` ``
- was: "The mapping between the data and the label helps in **classification**" → now: used for classification (a discrete label) and regression (a continuous value)
- was: "Predicting the price of a house, houses could be classified into new 2 bedroom houses ... This classification can then provide a price" → now: "Regression: predicting the price of a house from its size, number of bedrooms and year built"; fraud bullet becomes "Classification: detecting fraud ..., or marking an email as spam"
- was: ```` ```javascript ```` around the JSON object → now: ```` ```json ````
- was: regression paragraph with no pointer → now: adds "See [Linear regression](#linear-regression) below."
- was: "Document classification: Google news uses various clustering techniques" → now: "News clustering: Google News ... group ... into stories"
- was: Bloomberg sentiment scoring listed as a clustering application → now: moved to the Supervised examples with the sentence "Sentiment scoring into fixed classes is supervised classification."
- was: "`Input data + Number of clusters => Learning process => Clustered data`" → now: prefixed "For k-means:" and adds that DBSCAN and hierarchical clustering do not take the number of clusters as input
- was: "The model gets feedback only when it has finished its goal" → now: rewards may be dense (every step, pole balancing, robot control) or sparse; chess is the sparse example
- was: `## Deep learning` as a fourth same-level type; "has outperformed almost every other type of model, almost every time ... as compared to regression and classification" → now: new `## Model families` H2 with a two-sentence intro, `### Deep learning` under it, and its three H3s (Recurrent Neural Network, Activation function, LSTM) demoted to H4 so the tree stays consistent; overclaim replaced with "dominates perception (images, audio) and language tasks ... on tabular data gradient-boosted tree ensembles such as XGBoost and LightGBM remain strong and often match or beat it"
- was: "Google translate used a bit" → now: one sentence on what an RNN does and that Google Translate used LSTM-based recurrent networks from 2016 until Transformer models replaced them around 2020
- was: activations were Sigmoid and tanh only → now: added ReLU family (ReLU, GELU, SiLU), default since about 2012 because sigmoid and tanh saturate and cause vanishing gradients
- was: no transformers → now: `#### Transformers` paragraph: RNN/LSTM as predecessors, attention, parallel training, embeddings, self-supervised pre-training of LLMs then fine-tuning
- was: "Air B&B" → now: "Airbnb"
- was: "* Neural Machine Translation - NY times" fragment → now: deleted
- was: `### Data transformation` and `### Insuring Data Quality` nested under `## ML Cloud APIs` → now: new `## Data preparation` H2 holding both; heading spelled "Ensuring"
- was: "Use repositories such as DVC (Data Version Control) or Git LFS turnover to manage version control" → now: "Use tools such as DVC (Data Version Control) or Git LFS to version the data"
- Phase 1 appended `## Linear regression` left untouched.

## fundamentals/web and apis/Rendering Patterns.md

- was: `# Web Frameworks` → now: `# Rendering Patterns`
- was: SSR accessibility bullet claiming screen readers rely on HTML source and CSR HTML "may not be fully generated" → now: screen readers read the live DOM; the real CSR risk is focus management and announcing route changes; SSR gets full-page navigation for free
- was: no SSR downside → now: one indented sentence after the SSR sub-bullets: server CPU per request, cache invalidation, time to first byte grows with server work
- was: "Jekyll, Hugo, or Gatsby.js" → now: "Jekyll, Hugo, Astro or Eleventy"
- was: "performing AJAX calls can be quite complex ... when done using vanilla JavaScript" → now: true of `XMLHttpRequest`; `fetch()` (universal since 2017) and `querySelector` cover it, so new code rarely needs jQuery
- was: Angular "uses MVC architecture ... Model, Views and Controllers" → now: component-based, template plus TypeScript class, services via Dependency Injection, no controllers; AngularJS (1.x) named as the MVC framework with controllers and `$scope`, end of life January 2022
- was: "JSX - a declarative syntax to embed JavaScript into HTML", fence ```` ```javascript ```` → now: XML-like extension to JavaScript that describes UI as markup inside JavaScript with expressions in `{}`; fence ```` ```jsx ````; comment fixed to "switching from markup back to JavaScript"
- was: "Hybrid static (SSR), client (CSR) and server (SSR) rendering" with only the per-page model → now: "static (SSG), client (CSR) and server (SSR)"; per-page model attributed to the Pages Router; App Router (Next.js 13, 2022) with React Server Components added
- was: "Next.js supports **PWA features** natively" → now: no built-in PWA support; needs a web app manifest and a service worker, hand-written or via Serwist
- was: "Node.js is best for building ... I/O bound single-page applications ... complex synchronous calculations with waiting times" → now: suits I/O-bound servers (APIs, real-time and WebSocket backends); CPU-bound work blocks the single event loop
- was: `choose-web-ui?view=aspnetcore-8.0` link, "rendoring" → now: versionless link, "rendering"
- was: Blazor described as Server only; "Blazor Server" and "Blazor WebAssembly" nested under Razor Pages → now: Blazor bullet is a component model with hosting models static SSR, Server (SignalR), WebAssembly and Auto (Server on first visit while the WebAssembly runtime downloads, WebAssembly on later visits; chosen per component since .NET 8), linking the hosting-models doc; Razor Pages bullet ends at the template-engine sentence
- was: `### Component Gallery` under `## ASP.NET` → now: `## Component Gallery`
- Phase 1 appended "Middleware pipelines" section left untouched.

## Findings deliberately skipped

- All CLASSIFY rows: moving deployment orchestration out of Service Orientation; moving ML Cloud APIs to a cloud page; moving the training/backpropagation line out of the RNN section; the Web Frameworks folder move; the AMQP.md merge (already done in Phase 1); the SignalR move into this page. Out of scope by instruction.
- Concurrency Models gap: no .NET (TPL, async/await, `Channel<T>`, Orleans) section. A gap, not an error; adding it would be new content.
- Asynchronous Messaging L78 suggested an Azure Service Bus bullet. The appended "AMQP 0-9-1 model" section already names Service Bus; I added the one-line 0-9-1 vs 1.0 note and pointer as instructed, not a new bullet.
- Event Sourcing gap: snapshots, event versioning/upcasting, EventStoreDB/Kurrent. Not a finding against existing text; would be new content.
- Machine Learning L98-101 (Low STALE): TensorFlow-centric tool list, no PyTorch/Polars/HF datasets. Low confidence, would be new content.
- Machine Learning "recipie" typo and Concurrency Models H1 casing ("Concurrency models"): not in the assigned list; left as is.
- Asynchronous Messaging "Kafka provides some database like ACID guarantees" and Concurrency Models "Thousands of goroutines can run on a single thread": no finding against them, not rewritten.
- Rendering Patterns: Angular "standalone components and signals" suggested by the row. Omitted; the fix only needed the component/service/DI correction.
- Service Orientation: Simon Brown quote and other opinion passages not flagged as WRONG/STALE: untouched.
