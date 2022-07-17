# Security Headers

OWASP has a list of HTTP [Security headers](https://owasp.org/www-project-secure-headers/#tab=Headers) that your application can use  to make it more secure. [Hardening your HTTP response headers](https://scotthelme.co.uk/hardening-your-http-response-headers/) requires adopting best practice to set these security headers as part of your response. e.g. webserver config for [IIS](https://gist.github.com/The-Scott/f7b5d03e260036cfc4dce5ad89578377) and [nginx](https://gist.github.com/plentz/6737338). Browsers can block script execution based on the following HTTP headers returned by the server.

### X-XSS-Protection

The core issue exploited by XSS attacks is the browser’s inability to distinguish between scripts that are intended to be part of your application and the ones that have been maliciously injected by a third-party. This header lets domains toggle on and off reflective XSS prevention of the browser.

    ```sh
    X-XSS-Protection: 0 # disable XSS protection
    X-XSS-Protection: 1; # enables XSS protection
    X-XSS-Protection: 1; mode=block # rather than sanitize the page, when a XSS attack is detected, the browser will prevent rendering of the page
    X-XSS-Protection: 1; report=<reporting-uri> # If a cross-site scripting attack is detected, the browser will sanitize the page and report the violation
    ```

### Content-Security-Policy

HTTP header allows you to create a **whitelist of sources** of trusted content, and instructs the browser to only execute or render resources from those sources. Even if an attacker can find a hole through which to inject script, the script won’t match the whitelist, and therefore won’t be executed. You can define a policy that only allows script to execute when it comes from one of the two trusted sources: your self and google
    `Content-Security-Policy: script-src 'self' https://apis.google.com`

*Note: CSP can block `inline-eval` in your javascript or Node-js module dependencies without the usual console or on-screen errors.*

### HTTP Strict Transport Security (HSTS)

Instructs the browser to visit your site only over HTTPS to ensure they only use TLS to support secure transport. Supported widely by browsers and strongly recommended for internet-facing web applications. It protects

* users against passive eavesdropper and active **man in the middle attacks** If your login page page is served over http but the login form posts to https, is it secure? Not really. You cannot have confidence that the login form that has been served over http hasn't been modified by a man in the middle by the time it gets to the end user. Your traffic could still be intercepted before and after HTTPS connection begins and ends.
* mixed content and click-through certificate overrides
* against web server mistakes like loading JavaScript over an insecure connection
    
    ```sh
    Strict-Transport-Security: max-age=31536000 # HSTS policy is applied only to the domain of HSTS host issuing it and remains in effect for one year
    Strict-Transport-Security: max-age=31536000; includeSubDomains # HSTS policy is applied to the domain of the issuing host as well as its subdomains and remains in effect for one year.
    Strict-Transport-Security: max-age=0 # Directs the browser to delete the entire HSTS policy
    ```

### X-Frame-Options

HTTP response header that can be used to indicate whether or not a browser should be allowed to render a page in a `<frame>`, `<iframe>`, `<embed>`  or `<object>`. Sites can use this to avoid [click-jacking](https://scotthelme.co.uk/hardening-your-http-response-headers/#x-frame-options) attacks, by ensuring that their content is not embedded into other sites.

```sh
X-Frame-Options: SAMEORIGIN # only allow frame injection from your own site
X-Frame-Options: ALLOW-FROM https://example.com/ # lets you specify sites that are permitted to frame your own site
```

While the `X-Frame-Options` header is supported by the major browsers, it was never standardized and has been deprecated in favour of the `frame-ancestors` directive from `Content-Security-Policy` HTTP header. `frame-ancestors` [supports multiple domains and even wildcards](https://stackoverflow.com/questions/10205192/x-frame-options-allow-from-multiple-domains), for example
    
```sh
Content-Security-Policy: frame-ancestors 'self' example.com *.example.net
```

If a resource has both policies, the `frame-ancestors` policy SHOULD be enforced and the `X-Frame-Options` policy SHOULD be ignored.

### X-Content-Type-Options

This header only has one valid value, `nosniff`. It prevents Google Chrome and Internet Explorer from trying to mime-sniff the content-type of a response away from the one being declared by the server. It [reduces exposure](https://www.keycdn.com/support/what-is-mime-sniffing#how-to-avoid-mime-sniffing-vulnerabilities) to drive-by downloads and the risks of user uploaded content that, with clever naming, could be treated as a different content-type, like an executable.

### Referrer Policy

[Referrer Policy](https://scotthelme.co.uk/a-new-security-header-referrer-policy/) is a new header that allows a site to control how much information the browser includes with navigations away from a document and should be set by all sites.

### Feature Policy

[Feature Policy](https://scotthelme.co.uk/a-new-security-header-feature-policy/) is a new header that allows a site to control which features and APIs can be used in the browser.

## Same Origin Policy

One of the key principles of security is data isolation. Same origin policy is designed for segregating web content. Under this policy the web browser only allows Javascript in one web page to access data in another web page if the two pages have the same **origin**. An origin is [defined as](https://en.wikipedia.org/wiki/Same-origin_policy) a combination of the **protocol**, **domain name**, and **port**.

### Cross domain vulnerability

The same origin policy prevents a malicious script on one page from obtaining access to sensitive data on another web page through that page's DOM. Code from `https://mybank.com` should only have access to `https://mybank.com`'s data, and `https://evil.example.com` should certainly never be allowed access. This keeps a strong separation of content of unrelated sites.

It is important to note that the **same origin policy applies only to scripts**. This means that resources such as images, CSS, and dynamically-loaded scripts can be accessed across origins via the corresponding HTML tags (with fonts being a notable exception). Attacks take advantage of the fact that the same origin policy does not apply to HTML tags.

### Relaxing the same origin policy

Depending upon whether the target service allows cross-origin requests the [browser can deny such requests](https://stackoverflow.com/questions/20035101/why-doesn-t-postman-get-a-no-access-control-allow-origin-header-is-present-on). However, for large websites with multiple subdomains or when your API needs to be called by multiple web clients other than just the one hosted on the same server (origin) as your API, you may need to relax the same origin policy.

**Cross Origin Resource Sharing (CORS)** - Rather than deny cross-origin request, the browser asks the target service if it wants to allow a specific cross-origin request. The target service tells the browser whether it wants to allow cross-origin requests by inserting special HTTP headers in responses: For [using CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) it extends HTTP with a new `Origin` request header and a new `Access-Control-Allow-Origin` response header. It allows servers to use a header to explicitly list origins that may request a file or to use a wildcard and allow a file to be requested by any site.

```sh
Access-Control-Allow-Origin: * # resource can be shared by any domain

Access-Control-Allow-Origin: https://foo.example # no domain other than https://foo.example can access the resource in a cross-site manner

Access-Control-Allow-Methods: POST, GET, OPTIONS # POST and GET are viable methods to query the resource in question
Access-Control-Allow-Headers: X-PINGOTHER, Content-Type # permitted headers to be used with the actual request
Access-Control-Max-Age: 86400 # how long the response to the preflight request can be cached for without sending another preflight request
```

## CSP and CORS

Content security policy and same-origin policy (the lack of CORS) act as multiple lines of defense in protecting against malicious content. e.g. if `foo.com` wants to send a request to `bar.com`

1. When user visits `foo.com` in browser, `foo.com` server returns `foo.com` HTTP response, CSP restriction within this response can prevent `foo.com` in browser from issuing request to `bar.com`.
2. If there is no CSP restriction within `foo.com` HTTP response, then `foo.com` in browser can send a request to `bar.com`.
3. Upon receiving the request, `bar.com` server responds with `bar.com` HTTP response, CORS restriction within this response can prevent `foo.com` in browser from loading it. (Note that by default, Same-origin policy will restrict the response from loading, unless otherwise specified by CORS)
