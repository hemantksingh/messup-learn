---
title: "Testing Strategy"
summary: "What a test is for, why the I/O boundary matters more than the unit or integration label, and how to test performance."
kind: opinion
status: current
last_reviewed: 2026-09-16
sources: []
tags: [testing, tdd, bdd, unit-tests, integration-tests, performance-testing]
---
# Testing Strategy

The [purpose of testing](https://dannorth.net/2021/07/26/we-need-to-talk-about-testing) is not solely about identifying defects in code. It's about gaining confidence in the software's ability to meet user needs and business goals. Effective testing strategies should prioritise preventing issues from arising in the first place. This starts from architectural choices and defining well-designed user interfaces that minimise the likelihood of errors. North argues that the role of dedicated testers might diminish as development teams adopt better "_test thinking_" practices.

Automation is valuable, but not a silver bullet. Automated tests are beneficial in achieving repeatability and quick feedback but effective testing strategies should encompass a variety of approaches, including manual testing and exploratory testing and integrating testing throughout the development process, not just as a separate final stage. Confidence in the code being delivered is gained by working as a team that is evidence led and uses data to drive improvements

* **Quality as shared responsibility**: Testing is a shared collective ownership, not gated by individual QA approvals. Engineers actively consider testability throughout the development process and collaborate with quality engineers from the outset to build confidence and the right checks as early as possible. This involves defining the functional specs, detailing the acceptance criteria, identifying the layers of tests required, writing the test automation scripts and execution.
* **Automated testing as part of CI/CD**: Write automated tests that are independent of the environment that they run in. To reduce the risk of environment-specific bugs, tests should be able to run in a development environment and in a CI/CD pipeline.
* **Fast feedback loop**: Strive for quick execution times for automated tests to provide immediate feedback and prevent long regressions.
* **Independent tests**: Instead of testing your entire stack as one giant block, focus on testing components that fulfil a specific business functionality. The test boundaries should align with your business domains and the external dependencies should be mocked.
* **Measure test effectiveness**: While metrics alone do not guarantee quality, they provide a measure of the team's quality benchmarks. If feature delivery ends up in dropping the test coverage below an agreed threshold, this should act as a trigger for a conversation, rather than being used as a stick to beat the team. Automation coverage can be tracked by measuring the number of test cases automated and identifying areas for improvement. Monitor the impact of automation on overall quality and defect detection rates.

## Unit or integration tests ?

Test Driven Development (TDD) advocates writing automation tests before writing the actual implementation. TDD is often attributed to drive better design in your applications, however does performing TDD automatically lead you to a good design? In distributed applications that often depend upon external services, message queues, databases and other storage devices to accomplish their goals, there is a key component of good design:

> _Separation of I/O code from domain (Non I/O) code_

Being able to [move I/O code to the edges of your application](https://www.youtube.com/watch?v=P1vES9AgfC4&t=1327s) results in good design, where the **Non I/O** based code becomes easier to test because it

* has explicit inputs and outputs
* is deterministic - for a set of inputs it will give you the same results, everytime
* is not `async`
* does not have any side effects
* does not necessarily need to handle exceptions

> Own view: I have been part of teams where some TDD enthusiasts must insist on adopting testing patterns like writing tests around **units of logic** e.g. *classes and functions* and **mocking** all dependencies other than the unit or subject under test. At this point, its worth asking: What is the purpose of writing a test - testing a class or fulfilling a business requirement? Classes and functions are implementation details and tests that are tied to implementation or infrastructure tend to break a lot when either of them changes. Therefore it is best to focus on testing application behavior as opposed to implementation.

* BDD encourages you to stop thinking about HOW your software works to start thinking about WHAT your software does. It isn't about tools like `Cucumber`. It is about collaboration, the conversations between business and delivery that produce shared examples, and about describing the observable behaviour of your software from the user's pov. Identify your System Under Test (SUT) that provides a specific business value. 

  * Test workflows not classes
  * Test behaviours not implementation
  * Test at the boundaries of a system not internals, unless you have implemented a complex algorithm e.g. A loan interest calculator, tax computation, or pricing engine. 

![Two panels. Top, marked with a cross: OrderServiceTest, PaymentServiceTest and InventoryServiceTest, tinted red, each point at their own class inside the system under test, one test per class tied to implementation. Bottom, marked with a tick: a single PlaceOrderTest enters the system under test at OrderService on its boundary, and PaymentService and InventoryService inside the system are reached through OrderService](../images/test-boundaries.drawio.svg "Test behaviour at the boundary, not classes")

There could be cases where enforcing the separation of I/O and non I/O code is either too costly or adds little real value — where you’re better off testing the integration as a whole.  For data intensive applications it maybe better to write an integration test. 

e.g. A report generator that aggregates data from multiple tables using joins, filters, and window functions.
- You could abstract every query behind a pure interface and test the aggregation logic separately with mock data — but:
- The SQL itself is often the most fragile and critical part
- Most bugs arise from mismatches between ORM expectations and actual data.
- Mocking DB behaviour can become unrealistic and brittle.

While writing integration tests, you may want to mock external services that you don't control, as they could be:

- rate limited which leads to throttling during tests.
- flaky, external service may be down which leads to test failures.

### What is a unit test?

Kent Beck's point about unit tests is isolation: a unit test runs in **isolation** from other tests, nothing more nothing less. The stricter rules come from Michael Feathers (2005): a test is not a unit test if it talks to the database, communicates across the network, touches the file system, or needs special environment set up to run. Those rules are about **side effects** that can leak between tests.

My own working definition follows from that: a unit test essentially has **no I/O**, where a unit does not mean a class or a function.

Mocks/Stubs/Fakes allows tests to run in isolation. Adding abstractions, solely to achieve isolation can also end up creating multiple layers of indirection. So it is important to think about when to use mocks and what to mock?

#### Unit testing frontends

Javascript can run either in the browser or on a Javascript runtime like `nodejs` that is built on Chrome's V8 Javascript engine (written in C++ and used in the Google Chrome browser).

* Vitest and Jest are the common **test frameworks** for writing and executing unit tests in JS. Mocha and Jasmine are older alternatives.
  * Unit tests run on nodejs with a simulated DOM (`jsdom` or `happy-dom`), so no browser is opened. Run them in watch mode locally and headless in CI.
  * When you need a real browser, use Playwright, which drives headless Chromium, Firefox and WebKit.

### What is an integration test

Integration tests can be stateful i.e. they have side effects because they often involve testing systems that manage state e.g. the file system, database or a message queue. Therefore an integration test does not necessarily run in isolation with other integration tests, it can span more than one process space, therefore they are I/O dependent.

Rather than worrying about classifying a test as unit or an integration test, **may be the right question to ask is whether the test is I/O dependent?** Consider using integration testing where I/O code is inseparable from the rest. This is appropriate for data-heavy activities:
* ETL and data transformation pipelines
* Data science
* Exploratory coding and throw-away scripts

## Performance testing

### Defining Performance Needs 

The first step is to identify a clear performance goal and **quantify business impact**. Express slow performance in terms of business metrics e.g.
* Customer Impact: "5% of users experience page load times exceeding 3 seconds, leading to a 10% drop in conversion rate."
* Financial Impact: "Failing to meet SLA of 95% uptime for critical transactions results in $1,000 daily revenue loss."

These examples quantify the impact of performance issues and helps determine the level of effort justified for testing and optimisation.

### Identifying Performance Bottleneck 

The next step is to understand where performance bottlenecks might exist in your system. e.g. in an AWS serverless system utilising lambdas, analyse application logs and CloudWatch metrics to pinpoint the root cause of slow performance. Are Lambda functions themselves slow, or are they waiting on downstream services (databases, APIs)?. Here are some key factors:

* Function Location: The region where your Lambda functions reside can influence latency. Functions closer to users generally perform better.
* Function Workload: Focus on heavy tasks within your functions. If they heavily access downstream APIs or databases, network latency might be a major bottleneck.
* Data Processing: If functions perform complex data manipulation, the algorithm and language choice can significantly impact performance.

**Set Performance Goals**: Establish measurable performance targets based on the identified bottleneck and its business impact. e.g.
> _Reduce 95th percentile (p95) page load time from 3 seconds to 2 seconds for a smoother user experience_

### Testing and Optimisation Approach

* Baseline Performance Measurement
  * Use AWS Lambda Insights to measure current performance metrics for your functions, including cold start times, invocation duration, and throttling errors.
  * Utilize Lambda function profiling tools to identify code sections consuming the most CPU and memory. Resources like the official documentation and the aws-lambda-power-tuning project can guide you.

* Simulating Real-World Load

  * Consider tools like JMeter or [Locust](https://locust.io) to simulate realistic user traffic patterns and measure response times under load. Locust allows you to describe all your tests in python code, with good support for running multiple injectors, basic statistics generation and a useful web dashboard. JMeter is a well proven tool. Test plans are authored in its GUI but saved as `.jmx` files and run headless in CI (`jmeter -n -t plan.jmx`). Code-first tools like Locust and [k6](https://k6.io) are still easier to review in a pull request.

* Iterative Optimisation: Based on the identified bottlenecks, consider the following optimisation strategies:
  * Function Location: If latency is an issue, consider deploying functions closer to your users.
  * Downstream API Access: Explore caching mechanisms or optimizing API calls to reduce network latency.
  * Data Processing: Review algorithms and data structures for efficiency. Consider alternative languages or libraries if necessary.
  * Right-sizing Resources: While initially recommended to allocate 1GB RAM for customer-facing functions, you can analyze profiling data and cost considerations to adjust RAM allocation if needed. Sometimes, the cost savings from reduced RAM allocation might not outweigh the development time spent on optimisation.
