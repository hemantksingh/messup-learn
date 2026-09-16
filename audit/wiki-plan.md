# Wiki plan: from notes dump to a fundamentals knowledge base

## Purpose (owner's words, 2026-09-16)

> A reference for foundational knowledge at the fundamental level, not a copy of content available elsewhere at the source. A repository of knowledge gained by understanding the basics, in language without fancy words that I can understand clearly and rederive concepts from or refer back to. Content that is not relevant can be removed.

Downstream use: a knowledge base that agents will read. That adds three requirements: every page must be findable by its title, every claim an agent could repeat must be true, and opinion must be visibly separated from fact.

## Five design rules

1. **Organise by topic, never by format.** "Cheat sheets" and "Tools" are formats and grab-bags. They are the reason Ansible, Nginx and Kubernetes each exist in two folders. Both folders dissolve. Kind (concept, opinion, index) becomes a frontmatter field.
2. **One page, one question.** Each page answers "how does X work and why" in the owner's words. If a page needs a product version number to be true, that fact probably belongs at the vendor's docs with a link, not here.
3. **Own words, named sources.** Borrowed ideas get a `Source:` line. Verbatim passages either become a quoted block with attribution or get rewritten. The owner's positions are marked so an agent can tell doctrine from citation.
4. **A page is either current or says it is not.** Frontmatter carries `last_reviewed` and `status`. Nothing is silently stale.
5. **Provider pages hold mental models, not catalogues.** AWS and Azure pages explain how IAM evaluates a request or why a security group is stateful. Service lists, quotas and prices are one link away, not copied.

## Proposed structure

Nine topic folders plus cloud/ and practice/, one level deep. Names are page titles and filenames at the same time.

```
computing/         Algorithms and Complexity · Code Quality · Functional and Reactive Programming ·
                   Concurrency Models · The Unix Model
networking/        Network Layers · IP Addressing · DNS · Local IPC · TLS · TLS Certificates
web and apis/      HTTP · Realtime Web · HTTP Caching · REST · API Styles · Web Performance ·
                   Rendering Patterns
data/              Consistency Models · Choosing a Database · Data Platforms · Data Pipelines ·
                   Machine Learning
messaging/         Messaging Fundamentals · Sagas and Process Managers · Message Brokers ·
                   Event Sourcing and CQRS · Service Orientation
security/          Cryptography Basics · Security Principles and Threat Modelling ·
                   Browser Security Model · Cross Site Scripting · Cross Site Request Forgery ·
                   Security Headers · Web Application Risks · Secrets Management ·
                   Supply Chain and Container Security · Standards and Compliance ·
                   Data Privacy · Endpoint Security
platform/          Containers · Kubernetes · Kubernetes Security · Load Balancing and Proxies ·
                   Resilience Patterns · Observability · DevOps and Delivery ·
                   Infrastructure as Code · Configuration Management
cloud/
aws/               README (hub) · Identity · Key Management · VPC Networking · Messaging ·
                   Disaster Recovery · (EKS, if rewritten)
azure/             Tenants, Subscriptions and RBAC (incl. network access control)
practice/            Testing Strategy · Leadership · Influence and Negotiation · Roles and Hiring ·
                   Self Awareness
images/              16 editable .drawio.svg diagrams (source embedded in the SVG); no rasters
README.md            index: one line per page
AGENTS.md            how an agent should read this repo
```

Blog posts derived from wiki pages are drafted and published in the separate Jekyll repo `../hemantksingh.github.io`, never here (see `audit/blog-candidates.md`).

That is 61 topic pages from 96 notes (62 if EKS is rewritten rather than dropped), plus `README.md` and `AGENTS.md`. The mapping from every current file is in `file-triage.md`.

Why these moves, in one line each:

- **Distributed Systems → Messaging + Web and APIs + Data.** The folder mixed HTTP protocol notes, messaging, consistency and one delivery-practice note. The split matches the questions people actually ask.
- **Consistency Models under Data.** It is about databases and CAP; it sits next to Choosing a Database, which currently duplicates its Spanner section.
- **TLS under Networking, XSS/CSRF under Security.** TLS is a transport protocol. The web attacks are about the browser security model.
- **Security is cross-cutting only.** Provider security (IAM, KMS) stays with the provider. Kubernetes hardening stays beside Kubernetes. That ends the competition between `Security/Cloud Security.md` and `AWS/Security.md`.
- **Practice replaces People + Tools/Testing.** Testing Strategy is a philosophy essay in the owner's voice, the closest thing in the repo to the target style. It belongs with Leadership, not with a CI vendor table.
- **Renames that unblock retrieval.** Certification → Standards and Compliance (it was never about TLS certificates). Synchronous Messaging → API Styles. Scalability → Load Balancing and Proxies. NoSql → Choosing a Database. EventBridge_SQS_SNS → Messaging. Capabilites → Roles and Hiring.

## Page contract

Every page has this frontmatter:

```yaml
---
title: Consistency Models            # equals the H1 and the filename
summary: >                            # one sentence, plain words, what question this answers
  How a distributed database decides which reads see which writes, and what that costs.
kind: concept                         # concept | opinion | index
status: current                       # current | needs-review | draft
last_reviewed: 2026-09-16
sources:                              # books, talks, RFCs the page leans on
  - Kleppmann, Designing Data-Intensive Applications, ch. 9
tags: [consistency, linearizability, cap-theorem]
posts: []                             # blog posts derived from this page, once published (URL)
---
```

Body conventions:

- **Exactly one H1**, equal to `title`. Sections start at H2. (Today 16 files use H1 as a section marker and 9 have no H1.)
- **Start with the question**, then the plain-language answer, then the derivation. A closing "How to rederive this" or "Why this is true" section is encouraged where it fits.
- **Mark the owner's stance** with a blockquote prefix: `> Own view:`. Everything else is either derived or sourced.
- **No pasted passages.** If a paragraph came from a blog, book or vendor doc, rewrite it or quote it with the source. Five files currently carry first-person text that is not the owner's (Kreps, Atlantic interviewees, Scott Helme, a Datadog team guideline, Google CRE).
- **No product numbers unless the concept depends on them.** Quotas, prices, version-specific flags and click-paths go to a link. When a version matters (TLS 1.3 removed RSA key transport), say so because it changes the concept.
- **Length budget: 3,000 words of body prose per page, hard ceiling.** Tables of requirements, contracts, schemas and data are not counted; they are read by lookup, not start to finish. A page over budget is split, or the overflow moves to an appendix page. Never fix length with denser prose.
- **No employer or personal data.** Use `example.com`, `<tenant>`, `<gpg-uid>`. Today: Okta client names and user counts, a former employer's tenant names in Azure CLI snippets, a personal Azure DevOps org URL, a personal email in GPG examples, a real public IP in an Ansible example.
- **Code fences always have a language.** Command output goes in a separate `text` fence or is prefixed with `#`. (Today: 12 bare fences; HCL, YAML, HTTP and JSON tagged as `sh`, `javascript`, `js`.)
- **Images have descriptive alt text** and live in `images/`. Remote LaTeX-rendered images (6 in the TLS page) become inline code or text.
- **Every picture is a diagram we drew, as a `.drawio.svg` embedded in the page that explains it.** No screenshots, slides or third-party images; tables that were screenshotted become markdown tables. See "Diagrams and images" below.
- **Internal links are relative** and point at pages, not the old folders. Run `audit/tools/linkcheck.sh` before committing external links.

## Diagrams and images

Rule: **every picture in the wiki is a diagram we drew, stored as `.drawio.svg`.** No screenshots, no slides photographed from talks, no third-party artwork. This follows from the purpose (own understanding, own words) and it fixes three problems at once: images that contradict the corrected text, alt text that is just a filename, and copyright on borrowed pictures.

Of the 35 images today, 30 are rasters. Viewed one by one: 14 are worth redrawing as our own diagrams (they illustrate a fundamental the page keeps), 4 are tables that were screenshotted and should become markdown tables, 12 are screenshots or vendor graphics that go with the content they belong to. The remaining 5 are PNG exports of the two draw.io files and are replaced by the SVG conversion below. End state: `images/` holds 16 `.drawio.svg` files and nothing else.

### Redraw as `.drawio.svg` (14 images, 12 new files)

Redraw to match the corrected page, not the old picture. Where the source image encoded an error, the note says so.

| Current image | New diagram | Embed in | Note |
|---|---|---|---|
| `consistency-models.PNG` (slide) | `consistency-ladder.drawio.svg`: strong to weak ladder | Data / Consistency Models | Drop "strict" as a separate rung or mark it theoretical; the page currently equates it with linearizability, which is wrong |
| `http-stacks.PNG` (slide) | `http-protocol-stacks.drawio.svg`: HTTP/1.1, /2, /3 over TLS, TCP, QUIC, UDP, IP | Web and APIs / HTTP | Show QUIC carrying TLS 1.3 |
| `http-v-http2.jpg` | `http-multiplexing.drawio.svg`: sequential requests vs multiplexed streams over time | Web and APIs / HTTP | Sequence-diagram style |
| `business-layer.png` | `api-styles-shared-core.drawio.svg`: REST, GraphQL, RPC front-ends over one business layer | Web and APIs / API Styles | Trivial, but the point is the shared core |
| `osi.gif` (third-party chart) | `network-layers.drawio.svg`: OSI 7 vs TCP/IP 4, PDU per layer, example protocols | Networking / Network Layers | Include the layering convention the plan adopts |
| `password-hashing.png` | `password-hashing.drawio.svg`: salt + hash on creation, recompute and compare on verify | Security / Cryptography Basics | Add "slow, memory-hard KDF" label |
| `message-signing.jpg` (orphan) | `digital-signature.drawio.svg`: sign with private key, verify with public key | Security / Cryptography Basics | Pairs with the corrected MAC vs signature vs encryption table |
| `testing-behaviour.jpg` | `test-boundaries.drawio.svg`: tests mirroring classes vs one test per behaviour | Practice / Testing Strategy | The flagship essay deserves its own diagram |
| `ansible-components.png` | `ansible-push-model.drawio.svg`: inventory, playbook, modules, control node, SSH to managed nodes | Platform / Configuration Management | Already draw.io style; source lost |
| `elastic-log-shippers.jpg` and `elastic-stack.jpeg` (orphan) | `log-pipeline.drawio.svg`: shipper, aggregator, store, query and visualise | Platform / Observability | Vendor-neutral; name Beats, Fluent Bit, OTel Collector only as examples in the page text |
| `hangfire-singleprocess.png` and `hangfire-winservice.png` | `persisted-background-jobs.drawio.svg`: one diagram, in-process worker vs separate worker, both reading a persisted job store | Messaging / Messaging Fundamentals | The persistence is the point; the two hosting options are variants |
| `aws-vpc.png` (AWS docs) | `aws-vpc-layers.drawio.svg`: VPC, subnets, route tables, NACL at subnet edge, security group at the instance, IGW and VGW | Cloud / AWS / VPC Networking | Label security groups "stateful: return traffic allowed", NACLs "stateless: both directions" |
| `azure-role-assignment.png` | merge into `azure-tenant-subscription.drawio.svg` | Cloud / Azure / Tenants, Subscriptions and RBAC | Role, scope, principal triangle becomes part of the tenant diagram |

### Convert to markdown tables (4 images)

These are tables that were screenshotted. A table is searchable, diffable and readable by agents; a picture of one is none of those.

| Current image | Becomes | In |
|---|---|---|
| `cacheable-content.jpg` (slide photo) | Table: static, dynamic, user-specific content; examples; cacheability | Web and APIs / HTTP Caching |
| `default-cluster-roles.png` (825 KB slide) | Table: cluster-admin, admin, edit, view; scope; what each can and cannot touch | Platform / Kubernetes Security |
| `arm-terraform.png` (slide) | Table: ARM template concept vs Terraform concept | Platform / Infrastructure as Code |
| `network-admin-tools.jpg` (Julia Evans zine) | Table: tool, question it answers (own words; the zine is copyrighted) | Networking / Network Layers or the tools section it moves to |

### Delete with the content they belong to (12 images)

| Image | Why |
|---|---|
| `windows-schannel.png` | Screenshot of a Windows dialog; the Schannel section moves out of Compliance |
| `asc_as.png` | Microsoft marketing graphic for two renamed products; Azure product notes leave Cloud Security |
| `data-analysis-experimentation.png` | Belongs to the digital-analytics detour, which goes with Data in the Cloud |
| `logstash-fluentd-comparison.png` | Stale vendor comparison; the log-shipper section is replaced by the generic pipeline diagram |
| `nginx-dos-protection.jpg` | Vendor marketing; one sentence ("DDoS filtering sits in front of the WAF, which sits in front of the app") replaces it |
| `hadoop-stack.png` | Hadoop catalogue is dropped from Big Data |
| `patterns-effective-teams.jpg` | Orphan; third-party sketchnote |
| `mac.png` | Orphan; goes with the Mac cheat sheet |
| `okta-pricing.png` | Goes with Okta.md |
| `android-project-build.png`, `android-tools-architecture.png` | Go with Android.md (your call) |

### Converting the two draw.io sources

Today the two `.drawio` files are unreferenced, unreadable by agents, and their exported PNGs have drifted from the source (labels still say "Azure AD" and "Service Admin"). The fix is one file format that is both the source and the rendered image.

**Convention.** Every diagram is a `.drawio.svg` file in `images/`. It is a normal SVG, so GitHub, editors and agents render it as a picture. It also carries the draw.io XML inside, so opening it in draw.io edits the same file. One diagram page per file. The markdown embeds it like any image:

```markdown
![Federated access to AWS: corporate identities assume IAM roles for temporary credentials](../../images/aws-federated-access.drawio.svg)
```

**Tooling on this machine.** The VS Code extension `hediet.vscode-drawio` is installed and handles `.drawio.svg` natively: open the file, edit visually, save, and the SVG is regenerated with the source embedded. To convert an existing multi-page `.drawio`, open it, use the extension's "Convert To .drawio.svg" command, then split pages so each file holds one diagram. If a batch export is ever needed, install the desktop app (`brew install --cask drawio`) and run:

```sh
/Applications/draw.io.app/Contents/MacOS/draw.io -x -f svg --embed-diagram -p 0 -o images/aws-federated-access.drawio.svg "Cloud and Infrastructure/AWS/AWS.drawio"
```

The `--embed-diagram` flag is what makes the output re-editable; `-p` selects the page index.

**The four diagrams to convert.**

| Source file and page | New file | Embed in |
|---|---|---|
| `AWS.drawio` page "IAM" (federated access flow; also holds the IAM / KMS / VPC icon triad, which becomes a second file or is dropped) | `images/aws-federated-access.drawio.svg` | Cloud / AWS / Identity |
| `AWS.drawio` page "Serverless DR" (never exported) | `images/aws-serverless-dr.drawio.svg` | Cloud / AWS / Disaster Recovery |
| `AzureAd.drawio` page "Azure Isolation" (relabel to Entra ID, replace "Service Admin" with RBAC Owner, fix "Managed Identites") | `images/azure-tenant-subscription.drawio.svg` | Cloud / Azure / Tenants, Subscriptions and RBAC |
| `AzureAd.drawio` page "Access patterns" | `images/azure-access-patterns.drawio.svg` | Cloud / Azure / Tenants, Subscriptions and RBAC |

Once embedded, delete the two `.drawio` files and the five PNGs they generated (`aws-federated-identity.png`, `aws-security-patterns.png`, `azuread-subscription.png`, `tenant-transfer.png`, `access-patterns.png`).

### Order of work

Redraw in the order the pages are fixed, so each diagram is drawn against corrected text: VPC layers and the two cryptography diagrams first (they illustrate the biggest corrections), then the HTTP pair, consistency ladder, network layers, test boundaries, and the rest. Each new `.drawio.svg` gets descriptive alt text on embed. Any future diagram follows the same rule: draw it as `.drawio.svg` next to the page, never as a screenshot.

## AGENTS.md (draft)

```markdown
# How to use this repository

This is one person's knowledge base of engineering fundamentals, written in their own words.
It is not documentation for any product.

- Start at README.md, which lists every page with a one-line summary.
- Trust pages with `status: current` in their frontmatter. Treat `needs-review` as possibly stale
  and `draft` as incomplete.
- Pages with `kind: opinion` and paragraphs starting `> Own view:` are the owner's positions.
  Cite them as opinion, not as fact.
- Product facts (quotas, prices, CLI flags, version numbers) are deliberately kept out.
  Follow the `sources` links or the vendor's documentation for those.
- Titles equal filenames. If you are looking for a topic, search titles first.
- Under `audit/` you will find the September 2026 audit that produced this structure. It is
  history, not reference material.
- Some pages list blog posts in their `posts:` frontmatter. Those are opinion pieces with a date
  on the owner's website; the wiki page is the source of truth.
```

## Migration sequence

Do it in this order so every step leaves the repo usable.

**Phase 0. Decisions (owner).** Confirm or change the taxonomy above. Decide the two YOU DECIDE items (Photography, Android). Decide whether cheat-sheet gotchas stay as sections or go entirely.

**Phase 1. Cut (cheap, high signal).** Delete the 20 DROP files and 5 orphan or project images. Do the 14 MERGEs. Rename folders to the new structure with `git mv` so history follows. Fix the two filename typos. This removes roughly a third of the repo and every employer-specific fact.

**Phase 2. Correct.** Fix the "highest-impact errors" list in `README.md` in the 32 KEEP pages. These are the claims an agent would confidently repeat and be wrong. Most are one-line edits; each has a line number in `file-triage.md` and a suggested fix in `details/`.

**Phase 3. Rewrite.** Fifteen pages, in this order of value: Consistency Models · TLS · Cryptography Basics (from Data Security) · Algorithms and Complexity (from NP Complete + Algorithm Design) · The Unix Model · Containers · Kubernetes · Choosing a Database · IP Addressing · Web Performance · Security Cookies (into Browser Security Model) · Data Pipelines · Container Security · Secrets Management · EKS (or drop). Each rewrite starts from the question the page answers, not from the old text.

**Phase 4. Trim and split.** Nine TRIMs and four SPLITs. Mechanical: delete the catalogue or pasted section, keep the principle, add a source line.

**Phase 5. Wire it up.** Add frontmatter to every page (a script can seed `title`, `kind`, `last_reviewed` and leave `summary` for a human). Generate README.md from frontmatter. Add AGENTS.md. Fix fence languages in one sweep. Convert the four draw.io pages to `.drawio.svg`, redraw the 14 raster diagrams as 12 new `.drawio.svg` files, turn the 4 screenshotted tables into markdown, and delete every remaining raster (see "Diagrams and images"). Alt text is written as each diagram is embedded. Run the link checker and replace the 29 dead and 22 gutted links (list in `mechanical-findings.md`).

**Phase 6. Keep it alive.** A quarterly pass over pages whose `last_reviewed` is older than a year. The link checker in CI or as a pre-commit hook.

## What I would not do

- Do not keep the cheat sheets "just in case". They are the largest source of wrong commands in the repo (nuget `source`, `kubectl exec` without `--`, `rm -r *.*`, `tail` default 20) and every one of them is one search away at the source.
- Do not preserve the `Overview.md` convention. Four folders have an `Overview.md` whose H1 is the folder name; agents indexing by title see four different names for four different topics. Name the page after the topic.
- Do not migrate the Datadog team guideline, the Octopus deployment text or the Kreps essay into new pages. Link them.
