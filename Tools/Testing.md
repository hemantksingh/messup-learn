# Testing approach

In [this post](https://dannorth.net/2021/07/26/we-need-to-talk-about-testing) about the purpose of testing Dan North, argues that testing is not solely about identifying defects in code. It's about gaining confidence in the software's ability to meet user needs and business goals. Effective testing strategies should prioritise preventing issues from arising in the first place. This can involve architectural choices and well-designed user interfaces that minimise the likelihood of errors. The role of dedicated testers might diminish as development teams adopt better "test thinking" practices. Developers should be actively involved in considering testability throughout the development process.

Automation is valuable, but not a silver bullet. Automated tests are beneficial in achieving repeatability and quick feedback but effective testing strategies should encompass a variety of approaches, including manual testing and exploratory testing and integrating testing throughout the development process, not just as a separate final stage.

* **Automated testing as part of CI/CD**: Write automated tests that are independent of the environment that they run in. To reduce the risk of environment-specific bugs, tests should be able to run in a development environment and in a CI/CD pipeline.
* **Fast feedback loop**: Strive for quick execution times for automated tests to provide immediate feedback and prevent long regressions.
* **Independent tests**: Instead of testing your entire stack as one giant block, focus on testing components that fulfil a specific business functionality. The test boundaries should align with the your business domains and the external dependencies should be mocked.
* **Measure test automation and effectiveness**: Track automation coverage by measuring the number of test cases automated and identify areas for improvement. Monitor the impact of automation on overall quality and defect detection rates.

## Unit or integration tests ?

Test Driven Development (TDD) is a technique we use for writing automation tests before writing the actual implementation. In order to write effective software do we have to swear by it and treat is as the gospel truth? TDD is often attributed to drive better design in your applications, however does performing TDD automatically lead you to a good design? I am not too sure. In distributed applications that often depend upon external services, message queues, databases and other storage devices to accomplish their goals, there is a key component of good design:

> _Separation of I/O code from domain (Non I/O) code_

Being able to [move I/O code to the edges of your application](https://www.youtube.com/watch?v=P1vES9AgfC4&t=1327s&ab_channel=NDCConferences) results in good design, where the **Non I/O** based code becomes easier to test because it

* has explicit inputs and outputs
* is deterministic - for a set of inputs it will give you the same results, everytime
* is not `async`
* does not have any side effects
* does not necessarily need to handle exceptions

I have been part of teams where some TDD enthusiasts must insist on adopting testing patterns like writing tests around **units of logic** e.g. *classes and functions* and **mocking** all dependencies other than the unit or subject under test. At this point I try to pose a question: What is the purpose of writing a test - testing a class or fulfilling a business requirement? Classes and functions are implementation details and tests that are tied to implementation or infrastructure tend to break a lot when either of them changes. Therefore it is best to focus on testing application behavior as opposed to implementation. 

* Identify your System Under Test (SUT) that provides a specific business value
  * Test workflows, not classes
* Test at the boundaries of a system
  * No need to test internals

If we find ourselves mixing behavior with I/O it is time to pause and think.

### What is a unit test?

According to the definition by Kent Beck a unit test is a test that:

* runs in **isolation** from other tests, nothing more nothing less.
* has **no side effects** that can have an impact on other tests, thats why shared resources like file systems and databases are not touched.

This means a unit test essentially has **no I/O**, where a unit does not mean a class or a function

Mocks/Stubs/Fakes allows tests to run in isolation. Adding abstractions, solely to achieve isolation can also end up creating multiple layers of indirection. So it is important to think about when to use mocks and what to mock?

### What is an integration test

Integration tests can be stateful i.e. they have side effects because they often involve testing systems that manage state e.g. the file system, database or a message queue. Therefore an integration test does not necessarily run in isolation with other integration tests, it can span more than one process space, therefore they are I/O dependent.

Rather than worrying about classifying a test as unit or an integration test, **may be the right question to ask is whether the test is I/O dependent?** Consider using integration testing where I/O code is inseperable from the rest. This is appropriate for data-heavy activities:
* ETL and data transformation pipelines
* Data science
* Exploratory coding and throw-away scripts

## Performance testing

Inline automated performance testing allows you to run your performance tests as part of your CI/CD pipelines.

* https://locust.io/ - allows you to describe all your tests in python code, with good support for running multiple injectors, basic statistics generation and a useful web dashboard.
* https://gatling.io/ is similar to Locust and is much lighter weight than the older options such as JMeter and Grinder. Built on Scala, the DSL provides extensive functionality out of the box including easily configured data feeds and response assertions. In cases where customization is needed, it is easy to drop into Scala to provide extensions.
* Older GUI based tools like JMeter are well proven performance testing tools, but creating and maintaining tests is all done in the UI, therefore CI/CD integration isn't well supported.
* A comparision of open source load testing tools - https://medium.com/@loadimpact/open-source-load-testing-tool-review-9b3e622984c1

## Javascript testing

Javascript can run either in the browser or on a Javascript runtime like `nodejs` that is built on Chrome's V8 Javascript engine (written in C++ and used in the Google Chrome browser).

* Jasmine and Mocha are **test frameworks** for writing and executing unit tests in JS.
  * Tests are run via an html file (e.g. spec-runner.html) that includes references to your source and test js files. It is possible to run Jasmine tests programmatically by using a **test runner** like `karma` rather than opening a browser each time you want to run tests.
  * Mocha is a mature JS testing framework running on nodejs and in the browser. Jasmine is more commonly used in angular projects, including the angular project itself.

* Karma is a test runner for running tests programmatically across browsers and devices. You can target specific browser(s) like Chrome, Firefox, IE or PhantomJS (headless browser for faster test feedback) while running your tests.

### Javascript API testing framework

Testing REST APIs with outside-in tests exploiting BDD test narratives

* <http://dareid.github.io/chakram/>
* <https://github.com/apickli/apickli>
