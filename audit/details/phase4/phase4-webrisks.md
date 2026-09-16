# Phase 4 report: fundamentals/security/Web Application Risks.md

File edited: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Web Application Risks.md` (TRIM, one page). No other file touched. Not committed.

## (a) Question the page answers

What goes wrong in web applications, how does each attack work, and what stops it? Sections: security requirements and gates to guardrails (short), security theatre, the four testing categories in one paragraph, selected OWASP Top 10:2021 risks with the owner's examples and a 2025 delta, WAF and DDoS as layered concepts, what the browser does and does not protect, rederive bullets, Sources.

## (b) Prose word counts (code fences and table rows excluded)

| | Before | After |
|---|---|---|
| Web Application Risks | 2,756 | 1,979 |

Target was 1,600 to 2,000.

## (c) What was cut and why

Vendor and tooling catalogue (largest cut):
- The SAST section's four selection criteria (CI vs SaaS vs on-prem, Jira integration, language support) and the eight-product list (SonarQube, Checkmarx cx-flow, Snyk Code / Semgrep, Veracode, Coverity, Gitleaks / TruffleHog, Checkov, Semmle). Replaced by one paragraph defining SAST, DAST, IAST, SCA and pentest with one example each: CodeQL (the audit's Semmle fix), OWASP ZAP, OWASP Dependency-Check, Burp Suite. Coverity, Netsparker, Qualys, Intruder, Snyk, mend.io are not named at all, which removes the Synopsys / Black Duck and Netsparker / Invicti staleness rather than updating it.
- OpenVAS removed from DAST (audit: it is a network and host scanner).
- Burp vs Netsparker comparison and the "less focussed on automation" claim (stale per audit).
- The ZAP baseline scan and GitHub Actions link; kept as "can run headless in CI".

Duplicated supply chain material:
- SBOM paragraph, SLSA / in-toto / SSDF links and the four-step SBOM pipeline. Already covered in Supply Chain and Container Security; replaced with a link. The SolarWinds and Log4Shell narratives stay here because that page says "Both are described under Web Application Risks".
- Uncited "Accenture & WEF" line (audit row 61) dropped rather than sourced.

Marketing and stale product detail:
- "used by over a million sites" (ModSecurity).
- Trustwave commercial rule set, "ModSecurity 3.0 runs natively in NGINX", nginx compile guide and HAProxy trial links. Replaced with the OWASP custodianship, Trustwave's 2024 end of support, F5 NGINX ModSecurity WAF EOL, and Coraza.
- `nginx-dos-protection.jpg` embed removed (vendor graphic); replaced by the one sentence "DDoS filtering sits in front of the WAF, which sits in front of the application".
- NTP amplification paragraph shortened; the pasted Cloudflare wording rewritten; one line added on current reflectors (open DNS, Memcached).

Off-topic sublist:
- The API authentication bullet list (IP ACLs, mTLS, Basic, API key, JWT) and the Oracle OWSM link collapsed to one sentence (audit row 90-98: different topic).

Browser section:
- "Chrome shows a yellow triangle over the padlock" replaced: padlock removed in 2023, mixed content upgraded or blocked. observatory.mozilla.org renamed MDN HTTP Observatory with the current URL.

Learning resources:
- Firing range, Juice Shop, Hack yourself first and Open Bug Bounty moved to a single Sources entry; the Open Bug Bounty process description cut.

Corrections applied inside kept text:
- H1 now equals filename (`Web Application Risks`), leading blank line removed.
- OWASP Top 10 version named (2021), all ten 2021 categories listed in one line, section retitled "Selected risks", old wiki cheat-sheet URL replaced by owasp.org/Top10. Three-line 2025 delta added (Software Supply Chain Failures and Mishandling of Exceptional Conditions added; SSRF folded into Broken Access Control).
- Python: `os.system(f"{cmd} {user_input}")` (SyntaxError fixed), `input` renamed to avoid shadowing the builtin, `subprocess.run([cmd, user_input])`, comment now says the list form avoids the shell so no escaping happens, output lines `#`-prefixed. Added one sentence that parameterised SQL is the same idea.
- Log4Shell payloads now `${jndi:ldap://...}` with the opening brace; hostnames changed to `evil.example`. One version-free sentence on the fix (message lookups removed, JNDI off by default).
- SolarWinds: about 18,000 downloaded the trojanised update, roughly 100 actively targeted; the "30,000 affected" claim removed.
- British spelling throughout (defence, theatre, organisation, authorisation, honours). No em or en dashes.
- A short "Broken access control" paragraph added (the original had one line), since it is the number one risk and the brief's question is "how does each attack work".

## (d) What was moved where

Nothing moved to another page. Within the page: learning resources into `## Sources`; OWASP ModSecurity, CRS and Coraza links into Sources. Supply chain depth is linked to `Supply Chain and Container Security.md` rather than repeated.

## (e) Inbound links

Checked with `grep -rn "Web Application Risks|Web%20Application%20Risks|Web Application Security" fundamentals cloud practice README.md`.

- `fundamentals/security/Supply Chain and Container Security.md:9` links the page without an anchor. No change needed.
- `cloud/aws/README.md:144` links `Web%20Application%20Risks.md#ddos-protection`. The heading is now `## DDoS protection` (promoted from H4 under Layer 7, since SYN flood and NTP amplification are layers 3 and 4), which still slugs to `ddos-protection`. No change needed; anchor preserved deliberately.
- Outbound links added from this page (all targets verified to exist): Cross Site Scripting, Cross Site Request Forgery, Browser Security Model, Security Headers, Supply Chain and Container Security.

No links changed in other files. `git status` at hand-off shows other pages modified by parallel Phase 4 agents; this assignment touched only `fundamentals/security/Web Application Risks.md`.

## (f) Diagrams for Phase 5 and tables

- `layered-web-protection.drawio.svg`: DDoS filter (network edge) in front of WAF in front of application, with the browser as a fourth wall on the client side. Replaces the deleted `nginx-dos-protection.jpg`, which can now be removed from `images/` (it is no longer referenced anywhere).
- `syn-flood.drawio.svg`: TCP three way handshake next to the attacker's SYN with no ACK and the server's half open connection table filling up. Optional; the bullet is short enough to stand alone.
- Possible table (Phase 5, not built here): the five testing categories with columns "what it looks at", "needs source?", "runs against live app?", "typical tool". The paragraph form is within budget so I left it as prose.

## (g) Open questions for the owner

1. `audit/details/security.md` (Cloud Security row 68) says SQLMap should move to this page. I did not name it because the brief allowed at most one example per category and the page is at budget. Add one clause under Injection ("sqlmap automates finding SQL injection") if wanted.
2. The original had a bare "Broken Access Control" one-liner. I added four sentences on how the attack works and what stops it, in plain words, because the page's question needs it. Please check the wording is yours.
3. The 2025 delta names only the three changes the brief asked for and says so ("Three changes ... matter here"); Security Misconfiguration moving to #2 and the A07 rename to Authentication Failures are not mentioned.
4. The security theatre paragraph keeps the owner's neutral "Be aware of security theatre" plus the Stack Exchange link; I did not characterise what the link says.
5. Cryptographic Failures, Security Misconfiguration and the other 2021 categories are listed but not explained. If the page should cover them, it needs either a split or an appendix page; it is at 1,979 words now.
6. `images/nginx-dos-protection.jpg` is now orphaned. Delete in Phase 5.
