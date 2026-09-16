# Phase 4 report: split Code Quality into two pages

Files changed (not committed):

* `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/computing/Code Quality.md` (rewritten in place; H1 was `# Software Complexity`, now `# Code Quality`)
* `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/computing/Functional and Reactive Programming.md` (new)

No other file was edited. (`git status` shows other modified files under cloud/ and fundamentals/; those belong to other Phase 4 agents.)

## (a) Question each page answers

* Code Quality: what makes code hard to change, and how do I measure it? Answer: coupling, cohesion and cyclomatic complexity, each with a number computed from source; the numbers say where to look, not that the code is good.
* Functional and Reactive Programming: what do "functional" and "reactive" buy me, and what is each word actually about? Answer: functional is about side effects (keep them out of most of the code), reactive is about time (values that arrive over time as a composable stream).

## (b) Prose word counts

Counted with code fences and table rows excluded. "Body" additionally excludes headings and the Sources list.

| Page | Before | After (body) | After (incl. headings and Sources) | Target |
|---|---|---|---|---|
| Code Quality (whole old page) | 667 | | | |
| Code Quality (new) | | 941 | 1,033 | 800 to 1,000 |
| Functional and Reactive Programming (new) | | 886 | 943 | 700 to 900 |

The growth over the 667-word original is in the enumerated corrections (E - N + 2P with the three-`if` example that shows both bounds, the seven cohesion levels and LCOM, the Observable example and the pull vs push contrast), not in connective prose.

## (c) What was cut and why

* Pasted opinion: the six Atlantic "Coming Software Apocalypse" bullets (spaghetti code killed people, Visual Studio 55M lines, programmers afraid of math, first-person "I've found"). Reason: the first-person lines are interviewees', not the owner's; attributing a speaker would have been from memory (rule 9); the material does not answer either page's question. Dropped entirely rather than keeping one quotation.
* WRONG (audit L18): "pure function or higher order function has no side effects". Replaced by two separate definitions, stated as independent properties, with `forEach` as the higher-order-but-impure example.
* WRONG (audit L18): "a function is independent of any object instance like static methods". Dropped; static methods can still touch global state so it does not bear on purity.
* WRONG (audit L24): currying "enables passing fewer arguments". Now defined as f(a, b, c) to f(a)(b)(c), with partial application defined separately and `add.bind(null, 2)` as partial application without currying.
* OPINION (audit L28): "one of the hardest problems in computer science" attributed as the Rx framing.
* WRONG (audit L50-56): `.filter().map().foreach()` on an array presented as FRP. Kept, `forEach` fixed, labelled as ordinary collection processing (Fowler's collection pipeline), and a real RxJS `Subject` / `pipe(filter, map)` / `subscribe` example placed beside it. Section titled "Reactive programming", with one paragraph on why Rx is not Elliott's FRP.
* WRONG (audit L72): cyclomatic complexity as "number of possible paths, equivalent number of tests". Now linearly independent paths, M = E - N + 2P, upper bound for branch coverage and lower bound for path coverage, with a worked example (three sequential `if`s: M = 4, 2 tests for branches, 8 for paths). Decision-point counting stated for `if`/`while`/`for`/`case`, with `&&`/`||` noted as what most tools add.
* CLASSIFY (audit L76): global-state paragraph moved from Cyclomatic complexity to Coupling.
* WRONG (audit L80): "data cohesion" dropped; replaced by the seven cohesion levels, attributed to Yourdon and Constantine (*Structured Design*, 1979), and LCOM (Chidamber and Kemerer, 1994). Stevens, Myers and Constantine 1974 is cited in Sources as where coupling and cohesion were introduced, not for the seven-level list.
* STALE (audit L94): Panopticode dropped; "Sonar" is SonarQube; "data mining source control" replaced by "static analysis". JArchitect and Gource dropped (Gource is VCS visualisation, not a code metric; the brief asked for one sentence naming SonarQube and NDepend). The sentence says these tools compute "metrics like these" and that which ones varies by tool, since SonarQube no longer reports LCOM or package coupling.
* Fragments: "Anonymous functions", "Encapsulation", "Composability" bullets kept but each given a clause saying what it means.
* Own addition removed on review: two sentences on Robert Martin's instability metric (I = Ce / (Ca + Ce)) were drafted and then cut because they were neither a fix nor a join. See (g) if the owner wants them.

## (d) What was moved where

| Old section (Software Complexity.md) | New location |
|---|---|
| Functional programming, FRP | Functional and Reactive Programming.md |
| Coupling, Cohesion, Cyclomatic complexity, Anaemic domain model, Test Coverage, Complexity Metrics | Code Quality.md |
| Global state bullet (was under Cyclomatic complexity) | Code Quality.md, Coupling section |
| Atlantic article notes | Dropped (see (c) and (g)) |

Added joins (allowed under "what a fix or a join needs"): Code Quality links to the FRP page from the global-state paragraph; FRP links to Testing Strategy (I/O at the edges) and to Concurrency Models (CSP and actors); Code Quality links to Testing Strategy from Test coverage as the brief asked.

## (e) Inbound links

`grep -rn "Code%20Quality.md|Code Quality.md|Software Complexity" fundamentals cloud practice` found one inbound link:

* `fundamentals/computing/Algorithms and Complexity.md` line 5: `[Code Quality](Code%20Quality.md)`, for cyclomatic complexity. Checked, unchanged: the filename is the same and the page has a `## Cyclomatic complexity` section, so it still lands. No edit made.

No page linked to `Functional and Reactive Programming.md` before (it did not exist). No other inbound links to change. All four outbound relative links on the two pages resolve on disk:

* Code Quality.md -> Functional%20and%20Reactive%20Programming.md
* Code Quality.md -> ../../practice/Testing%20Strategy.md
* Functional and Reactive Programming.md -> ../../practice/Testing%20Strategy.md
* Functional and Reactive Programming.md -> Concurrency%20Models.md

Image embeds: the old page had none, so none were removed.

## (f) Diagrams and tables for Phase 5

* `control-flow-graph.drawio.svg` (Code Quality): a small function with three sequential `if`s drawn as a control-flow graph, nodes and edges labelled, showing E - N + 2 = 4 next to the 8 possible paths. Illustrates why M is not the path count.
* `pull-vs-push.drawio.svg` (Functional and Reactive Programming): left, a finished array pulled through filter, map, forEach once; right, a Subject pushing ticks through the same operators to a subscriber over time. Same shape, different source.
* Optional table (Code Quality): cohesion levels with a one-line example each, if the bullet list is judged too dense. Currently a bullet list; no table needed.

## (g) Open questions for the owner

1. The Atlantic article notes are gone. If you want them back, they want their own page (Formal Methods, or a "Why software is hard" essay) with each line attributed to its speaker (Chris Granger, Leslie Lamport, Chris Newcombe are the interviewees the audit named). I did not verify who said what, so I did not keep any.
2. Do you want Robert Martin's instability metric (I = Ce / (Ca + Ce), with the stable-abstractions rule) under Coupling? It answers "how do I measure it" but was not in your notes, so it is out for now.
3. `Concurrency Models.md` has H1 `# Concurrency models` (lowercase m) while the filename is title case. Outside this assignment; flag for the Phase 5 frontmatter sweep.
4. The RxJS example imports `filter` and `map` from `"rxjs"` (RxJS 7 style). If you target RxJS 6 the import is `"rxjs/operators"`. Left version-free in the text per rule 4.
5. No `> Own view:` block on either page: `git show HEAD:"fundamentals/computing/Code Quality.md"` has no owner stance sentences on these topics. The "high cyclomatic complexity is not always bad" and "coverage is perceived risk" points are the owner's original notes, kept as neutral statements.
