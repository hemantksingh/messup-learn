# Testing approach

TDD is a technique we use for writing automation tests before writing the actual implementation. In order to write effective software do we have to swear by it and treat is as the gospel truth? Is the test first approach the only technique to build confidence in your software? In order to answer these questions it is important to think about the [purpose of testing](https://dannorth.net/2021/07/26/we-need-to-talk-about-testing/).

## Unit or integration tests ?

I have been part of teams where some less experienced TDD enthusiasts must insist on adopting testing patterns like writing tests around **units of logic** e.g. *classes and functions* and **mocking** all dependencies other than the unit or subject under test. At this point I try to pose a question to them that Dan North (pioneer of Behavior Driven Development BDD) would: What is the trigger of writing a test - a class or implementing a specific requirement? Classes and functions are implementation details and tests that are tied to implementation or infrastructure tend to break a lot when either of them changes. Therefore we are told to to test application behavior as opposed to implementation. Tests should depend on the surface of your application, public contracts and interfaces.

### What is a unit test?

It is useful to remind us of the definition of a unit test that Kent Beck has given:

* A test that runs in isolation from other tests, nothing more nothing less.
* Tests that do not have a side effect that can have an impact on other tests.
* That is why shared resources like file systems and databases are not touched. Mocking allows tests to run in isolation. Adding abstractions in order to solely achieve isolation can also end up creating multiple layers of indirection. So it is important to think about when to use mocks and what to mock?
* Integration tests can be stateful i.e. they have side effects because they often involve testing systems that manage state e.g. the file system, database or a message queue. Therefore an integration test does not necessarily run in isolation with other integration tests. In general an integration test is a test that spans more than one process space.

Focus on moving logic inside the application and making the application infrastructure/framework agnostic and persistence ignorant. So how do you move most logic into the application and yet keep it framework agnostic? **Smart endpoints and dumb pipes** Most meaningful code (behavior) resides inside the application, the rest becomes ritual and ceremony. The idea is to make the I/O channel so dumb and ritualistic that testing it becomes meaningless. We should be able to trust that the framework, database do their jobs correctly. If we find ourselves putting behavior in the I/O channel or the persistence layer it is time to pause and think.

**May be the right question to ask is what tests give us quick feedback?**

* Tests that are framework (I/O channel) and infrastructure agnostic
* Tests that are mocking framework agnostic
* Tests that are persistence ignorant
* Tests that are UI agnostic.

## Performance testing

Inline automated performance testing allows you to run your performance tests as part of your CI/CD pipelines.

* https://locust.io/ - allows you to describe all your tests in python code, with good support for running multiple injectors, basic statistics generation and a useful web dashboard.

* https://gatling.io/ is similar to Locust and is much lighter weight than the older options such as JMeter and Grinder. Built on Scala, the DSL provides extensive functionality out of the box including easily configured data feeds and response assertions. In cases where customization is needed, it is easy to drop into Scala to provide extensions. 

* Older GUI based tools like JMeter are well proven performance testing tools, but creating and maintaining tests is all done in the UI, therefore CI/CD integration isn't well supported.
