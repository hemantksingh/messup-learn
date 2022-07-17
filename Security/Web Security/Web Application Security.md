
# Web application security

Securing web applications is not a single pronged approach. The **Defence in depth** strategy allows multiple layers of security that focus on delaying the attack rather than completely preventing it often compared to a **castle** with multiple walls of protection. The more layers of defence you have, the attack will lose momentum and you’ll have more time to respond appropriately. A Defence in Depth strategy is designed to increase the cost and effort of an attack against an organisation.

## Security requirements

We often have well defined tools and techniques for gathering functional requirements of a system. e.g. user stories, acceptance criteria, definition of done within a BDD approach. But we do not see the same level of maturity amongst teams when it comes to gathering non functional requirements, especially those related to security. This could be due to a number of factors:

* Deep technical knowledge maybe required
* Do not always have a security expert on board
* Stakeholders may not be aware of the security cost to revenue and unwilling to invest time and resource. You can never be 100% secure but it is worth thinking about what good looks like from a security point of view
  * How urgently do you fix a vulnerability identified in a production system? 
  * Do you understand the risk of letting the system run with vulnerabilities? 
  * What is the organisation's appetite for risk? What kind of data are you dealing with? e.g, finance, healthcare or provider of publically avaialble traffic data
  * Is certain amount of downtime acceptable to you?

### Gates to guardrails

Traditional approaches to secure development lifecycles have relied on high-touch and process-driven models involving a series of assessments (e.g. design review, threat model, vuln scan) and associated decisions on whether to proceed to the next phase and gate. While this model serves many well, there are an increasing number of organizations embracing concepts like DevOps, agile, cloud, and continuous delivery that are looking for more pragmatic, automated, and dynamic approaches that suit the technology and business environments in which they exist. Tension between SecOps, DevOps and application developers can lead to disjointed teams. How do you apply consistent security policies across multiple architectures?

Moving [from gates to guardrails](https://www.oreilly.com/library/view/devopssec/9781491971413/ch04.html) involves providing guidance and tooling to development teams to insert security policies into thier delivery pipelines rather than introducing delays via security compliance gates. Some of the [ways Netflix has approached this shift](https://www.youtube.com/watch?v=geumLjxtc54), emphasizing practical methods to problems ranging from continuous assessment to regulatory compliance to team staffing.

Data between the end user and your application flows through the data plane. Thinking of security as a horizontal capability across the data plane and use the metrics and telemetry from the data plane to get visibility of the applied security policies and application threats.

## Security testing

In order to understand and address your security requirements it is worth understanding the approaches and tools at hand. The security testing process involves:

* assessment - analysis and discovery of vulnerabilities without attempting to actually exploit those vulnerabilities
* testing - discovery and attempted exploitation of vulnerabilities

[Security testing methodologies](https://www.zaproxy.org/getting-started/) include:

* Vulnerability assessment – The system is scanned and analyzed for security issues.
* Penetration testing – The system undergoes analysis and attack from simulated malicious attackers.  It has the advantage of being more accurate because it has fewer false positives (results that report a vulnerability that isn’t actually present), but can be time-consuming to run. **Automated pentesting** part of CI validation can help uncover new vulnerabilities as well as regressions for previous vulnerabilities in an environment which quickly changes.
* Code review – The system source code undergoes a detailed review and analysis looking specifically for security vulnerabilities. This is also known as Static application security testing (SAST) or white box testing method. Some examples of static code analysis tools:
  * SonarQube
  * Coverity from Synopsis
* Software Composition Analysis - Rather than analysisng source code an SCA tool discovers all software components including their supporting libraries as well as all direct and indirect dependencies
  * Black Duck - https://www.synopsys.com/software-integrity/security-testing/software-composition-analysis.html
  * WhiteSource - https://www.whitesourcesoftware.com/resources/blog/software-composition-analysis/
* Runtime testing – The system undergoes analysis to discover security vulnerabilities while its running e.g. looking at the request and responses to the system. This is also known as Dynamic application security testing (DAST) or black box testing.

Crowd security testing platforms like https://www.openbugbounty.org allow security researchers to report a vulnerability on any website and submit it to Open Bug Bounty for responsible disclosure. The role of Open Bug Bounty is limited to independent verification of the submitted vulnerabilities and proper notification of website owners. Once notified, the website owner and the researcher are in direct contact to remediate the vulnerability and coordinate its disclosure.

### Web application security scanners

With the increasing number of web application security breaches, it is essential to keep your web application secure at all times. A web application security scanner acts as a *"man in the middle proxy"* and typically sits between the tester's browser and the web application so that it can intercept and inspect messages sent between browser and web application, modify the contents if needed, and then forward those packets on to the destination.

* [OWASP ZAP](https://www.zaproxy.org/) - Free and open source, can run headless as a daemon with a REST API. ZAP provides a [baseline scan feature](https://www.zaproxy.org/blog/2020-04-09-automate-security-testing-with-zap-and-github-actions/) to find common security faults in a web application without doing any active attacks. The scan can be integrated into your CI/CD pipelines using GitHub Actions.
* [Open VAS](https://www.openvas.org/) - Open Vulnerability Assessment Scanner 
* [BURP Scanner](https://portswigger.net/burp) - One of the best manual penetration testing tools out there, however a [comparison with Netsparker](https://www.netsparker.com/vulnerability-scanner-comparison/netsparker-vs-burp-suite/#) reveals it can be complicated to configure and relatively less focussed on automation and integration with other tools.
* [Netsparker](https://www.netsparker.com/)
* [Qualys web app scanning](https://www.qualys.com/apps/web-app-scanning/?_ga=2.142204082.1235140357.1591144958-1421731482.1591144958) - cloud based web app discovery and detection of vulnerabilities and misconfigurations
* [Intruder](https://www.intruder.io) - SaaS based vulnerability scanner, provides [comparisons with other solutions](https://www.intruder.io/qualys-alternative)  

You can use your existing website or **test websites** to perform security testing against e.g.

* Goolge's firing range - https://github.com/google/firing-range
* OWASP juice shop
    * https://owasp.org/www-project-juice-shop
    * https://github.com/bkimminich/juice-shop
* Hack yourself fist - https://www.troyhunt.com/hack-yourself-first-how-to-go-on/ is a great place to start actively seeking out vulnerabilities

### Protection offered by the browser

* Maintains a comprehensive list of phishing sites, warn the user against visiting such sites

* Check validity of SSL certificate.

* Detect weak cryptography, deficiency in the TLS (Transport layer security) or its predecessor SSL (Secure Sockets Layer) implementation.

* Detect pages with mixed content - A page served over https that also has content served over http. Chrome shows a yellow triangle over the padlock to warn the user.

* Apply [Security headers](./Security%20Headers.md)

### Protection not offered by the browser

* Parameter tampering (cookies, forms, headers, strings). Modifying attributes of the request (query string, changing ids).
* Persistent cross site scripting.
* Attackers making direct HTTP requests (access to unauthorised resources, deleting a resource).

These types of attempts can only be effective if the attacker is able to exploit an existing vulnerability, like a non secure API, SQL injection or gaining access to credentials.

## API Authentication Methods

* Protect APIs from unauthorized access with authentication
* [IP address-based ACLs](https://joelgsamuel.medium.com/ip-address-access-control-lists-are-not-as-great-as-you-think-they-are-4176b7d68f20) - may not be the most secure
* Mutual TLS
* HTTP Basic authentication
* API Specific authentication
  * API Key - shared secret
  * JSON Web Token (JWT)

## Resources

* [OWASP Top 10](https://www.owasp.org/index.php/OWASP_Top_Ten_Cheat_Sheet) provides list of the 10 Most Critical Web Application Security Risks
* [OWASP Dependency Check](https://www.owasp.org/index.php/OWASP_Dependency_Check) is a utility that identifies project dependencies and checks if there are any known, publicly disclosed, vulnerabilities
* API security - https://docs.oracle.com/middleware/1212/owsm/OWSMC/owsm-security-concepts.htm. Although specific to SOAP based web services but the concepts listed in the docs are still relevant to API security
* [Observatory](https://observatory.mozilla.org/) from mozilla allows free basic website scanning for security flaws
* National Vulnerability Database - https://nvd.nist.gov/
* [Application Security Verification Standard](https://www.owasp.org/index.php/Category:OWASP_Application_Security_Verification_Standard_Project) provides a basis for designing, building, and testing technical application security controls
* CIS Security Benachmarks - https://www.cisecurity.org/cis-benchmarks/