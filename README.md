# Mess-up and learn

Learnings from some successful and some failed experiments, kept as a wiki of fundamentals in my own words. Each page answers one question in plain language and says where the idea came from. Product detail lives at the source; this is the reasoning I want to be able to rederive.

Opinion is marked `> Own view:`. Every page carries frontmatter with a one-line summary, tags, sources and a `last_reviewed` date. Agents: read [AGENTS.md](AGENTS.md) first.

## Computing

- [Algorithms and Complexity](computing/Algorithms%20and%20Complexity.md): How to read Big O, what common data structures cost, and what P, NP and NP-complete actually mean.
- [Code Quality](computing/Code%20Quality.md): What makes code hard to change, and how coupling, cohesion, cyclomatic complexity and coverage measure it.
- [Concurrency Models](computing/Concurrency%20Models.md): Shared memory threads, CSP channels and actors as three ways to structure concurrent code, and when each fits.
- [Functional and Reactive Programming](computing/Functional%20and%20Reactive%20Programming.md): Functional programming is about side effects, reactive programming about values over time, and why the two answer different questions.
- [The Unix Model](computing/The%20Unix%20Model.md): Everything is a file, everything running is a process, and the shell glues them together with pipes and redirection.

## Networking

- [DNS](networking/DNS.md): How name resolution and caching work, why TTL delays a change, and what each DNS record type is for.
- [IP Addressing](networking/IP%20Addressing.md): How prefix lengths and masks split an address into network and host, and how routing, ARP, VLANs and NAT follow.
- [Local IPC](networking/Local%20IPC.md): Pipes, sockets and shared memory for processes on one machine, and why Unix domain sockets beat loopback TCP.
- [Network Layers](networking/Network%20Layers.md): The four layer TCP/IP model this wiki uses, mapped against OSI, with the protocols and PDUs at each layer.
- [TLS Certificates](networking/TLS%20Certificates.md): How X.509 certificates tie a key to a name, how they are issued, encoded, validated and revoked, and what DV, OV and EV mean.
- [TLS](networking/TLS.md): What the TLS 1.3 handshake does, why RSA key transport was dropped, and what the certificate actually proves.

## Web and APIs

- [API Styles](web%20and%20apis/API%20Styles.md): REST, RPC (SOAP, Thrift, gRPC) and GraphQL compared, and how to choose between resources, procedures and queries.
- [HTTP Caching](web%20and%20apis/HTTP%20Caching.md): What Cache-Control, ETag and Vary tell browsers and proxies, and when authenticated responses may be cached.
- [HTTP](web%20and%20apis/HTTP.md): Why each HTTP version exists: keep alive, multiplexing and QUIC each remove a cost the previous one left on the wire.
- [Realtime Web](web%20and%20apis/Realtime%20Web.md): How a server pushes data to a browser: polling, long polling, WebSockets and Server-Sent Events, and how they scale.
- [Rendering Patterns](web%20and%20apis/Rendering%20Patterns.md): Server side, client side and static rendering compared, where each fits, and the frameworks that implement them.
- [REST](web%20and%20apis/REST.md): What makes an API RESTful: resources, HTTP semantics, idempotency and hypermedia, and how PUT, PATCH and POST differ.
- [Web Performance](web%20and%20apis/Web%20Performance.md): What the Core Web Vitals measure, how lab and field data differ, and which levers move them.

## Data

- [Choosing a Database](data/Choosing%20a%20Database.md): Choose a datastore by workload shape: what sharding costs, what aggregate stores trade, and where relational still wins.
- [Consistency Models](data/Consistency%20Models.md): Which writes a read is guaranteed to see, from linearizability down to eventual consistency, and what each level costs.
- [Data Pipelines](data/Data%20Pipelines.md): How data moves from where it is produced to where it is wanted: batch or stream, ETL or ELT, CDC and idempotent steps.
- [Data Platforms](data/Data%20Platforms.md): How to organise data across an organisation: data mesh and data contracts, and lake versus warehouse versus lakehouse.
- [Machine Learning](data/Machine%20Learning.md): Supervised, unsupervised and reinforcement learning, the model families that serve them, and how linear regression fits a line.

## Messaging

- [Event Sourcing and CQRS](messaging/Event%20Sourcing%20and%20CQRS.md): Why storing every change as an event lets you rebuild, replay and project state, and how CQRS separates the write model from reads.
- [Message Brokers](messaging/Message%20Brokers.md): What a broker does, how queue brokers and log brokers differ, and when ordering makes Kafka the better choice.
- [Messaging Fundamentals](messaging/Messaging%20Fundamentals.md): Why send a message instead of making a call, which coupling it removes, and how the outbox and idempotent consumers make delivery reliable.
- [Sagas and Process Managers](messaging/Sagas%20and%20Process%20Managers.md): How a business process stays consistent across services without a distributed transaction, using compensation, orchestration and durable timeouts.
- [Service Orientation](messaging/Service%20Orientation.md) *(opinion)*: Where to draw service boundaries, and why distributing for isolation rather than availability builds a monolith over a network.

## Security

- [Browser Security Model](security/Browser%20Security%20Model.md): Which rules the browser enforces by origin and which by site, and why cookies ride along on requests the page cannot read.
- [Cloud Security](security/Cloud%20Security.md): How the cloud security frameworks stack from threat model to provider assurance, and what each layer answers that the others do not.
- [Cross Site Request Forgery](security/Cross%20Site%20Request%20Forgery.md): How an attacker forges an authenticated request using the victim's cookies, and why tokens remain the primary defence with SameSite behind them.
- [Cross Site Scripting](security/Cross%20Site%20Scripting.md): How injected script runs in a victim's page, and why context aware output encoding is the defence that filters and headers only back up.
- [Cryptography Basics](security/Cryptography%20Basics.md): Which primitive gives confidentiality, integrity, authenticity or non-repudiation, and why the others cannot.
- [Data Privacy](security/Data%20Privacy.md): What makes data personally identifiable, how fingerprinting tracks you without cookies, and what GDPR demands, including when data leaves the EU or UK.
- [Endpoint Security](security/Endpoint%20Security.md): How antivirus, EPP and EDR differ, how to read a VirusTotal verdict, and how YARA turns a malware description into a detector.
- [Secrets Management](security/Secrets%20Management.md): Where a secret can live, why each step from repo to store to workload identity moves the problem, and how to sign your work.
- [Security Headers](security/Security%20Headers.md): What each HTTP security header makes the browser do, which are obsolete, and why adding them blindly teaches you nothing.
- [Security Principles and Threat Modelling](security/Security%20Principles%20and%20Threat%20Modelling.md): How to find and rank the threats to a system with four questions and STRIDE, and the principles good mitigations follow.
- [Standards and Compliance](security/Standards%20and%20Compliance.md): What ISO 27001, SOC 2, PCI DSS and FIPS 140 each certify, and why FIPS validated cryptography is not the same as secure.
- [Supply Chain and Container Security](security/Supply%20Chain%20and%20Container%20Security.md): How to know that what you run is what you built, through signing, SBOMs and SLSA, and how to limit a compromised container.
- [Web Application Risks](security/Web%20Application%20Risks.md): What goes wrong in web applications, how the main OWASP risks work, and which layer of defence slows each attack.

## Platform

- [Configuration Management](platform/Configuration%20Management.md): How a configuration management tool converges machines to a declared state, using Ansible's push over SSH model as the example.
- [Containers](platform/Containers.md): Why a container is a process with a restricted view, not a small virtual machine, and what namespaces, cgroups and layers each decide.
- [DevOps and Delivery](platform/DevOps%20and%20Delivery.md): What DevOps means beyond the acronym, which metrics tell you delivery is improving, and why deployment and release are separate acts.
- [Infrastructure as Code](platform/Infrastructure%20as%20Code.md): What infrastructure as code gives you, how Terraform's providers, resources and modules fit together, and why state must be remote and locked.
- [Kubernetes Security](platform/Kubernetes%20Security.md): How the API server authenticates callers, how roles and bindings scope what they may do, and what hardens pods and the cluster.
- [Kubernetes](platform/Kubernetes.md): How one reconciliation loop explains Kubernetes, from control plane and workload objects to pod networking, Services and the Gateway API.
- [Load Balancing and Proxies](platform/Load%20Balancing%20and%20Proxies.md): What a reverse proxy or load balancer does for you, layer 4 against layer 7, and how Nginx and HAProxy differ in doing it.
- [Observability](platform/Observability.md): How to tell what the software is doing for real users from logs, metrics and traces alone, and which alerts deserve a page.
- [Resilience Patterns](platform/Resilience%20Patterns.md): How a system keeps working when a dependency is slow or down, by bounding every wait, capping what it sends and stopping calls.

## Cloud

- [AWS](cloud/aws/README.md): Index of the AWS pages, built on one idea: every action is an API call that IAM, KMS and VPC control and CloudTrail records.
- [AWS: Disaster Recovery](cloud/aws/Disaster%20Recovery.md): How disaster recovery differs from high availability, what RTO and RPO mean, and which of the four AWS strategies each budget buys.
- [AWS: EKS](cloud/aws/EKS.md): What AWS runs and what you still own on EKS, why pods run out of IP addresses, and how IAM becomes the cluster authenticator.
- [AWS: Identity](cloud/aws/Identity.md): How IAM decides who can do what in AWS, through users, roles and the policy types that grant or only restrict.
- [AWS: Key Management](cloud/aws/Key%20Management.md): Where KMS key material lives, how envelope encryption gets round the 4 KB limit, who may use a key and why deletion waits.
- [AWS: Messaging](cloud/aws/Messaging.md): What SNS, SQS and EventBridge each guarantee, how to fan out and dead letter reliably, and when a queue belongs between them.
- [AWS: VPC Networking](cloud/aws/VPC%20Networking.md): How route tables, NACLs and security groups decide what reaches a VPC resource, and how traffic to AWS services and on premises stays private.
- [Azure: Tenants, Subscriptions and RBAC](cloud/azure/Tenants%2C%20Subscriptions%20and%20RBAC.md): How an Entra ID tenant, its subscriptions and RBAC role assignments relate, what moving a subscription breaks, and how identities reach resources.

## Practice

- [Influence and Negotiation](practice/Influence%20and%20Negotiation.md) *(opinion)*: How to move people towards a goal by knowing theirs first, and the four Getting to Yes principles behind it.
- [Leadership](practice/Leadership.md) *(opinion)*: What a leader does to help others succeed: build culture and safety, delegate, communicate, motivate and handle politics.
- [Roles and Hiring](practice/Roles%20and%20Hiring.md) *(opinion)*: What engineering leaders, architects and engineers are for, which competencies to probe for in an interview, and how to sell the role.
- [Self Awareness](practice/Self%20Awareness.md) *(opinion)*: What self awareness means as an inner practice: how the mind works, how to concentrate, and how to find and share a goal.
- [Testing Strategy](practice/Testing%20Strategy.md) *(opinion)*: What a test is for, why the I/O boundary matters more than the unit or integration label, and how to test performance.

## About this repository

The September 2026 audit that produced this structure is under [audit/](audit/README.md). It is history, not reference material.
