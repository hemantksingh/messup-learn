---
title: "Code Quality"
summary: "What makes code hard to change, and how coupling, cohesion, cyclomatic complexity and coverage measure it."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "McCabe, A Complexity Measure, IEEE TSE, 1976"
  - "Stevens, Myers and Constantine, Structured Design, IBM Systems Journal, 1974"
  - "Yourdon and Constantine, Structured Design, 1979"
  - "Chidamber and Kemerer, A Metrics Suite for Object Oriented Design, IEEE TSE, 1994"
  - "Fowler, Anemic Domain Model (bliki); Refactoring (feature envy)"
  - "Seemann, From Primitive Obsession to Domain Modelling"
tags: [code-quality, coupling, cohesion, cyclomatic-complexity, test-coverage]
---
# Code Quality

What makes code hard to change, and how do I measure it?

Code is hard to change when a change in one place forces changes elsewhere (coupling), when one unit does several unrelated jobs (low cohesion), or when a unit has more paths through it than you can test (cyclomatic complexity). Each has a number you can compute from the source. The numbers say where to look, not that the code is good.

## Coupling

Coupling is how much one unit depends on another. Count it in two directions:

* Afferent (incoming) coupling: how many units depend on this one. High means a change here breaks many callers.
* Efferent (outgoing) coupling: how many units this one depends on. High means many reasons for this unit to change.

What you couple to matters too. Coupling to an interface leaves the implementation free to change; coupling to a concrete class does not. Static dependencies (assemblies, packages, libraries) are the coarsest form and the easiest to count.

The Law of Demeter, "only talk to your friends": a method should call methods on itself, its parameters, its own fields, or objects it created. `order.getCustomer().getAddress().getPostcode()` couples the caller to three classes it never asked for.

Global state is coupling that no dependency graph shows. Every reader and writer of a global is coupled to every other one. A local variable limits the scope of a change and the damage a bug can do; a global widens both, and one write becomes a side effect seen everywhere. The functional answer is on [Functional and Reactive Programming](Functional%20and%20Reactive%20Programming.md).

## Cohesion

Cohesion is how well the parts of one unit belong together. Yourdon and Constantine (*Structured Design*, 1979) rank it from worst to best:

* Coincidental: nothing in common (a `Utils` class).
* Logical: similar kinds of thing, chosen by a flag.
* Temporal: run at the same time (everything in `startup()`).
* Procedural: run in a fixed order, on unrelated data.
* Communicational: work on the same data.
* Sequential: the output of one is the input of the next.
* Functional: every part serves one well-defined task.

For a class, the measurable version is LCOM, Lack of Cohesion of Methods (Chidamber and Kemerer, 1994). Take every pair of methods. Count the pairs that share no instance field, subtract the pairs that share at least one, floor at zero. High LCOM says the class is two or more classes wearing one name. The simplest warning sign is a method that uses none of the object's state: it wants to live somewhere else.

## Cyclomatic complexity

McCabe's cyclomatic complexity is the number of linearly independent paths through a unit's control-flow graph:

M = E - N + 2P

where E is the number of edges, N the number of nodes and P the number of connected components (1 for a single function). For a single function this is the number of decision points plus one: each `if`, `while`, `for` and `case` adds one. Most tools also count each `&&` and `||`, since each hides a branch.

It is not the number of possible paths. Three `if` statements in a row give M = 4 but 2^3 = 8 paths; paths grow exponentially, M grows linearly. Its relation to tests:

* An upper bound on the tests needed for branch coverage. M tests along the basis paths cover every branch; often fewer will do (the three `if`s need two: all true, all false).
* A lower bound on the tests needed for path coverage. Fewer than M tests cannot cover every path, and you usually need far more (eight, above).

So M is not "the number of tests to write". It is the minimum the unit deserves, and a rough measure of how hard it is to hold in your head.

Beware of false positives. A `switch` over an enum with one line per case scores high and reads easily; the same M in nested conditions does not. Read the shape of the code, not just the number.

## Anaemic domain model

Domain objects as data holders with public getters and setters and no behaviour give an anaemic domain model (Fowler's name). The behaviour ends up in service classes that pull the data out, work on it and push it back. Fowler calls that smell feature envy: a method more interested in another object's data than its own. The fix is to move the behaviour to the data. Mark Seemann's [From Primitive Obsession to Domain Modelling](http://blog.ploeh.dk/2015/01/19/from-primitive-obsession-to-domain-modelling/) walks through it, starting with a `string` that wants to be a type.

## Test coverage

Coverage reports which lines or branches ran while the tests ran. It says nothing about whether any assertion checked the result, and nothing about the health of the code. Uncovered code is a real signal: nobody has exercised it. High coverage is not the reverse signal. It lowers perceived risk, not risk.

Use it as a trigger, not a target. A drop below an agreed threshold starts a conversation; [Testing Strategy](../practice/Testing%20Strategy.md) has the rest of that argument.

## Tools

Static analysis tools such as SonarQube and NDepend compute metrics like these from source (which ones varies by tool), and report coverage when fed a test run.

## How to rederive this

* Coupling: count dependencies in (afferent) and out (efferent); in means callers break, out means reasons to change.
* Cohesion: ask what the parts share. Nothing, a flag, a time, an order, data, a data flow, or one task.
* LCOM: method pairs sharing no field minus pairs sharing one; high means split the class.
* Cyclomatic complexity: M = E - N + 2P, or decisions plus one. Upper bound for branch coverage, lower bound for path coverage.
* Coverage counts what ran, not what was checked.

## Sources

* McCabe, "A Complexity Measure", IEEE Transactions on Software Engineering, 1976.
* Stevens, Myers and Constantine, "Structured Design", IBM Systems Journal, 1974 (coupling and cohesion introduced).
* Yourdon and Constantine, *Structured Design*, 1979 (the cohesion levels).
* Chidamber and Kemerer, "A Metrics Suite for Object Oriented Design", IEEE TSE, 1994.
* Fowler, [Anemic Domain Model](https://martinfowler.com/bliki/AnemicDomainModel.html); *Refactoring* (feature envy).
* Seemann, [From Primitive Obsession to Domain Modelling](http://blog.ploeh.dk/2015/01/19/from-primitive-obsession-to-domain-modelling/).
