
# Web application security

Securing web applications is not a single pronged approach. The **Defence in depth** strategy allows multiple layers of security that focus on delaying the attack rather than completely preventing it often compared to a **castle** with multiple walls of protection. The more layers of defence you have, the attack will lose momentum and you’ll have more time to respond appropriately. A Defence in Depth strategy is designed to increase the cost and effort of an attack against an organisation.

## Security requirements

We often have well defined tools and techniques for gathering functional requirements of a system. e.g. user stories, acceptance criteria, definition of done within a BDD approach.

But we do not see the same level of maturity amongst teams when it comes to gathering non functional requirements, especially around security:

* Deep technical knowledge maybe required
* Do not always have a security expert on board
* Business may not be aware of the security cost to revenue and unwilling to invest time and resource.
* Do you fix a system that is up and running but with certain vulnerabilities? What is the organisation's appetite for risk? You can never be 100% secure. The question worth asking is, does the business understand the risk of letting the system run with vulnerabilities?

## Security testing

In order to understand and address your security requirements it is worth understanding the approaches and tools at hand. The security testing process involves:

* assessment - analysis and discovery of vulnerabilities without attempting to actually exploit those vulnerabilities
* testing - discovery and attempted exploitation of vulnerabilities

[Security testing classification](https://www.zaproxy.org/getting-started/) is often done according to either the type of vulnerability being tested or the type of testing being done:

* Vulnerability assessment – The system is scanned and analyzed for security issues.
* Penetration testing – The system undergoes analysis and attack from simulated malicious attackers.  It has the advantage of being more accurate because it has fewer false positives (results that report a vulnerability that isn’t actually present), but can be time-consuming to run. **Automated pentesting** part of CI validation can help uncover new vulnerabilities as well as regressions for previous vulnerabilities in an environment which quickly changes.
* Runtime testing – The system undergoes analysis and security testing from an end-user.
* Code review – The system code undergoes a detailed review and analysis looking specifically for security vulnerabilities

Dynamic application security testing (DAST) is an application security test run to find vulnerabilities in web applications while they are running (black box testing) while Static application security testing (SAST) is a white box testing method which can involve code reviews.

Crowd security testing platforms like https://www.openbugbounty.org allow security researchers to report a vulnerability on any website and submit it to Open Bug Bounty for responsible disclosure. The role of Open Bug Bounty is limited to independent verification of the submitted vulnerabilities and proper notification of website owners. Once notified, the website owner and the researcher are in direct contact to remediate the vulnerability and coordinate its disclosure.

### Web application security scanners

A web application security scanner acts as a *"man in the middle proxy"* and typically sits between the tester's browser and the web application so that it can intercept and inspect messages sent between browser and web application, modify the contents if needed, and then forward those packets on to the destination.

* [BURP Scanner](https://portswigger.net/burp) - One of the best manual penetration testing tools out there, however a [comparison with Netsparker](https://www.netsparker.com/vulnerability-scanner-comparison/netsparker-vs-burp-suite/#) reveals it can be complicated to configure and relatively less focussed on automation and integration with other tools.
* [Netsparker](https://www.netsparker.com/)
* [OWASP ZAP](https://www.zaproxy.org/) - Free and open source, can run headless as a daemon with a REST API to do nearly everything that is possible via the desktop interface.
* [Qualys web app scanning](https://www.qualys.com/apps/web-app-scanning/?_ga=2.142204082.1235140357.1591144958-1421731482.1591144958) - cloud based web app discovery and detection of vulnerabilities and misconfigurations

You can use your existing website or **test websites** to perform security testing against e.g.

* Goolge's firing range - https://github.com/google/firing-range
* OWASP juice shop - https://github.com/bkimminich/juice-shop
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

## Resources

* [Web Security Concepts](https://docs.oracle.com/middleware/1212/owsm/OWSMC/owsm-security-concepts.htm#OWSMC116)
* [OWASP Top 10](https://www.owasp.org/index.php/OWASP_Top_Ten_Cheat_Sheet) provides list of the 10 Most Critical Web Application Security Risks
* [OWASP Dependency Check](https://www.owasp.org/index.php/OWASP_Dependency_Check) is a utility that identifies project dependencies and checks if there are any known, publicly disclosed, vulnerabilities
* [Observatory](https://observatory.mozilla.org/) from mozilla allows free basic website scanning for security flaws
* [National Vulnerability Database](https://nvd.nist.gov/)
* [Application Security Verification Standard](https://www.owasp.org/index.php/Category:OWASP_Application_Security_Verification_Standard_Project)
* [CIS Security Benchmarks (AWS)](https://github.com/awslabs/aws-security-benchmark)
