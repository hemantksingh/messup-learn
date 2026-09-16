# File triage: what to keep, rewrite, trim, merge or drop

Audit date: 2026-09-16. Every markdown note in the repo is graded against the stated purpose of the wiki:

> A reference for foundational knowledge, written in plain language the owner can rederive concepts from. Not a copy of content that lives at its source. Irrelevant content can go.

## Verdicts

| Verdict | Meaning |
|---|---|
| **KEEP** | Explains a fundamental in the owner's own words. Fix the listed errors, add frontmatter, keep. |
| **REWRITE** | The topic is fundamental, but the current text is wrong, stale, or pasted. Rewrite from basics; reuse only what survives. |
| **TRIM** | A fundamental is buried in product catalogue, command dumps or vendor text. Keep the principle, cut the rest. |
| **SPLIT** | Two unrelated topics in one file. Separate them, then treat each as KEEP or TRIM. |
| **MERGE** | Worth keeping, but not as its own page. Fold into the named page and delete the file. |
| **DROP** | Copy of source material, product or price catalogue, project data, or dead content. Delete. |
| **YOU DECIDE** | Off-topic for an engineering wiki. Owner's call. |

"Key fixes" lists the highest-impact items only, with line numbers from the current file. The full line-by-line tables are in `details/`.

Totals: 96 notes. KEEP 32 · REWRITE 15 · TRIM 9 · SPLIT 4 · MERGE 14 · DROP 20 · YOU DECIDE 1 · README (rewrite as index) 1.

---

## Cheat sheets/ (13 files) — dissolve the folder

Command lists are available at their source and age fast. Keep only the gotchas that came from experience, as a short section on the topic page.

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Ansible.md | MERGE | Command list is docs copy. The variable-scope and inventory gotchas are worth a "Gotchas" section. | Platform / Configuration Management | `ansible all` without `-m ping` fails (L70); non-standard variable taxonomy (L16-22); real public IP in example (L95) |
| Dotnet.md | TRIM | OWIN/middleware-pipeline idea is a fundamental; `dotnet` CLI commands are not. ASP.NET list duplicates Web Frameworks. | Web and APIs / Rendering Patterns (one paragraph) | Delete L11-31 duplicate; TFMs net6/net7 are out of support (L51) |
| IIS.md | DROP | ASP.NET Core 2.1 troubleshooting recipes. | — | — |
| Kubernetes.md | MERGE | The `ip addr` / `route` walk-through of pod networking is a genuine derivation. The kubectl list is not. | Platform / Kubernetes ("Seeing pod networking from inside a pod") | `kubectl exec` needs `--` (L61, L74); bridge is `cbr0` not `crbr0` (L75); context = cluster + user + namespace (L9) |
| Mac.md | DROP | Personal shortcuts and setup. Shell start-up file concept moves to The Unix Model. | — | (if kept) `.bash_profile` vs default zsh contradiction (L16-29) |
| Nginx.md | MERGE | Only the master/worker process model paragraph is a fundamental. | Platform / Load Balancing and Proxies | reload does not load a new binary (L18); `default_server` is a `listen` parameter, `server_name` does host routing (L29-31) |
| Nuget.md | DROP | nuget.exe commands, several wrong (`nuget source` should be `sources`). | — | — |
| SqlServer.md | DROP | Five sqlcmd commands. | — | — |
| Typescript.md | DROP | 2015-era: `tsd`, namespaces-as-modules, `outFile` without `module`. | — | — |
| Ubuntu.md | DROP | Personal dev-setup runbook; installs Compose v1. | — | — |
| Unix Basics.md | REWRITE | "Everything is a file", processes, permissions, pipes and redirection are exactly the fundamentals wanted. The command list is not. | Computing / The Unix Model | `tail` default is 10 not 20 (L165); `rm -r *.*` does not delete all files (L80); `chmod 777` as "make writable" (L86); merged lines (L164, L167) |
| VS.md | DROP | One shortcut. | — | — |
| VSC.md | DROP | Four shortcuts. | — | — |

## Cloud and Infrastructure/AWS/ (9 files + drawio)

Keep the mental models (how IAM evaluates, why security groups are stateful, queue vs topic vs bus). Drop console walkthroughs and service catalogues.

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| AWS Cli.md | DROP | Four CLI snippets. | — | — |
| DR and Business Continuity.md | KEEP | RTO/RPO, HA vs DR and the DR-test discipline are fundamentals. Trim DynamoDB pricing detail. | Cloud / AWS / Disaster Recovery (generic RTO/RPO part to Platform / Resilience Patterns) | RPO is a data-loss window, not PITR (L11); "PTO" should be RPO (L57); PRD/STG ratio is inverted relative to its own goal (L29); "costs no money" oversimplified (L61) |
| EKS.md | REWRITE or DROP | The central claim (a VPC is capped at /16 and cannot grow) is false. If kept: one page on what a managed control plane manages and how pod IPs are allocated. | Cloud / AWS / EKS | L26-28 secondary CIDRs and prefix delegation exist; "100 node max" is not a limit (L28) |
| EventBridge_SQS_SNS.md | KEEP | Queue vs topic vs event bus semantics is a fundamental. Rename to match siblings. | Cloud / AWS / Messaging | SNS has retry policies and DLQs (L20, L27); Pipes described as partner sources (L37); truncated sentence (L9); H1 collides with Distributed Systems note |
| Overview.md | DROP | EC2 console walkthrough copied from a tutorial; IMDSv1, Amazon Linux 2, `public-ip4` typo. | — | — |
| Security - IAM.md | KEEP | Identity vs resource policies, evaluation order and roles are a real mental model. | Cloud / AWS / Identity | ARN format missing resource segment (L47-51); JSON with `//` comments and missing comma will not paste (L53-83); DynamoDB "no resource policies" was false at commit (L17) |
| Security - KMS.md | KEEP | Key material sources, envelope encryption and rotation are fundamentals. | Cloud / AWS / Key Management | deletion is never instantaneous, 7-30 day window (L33); key categories are customer managed / AWS managed / AWS owned (L29-31); "CMK" retired term (L33); rotation period now configurable (L18) |
| Security - Networking.md | KEEP | Routing, subnets, SG vs NACL statefulness, endpoints. Most current file in the folder. | Cloud / AWS / VPC Networking | stateful does not mean rules are mirrored (L39); default SG allows all outbound (L37); "1 GB / 10 GB" should be Gbps and speeds go to 400 (L86); VPC has an implicit router (L5) |
| Security.md | TRIM | Service catalogue is AWS marketing copy. Keep as the folder index plus the shared-responsibility idea. | Cloud / AWS / README | S3 quota (L25); Security Hub renamed (L29); Inspector Classic EOL (L73-78); "HIPPA and GDPA" (L84) |
| AWS.drawio | CONVERT | Source of two PNGs; the "Serverless DR" page was never exported. Becomes two `.drawio.svg` files embedded in the Identity and Disaster Recovery pages, then deleted. | images/aws-federated-access.drawio.svg, images/aws-serverless-dr.drawio.svg | relabel "multi-master" to "multi-active"; see wiki-plan "Diagrams" |

## Cloud and Infrastructure/Azure/ (4 files + drawio)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Azure Cli.md | DROP | Most `az ad` snippets broke in CLI 2.37 (May 2022); contains former-employer tenant names. | — | — |
| Azure Functions.md | DROP | 2019 quickstart on the in-process model, which loses support 10 Nov 2026. Hosting-plan concept can be one paragraph in the Azure page. | — | — |
| Overview.md | KEEP | Tenant vs subscription vs RBAC scope is a genuine mental model that is hard to find stated plainly elsewhere. | Cloud / Azure / Tenants, Subscriptions and RBAC | Azure AD is Microsoft Entra ID (throughout); classic Service Admin role retired Aug 2024 (L22-27); Entra ID is not "scoped to a resource group", RBAC is (L37); add user-assigned identities (L52) |
| Security.md | MERGE | Service endpoints vs private endpoints is one principle, one paragraph. | Cloud / Azure / Network Access Control (section of the page above) | drop the "allow any IP" example (L22-31); add Private Endpoints |
| AzureAd.drawio | CONVERT | Source of three PNGs. Becomes two `.drawio.svg` files embedded in the Azure page, then deleted. | images/azure-tenant-subscription.drawio.svg, images/azure-access-patterns.drawio.svg | Relabel "AzureAD", "Service Admin", "Managed Identites" before converting |

## Cloud and Infrastructure/DevOps/ (6 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Ansible.md | KEEP | Push-over-SSH vs pull-agent model, in own words. Becomes the canonical Ansible page and absorbs the cheat sheet gotchas. | Platform / Configuration Management | mention `ansible-pull` and WinRM (L3) |
| Azure DevOps.md | DROP | Product vocabulary (stage/job/step, gates) from the docs, plus a personal org URL. | — | — |
| Chef.md | DROP | 2010-era glossary of a tool in decline. | — | — |
| Overview.md | KEEP | DevOps definition, DORA metrics, CI/CD principles, provisioning vs configuration management. Absorbs Continuous Deployment. | Platform / DevOps and Delivery | RTO is an objective, not a measured time (L28, same error in AWS DR L10); "Graphana" (L39); the "blue/green" steps describe an in-place deploy with downtime (L100-107); remove pasted Octopus text (L94-109) and duplicated People paragraph (L9-15) |
| SRE.md | MERGE | Fragmentary course notes; SLO/error-budget content is duplicated three times in the repo. | Platform / Observability (SLO section) | GCLB uses anycast, not geolocation (L9); empty bullet (L16) |
| Terraform.md | TRIM | State, providers, modules, workspaces and why remote state matters are fundamentals. Version-pinned snippets are not. | Platform / Infrastructure as Code | provider block fails on any current version, `cliend_id` typo (L40-48); "open source" — BSL since Aug 2023, OpenTofu fork (L9); `my.tfpan` (L150); copy-paste "this article" (L3-10) |

## Cloud and Infrastructure/ root and Kubernetes/ (7 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Docker.md | REWRITE | Namespaces, cgroups, layers, image vs container: fundamentals. Commands section has several wrong flags. | Platform / Containers | `-p host:container` direction reversed (L36); `:latest` is a tag, `docker run` does not re-pull (L28); `rmi dangling` is not "all unused" (L56); `docker save` missing image arg (L102); no `-d` for "detached" (L92); H1 "Virtualization" |
| Haproxy.md | TRIM | L4 vs L7, active vs passive health checks, retries. The rate-limiter vs circuit-breaker essay is generic and moves. | Platform / Load Balancing and Proxies; L79-87 to Resilience Patterns | nginx OSS has had TCP load balancing since 2015 (L9); HAProxy is a proxy, it does not forward raw packets (L8); circuit breaker described as a timeout (L85); CentOS 7 EOL (L12) |
| Nginx.md | TRIM | Event-driven vs process-per-connection and the reverse-proxy roles are fundamentals. Plus-only features, Amplify and ModSecurity are product content. | Platform / Load Balancing and Proxies | Amplify shut down Jan 2026 (L52); NGINX ModSecurity WAF EOL Mar 2024 (L30); nginx does not "jail" code, AppArmor is not an Apache mechanism (L20); `Allow`/`Deny` are lowercase (L38) |
| Scalability.md | MERGE | 13 lines of AWS whitepaper text plus links. | Platform / Load Balancing and Proxies (intro) | "NetScalar" (L12); "NewOps" should be NetOps (L14) |
| Kubernetes/Overview.md | REWRITE (keep the core) | Architecture and the three pod-networking rules are fundamentals worth keeping. Ecosystem catalogue, Helm commands, AKS section and vendor lists are not. | Platform / Kubernetes | "Docker or rkt" (L5, L63); "Google declined to donate Knative and Istio" — both in CNCF since 2022 (L235); ingress-nginx retired Mar 2026, Gateway API is the successor (L135-151); Helm 2 syntax (L196-200); kubelet 10255 disabled by default (L61); `kubeadm join` incomplete (L26) |
| Kubernetes/Kubernetes Security.md | KEEP | Authentication plugins, RBAC model, Role vs ClusterRole decision guide. | Platform / Kubernetes Security | basic-auth file removed in 1.19 (L8); client certs are not the common human path on managed clusters (L6); add Pod Security Admission, NetworkPolicy; H1 mismatch |
| Kubernetes/Production Readyness.md | MERGE | Eight unanswered questions. | Platform / Kubernetes (checklist section) | filename typo |

## Computer Theory/ (2 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| NP Complete.md | REWRITE | Exactly the kind of fundamental wanted, but the core definitions are wrong. | Computing / Algorithms and Complexity | NP is verifiable-in-polynomial-time, not "exponential time" (L9); NP-complete definition garbled, NP-hard and reductions absent (L18); H1 states P = NP |
| Software Complexity.md | SPLIT | Code-quality metrics and FP/reactive primer are two topics; Atlantic quotes are pasted opinion. | Computing / Code Quality + Computing / Functional and Reactive Programming | currying ≠ partial application (L24); cyclomatic = independent paths, not all paths (L72); pure ≠ higher-order (L18); `.filter().map()` on an array is not reactive (L50-56) |

## Data and AI/ (6 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Algorithm Design.md | REWRITE | Big-O fundamentals; no data or AI content. Move to Computing. | Computing / Algorithms and Complexity | best/worst case ≠ lower/upper bound (L5, L20); O(2n) is linear (L10); probing and chaining are both O(1) expected (L60-61); `0(n!)` (L12); no H1 |
| Big Data.md | TRIM | Data-mesh principles and lake vs warehouse vs lakehouse are worth keeping in own words. | Data / Data Platforms | Kreps' "The Log" pasted with his first person (L13-19); "data lakes are completely unstructured" (L78); Spark on Mesos removed (L99-103); map does not split data (L88) |
| Data in the Cloud.md | DROP | Cloud service catalogue. Several services renamed or discontinued (Glue Elastic Views, Kinesis Data Analytics, Cloud ML Engine). The digital-analytics detour is a different topic. | — | — |
| Data Processing Pipeline.md | REWRITE | Batch vs stream is the fundamental. 70% of the file is a log-shipper comparison that belongs in Observability. | Data / Data Pipelines | contradicts itself on Logstash persistent queues (L28 vs L53); batch DAGs "difficult to scale" (L11); media streaming is not stream processing (L20) |
| Machine Learning.md | KEEP | Supervised / unsupervised / reinforcement, in plain words. | Data / Machine Learning | house price is regression, not classification (L27); sentiment scoring is classification, not clustering (L53); deep learning is not a fourth type (L19/L65); add transformers, RNN is historical (L69) |
| Regression Analysis.md | MERGE | 19-line stub with an empty section. | Data / Machine Learning | least squares minimises over all points, not "outliers" (L7) |

## Distributed Systems/ (16 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| AMQP.md | MERGE | Presents the RabbitMQ 0-9-1 model as "the AMQP standard"; AMQP 1.0 has no exchanges. | Messaging / Message Brokers | binding key vs routing key (L9) |
| Asynchronous Messaging.md | KEEP (split in 3) | Coupling, delivery guarantees, idempotency, sagas, broker models: core content. | Messaging / Fundamentals · Sagas and Process Managers · Message Brokers | Kafka orders per partition only (L97); STOMP link goes to NATS (L79); RabbitMQ Streams exist since 3.9 (L93); name the Outbox pattern (L13); MSMQ is legacy (L115); U+2011 hyphen in H1 |
| Concurrency Models.md | KEEP | Shared memory vs CSP vs actors, in own words. | Computing / Concurrency Models | "Communicating Sequential Processing" (L5); concurrency/parallelism definitions inverted (L47); Go marketing copy (L13-16); Akka 2.0.1 links, Pekko fork (L77) |
| Consistency Models.md | REWRITE (keep the core) | This is the flagship fundamental. Several definitions are wrong. | Data / Consistency Models | strict consistency ≠ linearizability (L38); "partition tolerance is rarely achievable" inverts CAP (L65 vs L62); read-your-writes stated backwards (L69); external consistency = strict serializability (L84); H1 "Distributed Databases" |
| Continuous Deployment.md | MERGE | Deploy vs release; belongs with DevOps. Name feature flags and canary. | Platform / DevOps and Delivery | — |
| Event Sourcing.md | KEEP | Append-only log, projections, left fold: fundamentals. | Messaging / Event Sourcing and CQRS | attribute Fowler (L6-15); "memorisation" → memoization (L25); event store keys on (stream, version) (L29); CQRS never named |
| HTTP Caching.md | KEEP | Cache-Control semantics. | Web and APIs / HTTP Caching | `public` does not mean "cached at the server" (L6); `must-revalidate` definition garbled (L9); `sdch` dead (L14); cite RFC 9111 (L29) |
| HTTP.md | KEEP (split in 2) | HTTP/1 → 2 → 3 and realtime transports are fundamentals. | Web and APIs / HTTP + Realtime Web | "65,536 sockets per IP" misconception (L108); WebSockets do not require TCP-mode LB (L114); SignalR "Windows only" false since 2018 (L131); Server Push removed from browsers (L104); pipelining is dead (L47); drop Streamdata.io (L133-139) |
| Interprocess Communication.md | KEEP | Pipes, sockets, shared memory. | Networking / Local IPC | L42 and L44 contradict on default pipe ACL; impersonation direction reversed (L40) |
| IOT Device Landscape.md | DROP | List of boards discontinued by 2017. | — | — |
| Monitoring and Observability.md | TRIM | Logs/metrics/traces, SLOs and error budgets: fundamentals. The pasted first-person Datadog team guideline and vendor list are not. | Platform / Observability | L148-276 is an internal team doc with Datadog retention limits; OpenTelemetry explained three times, still recommends archived OpenTracing (L104); RUM ≠ white-box (L207); "Pomcat" (L127) |
| NoSql.md | REWRITE | "How to choose a database" is a good fundamental; product claims are 2012-era. | Data / Choosing a Database | MongoDB global lock (L3) and "no durable writes" (L14) false for a decade; Spanner is not NoSQL, duplicates Consistency Models (L69-78); "relational DBs lack relationships" (L52) |
| REST.md | KEEP | Verbs, idempotency, status codes, hypermedia. | Web and APIs / REST | URI is Uniform (L5); 201 puts URI in `Location` (L23); 405 vs 409 inconsistent (L29/L35); "available" → "unavailable" (L130); Atom section moves to Messaging; absorb Richardson Maturity Model from Synchronous Messaging |
| Service Orientation.md | KEEP (opinion) | Why and when to distribute, in own words. | Messaging / Service Orientation | attribute Fowler's First Law (L33); capability ≠ bounded context (L23) |
| Servicebus Frameworks.md | MERGE | What a bus library adds (routing, retry, DLQ, outbox) is one section; product links are stale (MassTransit v9 commercial, MSMQ legacy). | Messaging / Message Brokers | — |
| Synchronous Messaging.md | KEEP | REST vs RPC vs gRPC vs GraphQL trade-offs. | Web and APIs / API Styles | "browsers don't support HTTP/2" is not why gRPC needs gRPC-Web (L87); sentence ends mid-thought (L62); GET with body example (L15-25); UDDI (L68); U+2011 hyphen in H1 |

## Mobile/, Networking/, Photography/, SEO/ (6 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Mobile/Android.md | DROP (YOU DECIDE if Android stays in scope) | 2014-era, deprecated APIs, sample code does not compile. | — | (if kept) L121 two-arg inflate; L123-124 variable mismatch; L170 wrong constructor |
| Networking/DNS.md | KEEP | Resolution, caching, record types. | Networking / DNS | TTL is per record for every resolver, not an ISP setting (L17); NS delegates, it does not "determine the server used" (L37); add TXT/SOA/PTR/SRV/CAA |
| Networking/IPRouting.md | REWRITE | CIDR, subnets, NAT, DMZ are fundamentals; classful framing is 1993-stale and two images are dead. | Networking / IP Addressing | VLAN "resolves MAC to IP" (L30); on-link rule wrong and `10.10.20.0` is a network address (L32); no H1; no routing content despite the name |
| Networking/Network Layers.md | KEEP | OSI and TCP/IP layering. Command how-tos move out. | Networking / Network Layers | ephemeral ports are 49152-65535 or 32768-60999, not "8000+" (L19); "Median Access Control" (L23); transport "guarantees delivery" contradicts UDP (L6); `telnet telnet` (L45) |
| Photography/Photography Basics.md | YOU DECIDE | Off-topic. | — | (if kept) higher f-number = smaller aperture, less light (L2-4); ISO is not an acronym (L10) |
| SEO/Web Performance.md | REWRITE | What LCP, INP, CLS and TBT actually measure is a fundamental; 2010 statistics and SEO URL tips are not. | Web and APIs / Web Performance | TBT definition (L22) and TTI definition (L43) wrong; FID replaced by INP Mar 2024 (absent); H1 "Search Engine Optimization" |

## Tools/ (6 files) — dissolve the folder

None of these is a tool reference. Two are the best own-words essays in the repo; the rest is vendor or project material.

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| CICD.md | DROP | 2017 vendor price comparison; several cells were never true (Bitbucket "only .NET Core", VSTS "no Selenium", Bamboo "no pipeline-as-code"). | — | — |
| Okta.md | DROP | Employer client names, user counts, a 2020 price quote and screenshot. Generic SSO ideas are covered better elsewhere. | — | — |
| Tesseract.md | DROP | Three links. | — | — |
| Testing.md | KEEP | The closest existing page to the target style: a testing philosophy in the owner's voice. Label the first-person passages as own view. | Practice / Testing Strategy | BDD "isn't about collaboration" contradicts North's own definition (L30); JMeter runs headless in CI (L112); `npm benchmark` is not a command (L113); PhantomJS, Karma, IE are dead (L67); Lambda-specific performance section to AWS |
| Web Frameworks.md | KEEP | Rendering patterns (SSR, CSR, SSG), micro-frontends and PWA trade-offs are fundamentals. Link fixed in this audit. | Web and APIs / Rendering Patterns | Angular described as AngularJS MVC (L101); JSX direction reversed (L109); Next.js has no native PWA support (L141); Blazor hosting models nested under Razor Pages (L158-160) |
| Windows Background Tasks.md | MERGE | One idea worth keeping: a background job is reliable because the call is persisted, not because it runs on a thread. Topshelf is dormant; Hangfire ".NET Framework 4.5 only" was false at commit. | Messaging / Messaging Fundamentals (one paragraph) | L9 misses the persistence point; L19 stale; no H1 |

## People/ (5 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Capabilites.md | SPLIT | Role profiles (own words) and interviewing technique are two topics. | Practice / Roles and Hiring | filename typo; L45-51 is verbatim DevOps/Overview L9-15; "SIB" elsewhere; unclosed parenthesis (L47) |
| Influence.md | KEEP | Owner's influencing approach. Absorbs Negotiation. | Practice / Influence and Negotiation | add a Sources block (Carnegie, Fisher & Ury, Voss); "get a yes" conflicts with Voss's "that's right" (L20) |
| Leadership.md | KEEP | Owner's synthesis; needs sources named. | Practice / Leadership | "Schien, The Corporate Culture" → Schein, The Corporate Culture Survival Guide (L7); DLOQ has seven dimensions, not five (L17-22); SBI not SIB (L81); "deepest principle" is William James (L79); truncated sentence (L7) |
| Negotiation.md | MERGE | Uncited Getting to Yes summary; three sections already in Influence. | Practice / Influence and Negotiation | misplaced "separate inventing from deciding" (L9) |
| Self Awareness.md | KEEP (label as personal philosophy) | Owner's reflections. An agent must not read law-of-attraction passages as leadership doctrine. | Practice / Self Awareness | goldfish attention-span statistic is debunked (L5); Vedanta has six pramanas, list has five (L45-51); paragraph duplicated (L64/L80); orphan list (L53-56) |

## Security/ (15 files)

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| Certification.md | MERGE | Four links and a paragraph. | Security / Standards and Compliance | CREST is a body, not a cert (L7); no H1 |
| Cloud Security.md | TRIM | Framework landscape (NIST, CSA, CIS) in own words is useful; tool tables and Azure product notes are not. | Security / Standards and Compliance | NIST CSF conflated with SP 800-53 controls (L7); CSF 2.0 has six functions (L7); Prowler and Scout each "superior" to the other (L65/L69); Security Center / Sentinel renamed 2021 (L82-91) |
| Compliance.md | KEEP | Standards overview. FIPS algorithm list needs a hard refresh. | Security / Standards and Compliance | SOC 1 is financial controls (L28); PCI SSL deadline was 2018 (L32); EES withdrawn, DSA and 3DES no longer approved (L43-49); TLS 1.0 "acceptable" (L68); Schannel/PKCS moves to TLS |
| Container Security.md | REWRITE | TUF, signing, least privilege are fundamentals; Swarm/UCP/DTR fragments are dead. | Security / Supply Chain and Container Security | Docker Content Trust legacy, cosign/Notation (L5-13); "merkel" (L19) |
| Data Security.md | SPLIT | Cryptography basics and data privacy are two topics; the crypto half has the worst errors in the repo. | Security / Cryptography Basics + Security / Data Privacy | MAC and signatures do not provide confidentiality (L88); collisions always exist, preimage vs collision resistance swapped (L126); hash "provides confidentiality via encryption" (L132); fast hashes are correct, slowness is for passwords (L128); no GDPR staff-email exemption (L9); fine is EUR 20m or 4% whichever higher (L51); PCI DSS is a standard by the card brands, not "regulation by Stripe" (L74) |
| Endpoint Security.md | TRIM | EPP vs EDR vs XDR concept. Vendor copy (Tenable, BeyondTrust) goes. | Security / Endpoint Security | "EDP" → EPP (L11); YARA is not "VT's" (L65); two heading typos |
| Storing secrets.md | REWRITE | Title promises secret storage; content is a GPG + Blackbox recipe. Rewrite as the principle: encrypted-in-repo vs external store, and when each fits. | Security / Secrets Management | SSH signing exists since Git 2.34 (L5); personal email in examples; conflicts with DevOps "no secrets in source" without stating the trade-off |
| Threat Modelling.md | KEEP | Purpose, steps, attack surface, design principles. | Security / Security Principles and Threat Modelling | Four-Question Frame has four questions (L4-8); Open Design ≠ "many eyeballs" (L54); complete mediation misdefined (L53); add STRIDE |
| Web Security/Cross Site Request Forgery.md | KEEP | Clear own-words explanation. Fence fixed in this audit. | Security / Cross Site Request Forgery | add SameSite and `Sec-Fetch-Site` as defence in depth (absent); token "cryptographic pair" is ASP.NET-specific (L24) |
| Web Security/Cross Site Scripting.md | KEEP | Three XSS types. | Security / Cross Site Scripting | output encoding is the primary defence, not input validation (L13); `javascript.alert` payload never worked and `<img src=javascript:>` is dead (L21-25); "DNS records infected" (L29); add CSP |
| Web Security/Security Cookies.md | REWRITE | Cookie mechanics are a fundamental, but this 2025 commit carries 2009 facts. | Security / Browser Security Model (cookies section) | 4 KB is per cookie and browsers reject, not truncate (L21); SameSite is site-scoped, not origin (L53); IE8/Opera limits (L20); `<em>` tags in code (L14); H1 "HTTP Cookies" |
| Web Security/Security Headers.md | KEEP | CSP, HSTS, frame options, referrer policy. SOP/CORS section moves to Browser Security Model. | Security / Security Headers | "Cross-Origin-Resource-Policy" section is actually SOP/CORS and says CORP grants reads (L68-82); `ALLOW-FROM` unsupported (L45); `Blocked` is not a value (L6); "inline-eval" (L19); add strict CSP with nonces |
| Web Security/TLS Certificates.md | KEEP | Certificates, CSRs, formats, trust. | Networking / TLS Certificates | OpenSSL recipe has no SAN so browsers reject the result (L30-40); thumbprint is a hash of the whole cert (L81); `-CertLocation` and plain-string password (L71); `-days 356` (L26); add ACME, lifetime limits (200 days from Mar 2026, 47 by 2029), OCSP/CRLite |
| Web Security/Transport Layer Security.md | REWRITE | The handshake explanation is the fundamental, and it describes RSA key transport, removed in TLS 1.3. | Networking / TLS | L35 rewrite around ECDHE + signature; EV indicator removed from browsers 2019 (L65); no TLS version named anywhere; client cert is per connection, not per request (L92); DV/OV/EV moves to Certificates |
| Web Security/Web Application Security.md | SPLIT | OWASP risks explained with examples: keep. SAST/DAST/vendor catalogue: drop. | Security / Web Application Risks | Python snippet is a SyntaxError (L111); Log4Shell payload missing `{` (L138, L141); OWASP Top 10 version never named (L88); ModSecurity/Trustwave EOL (L155-158); Chrome padlock gone (L178) |

## Root and assets

| File | Verdict | Why | Proposed home | Key fixes |
|---|---|---|---|---|
| README.md | REWRITE | Three lines. Becomes the wiki index with one line per page. | / | — |
| 14 raster diagrams: consistency-models, http-stacks, http-v-http2, business-layer, osi, password-hashing, message-signing, testing-behaviour, ansible-components, elastic-log-shippers, elastic-stack, hangfire-singleprocess, hangfire-winservice, aws-vpc, azure-role-assignment | REDRAW | Slides, vendor diagrams or lost-source draw.io exports that illustrate a fundamental the page keeps. Redraw as 12 own `.drawio.svg` files against the corrected text. | images/*.drawio.svg (names in wiki-plan "Diagrams and images") | consistency ladder must not equate strict with linearizable; VPC diagram labels SG stateful, NACL stateless |
| 4 screenshotted tables: cacheable-content, default-cluster-roles, arm-terraform, network-admin-tools | TABLE | Pictures of tables. Become markdown tables in their pages. | HTTP Caching · Kubernetes Security · Infrastructure as Code · Network Layers | network-admin-tools is copyrighted third-party art; rewrite as tool → question |
| 12 screenshots and vendor graphics: windows-schannel, asc_as, data-analysis-experimentation, logstash-fluentd-comparison, nginx-dos-protection, hadoop-stack, patterns-effective-teams, mac, okta-pricing, android-project-build, android-tools-architecture | DROP | Each goes with content that is being dropped or trimmed, or is third-party artwork. | — | — |
| Networking/IPRouting.md bitbucket images (2) | REPLACE | 404. Draw classful-vs-CIDR and VLAN diagrams as `.drawio.svg` or describe in text. | images/ | — |
| images/aws-federated-identity.png, aws-security-patterns.png, azuread-subscription.png, tenant-transfer.png, access-patterns.png | REPLACE | Exported from the two draw.io files and already drifted from them. Superseded by the `.drawio.svg` files above. | — | delete once the SVGs are embedded |

End state for `images/`: 16 `.drawio.svg` files (4 converted, 12 redrawn), zero rasters.
