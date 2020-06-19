# Software Complexity

Some striking observations from [The Coming Software Apocalypse](https://www.theatlantic.com/technology/archive/2017/09/saving-the-world-from-code/540393/):

* Spaghetti code has killed people.
* Visual Studio is 55 million lines of code, 98% of it is irrelevant
* Do programmers understand the problem they are solving? Most of our time and energy is spent translating complex rules into code, rather than thinking about the rules. You cannot understand cancer by staring at a code editor.
* Code constrains your ability to think when you’re thinking in terms of a programming language, it makes you miss the forest for the trees
* Mathematics actually allows you to think at a higher level than code, the fact that it is completely ignored is the problem of modern software development
* Programmers are afraid of math. I’ve found that programmers aren’t aware—or don’t believe—that math can help them handle complexity. Complexity is the biggest challenge for programmers. When programmers encounter *formal methods* (so called because they involve mathematical, *formally* precise descriptions of programs), their deep-seated instinct is to recoil

## Functional programming

When multiple functions have access to some shared data and the ability to write to this shared data called **shared mutable state**, it can result in *side effects* leading to non determinism.

The big idea in functional programming is managing side effects. By avoiding side effects the overall system gains *referential transparency* which implies that provided a set of inputs a function will always result in the same output or it will have the same behaviour leading to determinism.

Evaluation of a **pure function** or **higher order function** has *no side effects*. A function is different from a method in the sense that a function is independent of any object instance like static methods. A function depends only on its input and returns a value without:

* accessing global state
* modifying input
* changing shared state

**Currying** enables passing fewer arguments to same function. This can result in expressive syntax and function composability.

### Functional Reactive Programming (FRP)

One of the hardest problems in computer science is - Dealing with values that change over time without complexity.

```javascript
var z = x+y
```

In the imperative world value of z is not guaranteed to be the sum of x and y if either x or y change over a period of time. Using reactive building blocks ensures z is always the sum of x and y, very much like a spreadsheet function.

Capturing of state is pretty standard in the imperative style of programming.

```javascript
for(i =0; i < stocks.length; i++)
{
	var shouldQuote = false;
	if(stocks[i].symbol === "FB") {
		shouldQuote = true; // state capture of a time varying value
	}
}
```

Exposing 'shouldQuote' outside the scope of the for loop can lead to undesired consequences. FRP provides an alternative way of handling *time varying values*.

```javascript
var res = stocks
		.filter(x => x.symbol == "FB")
		.map(x => x.quote)
		.foreach(x => console.log(x))
```
(Rx) Reactive Extensions

* Composability - Event streams are composable.
* Encapsulation
* Anonymous functions.

## Coupling

* Afferent (incoming) coupling
* Efferent (outgoing) coupling
* Coupled to an interface or a concrete class
* Law of Demeter - only talk to your friends
* Static dependencies (assemblies, packages, libraries)

## Cyclomatic complexity

* Number of branches/possible paths in the code. Should ideally lead to equivalent number of tests.

* Beware of false positives, sometimes high cyclomatic complexity may be not necessary be bad.

## Cohesion

* Data cohesion - how often is the state used within an object, is there a method that does not use any of the object's state?
* Behaviour cohesion - functional/ procedural cohesion

## Anaemic domain model

Domain objects as data holders with public getter and setters and no behaviour leads to **Feature Envy**. Great example of moving from [Primitive Obsession to Domain Modelling](http://blog.ploeh.dk/2015/01/19/from-primitive-obsession-to-domain-modelling/)

## Test Coverage

Just tells the number of lines of code covered in tests not the health of the code. Perceived risk.

## Complexity Metrics

* Gource - Software version control visualisation
* Sonar, NDepend, JArchitect, Panopticode - Data mining Source control