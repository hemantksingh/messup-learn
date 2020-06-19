### Testing approach

There are a lot of things we take for granted when doing TDD: **mocking frameworks**, writing tests that focus too much on specific units of logic **classes and methods**, thinking of a **unit** as a class without any collaboration. TDD is a technique we use for writing automation tests before we write the implementation but in order to write effective software do we have to swear by it and treat is as the gospel truth? Does TDD as a technique work in all situations?

TDD is great fun and by TDD I mean writing the test before the implementation, the rest of the stuff (mocks, tests tied to a class or method implementation without any collaboration) is just noise but often I have found when there are no clear inputs and outputs for a given problem, solving it using TDD is'nt always that fun.

Even if we decide to use TDD as an approach to writing automation tests, some questions I believe are still worth revisiting.

* We are generally told tests need to test application behaviour rather than infrastructure or implementation. What does that actually mean? Test behaviour rather than operations or classes (Dan North - BDD approach). What is the trigger of writing a test - a class or implementing a specific requirement?
* Tests tied to implementation detail break if implementation changes. Tests should depend on the surface of your application, public contracts and interfaces.
* What is a unit test?
* When to use mocks and what to mock?
* Adding abstractions in order to achieve isolation ends up creating multiple layers of indirection.


Focus on moving logic inside the application and making the application infrastructure/framework agnostic and persistence ignorant. So how do you move most logic into the application and yet keep it framework agnostic? **Smart endpoints and dumb pipes** Most meaningful code (behaviour) resides inside the application, the rest becomes ritual and ceremony. The idea is to make the I/O channel so dumb and ritualistic that testing it becomes meaningless. We should be able to trust that the framework, database do their jobs correctly. If we find ourselves putting behaviour in the I/O channel or the persistence layer it is time to pause and think. 

**Do we write unit or integration tests?** 
According to Kent Beck a unit test is

* A test that runs in isolation from other tests, nothing more nothing less. 
* Tests that do not have a side effect that can have an impact on other tests.
* That is why shared resources like file systems and databases are not touched. Mocking allows tests to run in isolation.
* Integration tests can be stateful i.e. they have side effects because they often involve testing systems that manage state e.g. the file system, database or a message queue. Therfore an integration test does not necessarily run in isolation with other integration tests. In general an integration test is a test that spans more than one process space.

**May be the right question to ask is what tests give us quick feedback?** 

* Tests that are framework (I/O channel) and infrastructure agnostic
* Tests that are mocking framework agnostic
* Tests that are persistence ignorant
* Tests that are UI agnostic.


### Static methods ###
Prevent global state, that in turn Reduces the scope of change if the global state were to change.