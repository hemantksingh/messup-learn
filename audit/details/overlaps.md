# Cross-folder overlap and contradiction audit — messup-learn

Scope: 43 files across 12 groups (the 41 assigned plus the two AWS `Security - IAM.md` / `Security - Networking.md` children). Every file was read in full. Repo root: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn`. Line numbers are 1-based as printed by `cat -n`.

Method notes:
- **Overlap %** = rough share of a file's lines/sections that address the same topic as the other file(s) in the group (not verbatim match unless stated). Stated relative to the *smaller* file unless noted.
- **Currency** judged against the file's last-commit date (in brackets) and today (2026-09-16). Two claims I rated High were verified by web search (Knative/Istio CNCF status; SNS retries/DLQ). Everything else is marked Medium/Unverified where it depends on external facts.
- Per-file issue tables and the file-classification table are deliberately omitted (per-folder auditors cover those); only cross-file findings and the items needed to justify merge decisions are listed.

Dates (last commit): Cheat/Ansible 2020-06 · DevOps/Ansible 2021-10 · Cheat/Nginx 2021-06 · Cloud/Nginx 2023-04 · Haproxy 2021-10 · Scalability 2021-10 · Cheat/Kubernetes 2021-11 · K8s/Overview 2021-11 · AWS/EKS 2021-11 · Container Security 2020-06 · K8s Security 2021-10 · Docker 2021-10 · Cloud Security 2023-07 · AWS/Security 2024-03 · AWS/IAM 2024-06 · AWS/Networking 2025-08 · AWS/KMS 2024-03 · Azure/Security 2022-03 · Storing secrets 2022-03 · Tools/CICD 2020-06 · Continuous Deployment 2020-06 · DevOps/Overview 2023-02 · Azure DevOps 2024-01 · HTTP 2021-08 · HTTP Caching 2021-09 · REST 2021-09 · Synchronous Messaging 2023-07 · Web Performance 2023-05 · Asynchronous Messaging 2021-04 · AMQP 2020-06 · Servicebus Frameworks 2020-08 · EventBridge_SQS_SNS 2024-01 · Event Sourcing 2022-06 · TLS 2022-06 · TLS Certificates 2022-06 · Certification 2020-10 · Network Layers 2021-08 · IPC 2021-08 · Capabilites 2025-08 · Leadership 2025-11 · Dotnet 2024-05 · Web Frameworks 2024-12 · Windows Background Tasks 2020-06.

---

## Group 1 — Ansible: `Cheat sheets/Ansible.md` vs `Cloud and Infrastructure/DevOps/Ansible.md`

**(a) Overlap ~5%.** No section duplicates another. `Cheat sheets/Ansible.md` (100 lines) is a how-to: install, variables, roles/handlers, inventory, ad-hoc commands, Windows hosts. `DevOps/Ansible.md` (7 lines) is a conceptual preface only: push-over-SSH vs Puppet/Chef pull model, agentless, plus an image. They are two halves of one document.

**(b) Contradictions.** None head-on; one tension with a third file:
- `DevOps/Ansible.md:3` "Ansible can be used for provisioning infrastructure, orchestrating and automating deployements" vs `DevOps/Overview.md:86` "OS installation ... are infrastructure provisioning tasks that tools like *Terraform and Cloudformation* can provide" and `:90` "*Chef, Ansible, Puppet and SaltStack*" listed as configuration-management tools, with `:92` recommending "keeping configuration management separate from provisioning". Not an error (Ansible *can* provision) but the two files give the reader different mental models without cross-reference.
- Structural: `Cheat sheets/Ansible.md:1` H1 is "Installation", not "Ansible".

**(c) Recommendation.** Canonical = one `Ansible.md` in the DevOps/configuration-management area. Body of `DevOps/Ansible.md` becomes the "## How it works" intro; the cheat sheet's sections follow as "## Variables / ## Roles / ## Inventory / ## Commands". Delete `Cheat sheets/Ansible.md`. Add a one-line link from `DevOps/Overview.md:90` and a sentence in the merged file stating the provisioning-vs-CM position from `Overview.md:92`.

**(d) Currency.** `DevOps/Ansible.md` is newer but has no operational content; the cheat-sheet commands are still valid (`-i/-m/-k/-vvv`, `win_ping`, `setup`). Cheat-sheet doc links point at the pre-2022 docs tree (`user_guide/...`) — leave to the link checker.

---

## Group 2 — Load balancing / reverse proxy cluster: `Cheat sheets/Nginx.md` vs `Cloud and Infrastructure/Nginx.md` vs `Haproxy.md` vs `Scalability.md`

**(a) Overlap.**
- Cheat/Nginx vs Cloud/Nginx: ~10% — only the architecture/Apache comparison (`Cheat:3-6` vs `Cloud:14-22`). Cheat sheet = process model, config paths, `nginx -s reload`, log paths; Cloud = history, use cases, Nginx vs Apache, API gateway/WAF/IPS, auth features, monitoring.
- Cloud/Nginx vs Haproxy: ~20% — feature lists (LB/reverse proxy `Nginx:7-8` vs `Haproxy:3-5`), rate limiting (`Nginx:10,42` vs `Haproxy:77-87`), WAF/ModSecurity (`Nginx:30` vs `Kubernetes/Overview.md:163`), Datadog monitoring (`Nginx:53` vs `Haproxy:107`).
- Scalability.md (13 lines) is ~60% about hardware vs software load balancers and exists mainly to link to the other two (`:14`). It is a load-balancing intro, not a scalability document.
- `Haproxy.md:77-87` (rate limiter vs circuit breaker) is generic resilience-pattern prose with no HAProxy-specific content.

**(b) Contradictions.**
- **WRONG (High):** `Haproxy.md:9` "Nginx only supports layer 7 HTTP mode. For load balancing services like LDAP, MYSQL if you want to use TCP mode, then you can use Nginx Plus or other web servers like Apache." Open-source nginx has had the `stream` module (TCP/UDP load balancing, `stream {}` block) since 1.9.0 (2015); it is not a Plus-only feature. `Cloud/Nginx.md:3` "provides layer 7 load balancing capabilities" echoes the same under-statement, while `Cloud/Nginx.md:5` describes it "accepting TCP connections and making new TCP connections to upstream servers".
- **INCONSISTENT (Low):** `Cheat sheets/Nginx.md:3` "Apache that spawns a process per connection" vs `Cloud/Nginx.md:16` "It spins new threads as the server get busy". Both are MPM-dependent (prefork = processes, worker/event = threads). Pick one framing.
- `Cloud/Nginx.md:20` "Apache runs PHP or Python in process and utilises *AppArmour* to elevate & downgrade privileges" — unsupported claim (mod_php is in-process; AppArmor is a Linux MAC system, not an Apache privilege mechanism). Low/unverified.

**(c) Recommendation.**
- Canonical `Nginx.md` = `Cloud and Infrastructure/Nginx.md`; append the cheat sheet as "## Operations (process model, config locations, reload, logs)". Delete `Cheat sheets/Nginx.md`.
- Rename `Scalability.md` → `Load Balancing.md`: keep vertical/horizontal + hardware vs software, add an L4-vs-L7 section built from the (corrected) `Haproxy.md:7-10` bullets, and a short Nginx/HAProxy comparison table. `Haproxy.md` then drops its Nginx comparison.
- Move `Haproxy.md:77-87` (rate limiting vs circuit breaker) to a resilience-patterns page in the architecture area (alongside retries, back-pressure, connection queueing already described at `:57-75`); leave HAProxy config snippets in `Haproxy.md` with a link.
- Move `Cloud/Nginx.md:24-34` (API gateway vs WAF vs IPS — concept, not nginx) to an "API Gateway" concept page or `Security/Web Security/Web Application Security.md` (WAF), leaving nginx-specific ACL/JWT/NTLM items (`:36-48`).

**(d) Currency.** `Cloud/Nginx.md` (2023) is the most recent but: `:30` NGINX ModSecurity WAF was end-of-sale/EOL'd by F5 (Medium, unverified date); `:52` NGINX Amplify free tier/EOL status should be re-checked (Medium). `Haproxy.md` (2021) is accurate about HAProxy (Runtime API, Data Plane API, `retry-on`, Prometheus endpoint in 2.0) but wrong about nginx. Cheat sheet content is timeless.

---

## Group 3 — Kubernetes: `Cheat sheets/Kubernetes.md` vs `Kubernetes/Overview.md` vs `AWS/EKS.md`

**(a) Overlap.**
- Cheat vs Overview: ~10% — pod networking (`Cheat:56-85` worked example with `ip addr`/`route` vs `Overview:66-104` concepts) and CoreDNS/service discovery (`Cheat:41` vs `Overview:10,94`). Otherwise complementary (commands vs concepts).
- EKS vs Overview: ~15% — managed vs self-hosted (`EKS:3-7` vs `Overview:29`), pod-IP allocation/CNI (`EKS:24-28` vs `Overview:86-104`, esp. the AKS subsection `:102-104`).
- Cheat vs EKS: 0%.
- Asymmetry: AKS networking lives inside `Kubernetes/Overview.md:102-104` while EKS networking lives in `AWS/EKS.md:24-28`; there is no `Azure/AKS.md`.

**(b) Contradictions / cross-file currency.**
- **INCONSISTENT (Medium):** `Overview.md:90` "All pods can communicate with all other pods without Network Address Translation (NAT)" and `:96` "all pods in a cluster can reach each other using the pods IP without NAT" vs `Overview.md:104` "With *kubenet* ... Pods can't communicate directly with each other. Instead, User Defined Routing (UDR) and IP forwarding is used". Kubenet pods *do* talk pod-IP-to-pod-IP; UDR is how node routing is implemented, so the CNI rule still holds. Reword.
- **STALE → now WRONG (High, verified):** `Overview.md:235` "Google have however declined to donate KNative and Istio to CNCF". Knative was accepted as a CNCF incubating project on 2 March 2022 and has since graduated; Istio joined CNCF in 2022 and graduated 12 July 2023. Sources: [CNCF: Knative accepted](https://www.cncf.io/blog/2022/03/02/knative-accepted-as-a-cncf-incubating-project/), [CNCF: Knative graduation](https://www.cncf.io/announcements/2025/10/08/cloud-native-computing-foundation-announces-knatives-graduation/), [CNCF: Istio graduation](https://www.cncf.io/announcements/2023/07/12/cloud-native-computing-foundation-reaffirms-istio-maturity-with-project-graduation/).
- **STALE (Medium):** `Overview.md:5,63` "Docker or Rkt-based" / "docker or rkt" — rkt is archived; dockershim was removed in Kubernetes 1.24 (containerd/CRI-O are the runtimes). `Overview.md:146` "future v2 Ingress API or equivalent" — Gateway API reached GA (v1.0) in 2023. `Overview.md:61` kubelet read-only port 10255 is disabled by default in current distributions. `Overview.md:104` "AKS clusters by default use kubenet" — Microsoft now steers to Azure CNI Overlay and has announced kubenet retirement (specifics unverified).
- **STALE (Medium):** `EKS.md:26-28` "The largest CIDR block that can be used in AWS for any VPC is /16 ... the /16 VPC size cannot be changed" — secondary CIDR blocks can be associated with a VPC and EKS custom networking lets pods draw from a secondary range (e.g. 100.64.0.0/10), which is the standard mitigation for the IP-exhaustion problem the file describes. `EKS.md:22` is a truncated sentence.
- `Cheat:75` "bridge crbr0" — the kubenet bridge is `cbr0` (typo, Low). `Cheat:1` H1 "Kubernetes cli" vs filename.

**(c) Recommendation.**
- Canonical concepts = `Kubernetes/Overview.md` (rename to `Kubernetes.md`). Rename the cheat sheet to a sibling `Kubernetes/kubectl.md`; move `Cheat:56-85` into it as "## Debugging pod networking" and link from Overview's pod-networking section.
- Move `Overview.md:102-104` (AKS kubenet/Azure CNI) to a new `Azure/AKS.md`, and add a "## Managed Kubernetes" paragraph in Overview linking `AWS/EKS.md` and `Azure/AKS.md` so provider content is symmetrical.
- `Overview.md:165-181` (cert-manager/ACME): keep cert-manager specifics, move the ACME/domain-validation explanation (`:174-181`) into `Security/Web Security/TLS Certificates.md` and link (see Group 9).
- Fix `:235` and the rkt/dockershim/Ingress-v2 statements when merging.

**(d) Currency.** All three are 2021-11. Overview is the most stale in absolute terms (five dated claims above). The cheat sheet commands remain valid (official cheatsheet URL has moved to `/docs/reference/kubectl/quick-reference/`). EKS Fargate limitations (`:18-22`) still broadly hold; `:26-28` is stale.

---

## Group 4 — Container security: `Security/Container Security.md` vs `Kubernetes/Kubernetes Security.md` vs `Docker.md` (security sections)

**(a) Overlap.**
- `Docker.md` has **no security section**. The only security-relevant lines are `:15` (cgroups/namespaces), `:17-24` (namespace isolation, "container isolation is not as good as a full VM's"). The gap itself is the finding.
- Container Security vs Kubernetes Security: ~5% — only mutual TLS (`Container:31` Swarm managers vs `K8s Security:14-20` cluster certs).
- Container Security vs Docker: ~5% (`Container:33-35` network-scoped service discovery vs `Docker:108-110` docker0 bridge).
- `Container Security.md` is fragmentary lecture notes: `:11-13`, `:19`, `:25`, `:35` are single-sentence fragments ("Adversarial environment", "Store root keys offline", "Traditionally - Hard shell soft interior").

**(b) Contradictions / cross-file currency.** No direct contradictions. Consistent pair worth cross-linking: `Docker.md:24` (shared-kernel isolation weaker than VM) ↔ `AWS/EKS.md:14-15` (Fargate gives each pod its own VM boundary, "mitigating ... container escapes").
- **STALE (Medium-High):** `K8s Security.md:8` "Basic HTTP - uses static password files read during API server startup" — static-password-file authentication was removed from the API server in Kubernetes 1.19 (2020), before this file's 2021 commit.
- **Misleading (Medium):** `K8s Security.md:6` "Client Certificates - most commonly used way to authenticate to the API server e.g. in managed cloud service like AKS" — on managed clusters the normal path is IdP tokens (AKS: Entra ID/OIDC; EKS: IAM via the authenticator webhook, not covered anywhere in `EKS.md`); client certs are the break-glass/local-admin path.
- **STALE (Medium):** `Container Security.md:7,9,21` "universal control planes" / "Docker Trusted Registry" — Docker Enterprise (UCP/DTR) was sold to Mirantis in 2019 and renamed; `:27-31` Docker Swarm is niche today.
- Structural: `Kubernetes Security.md` H1 (`:2`) is "Securing the API Server", not the filename; `Docker.md` H1 (`:1`) is "Virtualization".

**(c) Recommendation.**
- Keep `Kubernetes Security.md` as canonical for cluster hardening (authn plugins, RBAC, kube-bench); fix H1; add the missing topics an agent will expect: Pod Security Standards/Admission (PSP removed in 1.25), NetworkPolicy, secrets encryption at rest, EKS/AKS auth models (link to `EKS.md`, new `AKS.md`).
- Rewrite `Security/Container Security.md` as the vendor-neutral, cross-cutting page: image supply chain (content trust → Sigstore/cosign, TUF `:15-19`, SBOM), image scanning (Trivy/Grype; DTR paragraph `:21-23` becomes "registry scanning"), runtime hardening (`:37-39` drop privileges, non-root, read-only FS, seccomp/AppArmor), isolation spectrum (link `Docker.md:17-24` and `EKS.md:14-15`). Delete Swarm/UCP fragments (`:5-13`, `:27-31`) or move to an archive note.
- `Docker.md`: rename H1 to "Docker", keep as the Docker reference; add a "## Security" stub that links to Container Security rather than duplicating.

**(d) Currency.** `Kubernetes Security.md` (2021) is the more current and coherent; `Container Security.md` (2020) is an archive candidate in its present form; `Docker.md` (2021) is fine as a command reference (`:40` example uses `microsoft/aspnet:1.0.0-rc1` — a 2015 image, cosmetic).

---

## Group 5 — Cloud security: `Security/Cloud Security.md` vs `AWS/Security.md` (+ `Security - IAM/KMS/Networking.md`) vs `Azure/Security.md` vs `Security/Storing secrets.md`

**(a) Overlap.**
- Cloud Security vs AWS/Security: ~15% — CIS Benchmarks (`CS:23,42-52` vs `AWS:31,78`), Prowler/ScoutSuite (`CS:65,69` vs `AWS:39`), CSPM (`CS:56-59` vs `AWS:29`), IDS/IPS (`CS:33` vs `AWS:34,70`), SIEM (`CS:34,72-91` vs `AWS:87`).
- Cloud Security vs Azure/Security: 0% textual, but `CS:82-93` (Azure Security Center, Azure Sentinel, image) is Azure product content that belongs beside `Azure/Security.md`, which is network-only (VNet service endpoints, SQL firewall).
- Cloud Security vs KMS: one line (`CS:101` "encrypted e.g. using AWS Key Management Service").
- AWS/Security - Networking (`:23-30` VPC endpoints, `:61-67` PrivateLink) vs Azure/Security (`:5-9` VNet service endpoints): ~10% conceptual parallel, not cross-linked; Azure Private Link (the analogue of PrivateLink) is absent.
- Storing secrets vs AWS/Security `:160-175` (Secrets Manager, Parameter Store) and `DevOps/Overview.md:73-74`: ~5% textual, but they are the same decision space (where secrets live) with no cross-reference. `Storing secrets.md:3-21` is actually GPG commit/tag signing, not secret storage.

**(b) Contradictions.**
- **INCONSISTENT (High, same table):** `Cloud Security.md:65` "Prowler ... Superior security tool vs ScoutSuite ... Better reporting summaries and filtering vs ScottSuite" vs `:69` "Scout2 ... Superior security-auditing tool vs Prowler ... better reporting UI vs Prowler". Each is declared superior to the other. Additionally `:69` links `nccgroup/Scout2` (archived predecessor) while the text describes Scout Suite. `AWS/Security.md:39` is neutral ("leverages ScoutSuite and Prowler").
- **INCONSISTENT (Medium):** `Security - KMS.md:31` "**Customer managed key** where customers generate the key material" vs `KMS.md:12` "generated by default, within AWS KMS. The key material cannot be extracted". Customer-managed keys have KMS-generated material by default; customer-generated material is the *imported* case (`:13`). Also `:29` "Service managed keys" (AWS terms are "AWS managed keys"/"AWS owned keys") and `:33` "CMK" vs `:10` "KMS keys" — AWS retired "CMK" in 2021; the file mixes both.
- **Unreconciled guidance (Medium):** `Storing secrets.md:25` "store secrets safely in a VCS repository ... GPG encrypt specific files in a repo so they are 'encrypted at rest'" vs `DevOps/Overview.md:73-74` "no secrets in source code / store secrets in a vault not in auto-generated files on a CI server". Both patterns are legitimate (SOPS/git-crypt/sealed-secrets vs external vault) but the reader gets opposite advice with no trade-off stated.
- **STALE (Medium-High at file date):** `Cloud Security.md:82` "Azure Security center", `:89` "Azure sentinel" — renamed Microsoft Defender for Cloud and Microsoft Sentinel in Nov 2021; file committed 2023-07.
- **STALE (Medium, unverified):** `AWS/Security.md:25` "you can only have 100 S3 buckets within an account by default" — default quota was raised substantially in 2024. `Azure/Security.md` (2022) does not mention Private Endpoints/Private Link, which Microsoft now recommends over service endpoints.
- Minor: `Azure/Security.md:26-27` "provide access to any IP: `0.0.0.0 to 255.255.255.255` / `1.1.1.1 to 255.255.255.255`" — second line is nonsensical; the special `0.0.0.0–0.0.0.0` rule is what "Allow Azure services" (`:17`) maps to. `Cloud Security.md:16` "ENSIA" → ENISA. `AWS/Security.md:84` "HIPPA and GDPA" → HIPAA, GDPR.

**(c) Recommendation.**
- `Security/Cloud Security.md` = canonical **vendor-neutral** page: frameworks (NIST CSF, MITRE ATT&CK, ENISA, CSA CCM/STAR/CAIQ, NCSC principles, CIS), controls checklist, tool categories (CASB/CWPP/CSPM/CNAPP, SIEM/SOAR). Remove provider content: move `:82-93` (Defender for Cloud, Sentinel, image) to `Azure/Security.md`; move `:63-70` AWS tool table to `AWS/Security.md` beside `:39` after resolving the Prowler/Scout contradiction (state what each is good at, drop "superior").
- `AWS/Security.md` hub + three children is the right pattern; replicate it for Azure: rename `Azure/Security.md` → `Azure Security.md` with the same identity / network / data / detection structure, cross-linking VNet service endpoints ↔ `AWS/Security - Networking.md:23-30` and Private Link ↔ `:61-67`.
- Split `Storing secrets.md`: `:3-21` GPG key management/commit signing → `Tools/Git and GPG Signing.md` (or a "Code signing" page); `:23-40` Blackbox → new `Security/Secrets Management.md` that lays out the spectrum (encrypted-in-repo: Blackbox/SOPS/git-crypt/sealed-secrets → external: AWS Secrets Manager, Parameter Store, Azure Key Vault, HashiCorp Vault), reconciles with `DevOps/Overview.md:73-74`, and links `AWS/Security.md:160-175` and `Security - KMS.md`.
- Fix KMS terminology (`:29-33`) to AWS's current vocabulary.

**(d) Currency.** `AWS/Security - Networking.md` (2025-08) is the most current and accurate file in the group; `AWS/Security.md` and `IAM.md` (2024) current; `KMS.md` (2024) current but terminologically inconsistent; `Cloud Security.md` (2023) partially stale (Azure names, Scout2); `Azure/Security.md` (2022) stale (no Private Link); `Storing secrets.md` (2022) — Blackbox is low-activity, SOPS is the mainstream equivalent (Medium).

---

## Group 6 — CI/CD & DevOps: `Tools/CICD.md` vs `Distributed Systems/Continuous Deployment.md` vs `DevOps/Overview.md` vs `DevOps/Azure DevOps.md`

**(a) Overlap.**
- `Continuous Deployment.md` (20 lines, deploy ≠ release) is ~100% contained in one bullet: `DevOps/Overview.md:56` "separate application build, deployment and release". Overview also has blue/green steps (`:100-107`) that belong with it.
- `DevOps/Overview.md:9-15` ("DevOps capabilities") is a **near-verbatim duplicate of `People/Capabilites.md:45-51`** ("Infrastructure/Cloud Architect") — see Group 11. e.g. `Overview.md:9` "People who can work within organizations to bring people, processes and products together to enable continuous delivery of value to end users" == `Capabilites.md:45`.
- `Tools/CICD.md` vs Overview: ~10% (`CICD:14-21` on-prem CI costs vs `Overview:47` tooling). CICD.md is otherwise a 2018-era vendor comparison.
- `Azure DevOps.md` vs Overview: ~5% (`AzDo:39-54` release pipelines, `:60-64` approvals vs `Overview:56`).

**(b) Contradictions / cross-file currency.** No factual contradictions between the four. Cross-file duplication is the main issue. Notable per-file items that affect the merge:
- **STALE (High by rename; pricing Unverified):** `CICD.md:3` "VS Team Services", `:12` "**$110/month** https://www.visualstudio.com/team-services/pricing/" — product renamed Azure DevOps in 2018; both pricing cells are obsolete.
- **WRONG (Medium):** `CICD.md:27` "Bitbucket Pipelines ... only supports dotnet core" — Pipelines runs arbitrary Docker images; the linked page is a language-guides index.
- `Azure DevOps.md:25` YAML schema URL points at the owner's personal org (`dev.azure.com/hemantk`) — not a general reference. H1 mismatches: `Azure DevOps.md:1` "Terminology"; `Continuous Deployment.md:1` "Separate Deployment from Release".

**(c) Recommendation.**
- Canonical = `DevOps/Overview.md` → rename `DevOps.md`. Replace `:9-15` with a link to the People roles page (People is canonical for role definitions; it is the newer file).
- Create `Continuous Delivery.md` in the DevOps area from `Continuous Deployment.md` + `Overview.md:56-60` (build once/promote) + `Overview.md:100-107` (blue/green steps) + feature flags/canary; delete `Distributed Systems/Continuous Deployment.md` (it is a delivery-practice note, not a distributed-systems topic).
- `Tools/CICD.md`: archive, or rewrite as `CI-CD Tooling.md` (GitHub Actions, Azure Pipelines, GitLab CI, Jenkins, Buildkite) keeping only `:14-21` (self-hosted costs) and `:30-34` (fan-in/fan-out).
- `Azure DevOps.md`: keep as a tool reference beside the tooling page; fix H1; replace `:25` with the public schema link.

**(d) Currency.** `Azure DevOps.md` (2024) and `Overview.md` (2023) current; `Continuous Deployment.md` (2020) correct but tiny; `CICD.md` (2020) stale/archive candidate.

---

## Group 7 — HTTP / caching / performance: `HTTP.md` vs `HTTP Caching.md` vs `REST.md` vs `Synchronous Messaging.md` vs `SEO/Web Performance.md`

**(a) Overlap.**
- REST definition: `REST.md:1-15` vs `Synchronous Messaging.md:5-11` (~15% of each; SyncMsg's REST section `:5-58` is 40% of that file).
- Caching: `REST.md:80-84` links to `HTTP Caching.md` (good). `Web Performance.md` never mentions caching or HTTP/2 — the biggest performance levers — while `HTTP.md:13-15,23` (sprites, concatenation, domain sharding, HOL blocking) is web-performance content living in HTTP.md. 0% textual, same topic.
- Event feeds: `REST.md:122-140` (Atom pub-sub, broker SPOF, out-of-order) overlaps `Asynchronous Messaging.md:3,97` (Group 8) ~10%.
- HTTP/2 load balancing / gRPC: `HTTP.md:112` vs `SyncMsg:84,89` ~5%.
- `HTTP.md` itself is two documents: HTTP versions/persistence (`:1-57`) and realtime web (`:58-139`: long polling, WebSockets, SSE, SignalR, Streamdata.io).

**(b) Contradictions.**
- **INCONSISTENT (High):** `HTTP.md:114` "Websockets work on top of TCP and do not use the HTTP protocol, therefore your load balancer needs to work in TCP mode" vs `HTTP.md:94-96` "when a proxy server intercepts an Upgrade request from a client it needs to send its own Upgrade request to the backend server" (L7 proxying) and `Kubernetes/Overview.md:155` "Nginx can cut websocket connections whenever it reloads its configuration" (the nginx ingress proxies WebSockets at L7). L7 proxies handle WebSockets via Upgrade; TCP mode is one option, not a requirement.
- **WRONG/STALE (High):** `HTTP.md:131` "SignalR currently is based on the ASP.NET framework. This makes it unsuitable for Non Windows platforms" vs `HTTP.md:116` (links ASP.NET Core 5.0 SignalR scaling docs) and `Tools/Web Frameworks.md:157` "Blazor ... UI interactions are handled from the server over a real-time connection with the browser using SignalR". ASP.NET Core SignalR has been cross-platform since 2018.
- **INCONSISTENT (Medium):** `Synchronous Messaging.md:87` "Browsers don't fully support HTTP/2, making REST and JSON the primary way to get data into browser apps" vs `HTTP.md:21` "HTTP/2 ... supported by nearly two-thirds of all web browsers". Browsers support HTTP/2; what they lack is script access to HTTP/2 framing/trailers that gRPC needs (hence gRPC-Web). Both figures are also stale — HTTP/2 is supported by the overwhelming majority of browsers in use today (exact share Unverified).
- **Terminology (Medium):** `SyncMsg:89` "it uses HTTP2 at the transport layer" and `:62` "RPC spans the transport layer (TCP) and the application layer" vs `HTTP.md:3` "HTTP is a layer 7 protocol" and `Networking/Network Layers.md:17` (HTTP is application layer). See Group 10.
- **Internal tension (Low):** `HTTP.md:100` "HTTP/2 provides efficient HTTP based bidirectional communication" vs `HTTP.md:104` "HTTP/2 is not a replacement for push technologies such as Websocket or SSE".
- **STALE (Medium):** `HTTP.md:104` "HTTP/2 introduces Server Push" — Chrome removed Server Push support in 2022. `HTTP Caching.md:29` cites RFC 2616 §14.8 and `HTTP.md:47` RFC 2616 §8 — obsoleted by RFC 7234/7230, now RFC 9111/9112 (2022).
- `Web Performance.md:1` H1 "Search Engine Optimization" ≠ filename; `:3-11` is SEO URL-structure advice, `:13-43` is performance metrics mixing a 2010 "2 seconds" target (`:34`) with Lighthouse 10 weightings (`:21`). `:22` TBT definition is imprecise (it is the sum of the blocking portion of long tasks between FCP and TTI, not "sum of all time periods").

**(c) Recommendation.**
- Split `HTTP.md` → `HTTP.md` (`:1-57`: versions, keep-alive, pipelining, H2, H3) and `Realtime Web.md` (`:58-132`: long polling, WebSockets, SSE, SignalR — corrected; drop `:133-139` Streamdata.io as a vendor aside or reduce to one line).
- `HTTP Caching.md` stays canonical for caching; update RFC references; `Web Performance.md` and `Nginx.md` ("microcaching") link to it.
- `REST.md` canonical for REST. `Synchronous Messaging.md` → rename `API Styles - REST, RPC, gRPC, GraphQL.md`; shrink `:5-58` to a paragraph + link to REST.md; keep the RPC/SOAP/Thrift/gRPC/GraphQL comparison (its real value). Fix `:87,89`.
- Move `REST.md:122-140` (Atom feeds, messaging vs polling) into the messaging fundamentals page (Group 8) as "REST-based event feeds".
- Split `SEO/Web Performance.md` → `SEO.md` (`:3-11`) and `Web Performance.md` (`:13-43`, plus links to HTTP.md H2 section and HTTP Caching); fix H1.

**(d) Currency.** `Synchronous Messaging.md` (2023) newest but carries the two HTTP/2 errors; `HTTP.md` (2021) partially stale (H2 %, Server Push, SignalR); `HTTP Caching.md` (2021) semantically correct, RFC refs stale; `REST.md` (2021) timeless; `Web Performance.md` (2023) current on Lighthouse, stale on 2010 load-time advice.

---

## Group 8 — Messaging: `Asynchronous Messaging.md` vs `AMQP.md` vs `Servicebus Frameworks.md` vs `AWS/EventBridge_SQS_SNS.md` vs `Event Sourcing.md`

**(a) Overlap.**
- Delivery guarantees / idempotency / dedup: `Async:15-21` ≈ `Servicebus:6-8` ≈ `Event Sourcing:35-40` (~30% of each of the two small files).
- Outbox: `Async:13` describes the pattern in detail without naming it; `Servicebus:7` names it with a link.
- Distributed transactions / Helland quote: `Async:11` **and** `Async:62` (same quote twice in one file), `Servicebus:6`, `Event Sourcing:35`.
- Sagas: `Async:23-72` (canonical) vs `Servicebus:18` (one bullet).
- AMQP entities/fan-out: `AMQP.md` (whole) vs `Async:78,89`; `AMQP:15` fanout exchange vs `EventBridge:10,18` SNS fan-out.
- DLQ/retries: `Servicebus:10-15` vs `EventBridge:20,27`.
- `AMQP.md` and `Servicebus Frameworks.md` are ~40% conceptually subsumed by `Asynchronous Messaging.md`.

**(b) Contradictions.**
- **WRONG at time of writing (High, verified):** `EventBridge_SQS_SNS.md:20` "While SNS messages are sent once regardless of the consumer availability, SQS supports retries and dead-letter queues (DLQ)" and `:27` "in case of SNS -> Lambda, wherein if the lambda fails the message is lost". SNS has per-subscription delivery-retry policies (multiple delivery attempts before a message is discarded; the exact counts are endpoint-type dependent and not restated here) and per-subscription dead-letter queues; Lambda async invocations are additionally retried by Lambda with their own failure destinations. This also contradicts the generic statement in `Servicebus Frameworks.md:15` that DLQs "hold messages that cannot be processed after specified number of retries". The SNS→SQS→Lambda recommendation is still sound for batching/visibility, but the stated reason is wrong. Sources: [SNS dead-letter queues](https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html), [SNS delivery retries](https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html).
- **Title collision (High for agent retrieval):** `EventBridge_SQS_SNS.md:1` H1 "Asynchronous messaging" vs `Distributed Systems/Asynchronous Messaging.md` (H1 "Asynchronous message-based integration"). A title search lands on the AWS-specific file first.
- **WRONG link (Medium):** `Async:79` "STOMP ... https://docs.nats.io/" — NATS is not STOMP.
- **STALE (Medium):** `Async:93` "RabbitMQ ... once a message has been delivered, it is removed ... not suitable for long-term data storage" — RabbitMQ Streams (3.9+, 2021) provide a replayable append-only log; the Kafka-vs-RabbitMQ framing needs a caveat. `Async:115-126` MSMQ is legacy (no .NET Core/.NET support).
- `EventBridge:9` "If the consumer is down " — truncated sentence. `Event Sourcing:1` starts with a blank line before H1.
- No factual contradictions between `Asynchronous Messaging.md` and `Event Sourcing.md`.

**(c) Recommendation.**
- Split `Asynchronous Messaging.md` into: (1) `Messaging Fundamentals.md` (`:1-21` coupling, consistency options, delivery guarantees, idempotency — name the outbox pattern; absorb `Servicebus:5-8`, `Event Sourcing:35-40`, and `REST.md:122-140` as "polling feeds alternative"); (2) `Sagas and Process Managers.md` (`:23-72`); (3) `Message Brokers.md` (`:74-126` protocols, Kafka vs RabbitMQ, MSMQ-as-legacy) with `AMQP.md` folded in as "## AMQP model (exchanges, bindings, queues)" and a link out to the AWS page.
- Delete `AMQP.md` after folding. Reduce `Servicebus Frameworks.md` to the framework-specific value (routing, retries/back-off, ack/nack/DLQ, serialization, sagas; NServiceBus/MassTransit/CAP transports) and link Fundamentals for guarantees.
- Rename `EventBridge_SQS_SNS.md` → `AWS Messaging - SNS, SQS, EventBridge.md`, H1 to match, fix `:9,:20,:27`.
- `Event Sourcing.md` stays as an architecture-pattern page (pair with CQRS); link Fundamentals for idempotency.

**(d) Currency.** `EventBridge_SQS_SNS.md` (2024) is newest but factually wrong on SNS; `Asynchronous Messaging.md` (2021) conceptually sound with the RabbitMQ Streams caveat; `AMQP.md` (2020), `Servicebus Frameworks.md` (2020) and `Event Sourcing.md` (2022) remain correct.

---

## Group 9 — TLS: `Transport Layer Security.md` vs `TLS Certificates.md` vs `Security/Certification.md`

**Classification of `Certification.md`:** it is about **professional and organisational security certifications** (CISSP, SSCP, CEH, CREST; Cyber Essentials) — not TLS certificates. 0% overlap with the TLS files. It has no H1 (line 1 is a stray space, `:2` starts at H2), and CREST is an accreditation body rather than a certification (Medium). Rename to `Security Certifications (professional and organisational).md` or move to a People/career area so the word "Certification" can no longer be confused with "Certificates".

**(a) Overlap TLS vs TLS Certificates: ~25%.** `TLS.md:52-88` (DV/OV/EV, cost, Certificate Transparency, OIDs) is certificate content that belongs beside `TLS Certificates.md:11-17` (CA vetting, CSR). Conversely `TLS Certificates.md:89-93` (SNI) is a TLS-handshake extension → protocol content. `TLS.md:11` already links TLS Certificates (good). Also cross-folder: `Kubernetes/Overview.md:165-181` (cert-manager, ACME domain validation) is certificate-acquisition content living in Kubernetes; `TLS Certificates.md:50` and `Kubernetes Security.md:27` share the same `openssl x509 -in admin.crt -text -noout` command.

**(b) Contradictions.**
- **WRONG/STALE (High):** `TLS.md:35` "the web browser then generates a new secret key and encrypts it with the websites public key so that the secret can be shared with the website" presents RSA key transport as *the* TLS mechanism; `TLS.md:44` then says "The two most popular key exchange algorithms are RSA ... and Diffie-Hellman". TLS 1.3 (RFC 8446, 2018 — four years before this file's commit) removed RSA key transport entirely; modern handshakes use (EC)DHE for forward secrecy, and the certificate's key is used for *signing*, not encrypting the session secret.
- **STALE at file date (Medium-High):** `TLS.md:65` "When the site has EV, the organisation name and the country of origin is displayed along with the URL in the browser (Chrome & Firefox) address bar" — Chrome 77 and Firefox 70 (both 2019) removed the EV indicator from the address bar.
- **INCONSISTENT (Medium):** `TLS Certificates.md:7-9` a certificate "provides 1 and 2 above but is not so great at 3" (easy to obtain, renew, revoke) vs `Kubernetes/Overview.md:167` "Cert manager ... automatically requesting, retrieving and configuring TLS" and `Cloud/Nginx.md:40` "SSL/TLS offload with integration to Let's Encrypt - fully automated, free certificates". ACME makes obtain/renew trivial; only *revocation* remains weak (and `TLS Certificates.md:95-97` covers CRL but not OCSP/stapling or short-lived certs).
- **Layer placement:** `TLS.md:17` "between layer 4 and 7" vs `Network Layers.md:4` "Presentation - Encryption" — see Group 10.
- Minor: `TLS Certificates.md:26` `-days 356` vs `:36` `-days 365` (typo). H1s: `TLS.md:1` "HTTPS", `TLS Certificates.md:1` "What is a Certificate?" — neither matches its filename.

**(c) Recommendation.**
- `Transport Layer Security.md` → `TLS.md`: handshake rewritten for TLS 1.2/1.3 ((EC)DHE, signatures, cipher suites), client authentication (`:90-94`), SNI moved in from `TLS Certificates.md:89-93`.
- `TLS Certificates.md` = canonical for certificates: absorb `TLS.md:52-88` (DV/OV/EV, OID, CT) and the ACME explanation from `Kubernetes/Overview.md:174-181`; add OCSP/stapling beside CRL; fix `:9` to say revocation is the weak link.
- `Kubernetes/Overview.md` keeps cert-manager operational specifics and links.
- `Certification.md`: rename/move as above; add H1.

**(d) Currency.** Both TLS files are 2022-06. `TLS Certificates.md` is the more accurate (no wrong cryptographic claims); `TLS.md` carries the two stale/wrong claims above. `Certification.md` (2020) is thin but not wrong.

---

## Group 10 — Layering: `Networking/Network Layers.md` vs `Distributed Systems/Interprocess Communication.md` vs `Distributed Systems/HTTP.md`

**(a) Overlap ~10%.** Sockets/ports (`Network Layers:19` vs `IPC:23` TCP loopback). `Network Layers.md:33-49` ("Making Http requests": curl, telnet, `openssl s_client`) is HTTP tooling, not layering, and `:58-62` (netstat, port scanning) is a tools appendix — together ~45% of the file is cheat-sheet material. `HTTP.md:3,33,35` make layer claims that depend on Network Layers' model.

**(b) Contradictions — OSI/TCP layer claims.**
- Consistent: `HTTP.md:3` "HTTP is a layer 7 protocol that is transmitted over a TCP connection" ↔ `Network Layers.md:17,19` (HTTP application; TCP transport). `HTTP.md:33` (QUIC over UDP) ↔ `Network Layers.md:29-31`.
- **Three placements of encryption (Medium):** `Network Layers.md:4` "Presentation - Encryption", `:17,:53` "SSH ... uses part of the Presentation layer"; `TLS.md:17` "TLS ... doesn't really fit into the OSI model ... between layer 4 and 7". None is wrong (OSI L5/L6 have no clean TCP/IP equivalent) but a knowledge base should state one convention and link to it. Recommend: use the 4-layer TCP/IP model; TLS/SSH are application-layer protocols in that model; mention OSI only for the L4/L7 load-balancer vocabulary.
- **INCONSISTENT (Medium):** `Synchronous Messaging.md:62` "RPC spans the transport layer (TCP) and the application layer" and `:89` "uses HTTP2 at the transport layer" vs `Network Layers.md:17-19` (HTTP is application layer, TCP is transport).
- **WRONG (Medium):** `Network Layers.md:19` "A client (browser) also gets a port assigned dynamically between 8000 to 65535" — the ephemeral range is IANA 49152–65535 (Linux default 32768–60999).
- **Misleading (Medium):** `HTTP.md:108` "A server can handle 65,536 sockets per single IP address" — the ~64k limit is the client-side ephemeral-port space per (client IP → server IP:port) tuple; a server's concurrent-connection ceiling is bounded by file descriptors/memory, which `HTTP.md:108-110` itself goes on to say.
- **Internal (IPC, Medium):** `IPC.md:44` "a pipe with a default security descriptor can only be accessed by the LocalSystem account" vs `IPC.md:42` the default DACL "also grant[s] read access to members of the Everyone group and the anonymous account".
- Typos: `Network Layers.md:23` "48 bit hexadecimal layer", "Median Access Control" (Media Access Control).

**(c) Recommendation.**
- `Network Layers.md` canonical for layering; add a one-paragraph "layering convention" and have `TLS.md:17`, `HTTP.md:3`, `SyncMsg:62,89` link to it. Move `:33-49` + `:58-62` into `Networking/Network Tools.md` (curl, telnet, openssl s_client, netstat, ssh fingerprints) — cheat-sheet kind.
- `Interprocess Communication.md` is an OS/local-communication topic, not distributed systems: move to the Networking area as `Local IPC (pipes, Unix domain sockets).md`; keep the gRPC-over-UDS section and link to the gRPC section of the API-styles page.

**(d) Currency.** All 2021; `Network Layers.md` and `IPC.md` remain accurate apart from the items above.

---

## Group 11 — Roles: `People/Capabilites.md` vs `People/Leadership.md`

**(a) Overlap ~15%.**
- `Capabilites.md:33-35` "Getting results through others ... From player to coach, from doing to getting it done" ≈ `Leadership.md:25` "you shift from being a player to a coach, from doing to leading".
- `Capabilites.md:102-107` active listening via "labels and mirrors" (same Black Swan link) ≈ `Leadership.md:109`.
- `Capabilites.md:3-14` Engineering Leadership capabilities vs Leadership.md's whole theme (behaviours). `Capabilites.md:11` "build shared understanding" vs `Leadership.md:30-34` DAC.
- Cross-group: `Capabilites.md:43-51` ("Infrastructure/Cloud Architect") is verbatim `DevOps/Overview.md:9-15` (Group 6).
- Not read but flagged: `Leadership.md:36-46` "Self awareness" and `:112-127` "Influence" duplicate the topics of existing `People/Self Awareness.md` and `People/Influence.md` (Leadership.md:125 links the latter).

**(b) Contradictions.** None of fact. Role-definition observations:
- `Capabilites.md:43-51` is not a role definition — it is the DevOps-capabilities paragraph pasted under an "Infrastructure/Cloud Architect" heading and lacks the structure the "Architect" section (`:22-41`) has.
- `Capabilites.md:41` and `:60` repeat "work in the open - demonstrate progress transparently" under two roles.
- Filename `Capabilites.md` is misspelt (H1 `:1` "Capabilities").
- `Capabilites.md:89-121` ("Fact finding", "Selling the role") is interviewing/hiring content, a different topic from role capabilities.
- `Leadership.md:13` "scientific experiments have shown jerks diminish a team's performance by 30-40%" — unsourced figure (Low/Unverified; likely the Felps "bad apple" studies). `:7` "Schien" → Schein.

**(c) Recommendation.**
- Split `Capabilites.md` → `People/Roles and Competencies.md` (`:1-88`; fix spelling; write a real Infra/Cloud Architect list; make `DevOps/Overview.md:9-15` a link here) and `People/Hiring and Interviewing.md` (`:89-121`).
- `Leadership.md` canonical for behaviours; replace `Capabilites.md:102-107` with a link to `Leadership.md:109`; move `Leadership.md:36-46` into `Self Awareness.md` and reduce `:112-127` to a summary + link to `Influence.md`.

**(d) Currency.** Both 2025; `Leadership.md` (2025-11) newest. Content is timeless; both are opinion/essay and should be tagged as such.

---

## Group 12 — .NET cluster: `Cheat sheets/Dotnet.md` vs `Tools/Web Frameworks.md` vs `Tools/Windows Background Tasks.md`

**(a) Overlap.**
- `Dotnet.md:11-27` vs `Web Frameworks.md:153-162`: **`Dotnet.md:13` == `Web Frameworks.md:155` verbatim** ("Server side rendoring (SSR) technology for creating dynamic web content using HTML and C#..." — same typo), same bullet list; Web Frameworks has the richer Blazor detail (`:157-160`). ~20% of Dotnet, ~6% of Web Frameworks.
- **Broken internal link in both:** `Dotnet.md:18` and `Web Frameworks.md:162` link `../Tools/Javascript Frameworks.md`, which does not exist (`Tools/` contains `Web Frameworks.md`; the file was evidently renamed).
- `Windows Background Tasks.md` vs the others: 0% textual; it is .NET hosting content (services, Hangfire, Topshelf) with no H1.

**(b) Contradictions.** None of fact between Dotnet and Web Frameworks. Structural/currency:
- `Web Frameworks.md:157` describes Blazor as server-connected via SignalR, then `:158-160` nests "Blazor Server" and "Blazor WebAssembly" under **Razor Pages** as "hybrid rendering modes" — they are Blazor hosting models, not Razor Pages modes; .NET 8 also added static SSR and Auto render mode. (Medium)
- `Dotnet.md:51` "framework can be net6.0, net7.0, net8.0" — .NET 6 and 7 are out of support as of today (Medium).
- **STALE (High):** `Windows Background Tasks.md:19` "Currently Hangfire has .NET framework 4.5 requirement" — Hangfire has supported .NET Core/.NET Standard since 1.6 (2016). `:21-23` Topshelf is dormant; the current approach is the Generic Host (`UseWindowsService()`, `BackgroundService`/`IHostedService`).
- `HTTP.md:131` (Group 7) contradicts `Web Frameworks.md:157` on SignalR's platform support.

**(c) Recommendation.**
- `Web Frameworks.md` canonical for rendering patterns and ASP.NET UI options (fix the Blazor nesting). Replace `Dotnet.md:11-31` with two lines + link.
- `Dotnet.md` → `.NET/dotnet CLI.md` (`:33-84`, refresh TFM list). Move `:3-9` (OWIN/Katana history) into a new `.NET/Hosting and Background Services.md` that rewrites `Windows Background Tasks.md` (Kestrel/IIS in-process, Windows Service via Generic Host, `BackgroundService`, Hangfire/Quartz; Topshelf marked legacy). Delete `Windows Background Tasks.md`.
- Fix the `Javascript Frameworks.md` link in both files (→ `Web Frameworks.md`).
- Note: `Cheat sheets/IIS.md`, `Nuget.md`, `VS.md` (not read) belong in the same `.NET` area.

**(d) Currency.** `Web Frameworks.md` (2024-12) most current and richest; `Dotnet.md` (2024-05) current CLI content, stale TFM examples; `Windows Background Tasks.md` (2020) stale/archive candidate.

---

## Cross-group themes an agent will trip on

1. **Same topic, two folders, two titles:** Ansible, Nginx, Kubernetes (Cheat sheets vs Cloud and Infrastructure); "Asynchronous messaging" (AWS file H1 vs Distributed Systems file); "Certification" vs "TLS Certificates".
2. **Verbatim duplicates:** `DevOps/Overview.md:9-15` == `People/Capabilites.md:45-51`; `Dotnet.md:13` == `Web Frameworks.md:155`; Helland quote twice in `Asynchronous Messaging.md:11,62`.
3. **Provider content in vendor-neutral files and vice-versa:** Azure Defender/Sentinel in `Security/Cloud Security.md:82-93`; AWS tool table in `Cloud Security.md:63-70`; AKS networking in `Kubernetes/Overview.md:102-104`; ACME/certificates in `Kubernetes/Overview.md:174-181`.
4. **Generic patterns in product files:** rate-limit vs circuit-breaker in `Haproxy.md:77-87`; API gateway/WAF/IPS in `Nginx.md:24-34`; delivery guarantees in `Servicebus Frameworks.md:5-8`.
5. **Layer vocabulary drift:** `TLS.md:17`, `Network Layers.md:4,17,53`, `SyncMsg:62,89`, `HTTP.md:3`.
6. **Highest-value factual fixes (cross-file):** `Haproxy.md:9` (nginx TCP), `HTTP.md:114` (WebSockets need TCP mode), `HTTP.md:131` (SignalR Windows-only), `EventBridge:20,27` (SNS no retries/DLQ), `Kubernetes/Overview.md:235` (Knative/Istio not in CNCF), `TLS.md:35` (RSA key transport), `Cloud Security.md:65/69` (Prowler vs Scout), `KMS.md:12/31` (who generates key material).
7. **Broken internal links:** `Tools/Javascript Frameworks.md` (from `Dotnet.md:18`, `Web Frameworks.md:162`).

---

## Proposed top-level taxonomy

Design rule: **organise by topic only.** "Cheat sheets" is a *format* axis and "Tools" is a grab-bag; both cut across the three topic folders and create the ambiguity. Make *kind* (`reference` / `cheatsheet` / `concept` / `opinion`) a tag or front-matter field, not a folder. Cheat-sheet content either becomes a `## Commands` section of the topic page or a sibling `<Topic> CLI.md` in the topic folder. Provider-specific material lives under the provider; cross-cutting security lives under Security and links out to provider security hubs; product-specific hardening (Kubernetes) lives next to the product. Max three levels (Area / Section / Page).

```
1. Software Engineering
   1.1 .NET                      dotnet CLI · Hosting and Background Services · (IIS, NuGet, VS — not audited)
   1.2 Web Frontend              Web Frameworks · Web Performance · SEO
2. Architecture & Integration   (replaces "Distributed Systems")
   2.1 APIs & HTTP               HTTP · Realtime Web · HTTP Caching · REST · API Styles (REST/RPC/gRPC/GraphQL)
   2.2 Messaging                 Messaging Fundamentals · Sagas and Process Managers · Message Brokers (incl. AMQP) · Service Bus Frameworks · Event Sourcing
   2.3 Resilience & Scale        Load Balancing (ex-Scalability) · Resilience Patterns (ex-Haproxy:77-87)
3. Platform & Operations        (replaces "Cloud and Infrastructure" minus providers, plus Tools/CICD)
   3.1 Containers & Kubernetes   Docker · Kubernetes · kubectl · Kubernetes Security
   3.2 Web Servers & Proxies     Nginx · HAProxy
   3.3 DevOps & Delivery         DevOps · Continuous Delivery · CI-CD Tooling · Azure DevOps · Ansible · (Chef, Terraform, SRE — not audited)
   3.4 Networking                Network Layers · Network Tools · Local IPC · (DNS, IP Routing — not audited)
4. Cloud Providers
   4.1 AWS                       AWS Security (hub) · IAM · KMS · Networking · EKS · AWS Messaging (SNS/SQS/EventBridge)
   4.2 Azure                     Azure Security · AKS (new, from K8s Overview:102-104)
5. Security                     (cross-cutting only)
   5.1 Governance & Frameworks   Cloud Security Controls · Security Certifications (professional/organisational) · (Compliance, Threat Modelling — not audited)
   5.2 Transport & Web           TLS · TLS Certificates · (XSS, CSRF, headers, cookies, WAF — not audited)
   5.3 Workload & Supply Chain   Container Security
   5.4 Secrets & Keys            Secrets Management · Git and GPG Signing
6. People & Leadership
   6.1 Roles & Hiring            Roles and Competencies · Hiring and Interviewing
   6.2 Leading                   Leadership · (Influence, Self Awareness, Negotiation — not audited)
```

### Mapping of every file read

| Current path | Proposed location | Action |
|---|---|---|
| Cheat sheets/Ansible.md | 3.3 DevOps & Delivery / Ansible.md | merge into DevOps/Ansible.md; delete |
| Cloud and Infrastructure/DevOps/Ansible.md | 3.3 / Ansible.md | canonical (absorbs cheat sheet) |
| Cheat sheets/Nginx.md | 3.2 / Nginx.md | merge as "## Operations"; delete |
| Cloud and Infrastructure/Nginx.md | 3.2 / Nginx.md | canonical; move API-gateway/WAF concept out |
| Cloud and Infrastructure/Haproxy.md | 3.2 / HAProxy.md | keep; move :77-87 to 2.3 Resilience Patterns; fix :9 |
| Cloud and Infrastructure/Scalability.md | 2.3 / Load Balancing.md | rename + expand (L4/L7, HW vs SW) |
| Cheat sheets/Kubernetes.md | 3.1 / kubectl.md | rename; sibling of Kubernetes.md |
| Cloud and Infrastructure/Kubernetes/Overview.md | 3.1 / Kubernetes.md | canonical; AKS → 4.2, ACME → 5.2, fix :235 |
| Cloud and Infrastructure/AWS/EKS.md | 4.1 / EKS.md | keep; fix :26-28 |
| Security/Container Security.md | 5.3 / Container Security.md | rewrite (supply chain, runtime); drop Swarm/UCP |
| Cloud and Infrastructure/Kubernetes/Kubernetes Security.md | 3.1 / Kubernetes Security.md | keep next to product; fix H1, :8; add PSA/NetworkPolicy |
| Cloud and Infrastructure/Docker.md | 3.1 / Docker.md | keep; H1 → Docker; security stub links 5.3 |
| Security/Cloud Security.md | 5.1 / Cloud Security Controls.md | vendor-neutral only; Azure → 4.2, AWS table → 4.1 |
| Cloud and Infrastructure/AWS/Security.md | 4.1 / AWS Security.md | hub; absorb tools table; fix Prowler/Scout |
| Cloud and Infrastructure/AWS/Security - IAM.md | 4.1 / IAM.md | keep |
| Cloud and Infrastructure/AWS/Security - Networking.md | 4.1 / Networking.md | keep (most current); cross-link Azure endpoints |
| Cloud and Infrastructure/AWS/Security - KMS.md | 4.1 / KMS.md | keep; fix key-material/CMK terminology |
| Cloud and Infrastructure/Azure/Security.md | 4.2 / Azure Security.md | expand to hub (identity/network/data/detection); absorb Cloud Security:82-93; add Private Link |
| Security/Storing secrets.md | 5.4 / Secrets Management.md + Git and GPG Signing.md | split |
| Tools/CICD.md | 3.3 / CI-CD Tooling.md | rewrite or archive |
| Distributed Systems/Continuous Deployment.md | 3.3 / Continuous Delivery.md | merge with DevOps/Overview:56-60,100-107; delete |
| Cloud and Infrastructure/DevOps/Overview.md | 3.3 / DevOps.md | canonical; :9-15 → link to 6.1 |
| Cloud and Infrastructure/DevOps/Azure DevOps.md | 3.3 / Azure DevOps.md | keep; fix H1, :25 |
| Distributed Systems/HTTP.md | 2.1 / HTTP.md + Realtime Web.md | split at :58; fix :114,:131 |
| Distributed Systems/HTTP Caching.md | 2.1 / HTTP Caching.md | keep; update RFC refs |
| Distributed Systems/REST.md | 2.1 / REST.md | canonical; :122-140 → 2.2 Fundamentals |
| Distributed Systems/Synchronous Messaging.md | 2.1 / API Styles.md | rename; shrink REST section; fix :87,:89 |
| SEO/Web Performance.md | 1.2 / Web Performance.md + SEO.md | split; fix H1 |
| Distributed Systems/Asynchronous Messaging.md | 2.2 / Messaging Fundamentals.md + Sagas.md + Message Brokers.md | split three ways |
| Distributed Systems/AMQP.md | 2.2 / Message Brokers.md (section) | fold; delete |
| Distributed Systems/Servicebus Frameworks.md | 2.2 / Service Bus Frameworks.md | trim guarantees; link Fundamentals |
| Cloud and Infrastructure/AWS/EventBridge_SQS_SNS.md | 4.1 / AWS Messaging - SNS, SQS, EventBridge.md | rename + H1; fix :9,:20,:27 |
| Distributed Systems/Event Sourcing.md | 2.2 / Event Sourcing.md | keep; link Fundamentals |
| Security/Web Security/Transport Layer Security.md | 5.2 / TLS.md | rename; rewrite handshake for 1.3; absorb SNI |
| Security/Web Security/TLS Certificates.md | 5.2 / TLS Certificates.md | canonical; absorb DV/OV/EV + ACME |
| Security/Certification.md | 5.1 / Security Certifications.md | rename (professional/organisational); add H1 |
| Networking/Network Layers.md | 3.4 / Network Layers.md + Network Tools.md | split tools out; add layering convention |
| Distributed Systems/Interprocess Communication.md | 3.4 / Local IPC.md | move; fix :42/:44 |
| People/Capabilites.md | 6.1 / Roles and Competencies.md + Hiring and Interviewing.md | split; fix spelling |
| People/Leadership.md | 6.2 / Leadership.md | keep; dedupe with Self Awareness/Influence |
| Cheat sheets/Dotnet.md | 1.1 / dotnet CLI.md (+ OWIN → Hosting page) | trim ASP.NET section to link |
| Tools/Web Frameworks.md | 1.2 / Web Frameworks.md | canonical; fix Blazor nesting + broken link |
| Tools/Windows Background Tasks.md | 1.1 / Hosting and Background Services.md | rewrite (Generic Host); delete original |

### Biggest moves, one line each

- **Dissolve "Cheat sheets"** — format is not a topic; Ansible/Nginx/Kubernetes cheat sheets become sections or CLI siblings of their topic pages, ending the two-folders-one-subject problem.
- **Dissolve "Tools"** — its six files split by topic (.NET, web frontend, CI/CD); nothing is lost and "where does X go?" has one answer.
- **"Distributed Systems" → "Architecture & Integration"** with APIs/Messaging/Resilience sections — the current folder mixes HTTP protocol notes, messaging, and a CD practice note; the new name matches the actual content and gives Continuous Deployment an obvious home elsewhere.
- **Split providers out of "Cloud and Infrastructure"** — AWS/Azure pages are provider references with a different maintenance cadence from platform concepts (Docker, Kubernetes, DevOps); a "Cloud Providers" area also makes AKS/EKS symmetry visible.
- **Security = cross-cutting only** — provider security stays under the provider (hub + children pattern already proven by AWS), Kubernetes hardening stays beside Kubernetes; Security/ keeps frameworks, TLS, container supply chain and secrets, so "Security/Cloud Security.md" stops competing with "AWS/Security.md".
- **Rename to disambiguate for retrieval** — `Certification` → `Security Certifications`, `EventBridge_SQS_SNS` → `AWS Messaging`, `Scalability` → `Load Balancing`, `Synchronous Messaging` → `API Styles`, `Capabilites` → `Roles and Competencies`; each current name misleads a title-based search.
- **Create Azure/AKS.md** — the only place AKS networking exists today is inside the generic Kubernetes overview, the mirror image of where EKS content lives.
