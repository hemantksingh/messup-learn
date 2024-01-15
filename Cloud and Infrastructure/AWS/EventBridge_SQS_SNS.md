# Asynchronous messaging

Reliable asynchronous messaging in service oriented architectures and event driven systems, requires a messaging system, commonly referred to as a message broker, to establish decoupling among systems. AWS provides 3 alternatives for messaging:

## Simple Notification Service (SNS)

Producer (publishes message) ----> Topic ----> Consumer (gets notified based on a topic subscription)

* While in SQS a message is pulled by a consumer, in SNS the message is pushed to the consumer. If the consumer is down 
* A topic can have multiple subscribers each of which receives the message, supporting fan out messaging to large number of subscribers, inherently
* Can invoke different subscribers based on message metadata using SNS message filtering

## Simple Queue Service (SQS)

Producer (publishes message) ---> Queue ----> Consumer (polls for messages on a queue)

* A queue can have multiple subscribers but only one of them receives the message. This is useful where multiple instances of a consumer are running
* For **fan out** cases, you can have a queue per subscriber but it relies on the producer to publish the same message to multiple queues reliably
* Cannot decide the consumer based on message. Can use SNS message filtering to achieve this.
* While SNS messages are sent once regardless of the consumer availability, SQS supports retries and dead-letter queues (DLQ) in case a message fails. The message remains in the queue for a defined time (by default 4 days, maximum 14 days) before getting deleted automatically.
* Persistence, reliability and ability to batch multiple messages together into one, are the [key differences](https://blog.awsfundamentals.com/aws-sns-vs-sqs-what-are-the-main-differences) between using SNS and SQS.

## EventBridge

Very similar to SNS but uses different semantics.

Producer (publishes messages) ----> Message Bus (topic) ----> Target (Consumer)

* Provides conditional message processing helping to reduce your costs by only processing events that your application needs. You can filter events with rules. Event filtering can route messages to targets based on message contents. You can transform events before sending to targets. For a specific rule you can have a maximum of 5 targets.
* EventBridge Pipes provide many out of the box integrations built in for external third party providers like Datadog, PagerDuty, Shopify to prevent you from writing custom code.
* EventBridge Scheduler makes it easy to create, execute, and manage scheduled tasks at scale.

EventBridge is more suited when a central messaging system that can provide visibility of data going across your domains is needed. Data external to a domain could be published on EventBridge for cross domain/cloud account transfers while internal data within the domain/cloud account could be processed within the domain boundary via SQS or SNS. Permissions must be configured in both accounts to establish an agreement of trust before the events can be sent and received. An event bus policy that grants an upstream account X permission to route events to this account Y must be added.

Separate event bridge buses for external and internal events could also be deployed to prevent internal domain data from being exposed outside the domain.