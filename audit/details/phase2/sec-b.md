# Phase 2 report: security batch B (2026-09-16)

Files edited (nothing committed, no other file touched):
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Cross Site Request Forgery.md
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Cross Site Scripting.md
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Security Headers.md
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/networking/TLS Certificates.md

Rules applied consistently: High/Medium WRONG, STALE, INCONSISTENT, BROKEN fixed from the audit's suggested fix. OPINION rows fixed only where the audit names the real source (Scott Helme anecdote, OWASP CSRF sentence, ASP.NET-specific token text); unsourced Medium OPINION rows were skipped and are listed below. Low rows: only trivial typo or duplicate-fragment deletions. CLASSIFY moves skipped. New fences use `http`, `html` or `text`; pre-existing `sh` fences left alone. No web verification was needed; every High replacement fact matched the audit's already-verified rows or is a well-established version/date.

## Cross Site Request Forgery.md

- was: "**AuthCookie** keeps a user authenticated ... The Cookie is sent automatically ... This makes the server treat it as an authenticated request." (three-sentence cookie explainer, duplicate of the cookies note) → now: one sentence ("The browser attaches the session cookie automatically to every request that matches its domain and path, so the server treats the forged request as authenticated") plus a relative link to `./Browser%20Security%20Model.md`. This also removes the non-standard term "AuthCookie".
- was: "The token is generated as a pair with the session token ... They are a cryptographic pair ... The only way an attacker can set both ... is if they perform a XSS attack ... once you are authenticated the cookie gets keyed to your username ... identity comes from the **AuthCookie**" (ASP.NET-specific, stated as universal) → now: describes the synchronizer token (server-side store) and double-submit cookie patterns, notes that naive double-submit is defeated by cookie tossing from a sibling subdomain without XSS, and that OWASP recommends the signed (HMAC over session id) double-submit cookie. The ASP.NET "keyed to your username" text was dropped rather than attributed.
- was: "an XSS payload can simply read any page on the site" → now: "any same-origin page".
- was: "This technique is exactly how the MySpace (Samy) worm defeated MySpace's anti CSRF defenses in 2005 ..." (unattributed OWASP text) → now: quoted and attributed to the OWASP CSRF Prevention cheat sheet, linking the current cheatsheetseries.owasp.org URL.
- added: "## SameSite and other defences" (one paragraph): Chromium defaults missing SameSite to Lax since Chrome 80 (Feb 2020) with the two-minute Lax+POST exception; Firefox and Safari do not default to Lax; SameSite=None requires Secure; Lax does not stop top-level GET navigations or same-site subdomains; Sec-Fetch-Site checks; OWASP keeps tokens primary, SameSite and Fetch Metadata as defence in depth.

## Cross Site Scripting.md

- was: "Always validate un-trusted data i.e. all input fields. XSS vulnerabilities come from a lack of data escaping user inputs." → now: leads with context-aware output encoding at render time as the primary defence; input validation stated as defence in depth that cannot be relied on alone.
- was: fence tagged `javascript`, comment "equivalent unicode escaped form" → now: fence `text`, comment "equivalent HTML entity encoded form".
- was: `<IMG SRC="javascript.alert('XSS');">` in a `javascript` fence (typo, dead payload) → now: `<img src=x onerror=alert(1)>` in an `html` fence; prose changed to "an IMG tag with an event handler".
- was: HttpOnly bullet with no cross-reference → now: same bullet plus "Cookie attributes are covered in [Browser Security Model](./Browser%20Security%20Model.md)".
- was: "Even DNS records can be infected by XSS attacks." → now: "Any untrusted data source rendered into HTML, including DNS TXT records or log lines, can carry an XSS payload."
- added: a six-line "Other mitigations" sub-list under the existing "Preventing XSS attacks" heading: strict CSP with nonces/hashes and 'strict-dynamic' (linked to Security Headers), Trusted Types, framework auto-escaping, DOMPurify, and X-XSS-Protection deprecated (set 0 or omit, linked to Security Headers "Deprecated").

## Security Headers.md

- was: "having `X-Frame-Options` set to Blocked" → now: "set to `DENY`".
- was: example `default-src 'self' https://apis.google.com; object-src 'none'` described as only allowing script → now: `script-src 'self' https://apis.google.com; object-src 'none'` (prose unchanged).
- added: paragraph that host allowlists are weak (JSONP/script gadgets) and a strict CSP example in an `http` fence: `script-src 'nonce-r4nd0m' 'strict-dynamic'; object-src 'none'; base-uri 'none'`.
- was: "CSP can block `inline-eval` in your javascript or Node-js module dependencies without the usual console or on-screen errors." → now: eval() and inline scripts are blocked unless 'unsafe-eval'/'unsafe-inline' (or a nonce or hash) is allowed; violations are logged in the console and can be sent to a `report-to` endpoint.
- added (HSTS): one paragraph on the `preload` directive and hstspreload.org (max-age at least one year, includeSubDomains; preload, removal takes months).
- was: `### X-Frame-Options` nested under HSTS → now: `## X-Frame-Options` (position unchanged).
- was: `X-Frame-Options: SAMEORIGIN` and `X-Frame-Options: ALLOW-FROM https://example.com/` → now: `DENY` and `SAMEORIGIN` only, plus a sentence that ALLOW-FROM was IE/old Firefox only (removed Firefox 70, 2019), never worked in Chrome or Safari, and is obsolete.
- was: "it was never standardized and has been deprecated in favour of the `frame-ancestors` directive" → now: "it was only standardised informationally (RFC 7034, 2013) and is obsoleted by the `frame-ancestors` directive".
- was: "I know that 4,000 users came from Twitter this week because when they visit my site they set the referrer[sic] header in their request." (Scott Helme first-person anecdote in the owner's voice) → now: sentence removed; the link to Helme's post stays.
- added (Referrer Policy): `http` fence listing no-referrer, same-origin, strict-origin, strict-origin-when-cross-origin, no-referrer-when-downgrade, unsafe-url, and a sentence that browsers default to strict-origin-when-cross-origin (Chrome 85, Firefox 87, 2020 to 2021; Safari the same).
- was: `## Cross-Origin-Resource-Policy` heading over SOP/CORS text → now: `## Same-Origin Policy and CORS` (content kept in place, per the phase rule).
- was: standalone `Cross-Origin-Resource-Policy: same-origin` line under the SOP paragraph → now: removed (CORP is not an SOP mechanism).
- was: "the **same origin policy applies only to scripts** ... images, CSS, and dynamically-loaded scripts can be accessed across origins" → now: SOP restricts reading cross-origin responses, not embedding them; embedded resources are opaque (script source unreadable, image not readable via canvas); CSRF exploits that embedded requests still carry cookies.
- was: "By setting the `Cross-Origin-Resource-Policy: cross-origin` in the response the target service tells the browser that it wants to allow cross-origin requests. For using CORS it extends HTTP ..." → now: "This is what CORS is for. It extends HTTP with ... `Access-Control-Allow-Origin`; by returning that header the target service tells the browser which origins may read the response."
- was: "CORS restriction within this response can prevent `foo.com` in browser from loading it. (Note that by default, Same-origin policy will restrict ...)" → now: "The same-origin policy stops `foo.com` in the browser from reading it unless the response carries CORS headers (`Access-Control-Allow-Origin`) that permit `foo.com`."
- was: "**Cross-origin isolation** is a new security feature (as of April 2021)" → now: "shipped in browsers in 2020 to 2021 (Chrome 88, Firefox 79)".
- was: "If CORP not set explicitly, browsers default to `cross-origin` ... For security purposes, the browser default should be same-origin, That shift is going to take some time ..." (speculation) → now: a two-sentence CORP definition (resource owner controls which origins may embed via no-cors requests; values same-origin, same-site, cross-origin with cross-origin the default; does not grant reads, that is CORS; Spectre defence), an `http` example, and a rewritten COEP sentence adding `Cross-Origin-Embedder-Policy: credentialless` (Chrome 96, Firefox 119).
- was: X-XSS-Protection block documenting values 0, 1, 1; mode=block, 1; report= → now: only `X-XSS-Protection: 0` with a sentence that the filter was removed from Chrome 78 (2019) and Safari 15.4, never existed in Firefox, and had side-channel bugs.

## TLS Certificates.md

- was: `# What is a Certificate?` → now: `# TLS Certificates`.
- was: "provides 1 and 2 above but is not so great at 3" → now: "provides 1 and 2 above. Point 3 used to be the weak spot; since 2015 the ACME protocol (Let's Encrypt, certbot) automates issue and renewal" with an in-page link to the new section.
- was: `-days 356 -nodes` → now: `-days 365 -nodes`.
- was: CSR with `-subj` only; signing with no extension copy → now: `-addext "subjectAltName=DNS:demo.applicant.com"` on the CSR, `-copy_extensions copy` on `openssl x509 -req` (comment notes OpenSSL 3, older versions need -extfile), and a comment that browsers ignore the CN and require a SAN (Chrome 58, 2017).
- was: `“—–BEGIN CERTIFICATE—–” and “—–END CERTIFICATE—–` (smart quotes, em/en dashes) → now: `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----` in backticks.
- was: duplicated parenthetical "(end entity certificate, intermediate certificates, root authority certificates and private key) in a single file." → now: removed; replaced with one line that OpenSSL 3 (2021) writes PKCS#12 with AES-256-CBC and PBKDF2 and legacy importers need `openssl pkcs12 -export -legacy`.
- was: "On a Linux host 'trustung' the certificate is different and distro dependent On Windows" → now: "trusting ... distro dependent. On Windows".
- was: `Import-PfxCertificate -FilePath certificate.pfx -CertLocation 'Cert:\LocalMachine\Root' -Password 'password'` → now: `-CertStoreLocation 'Cert:\LocalMachine\Root' -Password (ConvertTo-SecureString 'password' -AsPlainText -Force)`.
- was: "purchase a public domain name ... then get a publicly-trusted certificate for it" (no mention certs are free) → now: appended "The certificate itself is free from an ACME CA such as Let's Encrypt" with a link to the new section (DNS-01 detail lives there, stated once).
- was: "A thumbprint ... **identifies the public key of the certificate**. The thumbprint is almost certainly contained in the signature of the request ..." → now: thumbprint is the SHA-1/SHA-256 hash of the whole DER-encoded certificate and changes on renewal; not a hash of the public key; the SPKI hash is the separate value used for pinning. Speculative second sentence deleted.
- was: "SAN certificates are different from wildcard certificates. While wildcard certificates allow for unlimited subdomains ..., a SAN cert allows multiple domain names ..." → now: every public certificate is a SAN certificate because browsers ignore the CN; the distinction is multi-domain versus wildcard (one certificate can carry both). Original link kept.
- added: "## Validity limits and automation" (one paragraph, before the CRL section): 398-day maximum since Sep 2020; CA/B Forum SC-081v3: 200 days from 15 Mar 2026, 100 from 15 Mar 2027, 47 from 15 Mar 2029, DCV reuse to 10 days; automate with ACME (Let's Encrypt, ZeroSSL, certbot or load-balancer ACME clients), DNS-01 works for internal hosts, wildcards are free.
- added (under CRL): one paragraph on OCSP, OCSP stapling, browser aggregated lists (Chrome CRLSets, Firefox CRLite), CA/B Forum making OCSP optional in 2023, and Let's Encrypt ending OCSP in 2025 (month left unstated, as the audit marks it unverified).

## Findings deliberately skipped

- CSRF L12 and XSS L27: stale OWASP wiki links (Low STALE). Not trivial typos; left as they redirect. The new CSRF attribution links the current cheat sheet URL, so the current location is now in the file anyway.
- CSRF L5 "AuthCookie" (Low OPINION): not fixed as its own row, but the term disappeared when the duplicate cookie explainer was replaced with a link.
- XSS L5-7 DOM-based XSS definition (Medium OPINION, no source named): skipped under the OPINION rule (attribute or remove only where the finding names a real source).
- Security Headers L23 "CSP is not applicable in case of APIs" (Medium OPINION, no source named for the claim): skipped for the same reason.
- Security Headers L60 nosniff/CORB note (Low, marked optional) and L138 Permissions-Policy example (Low STALE): not typos, not in the task list, skipped.
- Security Headers whole-file CLASSIFY (move SOP/CORS to a browser-model note): skipped as instructed; section retitled only.
- Security Headers `sh` fences holding HTTP header examples: left as `sh` (they have a tag and no finding); new fences use `http`.
- TLS Certificates L47-62 DUPLICATE (move DV/OV/EV from TLS.md into this page): skipped as instructed (later phase).
- TLS Certificates old L75 em-dashes and curly apostrophes: pre-existing, no finding, left alone; no new em-dashes were introduced.
- Cookie-basics DUPLICATE row (filed under Security Cookies.md, Medium): its CSRF half was applied (see CSRF first bullet); the XSS half was applied as a link from the HttpOnly bullet; the Browser Security Model page itself is not in my assignment and was not touched.
