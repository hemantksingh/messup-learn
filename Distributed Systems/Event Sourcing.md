
# Event Sourcing

Event Sourcing is not an over arching architecture but applied to a specific part of the system. Event sourcing is useful when history matters, suitable for transactional write heavy systems that need to maintain an audit log of the transactions. It allows you to deterministically bring up the state of a system at a given time using the audit log. You never really query the log but construct denormalized read models that chase the audit log. These read only views are also called projections of the audit log.

Event Sourcing ensures that all changes to an application state are stored as a sequence of events. The event store capture the series of events and the application final state can be determined by running through the event series.
The most obvious thing gained by Event Sourcing is that we now have a log of all the changes, but the key to Event Sourcing is that we guarantee that changes to all domain aggregates are initiated by event objects. This leads to a number of facilities that can be built on top of the event log:

* Complete Build: We can discard the application state completely and rebuild it by re-running the events from the event log on an empty application.

* Temporal Query: We can determine the application state at any point in time.

* Event Replay:  If we find a past event was incorrect, we can compute the consequences by reversing it and later events and then replaying the new event and later events. The same technique can handle events received in the wrong order.

A common example of an application that uses Event Sourcing is a version control system. Such a system uses temporal queries quite often. Subversion uses complete rebuilds whenever you use dump and restore to move stuff between repository files.

## Event Sourcing is a functional model

In a functional language an event sourcing framework is a:

* Function
* Pattern match
* Left fold.

Current state is a left fold of previous behaviors. A snapshot is a memorisation of left fold. A projection is a fold over your event log.

## [Building Event Storage](https://cqrs.wordpress.com/documents/building-event-storage/)

Since events are never updated there is no primary key on the EventLog table. Commands are in imperative tense. Events are something that has happened in the past.

Events capture business centric data. Events can capture certain info as metadata e.g. user data but not every subscriber of the event is interested in this info. There can be a translation layer that filters event data for things outside the service boundary interested in that particular event.

Depending upon the partition strategy the events can be bound against an aggregate id or tenant id in case of a multi tenanted system. It is feasible to store multiple aggregate events across bounded contexts in the same Event Store bound against tenant id.

Event Store is an appending file therefore it can be used as a queue as well as a persistent store for all your events that capture the system state. In order to achieve guaranteed message delivery, event driven systems may use a distributed transaction that involves a 2 phase commit of the event once to the event storage and once to the persistent queue. Having the Event Store act as a queue removes the latency of writing the event to the Event Store and the queue in the same transaction. This allows us to avoide distributed transactions like DTC which may provide consistency but at the cost of availability.

Messaging systems with **at least once delivery** require the event handlers to be

* idempotent
* able to deduplicate events i.e. handlers are able to recognise duplicate events and drop them if they have already been processed.
