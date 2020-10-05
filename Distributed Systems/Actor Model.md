# Actors

*"The Actor model retained more of what I thought were the good features of the object idea"* - Alan Kay, pioneer of object orientation and co designer of Smalltalk. 

Alan Kay thought of messaging between components as "the big idea" in object orientated languages that should be the focus, rather than object properties and their internal behaviour.

Actors are a model of concurrent computation based on messaging. When an actor wants to communicate with another actor, it sends a message rather than contacting it directly, all messaging being asynchronous. The messages are put on a queue, and the receiving actor pulls the messages off the queue one at a time to process them. An actor reacts to messages by doing one of 3 things:

* Can create a new actor (a constructor message)
* Can send a message to an existing actor or
* Can specify its own replacement behaviour (was acting like this, from now on it will start acting differently).

Actors can have internal state between processing messages but **do not share mutable state**.

## Concurrency models

There are other [models of concurrent computing](https://en.wikipedia.org/wiki/Concurrent_computing), such as [Communicating sequential processing](http://www.usingcsp.com/cspbook.pdf) which is [highly influential](https://godoc.org/github.com/thomas11/csp) in the design of programming languages such as *Go* and *Clojure*.

*Java* *C++* *C#* *Python* on the other hand use a shared memory model using threads for concurrency. Threads work on **shared mutable state** using locks to get access to data. Locking means threads contend for data access and need  synchronization. This leads to limited fault tolerance - on crashing, a thread can leave other threads in an inconsistent state and sometimes bring the entire process down.

*Nodejs* uses a single threaded [event loop](https://blog.sessionstack.com/how-javascript-works-event-loop-and-the-rise-of-async-programming-5-ways-to-better-coding-with-2f077c4438b5) that dispatches events to handlers executing asynchronously. It is a proven model that solves some concurrency problems but still relies on a single process to handle multiple requests. [Nested callbacks](https://joearms.github.io/published/2013-04-02-Red-and-Green-Callbacks.html) are inevitable and can cause complexity.

*Erlang* is based on the Actor model and has similar semantics to an OS process. In order words it's completely isolated. If it crashes all resources are released and the other processes around it are unaffected to the same degree as an OS process. It has well established design patterns for fault tolerance. Joe Armstrong explains how Erlang is well suited to [run programs on multicore](https://www.youtube.com/watch?v=bo5WL5IQAd0) machines.

F# implements a message based approach using `MailboxProcessor` that acts as an Actor.

## Actor characteristics

* Actors are an abstraction over processes and threads.

* Actors are **location transparent**. This means no matter where an actor is, as long as it has an address a message can be delivered to the actor. You can have an actor in the same process, an actor on a different machine, an actor in a different process on the same machine. The way you send messages to the actor does not change.

* **Transparent lifecycle management** provides reliability, fault tolerance and self healing capabilities. If an actor errors, supervisor kicks in, handles the error, restarts the actor and prevents an exception bubbling up all the way up and crashing the application.

* **Concurrency** is [different](http://stackoverflow.com/questions/1897993/what-is-the-difference-between-concurrent-programming-and-parallel-programming) from parallelism. Concurrency describes multiple computations occurring simultaneously. Parallelism is concurrency but applied to achieving a single goal. Parallelism is achieved by dividing a single complex process into smaller tasks and executing them concurrently. Concurrent programs are typically concerned with improving both throughput and latency, whereas parallel programming concerns with concurrent operations for the specific goal of improving throughput.

* **Futures/promises** provide a means to receive a result from an asynchronous operation, either as successful completion or as a failure. The component holding the future may choose to wait/block on the result or to receive it asynchronously.

**Latency** is the time required to perform some action (e.g. 8 hours to build a car) whereas **throughput** is the number of tasks that can be completed in a unit of time (e.g. 5 cars per hour produced in a factory)

Actors can be created as needed or can be long lived. As a request comes in it is served by an actor that terminates after processing the request. Long lived actors hold some state and do the work based on previous state aka **process managers**

## When is it a good idea to use actors?

In the synchronous model you have a sequence of events that execute sequentially (in a given order) which in theory is easy (read familiar) to program and reason about, whereas in the event driven asynchronous model the order of execution of concurrent code is not guaranteed. This leads to non determinism and can make it very hard to debug concurrent programs. Depending upon the underlying business problem you may have to explicitly impose ordering on the incoming requests (e.g. by using **correlation**). There may be a practicality limit to parallelizing certain areas of your specific system, if further parallelization could complicate the system beyond your team's ability to reason on it. Therefore it is important to design a system to execute as concurrently as is practical to manage complexity.

Apart from the [asynchronous vs synchronous](https://www.infoq.com/presentations/asynchronous-vs-synchronous?utm_source=twitter&utm_medium=link&utm_campaign=qcon
) designs [debate](https://www.youtube.com/watch?v=bzkRVzciAZg), actors are considered to be a good fit for real time low latency solutions e.g. a chat system where you can have lots of consumers (think millions).

### Actors and messaging systems

Since messaging is a key feature in the Actor model, therefore it often gets confused with messaging systems based on AMQP or JMS. Actors are a model of concurrent computation while messaging is a means to pass messages reliably with *transactional and persistence guarantees*.

Concurrency and parallelism are extremely important for the overall success of reactive, actor-based systems. According to *Amdahl's law*, the speedup of a program using multiple processors in parallel computing is limited by the time needed for the sequential component of the program. For example, if a program needs 20 hours using a single processor core and a part of the program takes 1 hour to execute and cannot be parallelized while the remaining 19 hours (95%) of execution can be parallelized, the minimum execution time for the entire program cannot be less than an hour.

What constitutes the critical one hour that cannot be parallelized?

* Could be a matter of pure blocking for IO on various devices.
* Could be some system complexity that could be unmanageable if treated asynchronously.

Since an actor **does not share its mutable state** with other actors, there is no need for it to lock system resources while handling incoming messages. Being lock- free, theoretically an actor's throughput should be quite fast. This assumes you are avoiding blocking mechanisms (locks) and mechanisms that cause blocking (IO on serial devices). All this enables an actor system to support high-performance, high throughput and low latency operations.

Messaging is better fit if you have long running tasks blocking for IO (frequent in an enterprise with 3rd party integrations) e.g. a scheduled transactional batch processing system.

In theory you could use a messaging transport like AMQP to enable communication between actors but Actors do have their own [remoting](http://doc.akka.io/docs/akka/snapshot/scala/remoting.html) capability with a TCP transport.

http://stackoverflow.com/questions/5693346/when-to-use-actors-instead-of-messaging-solutions-such-as-websphere-mq-or-tibco

## Further reading

http://wiki.c2.com/?ActorsModel

https://www.amazon.co.uk/Reactive-Messaging-Patterns-Actor-Model/dp/0133846830

http://doc.akka.io/docs/akka/2.0.1/
https://www.chrisstucchio.com/blog/2013/actors_vs_futures.html
