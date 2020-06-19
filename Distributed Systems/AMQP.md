# AMQP

[Advanced Message Queueing Protocol](https://www.rabbitmq.com/tutorials/amqp-concepts.html) standard defines the following *AMQP* entities

* Exchange - Post offices or Mailboxes
* Bindings - Rules that determine message distribution
* Queue - receives messages from an exchange it is bound to for delivery to consumers.

A queue binds to the exchange with a routing key (address for the queue).

## Types of Exchange

* **Direct** - Exchange receives a message with a routing key 'K' . If queue binds to the exchange using the same key 'K' it gets the message.

* **Fanout** - A fanout exchange routes messages to all of the queues that are bound to it and the routing key is ignored.

* **Topic** - Topic exchanges route messages to one or many queues based on matching between a message routing key and the pattern that was used to bind a queue to an exchange.

* **Headers** - When matching requires more than one attribute, routing key is ignored.
