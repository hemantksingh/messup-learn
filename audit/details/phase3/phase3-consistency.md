# Phase 3 report: fundamentals/data/Consistency Models.md

File edited: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/data/Consistency Models.md` (not committed). Final count: **1199 words by `wc -w`**, which includes markdown bullets, headings, the image alt text and the Sources list; about 1,150 words of prose. Under the 1,200 ceiling after the owner's tighten-pass request. One H1 equal to the filename, eight H2 sections, no dashes, no rhetorical questions, no `> Own view:` blocks, no filler words. Relative links to `Choosing%20a%20Database.md` and `../messaging/Asynchronous%20Messaging.md` and the image path `../../images/consistency-models.PNG` verified to resolve.

## (a) Question the page answers

When I read from a distributed database, which writes am I guaranteed to see, and what does each guarantee cost? The first paragraph answers it: linearizability behaves like one copy on one machine, eventual consistency only promises convergence, and every stronger model costs coordination (latency on every request, unavailability during a partition).

## (b) Kept from the original

- Stateless scales by adding servers, databases are stateful, bigger machine only goes so far, partition functionally or by sharding.
- Lost secondary indexes, foreign keys, joins, query optimiser; "that work does not vanish, the application does it" (now one sentence, with a pointer to Choosing a Database).
- Bank account cannot be negative; order quantity and order total; aggregate = group of properties that change together; relook the use case for eventual consistency.
- The italic line "Serializability is not about doing one thing at a time but the effect of what you did is like you did one thing at a time"; serializability is not serial execution; cost is concurrency control, locking and coordination.
- Single-thread, single-processor analogy for linearizability.
- Total vs partial ordering definitions and the `{A, B, C}` example, near verbatim.
- Git as the loosely connected, causal, conflict-resolving example.
- Partitions: servers stop hearing from each other (GC pause), unknown duration, a delayed server looks dead.
- "Consistency here means linearizability"; "client perceives the operations occurred all at once".
- TrueTime as an interval containing true time; non-overlapping intervals ordered, overlapping not; GPS and atomic clocks; serializability from locks, external consistency from TrueTime.
- Overuse of transactions = bottlenecks over a network (2PC) and across cores (serialisation, cache line transfers); the Spanner authors' preference for transactions, now paraphrased with attribution rather than quoted.
- "Identify transactions that always need to be consistent", stated neutrally.
- The consistency-models image embed, with descriptive alt text.

## (c) Dropped and why

- H1 "Distributed Databases" (BROKEN, L1): now "Consistency Models".
- "Strict consistency or Linearizability" heading (WRONG, L38): strict consistency is now defined as needing a perfect shared clock, unimplementable; the slide's top rung is to be read as linearizability.
- "It's cheaper and a reasonable thing to be doing. Majority of the systems can be linearized" (INCONSISTENT, L40): removed; replaced by the cost derivation.
- "External consistency requires monotonically increasing timestamps" (WRONG, L52): now "TrueTime is Spanner's answer, not a general requirement; single-leader replication and consensus give linearizability with no synchronised clocks".
- "### Eventual consistency" heading over CAP text (BROKEN, L54): eventual consistency is defined in the ladder; CAP has its own section.
- Partition tolerance as "components unavailable" (WRONG, L60): now "messages between nodes lost or delayed indefinitely".
- "Partition tolerance is rarely achievable, therefore two choices" (WRONG, L65): now "partitions are a given; during one you choose CP or AP".
- "Do not show the users the same data that they have changed" (WRONG, L69): now "Users must see the data they have just changed", named read-your-writes.
- "Stay out of the newspapers. Avoid globalised widespread failure by compromising the architecture. Localised failure ... cost of doing business" (OPINION, unattributed talk notes, L69-71): dropped per the owner's instruction not to invent Own view text; only the neutral "identify transactions that always need to be consistent" survives.
- "External consistency (similar to linearizability)" (WRONG, L84): now "external consistency is strict serializability".
- Spanner "claims CA, technically CP, five nines" paragraph (L79): dropped for length; it duplicates Choosing a Database and does not answer this page's question.
- Brewer's biography (Berkeley, Inktomi): dropped. The two bare Spanner PDF links: replaced by citations in Sources.
- The verbatim Spanner quote on overuse of transactions: paraphrased with attribution to save words.
- YouTube conflict-resolution link: dropped, unverifiable timestamp.
- `Images/consistency-models.png` vs `.PNG` collision (BROKEN, L36): only `images/consistency-models.PNG` exists now and the embed references it.

## (d) Added, with sources

- Linearizability defined as "takes effect at one instant between request and reply, instants agree with real time"; strict consistency as absolute global time needing a perfect clock. Kleppmann DDIA ch. 9.
- Serializability is formally the I in ACID; the C belongs to the application. Kleppmann DDIA ch. 7.
- The stale-read example (serializable order "read, then transfer" returns the old balance) and strict serializability as serializable plus real-time order. Bailis, "Linearizability versus Serializability" (2014).
- Spanner external consistency = "if T1 commits before T2 starts, T2 sees T1's writes" = strict serializability. Corbett et al. 2012.
- Ladder: sequential, causal, read-your-writes, monotonic reads, eventual, with PRAM = read-your-writes + monotonic reads + monotonic writes. Kingsbury, Jepsen consistency models; Kleppmann ch. 5.
- CAP definitions of A and P. Gilbert and Lynch 2002.
- "2 of 3 is misleading": Brewer 2012. "Either consistent or available when partitioned": Kleppmann ch. 9. PACELC: Abadi 2012.
- Cost derivation: leader or majority on the request path; Raft/Paxos and single-leader replication need no synchronised clocks. Kleppmann ch. 9.
- TrueTime commit-wait and ordering across independent Paxos groups. Corbett et al. 2012, section 4.
- Vernon named for the small-aggregates heuristic. Vernon, "Effective Aggregate Design" (2011).

## (e) Diagrams for Phase 5

- Redraw `images/consistency-models.PNG` as `images/consistency-ladder.drawio.svg`. The slide's top rung is "strict consistency" and the old page equated it with linearizability. The new ladder must not have a strict rung equal to linearizability: either drop strict or draw it above the ladder as a theoretical bound (perfect global clock), with linearizability as the top achievable rung. Suggested rungs, strong to weak: linearizability (single object; strict serializability alongside for transactions), sequential, causal, PRAM (= read-your-writes + monotonic reads + monotonic writes), eventual. The prose already matches this ordering, so only the alt text changes when the picture is swapped.
- Optional: a timeline showing one request's interval and the instant inside it where the operation takes effect, to make linearizability vs strict consistency visible.

## (f) Open questions for the owner

1. Source of the old talk notes "Stay out of the newspapers / localised failure is the cost of doing business". Dropped for now; say if it should return with attribution.
2. `fundamentals/data/Choosing a Database.md` is being rewritten in parallel (modified in the working tree). The audit says this page owns Spanner detail; verify the parallel rewrite shrank its Cloud Spanner section to a link here. If not, Phase 4/5 follow-up.
3. The Spanner "technically CP, treat as CA" point was dropped for length. Say if it should return as one sentence in the CAP section.
4. The old "reasons for non-linearization: low latency and high throughput" is now implicit in the cost section. Say if you want it as an explicit line.
