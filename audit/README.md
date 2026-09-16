# Audit of messup-learn, 16 September 2026

Every markdown note in this repository was read in full and checked for factual errors, stale claims, internal contradictions, duplication, unlabelled opinion, broken structure and misclassification. Every external link was fetched. The goal was to decide how to turn the repository into a wiki of foundational knowledge in the owner's own words.

Nothing in the repo was moved, merged or deleted. Five unambiguous breakages were fixed in place (see "Changes made"). Everything else is a recommendation.

## What is in this folder

| File | What it is |
|---|---|
| `README.md` | This summary: headline numbers, the errors to fix first, what was changed. |
| `file-triage.md` | One row per note (96) with a verdict: keep, rewrite, trim, split, merge, drop, or your call. Line-numbered key fixes. |
| `wiki-plan.md` | Purpose, design rules, proposed structure (61 pages), page frontmatter contract, image policy (every picture becomes an own `.drawio.svg`; 14 rasters redrawn, 4 screenshotted tables become markdown, 12 dropped), `AGENTS.md` draft, migration sequence. |
| `blog-candidates.md` | Which notes can become blog posts and which should not, with a thesis, outline and pre-publication fixes per post. Adds two candidates the owner did not name; pushes back on three that were named. |
| `mechanical-findings.md` | Scripted checks: internal links, images, headings, code fences, and the 575-URL link check with per-file dead-link list. |
| `details/*.md` | Eleven full reports, one per folder group plus one on cross-folder overlaps. Every finding has a line number, quoted claim, problem, suggested fix and confidence. |
| `details/linkcheck.tsv` | Raw result for every URL. |
| `tools/linkcheck.sh` | Re-runnable link checker. |

## Headline numbers

| | |
|---|---|
| Markdown notes | 96 (611 KB, 7,430 lines), plus 35 images and 2 draw.io sources |
| Age | 18 notes untouched since the June 2020 import; 48 last touched in 2020-21; 10 touched since 2025 |
| Line-level findings | 1,098 |
| of which wrong (never true) | 270, of which 156 rated high confidence |
| of which stale (true once, superseded) | 325 |
| Verdicts | keep 32 · rewrite 15 · trim 9 · split 4 · merge 14 · drop 20 · your call 1 · README rewritten as index 1 |
| External URLs | 575 unique: 363 OK, 94 moved, 29 dead, ~22 redirect to a generic landing page, 61 blocked bot checks, 11 unreachable hosts |
| Internal links | 16, of which 2 broken (both now fixed) |
| Notes with no H1 or an H1 that does not match the filename | 61 of 96 |

## The pattern

The repository has three kinds of content mixed together:

1. **Fundamentals in the owner's words.** Consistency models, HTTP, REST, messaging guarantees, TLS, the web attack pages, testing philosophy, the leadership notes. This is the wiki. It has real errors (below) but the shape is right.
2. **Copies of things that live elsewhere.** Command cheat sheets, cloud service catalogues, a CI vendor price table, Okta pricing, Android setup steps, a Datadog team guideline pasted whole, Kreps' essay pasted with his first person intact. This is where most of the staleness lives, and it is what the owner said the wiki should not be.
3. **Project residue.** Employer tenant names, client user counts, a personal Azure DevOps URL, a real public IP. This has to go before agents read the repo.

Roughly a third of the files are type 2 or 3. Removing them costs nothing the wiki needs.

## Highest-impact errors to fix first

These are claims an agent would confidently repeat and be wrong. File and line refer to the current repo. Full context and suggested wording are in `details/`.

**Cryptography and TLS**
- `Security/Data Security.md:88` says MACs and digital signatures provide confidentiality. They do not; only encryption does.
- `Security/Data Security.md:126-132` says two inputs can never produce the same hash, swaps preimage and collision resistance, and says a hash "provides confidentiality via encryption".
- `Security/Web Security/Transport Layer Security.md:35` describes the TLS handshake as the browser encrypting a secret with the server's public key. That is RSA key transport, removed in TLS 1.3; modern handshakes use ephemeral Diffie-Hellman and the certificate key only signs.
- `Security/Web Security/Transport Layer Security.md:65` says browsers show the EV organisation name in the address bar. Removed in 2019.
- `Security/Web Security/TLS Certificates.md:30-40` the OpenSSL recipe produces a certificate with no Subject Alternative Name, which every modern browser rejects. Line 81 defines a thumbprint as a hash of the public key; it is a hash of the whole certificate.
- `Security/Compliance.md:43-49` lists EES (withdrawn 2015), DSA (removed from FIPS 186-5) and 3DES (disallowed for encryption since 2024) as approved. Line 68 accepts TLS 1.0.

**Web security**
- `Security/Web Security/Security Headers.md:68-82` the section titled Cross-Origin-Resource-Policy is actually about Same-Origin Policy and CORS, and says CORP lets other origins read your resources. It does not.
- `Security/Web Security/Security Headers.md:45` presents `X-Frame-Options: ALLOW-FROM` as usable. Never worked in Chrome or Safari, removed from Firefox in 2019. Line 6 gives `Blocked` as a value; the values are `DENY` and `SAMEORIGIN`.
- `Security/Web Security/Security Cookies.md:21` says the 4 KB limit covers all cookies and browsers truncate. It is per cookie and browsers reject. Line 53 says SameSite binds a cookie to an origin; it is site-scoped.
- `Security/Web Security/Cross Site Scripting.md:13` makes input validation the primary XSS defence. Output encoding is. Line 21-25's `javascript.alert` payload has a typo and has not executed in any browser for fifteen years.
- SameSite cookies are not discussed in any of the three files where they matter (Cookies, CSRF, Headers).

**Distributed systems and data**
- `Distributed Systems/Consistency Models.md:38` equates strict consistency with linearizability (strict is stronger and unachievable). Line 65 says "partition tolerance is rarely achievable, so there are two choices", which inverts CAP; partitions are unavoidable and the choice is C vs A during one. Line 69 states read-your-writes backwards.
- `Distributed Systems/Asynchronous Messaging.md:97` says Kafka "does not suffer from" ordering problems because of a time-ordered log. Kafka orders within a partition only.
- `Cloud and Infrastructure/AWS/EventBridge_SQS_SNS.md:20,27` says SNS sends once with no retry and a failing Lambda loses the message. SNS has per-subscription retry policies and dead-letter queues; Lambda retries async invocations.
- `Distributed Systems/HTTP.md:108` repeats the "65,536 sockets per IP" misconception (that is the client-side ephemeral port space). Line 114 says WebSockets require a TCP-mode load balancer; L7 proxies handle the Upgrade. Line 131 says SignalR is Windows-only; false since 2018.
- `Distributed Systems/HTTP Caching.md:6,9` misdefine `Cache-Control: public` and `must-revalidate`.
- `Distributed Systems/REST.md:5` "Universal Resource Identifier" (Uniform). Line 23 puts the new resource URI in the 201 body; it goes in `Location`.
- `Distributed Systems/NoSql.md:3,14` MongoDB global write lock and non-durable writes by default. Both false for over a decade.
- `Distributed Systems/Concurrency Models.md:47` defines concurrency and parallelism the wrong way round. Line 5 names CSP "Communicating Sequential Processing".

**Cloud**
- `Cloud and Infrastructure/AWS/Security - Networking.md:39` says stateful means an inbound rule automatically creates the matching outbound rule. Stateful means return traffic for an allowed connection is permitted; rules are not mirrored. Line 37 says everything is blocked by default; outbound is allowed.
- `Cloud and Infrastructure/AWS/Security - KMS.md:33` says key deletion is instantaneous. There is a mandatory 7-30 day waiting period.
- `Cloud and Infrastructure/AWS/Security - IAM.md:47-51` ARN format omits the resource segment. Lines 53-83 are JSON with `//` comments and a missing comma; they fail if pasted.
- `Cloud and Infrastructure/AWS/EKS.md:26-28` says a VPC cannot exceed /16 or grow. Secondary CIDRs have existed since 2017.
- `Cloud and Infrastructure/Kubernetes/Overview.md:235` says Google declined to donate Knative and Istio to CNCF. Both were accepted in 2022 and have graduated. Lines 135-151 are built on ingress-nginx, retired March 2026.
- `Cloud and Infrastructure/DevOps/Overview.md:100-107` labels an in-place deployment with a maintenance window as blue/green. Line 28 (and `AWS/DR and Business Continuity.md:10-11`) treats RTO as a measured time rather than an objective.

**Computing fundamentals**
- `Computer Theory/NP Complete.md:9` defines NP as "problems that can take exponential time". NP is problems whose solutions can be verified in polynomial time.
- `Data and AI/Algorithm Design.md:5` equates best/worst case with lower/upper bound. Line 60-61 gives probing O(n) and chaining O(n/k); both are O(1) expected.
- `Computer Theory/Software Complexity.md:24` defines currying as passing fewer arguments (that is partial application). Line 72 defines cyclomatic complexity as all possible paths (it is linearly independent paths).
- `Data and AI/Machine Learning.md:27` uses house-price prediction as the classification example. It is the canonical regression example.
- `Data and AI/Regression Analysis.md:7` says least squares minimises error to the outliers. It minimises squared residuals over all points.

**Networking and web**
- `Networking/Network Layers.md:19` gives the ephemeral port range as 8000-65535. It is 49152-65535 (IANA) or 32768-60999 (Linux). Line 23: "Median Access Control".
- `Networking/IPRouting.md:30` says a VLAN "resolves MAC addresses to IP addresses". ARP does, and in the other direction.
- `Networking/DNS.md:17` describes TTL as an ISP cache setting. It is a per-record value every resolver honours.
- `SEO/Web Performance.md:22,43` misdefine Total Blocking Time and Time to Interactive; INP, the Core Web Vital since March 2024, is absent.
- `Tools/Web Frameworks.md:101` describes Angular as MVC with controllers (that is AngularJS, EOL 2022). Line 109 says JSX embeds JavaScript in HTML (the reverse). Line 141 says Next.js has native PWA support (it does not).

**People**
- `People/Leadership.md:17-22` says the DLOQ measures five dimensions and names two that do not exist. It has seven. Line 7 misnames Schein and his book. Line 81 "SIB" for SBI. Line 79 attributes William James's line to Dewey.
- `People/Self Awareness.md:5` repeats the debunked "eight-second goldfish attention span" as a Microsoft study.

## Duplicates and collisions an agent will trip on

- Three topics live in two folders with different titles: Ansible, Nginx, Kubernetes (cheat sheet vs concept page).
- Two files have the H1 "Asynchronous messaging" (the AWS note and the Distributed Systems note).
- `Security/Certification.md` is about professional certifications, not TLS certificates.
- `DevOps/Overview.md:9-15` and `People/Capabilites.md:45-51` are the same paragraph. `Cheat sheets/Dotnet.md:13` and `Tools/Web Frameworks.md:155` are the same sentence, same typo.
- Idempotency and at-least-once delivery are explained in three files; the Outbox pattern is described in one and named in another; Spanner appears in two; PCI DSS in two with contradictory authorship.
- `Security/Cloud Security.md:65,69` declare Prowler superior to ScoutSuite and ScoutSuite superior to Prowler.

## Content that should leave before agents read the repo

- `Tools/Okta.md` client names, user counts, a 2020 price quote and screenshot.
- `Cloud and Infrastructure/Azure/Azure Cli.md:124-137` former-employer tenant and app names.
- `Cloud and Infrastructure/DevOps/Azure DevOps.md:25` personal Azure DevOps organisation URL.
- `Security/Storing secrets.md` personal email in five examples; `Cheat sheets/Ansible.md:95` a real public IP.
- `Distributed Systems/Monitoring and Observability.md:148-276` an internal team guideline ("our squad", Datadog retention limits) presented as general best practice.

## Changes made in this audit

Only breakages with one correct answer were fixed:

- `Cheat sheets/Dotnet.md:18` link to non-existent `Tools/Javascript Frameworks.md` now points at `Tools/Web Frameworks.md`.
- `Tools/Web Frameworks.md:162` the same link was a self-link to the file's pre-rename name; now an in-page anchor.
- `Data and AI/Data in the Cloud.md:74` image title "AWS Security Patterns" on an experimentation diagram, corrected.
- `Distributed Systems/Synchronous Messaging.md:140` image title "HTTP stacks" on the business-layer diagram, corrected.
- `Security/Web Security/Cross Site Request Forgery.md:16-22` an unclosed code fence that rendered the rest of the file as code, closed and tagged `html`.

The five edits and this folder were committed as the baseline on 2026-09-16.

## Method and limits

- Eleven reviewers each read one folder group in full; a twelfth read 43 files across folders for overlaps and contradictions. Each worked to a fixed schema (line, type, quoted claim, problem, fix, confidence).
- Type "wrong" means never true; "stale" means true when written and superseded since, judged against the file's last commit date.
- Web verification was done only for high-severity, date-dependent claims (about 40 in total, cited inline in `details/`). Version numbers, prices and limits that were not verified are marked "Unverified" rather than guessed.
- Link status is a single fetch on 2026-09-16 with a browser user agent. 403 responses are reported as unverified, not dead. Two apparent dead links were false positives from trailing parentheses and were removed.
- One reviewer reported a duplicate `consistency-models.png` / `.PNG` pair; only the `.PNG` exists (case-insensitive filesystem artefact). Disregard that row in `details/distsys-1.md`.
- Detail-report line numbers refer to the files as they were before the five fixes above; the CSRF fix shifts later lines in that file by one.

## Status

Phase 1 (cut, merge, move) ran on 2026-09-16, straight after the baseline commit. Every path named in this folder is **pre-migration**; `phase1-moves.md` maps each old path to where its content now lives. Phase 2 (correct the KEEP pages) ran the same day: 33 pages, every High and Medium WRONG, STALE, INCONSISTENT and BROKEN finding applied, opinion attributed where the source was known. Per-page "was → now" logs are in `details/phase2/`. Phases 3 onward (rewrite, trim, wire up) had not started when this note was written.
