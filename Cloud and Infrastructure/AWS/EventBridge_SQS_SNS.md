# Asynchronous messaging

Reliable asynchronous messaging between systems in a service oriented architecture requires a messaging system (often known as a message broker) to decouple systems. AWS provides the following 3 options in this area

## Simple Queue Service (SQS)

Producer (generates message) ---> Queue ----> Consumer (polls for messages on a queue)

* A queue can have multiple subscribers but only one of them receives the message. This is useful where multiple instances of a consumer are running
* For **fan out** cases, you can have a queue per subscriber but it relies on the producer to publish the same message to multiple queues reliably
* Cannot decide the consumer based on message. Can use SNS message filtering to achieve this.

## Simple Notification Service (SNS)

Producer (publishes message) ----> Topic ----> Consumer (gets notified based on a topic subscription)

* While in SQS a message is pulled by a consumer, in SNS the message is pushed to the consumer
* A topic can have multiple subscribers each of which receives the message, supporting fan out cases inherently
* Can invoke different subscribers based on message metadata using SNS message filtering

## EventBridge

Very similar to SNS but uses different semantics

Producer (publishes messages) ----> Message Bus (topic) ----> Target (Consumer)

* For a specific rule you can have a maximum of 5 targets
* Many out of the box integrations built in for external third party providers like Datadog,PagerDuty, Shopify to prevent you from writing custom code
* Provides conditional message processing. Event filtering can route messages to targets based on message contents. Can transform events before sending to targets.
