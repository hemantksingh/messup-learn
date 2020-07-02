
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

* [Security headers](https://zinoui.com/blog/security-http-headers#referrer-policy) - The core issue exploited by XSS attacks is the browser’s inability to distinguish between script that’s intended to be part of your application, and script that’s been maliciously injected by a third-party. Browsers can block script execution based on the following HTTP headers returned by the server.

  * **X-XSS-Protection** is a HTTP response header understood by new browsers. This header lets domains toggle on and off reflective XSS prevention of the browser.

    ```sh
    X-XSS-Protection: 0 # disable XSS protection
    X-XSS-Protection: 1; # enables XSS protection
    X-XSS-Protection: 1; mode=block # rather than sanitize the page, when a XSS attack is detected, the browser will prevent rendering of the page
    X-XSS-Protection: 1; report=<reporting-uri> # If a cross-site scripting attack is detected, the browser will sanitize the page and report the violation
    ```

  * **Content-Security-Policy** HTTP header allows you to create a **whitelist of sources** of trusted content, and instructs the browser to only execute or render resources from those sources. Even if an attacker can find a hole through which to inject script, the script won’t match the whitelist, and therefore won’t be executed. You can define a policy that only allows script to execute when it comes from one of the two trusted sources: your self and google
    `Content-Security-Policy: script-src 'self' https://apis.google.com`

  * **HTTP Strict Transport Security** Instructs the browser to visit your site only over HTTPS to ensure they only use TLS to support secure transport. It protects
    * users against passive eavesdropper and active **man in the middle attacks** If your login page page is served over http but the login form posts to https, is it secure? Not really. You cannot have confidence that the login form that has been served over http hasn't been modified by a man in the middle by the time it gets to the end user. Your traffic could still be intercepted before and after HTTPS connection begins and ends.
    * mixed content and click-through certificate overrides
    * against web server mistakes like loading JavaScript over an insecure connection
    
    ```sh
    Strict-Transport-Security: max-age=31536000 # HSTS policy is applied only to the domain of HSTS host issuing it and remains in effect for one year
    Strict-Transport-Security: max-age=31536000; includeSubDomains # HSTS policy is applied to the domain of the issuing host as well as its subdomains and remains in effect for one year.
    Strict-Transport-Security: max-age=0 #Directs the browser to delete the entire HSTS policy
    ```
    
    Because HSTS provides protection against a wide array of attacks, is supported widely by browsers, and can be configured with a one-line setting, it is strongly recommended for all internet-facing web applications.

  * **X-Frame-Options (obsolete)** HTTP response header that can be used to indicate whether or not a browser should be allowed to render a page in a `<frame>`, `<iframe>`, `<embed>`  or `<object>`. Sites can use this to avoid [click-jacking](https://developer.mozilla.org/en-US/docs/Web/Security/Types_of_attacks#Click-jacking) attacks, by ensuring that their content is not embedded into other sites.  While the `X-Frame-Options` header is supported by the major browsers, it was never standardized and has been deprecated in favour of the `frame-ancestors` directive from `Content-Security-Policy` HTTP header.

* Same Origin Policy - One of the key principles of security is isolation. Same origin policy is designed for segregating web content. Under this policy the web browser only allows Javascript in one web page to access data in another web page if the two pages have the same origin. An **Origin** is [defined as](https://en.wikipedia.org/wiki/Same-origin_policy) a combination of the **protocol**, **domain name**, and **port**.

#### Cross domain vulnerability

The same origin policy prevents a malicious script on one page from obtaining access to sensitive data on another web page through that page's DOM. Code from `https://mybank.com` should only have access to `https://mybank.com`'s data, and `https://evil.example.com` should certainly never be allowed access. This keeps a strong separation of content of unrelated sites.

It is important to note that the **same origin policy applies only to scripts**. This means that resources such as images, CSS, and dynamically-loaded scripts can be accessed across origins via the corresponding HTML tags (with fonts being a notable exception). Attacks take advantage of the fact that the same origin policy does not apply to HTML tags.

#### Relaxing the same origin policy

Depending upon whether the target service allows cross-origin requests the [browser can deny such requests](https://stackoverflow.com/questions/20035101/why-doesn-t-postman-get-a-no-access-control-allow-origin-header-is-present-on). However, for large websites with multiple subdomains or when your API needs to be called by multiple web clients other than just the one hosted on the same server (origin) as your API, you need to relax the same origin policy.

**Cross Origin Resource Sharing (CORS)** - Rather than deny cross-origin request, the browser asks the target service if it wants to allow a specific cross-origin request. The target service tells the browser whether it wants to allow cross-origin requests by inserting special HTTP headers in responses: For [using CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) it extends HTTP with a new `Origin` request header and a new `Access-Control-Allow-Origin` response header. It allows servers to use a header to explicitly list origins that may request a file or to use a wildcard and allow a file to be requested by any site.

```sh
Access-Control-Allow-Origin: * # resource can be shared by any domain

Access-Control-Allow-Origin: https://foo.example # no domain other than https://foo.example can access the resource in a cross-site manner

Access-Control-Allow-Methods: POST, GET, OPTIONS # POST and GET are viable methods to query the resource in question
Access-Control-Allow-Headers: X-PINGOTHER, Content-Type # permitted headers to be used with the actual request
Access-Control-Max-Age: 86400 # how long the response to the preflight request can be cached for without sending another preflight request
```

#### CSP and CORS

Content security policy and same-origin policy (the lack of CORS) act as multiple lines of defense in protecting against malicious content. e.g. if `foo.com` wants to send a request to `bar.com`

1. When user visits `foo.com` in browser, `foo.com` server returns `foo.com` HTTP response, CSP restriction within this response can prevent `foo.com` in browser from issuing request to `bar.com`.
2. If there is no CSP restriction within `foo.com` HTTP response, then `foo.com` in browser can send a request to `bar.com`.
3. Upon receiving the request, `bar.com` server responds with `bar.com` HTTP response, CORS restriction within this response can prevent `foo.com` in browser from loading it. (Note that by default, Same-origin policy will restrict the response from loading, unless otherwise specified by CORS)

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
