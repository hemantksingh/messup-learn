# Phase 5: wire up the wiki (2026-09-16)

Phase 5 turned the corrected pages into a wiki. Ten agents produced manifests and content edits; a script applied them in one pass, then a structural check ran clean.

## What changed

* **H1s** aligned to filenames on nine pages (Ansible to Configuration Management, Compliance to Standards and Compliance, Azure to Tenants, Subscriptions and RBAC, and so on). The AWS hub keeps its H1 "AWS".
* **Frontmatter** on all 63 pages: title, summary, kind (concept, opinion or index), status, last_reviewed, sources, tags. `frontmatter.yaml` is the manifest. Six pages are opinion, one is index.
* **Root README.md** generated from the frontmatter: every page grouped by area with its one-line summary, opinion pages marked.
* **AGENTS.md** written: how an agent should read the repository.
* **Diagrams**: 37 drawn as draw.io XML (`diagrams.yaml` lists file, page, placement and alt text; `diagram-guide.md` is the palette and template the agents followed), exported with the draw.io CLI as `images/*.drawio.svg` with the source embedded, and placed in the pages. Two labels changed after review: the Ansible diagram says control node to match the page, and the saga diagram's placeholder "command" arrows became FetchItem and ShipOrder.
* **Rasters**: all 29 remaining raster images removed; each was either replaced by a diagram, replaced by a table (HTTP Caching cacheable content, Kubernetes Security default roles, Network Layers admin tools) or dropped (Standards and Compliance Schannel screenshot). The two `.drawio` source files went too; the SVGs carry the source.
* **Dead links**: 345 URLs checked; 32 replaced, 6 removed (`links.yaml`). Two removals needed rewording: the Inspector Classic bullet in the AWS hub and a bare bullet in DevOps and Delivery. Two URLs could not be verified either way from this machine and were left alone: Bernd Rücker's long-running processes post (Medium) and promcat.io.
* **Content edits** (`content-edits.md`): Data Privacy corrected in full (staff email, fingerprinting history, UK law, fines, international transfers, PCI DSS moved out); Configuration Management given an opening sentence; three pictures replaced by tables.
* **Text tidy-ups** the diagrams made necessary: Consistency Models no longer refers to "the slide"; TLS lost its ASCII arrow line; the AWS hub lost its pointer to `AWS.drawio`; Concurrency Models' "Further reading" became "Sources".

## Checks

* Structural check: one H1 per page, every code fence tagged, every relative link and anchor resolves, frontmatter present with title equal to filename, alt text not a filename, no orphan images. 0 problems.
* Prose length: longest page 2,949 words (Leadership); all under the 3,000-word ceiling.
* Every diagram rendered to PNG and reviewed by eye.

## Left for later

* 28 pages have no `## Sources` section (their frontmatter has `sources: []`): DNS, Local IPC, Network Layers, TLS Certificates, API Styles, HTTP Caching, Rendering Patterns, REST, Machine Learning, Event Sourcing and CQRS, Service Orientation, Cross Site Request Forgery, Cross Site Scripting, Security Headers, Security Principles and Threat Modelling, Standards and Compliance, Configuration Management, DevOps and Delivery, Kubernetes Security, Disaster Recovery, Identity, Key Management, Messaging, VPC Networking, Tenants, Subscriptions and RBAC, Roles and Hiring, Self Awareness, Testing Strategy.
* The two unverified URLs above.
