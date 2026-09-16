# Phase 4 report: Load Balancing and Proxies (trim) and Resilience Patterns (new)

Files edited (nothing committed):

* /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Load Balancing and Proxies.md (rewritten in place)
* /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Resilience Patterns.md (new)

No other page was edited.

## (a) Question each page answers

* **Load Balancing and Proxies**: what does a load balancer or reverse proxy do for me, and how do Nginx and HAProxy differ in doing it?
* **Resilience Patterns**: how does a system keep working when a dependency is slow or down?

## (b) Word counts

Method: `awk '/^```/{f=!f;next} !f && !/^\|/' <file> | wc -w` (drops code fences and table rows; keeps headings, link text and the Sources section). The "body" figure additionally drops headings and everything from `## Sources` on.

| Page | Before (same method) | After (same method) | After, body only | Target |
|---|---|---|---|---|
| Load Balancing and Proxies | 3,313 | 1,799 | 1,676 | 1,500 to 1,800 |
| Resilience Patterns | 0 (new) | 991 | 888 | 700 to 900 |

Resilience Patterns is inside the target on the body measure and 91 words over it on the same-method measure (headings and the Sources section account for the difference). Not trimmed further; denser prose is forbidden by rule 1.

## (c) What was cut and why

**Vendor and product catalogue**
* Nginx Plus feature list (JWT, identity propagation, NTLM, key-value store, monitoring) reduced to one sentence. Product content, not fundamentals.
* NGINX Amplify section: product shut down 31 January 2026. Removed entirely along with the Datadog nginx and HAProxy monitoring links and dashboard.
* ModSecurity WAF section: F5 NGINX ModSecurity WAF end of life March 2024. Replaced by one sentence stating the EOL and pointing at `../security/Web%20Application%20Risks.md`.
* NGINX App Protect mention removed.
* "HAProxy on CentOS 7 default repository": CentOS 7 EOL June 2024; removed.
* mod_jk / Tomcat connector paragraph removed (product detail, not a fundamental).
* Vendor benchmark paragraph reduced to one line labelled as contested marketing.

**Pasted or borrowed passages**
* AWS "Architecting for the Cloud" whitepaper paragraphs on scalability and vertical scaling rewritten in plain words and attributed in Sources. The EC2 example generalised to "in a cloud you stop the instance and resize it".
* The API gateway / WAF / IPS essay (four paragraphs plus links to nginx.com and lanner-america) reduced to one paragraph, linking Web Application Risks. Kept the owner's "overambitious API gateway" warning as one sentence.
* The rate limiting versus circuit breaker essay (`### Rate limiting`, five paragraphs) moved out and rewritten correctly on Resilience Patterns (see d).
* Chaos engineering paragraph (HAProxy blog) removed; it was a lead-in to the resilience material, not load balancing.

**WRONG / STALE / INCONSISTENT findings now absent**
* "Nginx only supports layer 7 HTTP mode ... use Nginx Plus": corrected; nginx OSS `stream` module doing TCP since 2015 and UDP the year after stated explicitly (year kept because it refutes the Plus-only claim; version number left out), comparison table row added.
* "HAProxy forwards the RAW TCP packets": corrected to proxying the byte stream with a terminated connection; LVS/IPVS named as the packet-level alternative.
* "never touches the file system, therefore it cannot serve static content": corrected to "not a web server; `http-request return` for small fixed responses".
* Apache "spins new threads" / "spawns a process per connection": now MPM-dependent (prefork processes, worker/event threads, event default since 2.4).
* AppArmor / "jail" claim: replaced with embedded interpreter (mod_php) versus separate application process (php-fpm, gunicorn).
* `Allow`/`Deny` lowercased; "Failtoban" is now "Fail2ban" throughout; "NetScalar" is "NetScaler (for a while Citrix ADC)"; "NewOps" removed with its sentence.
* Retries: `retries` (default 3) governs attempts, wait between attempts is min(`timeout connect`, 1 s), `timeout connect` bounds one attempt; `option redispatch` and `retry-on` (2.0+) described.
* Prometheus: exporter in core since 2.4, enabled with `http-request use-service prometheus-exporter`; the "2.0 native support" wording is gone.
* Circuit breaker described as a timeout with fallback (100 ms example): rewritten on Resilience Patterns as the explicit contrast (timeout bounds one call, fallback replaces one result, breaker stops calling).
* Version-pinned links (`cbonte.github.io/haproxy-dconv/2.0`, `hapee/latest`) removed; Sources point at `docs.haproxy.org`.
* `sh` fence language on HAProxy config blocks changed to `haproxy`.
* "Pasive", "implemeted", "guage" typos gone with their sentences.
* "the most popular open source software load balancer" softened to "widely used".
* "most load balancers stay idle until peak" labelled as a vendor claim.
* "trusted by 99% of browsers" removed.
* "(HTTP2)" attribution on upstream connection interleaving removed with the NTLM paragraph.
* `auth_request` named as the OSS directive; nginx's reference HTTP-to-LDAP service mentioned instead of "you'll have to write a converter".
* The "Horizontal scaling" heading that had no horizontal-scaling body now has two sentences on identical, stateless instances behind one address before handing off to the load balancer.

**Style**
* All em-dashes and en-dashes removed. Filler phrases removed. British spelling checked by grep.

## (d) What was moved where

* `### Rate limiting` (rate limiter versus circuit breaker essay), `#### Circuit breaker`, the generic parts of `#### Automatic retries`, and the back-pressure sentence from `#### Connection queueing` moved from the HAProxy section to `fundamentals/platform/Resilience Patterns.md` and rewritten as: timeouts; retries with backoff and jitter (plus retry budgets and idempotency); circuit breakers as a closed / open / half-open state machine; bulkheads; rate limiting versus load shedding; back-pressure; health checks as the input (active versus passive, HAProxy `observe` as a proxy-side breaker, Kubernetes readiness versus liveness); and a placement table (client library, sidecar or mesh, proxy).
* HAProxy-specific config facts (`check`, `option httpchk`, `observe`, `error-limit`, `on-error`, `agent-check`, `retries`, `retry-on`, `option redispatch`, `maxconn`, `timeout queue`, Runtime API, Data Plane API, Prometheus exporter) stay on Load Balancing and Proxies, which links to Resilience Patterns three times.
* Two `#### Rate limiting`-era opinion sentences ("Rate limiters are pretty dumb", "You should not enable circuit breaking between your application and end users") are stated neutrally on Resilience Patterns (the second as "The usual placement is between backend services; at the edge an open breaker turns one slow page into a blank one for everyone"). Neither page has an `> Own view:` block; the source page had none in HEAD.

## (e) Inbound links changed

* None needed. The only inbound link, `fundamentals/platform/Kubernetes.md:91` → `Load%20Balancing%20and%20Proxies.md`, points at the unchanged filename. Grep for `Scalability.md`, `Nginx.md`, `Haproxy.md` and the old anchors (`#haproxy`, `#nginx`, `#rate-limiting`, `#circuit-breaker`) across `fundamentals cloud practice` returned nothing.
* One outbound link on Resilience Patterns was changed on disk by another Phase 4 agent while I worked: `../messaging/Asynchronous%20Messaging.md` became `../messaging/Messaging%20Fundamentals.md#coupling` after that page was renamed. I verified the target file and its `## Coupling` heading exist and kept the change.

Outbound links from the two pages (all verified to exist): `Kubernetes.md`, `Observability.md`, `Resilience%20Patterns.md`, `Load%20Balancing%20and%20Proxies.md`, `../networking/TLS%20Certificates.md`, `../security/Web%20Application%20Risks.md`, `../messaging/Messaging%20Fundamentals.md#coupling`.

**Suggested link changes for pages I did not edit (owners of those pages to apply):**

1. `fundamentals/messaging/Service Orientation.md`, Service Discovery section, last paragraph. Current sentence: "Service meshes such as **Istio** and **Linkerd** sit on top of discovery and add routing, retries, mutual TLS and telemetry between services." Suggested: "... add routing, retries, mutual TLS and telemetry between services ([Resilience Patterns](../platform/Resilience%20Patterns.md))."
2. `fundamentals/platform/Kubernetes.md`, "Service mesh and serverless" section: "A service mesh moves mutual TLS, retries, timeouts and request telemetry out of application code into the platform" would take the same link `(Resilience%20Patterns.md)`.
3. `fundamentals/security/Web Application Risks.md`, `#### ModSecurity WAF`: still describes ModSecurity for NGINX as current and links the nginx.com compile guide. Load Balancing and Proxies now states the F5 module's March 2024 EOL and points readers to this page for WAF options, so the section should say the same (OWASP now maintains ModSecurity and the CRS; Coraza and NGINX App Protect are current alternatives). Also the `nginx-dos-protection.jpg` embed there is on the Phase 5 delete list.
4. `fundamentals/platform/Observability.md`: Load Balancing and Proxies links it for scraping the HAProxy Prometheus endpoint; no change required, but a one-line mention of HAProxy stats / nginx `stub_status` as sources would close the loop.

## (f) Diagrams for Phase 5 to draw, tables built

Diagrams (as `.drawio.svg`):
* `layer4-vs-layer7-proxy.drawio.svg`: client, proxy, server; two TCP connections through the proxy; L4 copies bytes and routes on port, L7 parses HTTP and routes on host and path. Embed under "Layer 4 or layer 7".
* `event-loop-vs-prefork.drawio.svg`: nginx master with N workers each holding thousands of connections versus Apache prefork with one process per connection. Embed under "Nginx".
* `circuit-breaker-states.drawio.svg`: closed, open, half-open with the transitions labelled (threshold, cool-off, probe success or failure). Embed under "Circuit breakers".
* `resilience-pattern-placement.drawio.svg` (optional): client library, sidecar, proxy along one request path, with the retry multiplication (3 x 3 x 3) called out. The placement table already covers this; draw only if the table is felt to be too dense.

Tables built in this pass (not counted in prose):
* "Nginx and HAProxy side by side" (9 rows) on Load Balancing and Proxies.
* "Where each pattern sits" (7 rows, 3 placements) on Resilience Patterns.

Image embeds removed: none; the source page had no embeds.

## (g) Open questions for the owner

1. `audit/file-triage.md` row 52 routes the generic RTO/RPO part of DR and Business Continuity to "Platform / Resilience Patterns". That page now answers "how does a system keep working when a dependency is slow or down", which is not disaster recovery. Recommend RTO/RPO stays in `cloud/aws/Disaster Recovery.md` or gets its own short page rather than being appended here.
2. Two sentences from the old HAProxy section read as opinion and may be yours: "Rate limiters are pretty dumb" and "You should not enable circuit breaking between your application and end users". Both are stated neutrally on Resilience Patterns. If either is your stance, it can become an `> Own view:` block.
3. "Beyond performance, choose the server your team already knows" (from the old Nginx and Apache section) is kept as a plain sentence. Same offer.
4. Nginx Plus is named in one sentence and one table column. If the wiki should avoid commercial products entirely, that sentence can go; the table row "Active health checks: Plus only" is the one place the distinction carries a real fact.
5. The HAProxy config snippets carry the `haproxy` fence language. If the repo's fence-language sweep (Phase 5) standardises on `text` for non-code configs, change both.
6. Vendor benchmark line ("treat them as contested marketing") could be dropped entirely rather than labelled; I kept it because the brief offered either.
