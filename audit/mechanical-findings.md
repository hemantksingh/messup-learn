# Mechanical findings (scripted, 2026-09-16)

## Repo shape
- 96 markdown files, ~611 KB, 7,430 lines; 35 images (4.6 MB); 2 draw.io diagrams; 433 commits (2020-06 → 2026-07).
- Age profile by last commit: 18 files untouched since 2020-06-19 (initial import); 30 files last touched in 2021; only 10 files touched since 2025-01.
- README is 3 lines and has no index of contents.

## Internal links (16 checked)
- BROKEN (2): `Cheat sheets/Dotnet.md:18` and `Tools/Web Frameworks.md:162` → `../Tools/Javascript Frameworks.md` (file does not exist; it is `Tools/Web Frameworks.md`; the second is a self-link).
- All other 14 resolve, including the one `#ddos-protection` anchor.

## Images
- Orphans (4, never referenced): `elastic-stack.jpeg`, `mac.png`, `message-signing.jpg`, `patterns-effective-teams.jpg`.
- Dead remote images (2): `Networking/IPRouting.md:18,36` → bitbucket.org (404). Content lost.
- Remote LaTeX-rendered formula images (6): `Security/Web Security/Transport Layer Security.md:23,30,37,46` depend on latex.codecogs.com; should be inline text/MathJax.
- Wrong title text (2, copy-paste): `Data and AI/Data in the Cloud.md:74` titled "AWS Security Patterns"; `Distributed Systems/Synchronous Messaging.md:140` titled "HTTP stacks".
- Alt text is the filename in ~30 of 34 embeds (useless to an agent or screen reader).
- Case-sensitive extensions: `http-stacks.PNG`, `consistency-models.PNG` (fine on macOS, breaks on case-sensitive hosts if renamed).
- draw.io (2, unreferenced, unreadable by agents): `AWS.drawio` = "Federated Access to AWS" + multi-region DR (weighted DNS, global tables, bucket replication); `AzureAd.drawio` = tenant/subscription/role-assignment model + tenant transfer. Convert each page to an editable `.drawio.svg` and embed in the page it explains (see wiki-plan.md "Diagrams").

## Headings / structure
- No H1 at all (9): Cheat sheets/Mac.md, Cheat sheets/VS.md, Kubernetes/Production Readyness.md, Data and AI/Algorithm Design.md, Networking/IPRouting.md, Photography/Photography Basics.md, Security/Certification.md, Tools/Windows Background Tasks.md
- Multiple H1s used as section headers (16 files) e.g. Azure Cli.md (21 H1s), Cheat sheets/Kubernetes.md (16), Azure Functions.md (11), Dotnet.md (10), Unix Basics.md (10), AWS/Overview.md (9).
- H1 materially different from filename (notable): Consistency Models.md → "Distributed Databases"; EventBridge_SQS_SNS.md → "Asynchronous messaging" (clashes with Distributed Systems/Asynchronous Messaging.md); Continuous Deployment.md → "Separate Deployment from Release"; NoSql.md → "Questions to think about before deciding on a DB"; Security Cookies.md → "HTTP Cookies"; Transport Layer Security.md → "HTTPS"; Web Performance.md → "Search Engine Optimization"; Cloud Security.md → "Cloud Security Controls Framework"; Azure DevOps.md → "Terminology"; IIS.md → "Troubleshooting"; Nginx.md (cheat) → "Architecture"; CICD.md → "CI tools".
- Filename typos: `People/Capabilites.md`, `Kubernetes/Production Readyness.md`. Inconsistent naming: `EventBridge_SQS_SNS.md` (underscores) vs spaces everywhere else; `NoSql`, `IOT`, `IPRouting`.
- Code fences without a language (12 total): Unix Basics.md (7), Synchronous Messaging.md (3), Mac.md (1), Transport Layer Security.md (1).
- Unclosed code fence: `Security/Web Security/Cross Site Request Forgery.md` (odd fence count → rest of file renders as code).

## External links (575 unique URLs)
| Result | Count | Meaning |
|---|---|---|
| OK | 363 | 2xx on same host |
| MOVED | 94 | 2xx after redirect to a different host (mostly docs.microsoft.com→learn.microsoft.com, terraform.io→developer.hashicorp.com, twitter→x; harmless) |
| DEAD | 29 | 404/410 (after removing 2 false positives caused by trailing parentheses) |
| Content gone | ~22 | Redirects to a generic product/landing page (all nginx.com blog posts → f5.com product page; streamdata.io → axway.com; sessionstack → playbookux; getambassador → gravitee; captricity → blueprism; amplify.nginx.com → EOL notice) |
| UNVERIFIED | 61 | 403/429 bot-blocking (18 stackoverflow, 5 medium, 5 beyondtrust, 4 security.stackexchange …) — probably fine |
| ERR | 11 | Host unreachable/DNS fail: www-db.cs.wisc.edu (CIDR'07 paper), usingcsp.com (CSP book), webperformancetoday.com, blog.bernd-ruecker.com, blog.envoyproxy.io, blog.sqreen.com, constantrenewal.com, dataform.co (x2), promcat.io, techbeacon.com |
| PLACEHOLDER | 10 | example.com, localhost, 169.254.169.254, $tenant — intentional |

### Dead links by file (29)
- Cheat sheets/Ansible.md:49 codereviewvideos.com ansible-handlers
- Cloud and Infrastructure/DevOps/Overview.md:31 leanix.net flow-metrics; :41 tutorialworks.com devops-metrics
- Cloud and Infrastructure/Kubernetes/Overview.md:155 vitobotta.com haproxy-kubernetes-hetzner
- Cloud and Infrastructure/Nginx.md:28 owasp.org Web_Application_Firewall (old wiki); :32 lanner-america.com waf-vs-ips
- Data and AI/Big Data.md:93 analytics.today snowflake-vs-hadoop
- Data and AI/Data in the Cloud.md:56 dzone.com ML-in-prod; :100 towardsdatascience cloud-ml-engine
- Data and AI/Data Processing Pipeline.md:41 towardsdatascience elasticsearch-for-data-science
- Data and AI/Regression Analysis.md:5 towardsdatascience multiple-linear-regression
- Distributed Systems/Concurrency Models.md:77 doc.akka.io remoting (snapshot)
- Distributed Systems/Monitoring and Observability.md:45 engineering.linkedin.com "The Log" (Jay Kreps) — canonical essay, find mirror
- Distributed Systems/Servicebus Frameworks.md:22 cap.dotnetcore.xyz transports; :24 masstransit-project.com transports
- Networking/IPRouting.md:18,36 bitbucket.org images
- Security/Web Security/Cross Site Request Forgery.md:12 owasp.org old wiki CSRF
- Security/Web Security/Cross Site Scripting.md:27 owasp.org old wiki XSS_Filter_Evasion
- Security/Web Security/Security Headers.md:3 owasp.org www-project-secure-headers (→ owasp.org/projects/secure-headers)
- Security/Web Security/Transport Layer Security.md:75 alvestrand.no OID 2.23.140.1.2.1
- Security/Web Security/Web Application Security.md:37 owasp ASVS (→ owasp.org/projects/application-security-verification-standard); :88 owasp old wiki Top_Ten_Cheat_Sheet; :198 github bkimminich/juice-shop (→ github.com/juice-shop/juice-shop)
- SEO/Web Performance.md:13 webmasters.googleblog.com 2010 site-speed
- Tools/Tesseract.md:6 arxiv.org ftp 1003.5893 (→ arxiv.org/abs/1003.5893)
