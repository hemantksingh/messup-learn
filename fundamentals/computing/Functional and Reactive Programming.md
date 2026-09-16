# Functional and Reactive Programming

What do "functional" and "reactive" buy me, and what is each word actually about?

Functional is about side effects: keep them out of most of the code, so that most of the code is a function of its inputs and nothing else. Reactive is about time: treat values that arrive over time as a stream you compose, instead of state you poll and copy. The two are often sold together, but they answer different questions.

## Functional programming

When multiple functions have access to some shared data and the ability to write to it, that data is **shared mutable state**. Writes to it are *side effects*, and side effects make the result of a call depend on what ran before it. That is non-determinism.

The big idea in functional programming is managing side effects. Avoiding them gives *referential transparency*: an expression can be replaced by its value without changing the program, because it has no other effect. A function with that property is deterministic. The same inputs always give the same output.

### Pure functions

A **pure function** depends only on its input and returns a value without:

* accessing global state
* modifying its input
* changing shared state

Nothing observable happens except the return value. That makes it trivial to test and safe to call from any thread.

A **higher-order function** is a different thing: one that takes a function as an argument or returns one. `map` and `filter` are higher-order. So is `forEach`, which exists only for its side effects. Purity and being higher-order are independent properties.

### Immutability

Shared state is only a problem if it is mutable. An immutable value cannot change after it is created, so it can be shared freely: no reader can be surprised by a write. Change means producing a new value from the old one; anyone still holding the old one sees what they had before.

In an ordinary codebase this becomes: I/O and mutation at the edges, pure domain logic in the middle. [Testing Strategy](../../practice/Testing%20Strategy.md) makes the same point from the testing side.

### Currying and partial application

**Currying** turns a function of several arguments into a chain of functions of one argument each: `f(a, b, c)` becomes `f(a)(b)(c)`. Each call returns a function waiting for the next argument.

```javascript
const add = (a, b) => a + b;
const addCurried = a => b => a + b;

add(2, 3);          // 5
addCurried(2)(3);   // 5
```

**Partial application** is fixing some arguments and getting back a function of the rest: `addCurried(2)` is a function that adds two. Currying makes partial application fall out for free, which is why the two get confused. They are different: `add.bind(null, 2)` partially applies a function that was never curried.

Together they give expressive syntax and composability: small single-argument functions plug into each other.

## Reactive programming

The Rx (Reactive Extensions) framing: one of the hard problems in programming is dealing with values that change over time. Its answer is the Observable, a sequence of values pushed to you as they arrive, with the operators you would use on a collection.

```javascript
var z = x + y;
```

In the imperative world the value of `z` is not guaranteed to be the sum of `x` and `y` if either changes later. `z` is a copy taken at one instant. Reactive building blocks make `z` always the sum of `x` and `y`, like a spreadsheet cell.

Capturing state is the standard imperative move:

```javascript
for (var i = 0; i < stocks.length; i++) {
    var shouldQuote = false;
    if (stocks[i].symbol === "FB") {
        shouldQuote = true; // a time-varying value, captured
    }
}
```

Exposing `shouldQuote` outside the loop leaks a snapshot that is stale as soon as the stocks change.

The chained form on an array is cleaner but is still not reactive:

```javascript
stocks
    .filter(x => x.symbol === "FB")
    .map(x => x.quote)
    .forEach(x => console.log(x));
```

This is ordinary collection processing, what Fowler calls a collection pipeline. The array is finished before the chain starts, the consumer pulls each element, and the chain runs once. Nothing handles a value that changes after the call.

The reactive version has the same shape, but the source is a stream and values are pushed to the consumer:

```javascript
import { Subject, filter, map } from "rxjs";

const ticks = new Subject();            // quotes arrive over time

ticks.pipe(
    filter(t => t.symbol === "FB"),
    map(t => t.quote)
).subscribe(q => console.log(q));       // runs for every matching tick, forever

ticks.next({ symbol: "FB", quote: 101 });    // printed
ticks.next({ symbol: "AAPL", quote: 190 });  // ignored
ticks.next({ symbol: "FB", quote: 102 });    // printed
```

The pipeline is declared once and stays live. Each tick flows through `filter` and `map` to the subscriber. There is no `shouldQuote` to capture because nothing is stored; the answer is recomputed for every arrival. That is the spreadsheet behaviour.

What Rx gives you:

* Composability: event streams combine with collection operators (`filter`, `map`, `merge`, `debounce`), so a click stream and a network response stream are the same kind of thing.
* Encapsulation: the subscriber sees values, not the timer, socket or callback that produced them.
* Anonymous functions do the work; there is no loop and no loop state.

Rx is often called functional reactive programming. Conal Elliott's original FRP is about continuous, time-varying behaviours; Rx is discrete event streams with functional operators. The operators are the functional part, the stream is the reactive part.

## Related: CSP and actors

Functional programming removes shared mutable state by forbidding the mutation. CSP and the actor model remove it by forbidding the sharing: each process or actor owns its state, and others reach it only through messages on a channel or in a mailbox. [Concurrency Models](Concurrency%20Models.md) covers both.

## How to rederive this

* Pure: output depends only on input, nothing else observable happens. Higher-order: takes or returns a function. Independent.
* Referential transparency: swap an expression for its value; if the program changes, there was a side effect.
* Currying: n arguments become n nested single-argument functions. Partial application: fix some arguments now, supply the rest later.
* Collection pipeline: pull from a finished array, run once. Observable: values pushed over time, pipeline stays live.
* Shared mutable state has two exits: stop mutating (functional) or stop sharing (CSP, actors).

## Sources

* Fowler, [Collection Pipeline](https://martinfowler.com/articles/collection-pipeline/).
* [ReactiveX: Introduction](https://reactivex.io/intro.html) and [Observable](https://reactivex.io/documentation/observable.html).
* [RxJS documentation](https://rxjs.dev/guide/overview).
* Elliott and Hudak, "Functional Reactive Animation", ICFP 1997 (the original FRP).
