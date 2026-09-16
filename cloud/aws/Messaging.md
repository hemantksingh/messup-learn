# AWS Messaging: SNS, SQS and EventBridge

Reliable asynchronous messaging in service oriented architectures and event driven systems, requires a messaging system, commonly referred to as a message broker, to establish decoupling among systems. AWS offers many messaging services; this note covers three:

## Simple Notification Service (SNS)

Producer (publishes message) ----> Topic ----> Consumer (gets notified based on a topic subscription)

* While in SQS a message is pulled by a consumer, in SNS the message is pushed to the consumer. If the consumer is down, SNS retries per the subscription's delivery policy and can send messages that still fail to a subscription dead-letter queue (an SQS queue)
* A topic can have multiple subscribers each of which receives the message, supporting fan out messaging to large number of subscribers, inherently
* Can invoke different subscribers based on message metadata using SNS message filtering

## Simple Queue Service (SQS)

Producer (publishes message) ---> Queue ----> Consumer (polls for messages on a queue)

* A queue can have multiple subscribers but only one of them receives the message. This is useful where multiple instances of a consumer are running
* For **fan out** cases, you can have a queue per subscriber but it relies on the producer to publish the same message to multiple queues reliably
* Cannot decide the consumer based on message. Can use SNS message filtering to achieve this.
* SNS is push based: delivery is retried per subscription and undeliverable messages can go to a subscription DLQ, but SNS does not persist messages for a consumer to poll later. SQS does. It supports retries and dead-letter queues (DLQ) in case a message fails, and the message remains in the queue for a defined time (by default 4 days, maximum 14 days) before getting deleted automatically.
* Persistence, reliability and ability to batch multiple messages together into one, are the [key differences](https://blog.awsfundamentals.com/aws-sns-vs-sqs-what-are-the-main-differences) between using SNS and SQS.
* Ordering and filtering: standard queues and topics are best-effort ordered and at-least-once. SQS FIFO queues and SNS FIFO topics give strict ordering within a message group plus deduplication. SNS filter policies match on message attributes and, since 2022, on the message payload itself.

### SNS -> Lambda vs SNS -> SQS -> Lambda

SNS -> Lambda approach can be deployed if Lambda's built-in retries are enough for you and if you need to fan out a single message to multiple destinations, however if your messages are critical, SNS -> SQS -> Lambda can prove to be a better solution, as it provides:

* Reprocessing of messages in case of failures and configuring retries before you give up (receive count) on processing a message. So if your lambda fails due to a timeout or a downstream service being unavailable, the message can be sent to a DLQ for reprocessing. SNS -> Lambda gives you less control: Lambda retries an asynchronous invocation twice, then hands the event to an on-failure destination or Lambda DLQ if you configured one, and SNS can also send what it could not deliver to a subscription DLQ. The message is only lost if none of these are set up.
* Batching of messages can provide better scaling and cost efficiency as it allows you to process multiple messages together. So compared to a lambda invocation per message with SNS, batching with SQS leads to fewer lambda invocations which can be more cost effective.

## EventBridge

Very similar to SNS but uses different semantics.

Producer (publishes messages) ----> Event Bus ----> Target (Consumer)

* Provides conditional message processing helping to reduce your costs by only processing events that your application needs. You can filter events with rules. Event filtering can route messages to targets based on message contents. You can transform events before sending to targets. For a specific rule you can have a maximum of 5 targets.
* **Partner event sources** bring events from SaaS providers like Datadog, PagerDuty and Shopify onto an event bus without custom code.
* **API destinations** send events from a bus to an external HTTP endpoint, with EventBridge handling the authentication.
* **EventBridge Pipes** (Dec 2022) are point-to-point: one source (SQS, Kinesis, DynamoDB Streams, MSK, Amazon MQ), an optional filter and enrichment step, one target. No bus in between.
* EventBridge Scheduler makes it easy to create, execute, and manage scheduled tasks at scale.

EventBridge is more suited when a central messaging system that can provide visibility of data going across your domains is needed. Data external to a domain could be published on EventBridge for cross domain/cloud account transfers while internal data within the domain/cloud account could be processed within the domain boundary via SQS or SNS. Permissions must be configured in both accounts to establish an agreement of trust before the events can be sent and received. An event bus policy that grants an upstream account X permission to route events to this account Y must be added.

Separate event bridge buses for external and internal events could also be deployed to prevent internal domain data from being exposed outside the domain.
