# Service Orientation

There are without question pros and cons to the SOA approach, and some of the cons are pretty long. But overall it allows organisations to form independent teams around business capabilities and deliver value to end users quickly and frequently. SOA-driven design enables platforms, build an entire constellation of products by allowing other people to do the work.

Business management in 1950s was done by people passing files across business departments. People were the services and files were the messages. That is why we see organisational aspects keep getting linked back to SOA and microservices.

Conway's Law suggests a link between organizational structure and the software that it creates.

*"Any organization that designs a system (defined more broadly here than just information systems) will inevitably produce a design whose structure is a copy of the organization's communication structure."*

## Business Capability Mapping

* Modelling *what* a business does to reach its objectives (its capabilities), instead of *how* it does it (its business processes)
* Model the business on its most stable elements (Business processes likely to change frequently but the capabilities that it offers remain constant)
* Linked to how businesses organized themselves traditionally around departments
* Have autonomous capabilities/domains with explicit boundaries around them that govern the rules of what messages/data comes in and what goes out
* Align the business architecture with the technical architecture
* Common semantics across the business to determine the ubiquitous language

https://msdn.microsoft.com/en-us/library/bb402954.aspx

### Identifying Service Boundaries

Finding service boundaries is not an easy task and there are no fixed rules. Following are a few heuristics that may or may not enable you to identify service boundaries:

* Immutable data (once created, it does not change) could divide up your services or may be this is immutable data within a service. The data going through service boundaries should be minimal and very basic. This data forms the messages flowing through the system.
* The UI composition may lead you to identify the service boundaries.
* Identify anti requirements - Is there a possibility of requesting one or more fields of entity A along with one or more fields of entity B. For example If the name of the book starts with "Something", customer gets a discount of 10%.

If you happen to share a lot of raw business data between services, even through pub-sub it is generally an indication that your service boundaries are wrong. Preserve the Single source of truth within the service confines and avoid duplication of data across services.

## Cross cutting concerns

### 1st law of distributed computing - Do not distribute

Most systems can run on a single computer. The time to think about more than 1 is when you need availability, because a single machine is not going to be highly available.

<blockquote>“If you can't build a monolith what makes you think you can build distributed Microservices?” - *Simon Brown*</blockquote>

You could easily end up building a monolith over a network instead of memory.

### Distribute mostly for availability and scalability not isolation

The fundamental problem in building applications is finding the balance between isolation and coupling. Isolation allows us to reduce coupling and manage applications better from a technical perspective. It provides more agility where different development teams can work on isolated components without stepping on each others toes. but in order to solve a business problem, applications need to coordinate and sometimes depend on each other. ***The more you isolate, the more coordination is required***.

Coordination itself isn't bad. It is like coupling. You need  enough of it to actually get a system to function and provide value. Coordination can hamper agility when it becomes pervasive and widespread within an application.

One way of isolating stateless applications is distribution. Distribution adds exponential amounts of complexity to coordination. An in memory call can assume that the call will happen fast and safely. When you put a network in the middle, you lose that guarantee. An in memory call takes nano seconds, whereas a network call could take significantly longer which means application coordination over the wire may have to utilise asynchronous communication. This can result in change of application design and further complexity inside your code.

Therefore decision to distribute should be a considered one:

* Do you have the need to be available 24 * 365 ?
* Are you distributing to achieve isolation or scalability and availability? Isolation is difficult to enforce in a monolith. You rely on developer discipline to prevent an object accessing another object's memory. Developer discipline is hard to achieve, especially in a big team. Therefore the tendency is to put a network between 2 pieces of code to achieve this isolation. Distribution is not the only means of enforcing isolation and componentization. This can be done via:
    * building object abstractions, which admittedly is hard especially when working in a big team, but good design is hard.
    * seperate source code repositories for distinct applications
    * running applications in different processes (Erlang has multiple processes running inside the same process space from an OS perspective) on the same machine     
* Do you prefer autonomy over authority? i.e do you prefer the ability to isolate components over the ability to get consistent authoritative answer? By adopting microservices you are by default making this tradeoff. If you are at scale you do not have much of a choice, you have to make this trade off.
* There might be different scaling needs for different software components.
* Log aggregation, monitoring, service location, alerts
* Handling versioning is easier, you can independently bring a service instance down and update it whilst keeping the rest running.

### Isolated deployments

A single deployment unit encapsulating the entire system is easier to manage but inflexible. Splitting the system into multiple components and deploying them individually is desirable, as it allows you to deliver value to end users in small chunks. This means you can perform targeted testing with less regression and rollout changes quickly with minimal risk.

#### Deployment orchestration

Isolating components has an affect on the way they get deployed. More often than not individual components depend on each other, therefore coordination is required to ensure that an individual deployment is compatible with all the clients of that component and does not break the overall system. This coordination can be achieved by orchestrating the deployment and ensuring all dependant components are promoted in a particular order so as to keep the overall system functioning. The deployment orchestration can be manual or automated, depending upon the size of your system, its dependencies and whether you have control over all the system dependencies. Manual orchestration of disparate components into a release is often controlled by processes like **release management** aiming to bring some order and control into the process.

* Guarantee specific versions of components are always deployed to an environment to ensure there is no version misalignment across environments. e.g. individually deploying a new version of component y in environment A and B below can result in breaking the overall system in environment B because someone forgot to upgrade component z.
    
    | Env A (pre) | Env A (post)| Env B (pre)  | Env B (post) |
    | ------------|:-----------:|:------------:|:------------:|
    | x1          | x1          | x1           | x1           |
    | y1          | y2          | y1           | y2           |
    | z2          | z2          | z1           | z1           |

* Deployments are idempotent. Regardless of the specified version, deployments should be able to run repeatedly, multiple times with the same effect even if the specified version is already deployed. This may require checking if the specified version is already deployed in order to skip the deployment or force the deployment of the component anyway.

Deployment orchestration may not be required for components that are completely decoupled from each other i.e. components do not suffer from [temporal and behavioral coupling](https://www.infoq.com/news/2009/04/coupling/) but that is rarely the case. Even if you are working on a library, you cannot control how the clients of the library end up using it out there. The first thing that usually happens, if you weren't careful, is that clients start to depend way too much on the internals of other components. This is a serious problem because clients are not updated on your schedule. They're updated on someone else's schedule, which means that if you leak your internal architecture to a client, you're basically stuck with it for five-plus years.

We are repeatedly fed the microservices juice that tells you to have individual isolated deployments for all your components but if you jump directly to addressing the deployment problem without addressing the coupling and the automated testing problem you can end up putting the cart before the horse.

### Service Discovery

Services need to communicate with each other to fulfill a business request and highly reliable distributed coordination is a challenge in a microservices architecture. In an auto scaling environment, services can be coming up and going down quite frequently, service discovery allows each service to be have a single named identifier that gets resolved or **load balanced** to individual service location. DNS server enables mapping a service location to its IP and PORT. Having a central **service registry** of all the available services, provides the ability to discover a healthy service by querying the central registry. Whenever a new service comes in, it populates that registry and allows other services to know that service X is now available at a particular IP and port. This lets us build much more dynamic infrastructure where, as services come and go or get scaled up and down, we don't have to wait for load balancers and firewalls to be updated before starting to use those services.

Simple routing using [round robin load balancing](https://www.nginx.com/resources/glossary/round-robin-load-balancing/) is sufficient in most cases, however more granular control over load balancing algorithms to each of the services allows us to optimize the resources available to each of the instances of our services.

* Least time algorithm - chooses the instance of the service that has the lowest current response time and continues to route traffic in that manner by continuously updating and monitoring those response times.
* Least connection algorithm - instance with the fewest connections will receive the next connection

According to **Nginx** the least time algorithm has yielded most valuable results for customers with microservices architectures.

Service discovery can be achieved by something simple as  DNS based routing using a load balancer or have a centralised service like **Apache zookeeper** as an address/naming registry to determine what service resides where for large distributed systems. For more dynamic runtime environments like kubernetes, service meshes like **Consul** and **Istio**

### Security

Ingress traffic coming into services
  
* WAF - Web application firewall
* DDOS mitigation
* Rate Limiting

Secure interservice communication

* TLS communication amongst services behind a firewall
* Adopt [Zero trust model](https://www.cloudflare.com/learning/security/glossary/what-is-zero-trust)

### Monitoring and Observability

There is a big distinction being made between monitoring and observability. Monitoring allows us to gauge application health and identify system health.

Observability on the other hand allows us to understand the life of a request as it passes through the services
    * Map cyclic service dependencies
    * Identify Performance bottlenecks
    * OpenTrace based Tracers

## Monolith to Microservices

* Microservices architecture approaches: https://www.nginx.com/blog/introducing-the-nginx-microservices-reference-architecture
* Working Effectively With Legacy Code by Michael Feathers       Chapter 4 - The Seam Model
* Building Microservices by Sam Newman Chapter 5 - Splitting the Monolith
* https://particular.net/blog/break-that-big-ball-of-mud
* https://www.nginx.com/blog/refactoring-a-monolith-into-microservices/
* What about the UI ?
    * https://www.infoq.com/news/2016/02/tilkov-microxchg-human-users
    * https://www.infoq.com/articles/no-more-mvc-frameworks