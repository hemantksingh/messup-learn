# Sagas and Process Managers

How do I keep a business process consistent across services without a distributed transaction?

There are occasions when a business process requires a flow of steps that need to execute in a particular order.

```text
Order -> Payment -> Shipment
```

In SOA based architectures these steps are often encapsulated as separate services. Asynchronous event based collaboration is often used to decouple the communication between these services by publishing and consuming events.

```text
Order (OrderPlaced) -> Payment (PaymentReceived) -> Order (OrderAccepted) -> Shipment (OrderShipped)
```

## Event chains and their coupling

The above approach can still lead to **behavioural coupling**: the Payment service needs to know about the OrderPlaced event. If the payment also needs to be triggered from a different service, the Payment service must change to process the new incoming event. And if the publishing service changes the published event, the consuming service needs to change too.

The order of the business flow can also change, e.g. an inventory check now needs to be performed before shipping the goods.

```text
Order (OrderPlaced) -> Payment (PaymentReceived) -> Order (OrderAccepted) -> Inventory (ItemFetched) -> Shipment (OrderShipped)
```

This leads to **ordering coupling** (a change in the order of business steps forces a consumer change): the Shipping service now needs to process a different event, published from the Inventory service. [Messaging Fundamentals](Messaging%20Fundamentals.md#coupling) defines these couplings.

[Avoiding puristic event chains](https://www.infoq.com/articles/microservice-event-choreographies) is key to reducing such coupling between services and managing complexity in an event driven asynchronous model. The communication between the services can be routed through a centralised component, a **saga**, that tracks the progress of the overall business process and passes control to the next step or reacts to an event raised by a service.

```text
OrderPlaced -> (Saga) Transformation -> CollectPayment -> Payment
```

## What a saga is

A **saga** is a long lived business transaction or process. It needs to exist when a business process spans more than one service/domain or bounded context. The original saga (Garcia-Molina and Salem, 1987) is a sequence of local transactions, each with a **compensating action** that undoes its business effect. If step three fails, the saga runs the compensations for steps two and one. Nothing is rolled back: a refund is issued, a reservation is released, and the intermediate states were visible all along. The saga gives up isolation so that no lock is held across services.

"Saga" on this page means the orchestrator style (also called a process manager), the usage NServiceBus and Udi Dahan popularised. Sagas listen to events and dispatch commands while services receive commands and publish events (**event command transformation**), and a saga uses a state machine to hold the current status of the business process (e.g. an order status).

## Orchestration versus choreography

The original saga can also be choreographed, with each service reacting to the previous event and no central coordinator. That is the event chain above, and its coupling grows with every step.

Orchestration puts the sequence in one place. The saga knows the order of steps; the services do not.

There is however now the danger of the saga becoming a central monolithic controller that becomes hard to change over a period of time, but if you treat the saga just as a means of keeping track of the status and the order of the business process, you can avoid that knowledge creeping into each individual service. This allows each service to evolve independent of its clients and the business process it supports and move towards a more decoupled design.

## Timeouts and long-running processes

A business process can wait minutes or days for its next step: a payment that never arrives, a warehouse that never confirms. The saga cannot block a thread for that long, and the process hosting it will restart in the meantime, so the wait has to be durable.

The saga's state is persisted after each message it handles. A deadline is set by the saga sending a **timeout message** to itself, delayed by the [broker](Message%20Brokers.md) or a scheduler. When the timeout arrives the saga checks its state: if the step has completed, ignore it; if not, compensate or escalate. The timeout is just another message, so the wait survives a restart. Saga state, like any consumer state, must be saved in the same transaction as the messages the saga sends, see [Messaging Fundamentals](Messaging%20Fundamentals.md#domain-and-message-persistence-consistency).

## Sagas and distributed transactions

Another approach to implement the business process is to wrap it into a distributed transaction spanning more than one service. This often involves going across a network (e.g. Http requests in RESTful services) and is not reliable because *networks aren't reliable, they can and will fail*.

Transactions work well when your resources are modelled within the same database. If you happen to do transactions over Http, it is time to rework your domain model because you are no longer dealing with SQL. Helland's verdict on distributed transactions is quoted in [Messaging Fundamentals](Messaging%20Fundamentals.md#domain-and-message-persistence-consistency).

> "...for now I consider 'rest transaction' to be an oxymoron." - Roy Fielding

Sagas are conceptually similar to a distributed transaction coordinator (DTC) but avoid locking transactions across multiple resources. As opposed to a DTC, sagas offer resilience by compensating state rather than rolling back changes in case of a failure, and the changes made to a resource state are visible externally.

## How to rederive this

* No lock can be held across a network for the life of a business process, so the process is a chain of local commits.
* Anything committed and later regretted is undone by a new action, not a rollback. That is the compensation.
* Someone has to know the order of steps: each service knows its neighbour (choreography) or one component knows the sequence (orchestration).
* A wait that outlives a process must be stored. The cheapest durable wait is a message to yourself.

## Sources

* Hector Garcia-Molina and Kenneth Salem, [Sagas](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf), SIGMOD 1987
* Bernd Rücker, [Avoiding puristic event chains](https://www.infoq.com/articles/microservice-event-choreographies) and [What are long running processes](https://blog.bernd-ruecker.com/what-are-long-running-processes-b3ee769f0a27)
* Udi Dahan, [Saga persistence and event driven architectures](http://udidahan.com/2009/04/20/saga-persistence-and-event-driven-architectures/)
* Jonathan Oliver, [CQRS sagas with event sourcing](http://blog.jonathanoliver.com/cqrs-sagas-with-event-sourcing-part-i-of-ii/)
* Roy Fielding, on transactions and REST, rest-discuss mailing list
