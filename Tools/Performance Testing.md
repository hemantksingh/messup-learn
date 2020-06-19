# Performance testing

Inline automated performance testing allows you to run your performance tests as part of your CI/CD pipelines.

* https://locust.io/ - allows you to describe all your tests in python code, with good support for running multiple injectors, basic statistics generation and a useful web dashboard.

* https://gatling.io/ is similar to Locust and is much lighter weight than the older options such as JMeter and Grinder. Built on Scala, the DSL provides extensive functionality out of the box including easily configured data feeds and response assertions. In cases where customization is needed, it is easy to drop into Scala to provide extensions. 

* Older GUI based tools like JMeter are well proven performance testing tools, but creating and maintaining tests is all done in the UI, therefore CI/CD integration isn't well supported.