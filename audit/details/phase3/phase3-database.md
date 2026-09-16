# Phase 3 report: fundamentals/data/Choosing a Database.md

File: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/data/Choosing a Database.md (was Distributed Systems/NoSql.md). Not committed.

Final word count after the owner's tighten instruction: 1,271 body words plus a 68-word Sources list (target 1,000 to 1,300). Started at 1,810, cut in three passes. One H1 "Choosing a Database", nine H2s, no images, no code fences, no em or en dashes, no connective filler, trailing newline. The only `> Own view:` line is the owner's own sentence from the original ("if your data can comfortably fit on a single database server, a relational database is a good choice"); nothing else is attributed to the owner. Only link out is to `../data/Consistency%20Models.md`. All five external source URLs return 200. The parallel Consistency Models rewrite links back with `Choosing%20a%20Database.md` and keeps only a one-line summary of the sharding cost list, so the two pages do not duplicate.

## (a) Question the page now answers

How do I choose a datastore for a workload, and what am I trading away with each choice? First paragraph: choose by workload shape (write mix, access pattern, wrong-answer tolerance, loss tolerance); every store decides which work it does for you and which moves into your application.

## (b) Kept from the original

* The owner's checklist as seven questions, each with one line on why it matters: read/write mix and concurrent writers; fits on one machine or in memory; access patterns ("a few primary key lookups: a key-value store may be enough"; "if you have not partitioned on the keys you query by, you load everything and filter in the application"); authoritative answers vs availability with the owner's "weird result tolerance"; durability as "on disk before the server says committed" and "you could miss some writes to a logging store"; latency, concurrent users, downtime; team familiarity.
* "If your data can comfortably fit on a single database server relational database is a good choice", as the `> Own view:` block.
* The three relational scaling steps (replication with async lag, functional partitioning, sharding).
* From Consistency Models, as the brief directed: the four sharding losses (secondary indexes, foreign keys, query optimisation, joins) and "this work does not vanish; your application now does it". Cross-shard transactions added.
* "Monotonically increasing sequence is an anti-pattern for horizontal scaling", moved from the old Spanner section into sharding and qualified (see d).
* Fowler's aggregate orientation: order plus line items as one aggregate; "revenue by product makes Product the root"; a second copy rebuilt in batch; "schemaless but implicit schema"; the impedance mismatch; "aggregates are transaction boundaries".
* Graph: the owner's "who bought a particular product rather than what products a customer bought"; index-free adjacency as pointers between adjacent nodes; native vs non-native storage; traversal gains at the cost of non-traversal queries.
* The Redis fork observation, corrected (see d).

## (c) Dropped and why

* "MongoDB has a global write lock per db per server" (L3). False since 2015; brief forbids even a historical mention. Replaced by "check how the engine handles concurrent writers".
* "MongoDB does not provide durable writes by default, does not call fsync" (L14). False for over a decade. Replaced by the current default (majority-acknowledged, journaled).
* "Redis is not a durable data store ... only for caching" (L14). Only true of RDB-only mode. Replaced by RDB vs AOF.
* "This can crash your server if it doesn't have 2X the memory" (L6). Wrong mechanism; corrected to copy-on-write and `fork()` refusal under `vm.overcommit_memory=0`.
* "Relational dbs and NoSQL dbs lack relationships" (L52). Wrong; replaced with "lack cheap multi-hop traversal".
* "With NoSQL you trade off consistency for scalability" (L71). Overgeneralisation; replaced by the consistency dial section.
* The "## Cloud Spanner" section (L69-78). Duplicate of Consistency Models, and Spanner is not NoSQL. Reduced to one distributed SQL paragraph that links there. "Open standards, Standard SQL, JDBC" dropped as catalogue.
* "Partitioning ... (aka microservices)" (L25). Conflation; now "a data technique, not an architecture".
* The three graph use-case bullets (L62-66). Vendor copy with no mechanism.
* "ACID and BASE ... Conflict resolution is handled by versioning" (L44-48). Fragments in Fowler-era framing; replaced by the transactions paragraph and the dial section. Versioning belongs to Consistency Models.
* "Ease of Development / agility / cost of setting up an RDBMS" (L34). Kept only the impedance-mismatch point.
* In the tighten passes: the Own view sentences I had written myself, the "no store removes work" restatements, the "why it matters" padding in the checklist, and the descriptive clauses in the graph and durability sections.

## (d) Added, with sources

* Sharding cost list plus cross-shard transactions: Kleppmann DDIA ch. 6.
* Hot-spot from sequential keys, qualified: "under range partitioning an auto-increment key is an anti-pattern: every new row lands on the last shard; hashing the key spreads writes but loses range scans." DDIA ch. 6. The owner's original was unconditional and wrong under hash sharding.
* Read replica lag: DDIA ch. 5.
* Fowler's four categories; graph as the fourth but not aggregate-oriented: Sadalage and Fowler, NoSQL Distilled ch. 2 and 3.
* Classification table (key-value: Redis, DynamoDB; document: MongoDB, Cosmos DB (multi-model), Couchbase; wide-column: Cassandra, HBase, Bigtable; graph: Neo4j, Neptune): as specified in the brief.
* Multi-document/multi-item transactions in MongoDB, DynamoDB and Cosmos DB "at higher latency and with size limits": vendor docs. Cassandra Accord omitted (audit marks it Unverified).
* Consistency options: Cassandra per-operation levels; DynamoDB strongly consistent reads; Cosmos DB five levels; MongoDB read/write concerns up to majority and linearizable. Vendor docs; long-standing features.
* MongoDB default write concern majority with journal acknowledgement: https://www.mongodb.com/docs/manual/reference/mongodb-defaults/ (audit web-verified; 200).
* Redis RDB vs AOF, `everysec` and `always`: https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/ (200).
* Redis fork copy-on-write, `vm.overcommit_memory=1`: https://redis.io/docs/latest/develop/get-started/faq/ (web-verified this session).
* Redis left BSD in 2024, AGPLv3 added with Redis 8, Valkey fork kept BSD: https://redis.io/legal/licenses/ and https://redis.io/blog/redis-adopts-dual-source-available-licensing/ (web-verified this session). "Redis 8" is the only version number on the page; it is the version that changes the licence.
* Index-free adjacency, native vs non-native storage: Robinson, Webber and Eifrem, Graph Databases ch. 6.
* Distributed SQL paragraph (Spanner, CockroachDB, YugabyteDB; TrueTime uses GPS and atomic clocks): Brewer, "Spanner, TrueTime and the CAP Theorem".
* "How to rederive this": five terse bullets, derived.
* Spelling: "journaled" (one l) kept as MongoDB's own term; Consistency Models does not use the word.

## (e) Diagrams for Phase 5

The old page had no images and the new one embeds none. None are required. Optional: `aggregate-vs-relational.drawio.svg`, one order with its line items as a single aggregate on one node versus the same order as rows in two joined tables, with a second panel showing "revenue by product" cutting across aggregates.

## (f) Open questions for the owner

1. Cosmos DB sits in the document row as "(multi-model)". It also exposes Cassandra, Gremlin and Table APIs. Is one cell enough?
2. DynamoDB is listed as key-value per the brief. Its partition key plus sort key model is often called wide-column. Left as key-value.
3. The team-familiarity question is broadened from the owner's "are your developers more familiar with relational" to "what does the team already run well", covering operations. Confirm.
4. The page is at 1,271 body words, under the 1,300 ceiling but not at the 1,000 low end. All nine sections are mandated by the outline; the checklist (232 words) and the aggregate section (256, including the table) are the places to cut further if wanted.
