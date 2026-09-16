# Security Headers

OWASP has a list of HTTP [Security headers](https://owasp.org/www-project-secure-headers/#tab=Headers) that you should consider adding to your web application to make it more secure. Adopting best practices for [hardening your HTTP response headers](https://scotthelme.co.uk/hardening-your-http-response-headers/) e.g. webserver config for [IIS](https://gist.github.com/The-Scott/f7b5d03e260036cfc4dce5ad89578377) or [nginx](https://gist.github.com/plentz/6737338) is a good baseline, however understanding the impact of including or excluding these headers should be duly considered. Blindly following best practice guides or security scanners that tell you headers are missing does not help you understand the security impact. For example

- if your website is not public-facing web application or locked down to a corporate network?
- if your website does not serve any dynamic content and thereby does not allow any user actions e.g. button clicks, it is clickjacking safe. In such a case having `X-Frame-Options` set to `DENY` may not do any harm, it probably adds a bit of protection but the missing header doesn't necessarily open you up to attacks.

Browsers can block script execution based on the following HTTP headers returned by the server.

## Content-Security-Policy

HTTP header allows you to create a **whitelist of sources** of trusted content, and instructs the browser to only execute or render resources from those sources. Even if an attacker can find a hole through which to inject script, the script won’t match the whitelist, and therefore won’t be executed.

The following policy only allows script to execute when it comes from one of the two trusted sources: the site's own origin (this excludes subdomains) and apis.google.com
    `Content-Security-Policy: script-src 'self' https://apis.google.com; object-src 'none'`

Allowlisting hosts is now considered a weak form of CSP, because allowed hosts often expose JSONP endpoints or script gadgets that bypass it. Current guidance is a **strict CSP** that trusts scripts by a per-response nonce (or hash) and lets those scripts load further scripts with `'strict-dynamic'`:

```http
Content-Security-Policy: script-src 'nonce-r4nd0m' 'strict-dynamic'; object-src 'none'; base-uri 'none'
```

You can use <https://csp-evaluator.withgoogle.com/> to evaluate your CSP policy whether it is strong enough to mitigate against XSS attacks.

*Note: `eval()` and inline scripts are blocked unless `'unsafe-eval'` or `'unsafe-inline'` (or a nonce or hash) is allowed. Violations are logged in the browser console and can be sent to a `report-to` endpoint.*

### CSP and APIs

CSP involves white listing of sources for the content of your website to impair XSS attacks. It directs the browser to load content from legitimate trusted sources. CSP is not applicable in case of APIs that are primarily data APIs serving JSON/XML without any dynamic content.

## HTTP Strict Transport Security (HSTS)

Instructs the browser to visit your site only over HTTPS to ensure they only use TLS to support secure transport. Supported widely by browsers and strongly recommended for internet-facing web applications, however it is only honoured by the browser only when the site has been loaded previously once over https without any certificate errors. It protects

- users against passive eavesdropper and active **man in the middle attacks**. If your login page page is served over http but the login form posts to https, is it secure? Not really. You cannot have confidence that the login form that has been served over http hasn't been modified by a man in the middle by the time it gets to the end user. Your traffic could still be intercepted before and after HTTPS connection begins and ends.
- mixed content and click-through certificate overrides
- against web server mistakes like loading JavaScript over an insecure connection
- this policy will enforce TLS on your site and all subdomains for a year

    ```sh
    Strict-Transport-Security: max-age=31536000; includeSubDomains # HSTS policy is applied to the domain of the issuing host as well as its subdomains and remains in effect for one year.
    Strict-Transport-Security: max-age=0 # Directs the browser to delete the entire HSTS policy
    ```

Adding `preload` and submitting the site to <https://hstspreload.org/> bakes the policy into browsers, so even the first visit is protected. The preload list requires `max-age` of at least one year with `includeSubDomains; preload`, and removal takes months, so only preload a domain where every subdomain can serve HTTPS.

## X-Frame-Options

HTTP response header that can be used to indicate whether or not a browser should be allowed to render a page in a `<frame>`, `<iframe>`, `<embed>`  or `<object>`. Sites can use this to avoid [click-jacking](https://scotthelme.co.uk/hardening-your-http-response-headers/#x-frame-options) attacks, by ensuring that their content is not embedded into other sites.

```sh
X-Frame-Options: DENY # never allow the page to be framed
X-Frame-Options: SAMEORIGIN # only allow framing from your own origin
```

These are the only two values. `ALLOW-FROM` was only ever supported by Internet Explorer and old Firefox (removed in Firefox 70, 2019) and never worked in Chrome or Safari, so treat it as obsolete.

While the `X-Frame-Options` header is supported by the major browsers, it was only standardised informationally (RFC 7034, 2013) and is obsoleted by the `frame-ancestors` directive from `Content-Security-Policy` HTTP header. `frame-ancestors` [supports multiple domains and even wildcards](https://stackoverflow.com/questions/10205192/x-frame-options-allow-from-multiple-domains), for example

```sh
Content-Security-Policy: frame-ancestors 'self' example.com *.example.net
```

If a resource has both policies, the `frame-ancestors` policy SHOULD be enforced and the `X-Frame-Options` policy SHOULD be ignored.

## X-Content-Type-Options

This header prevents browsers from trying to mime-sniff the content-type of a response declared by the server. The web browser "sniffs" the content to analyze what file format that particular asset is. It [reduces exposure](https://www.keycdn.com/support/what-is-mime-sniffing#how-to-avoid-mime-sniffing-vulnerabilities) to drive-by downloads and the risks of user uploaded content that, with clever naming, could be treated as a different content-type, like an executable.

This header only has one valid value, `nosniff`

## Referrer Policy

[Referrer Policy](https://scotthelme.co.uk/a-new-security-header-referrer-policy/) allows a site to control how much information the browser includes while navigating away from one site to another. This is how we get metrics like those provided by Google Analytics on where our traffic came from.

This header lets you know where the inbound visitor came from, and is really handy, but there are cases where we may want to control or restrict the amount of information present in this header like the path or even whether the header is sent at all.

```http
Referrer-Policy: no-referrer                      # never send the header
Referrer-Policy: same-origin                      # send the full URL for same-origin requests only
Referrer-Policy: strict-origin                    # send only the origin, and nothing on an https to http downgrade
Referrer-Policy: strict-origin-when-cross-origin  # full URL same-origin, origin only cross-origin, nothing on downgrade
Referrer-Policy: no-referrer-when-downgrade       # the old browser default; full URL unless downgrading
Referrer-Policy: unsafe-url                       # always send the full URL
```

Browsers default to `strict-origin-when-cross-origin` when no policy is set (Chrome 85 and Firefox 87, 2020 to 2021; Safari behaves the same), so cross-origin sites only see your origin unless you loosen it.

## Same-Origin Policy and CORS

The same-origin policy, CORS and the `Access-Control-*` headers are covered in [Browser Security Model](Browser%20Security%20Model.md), together with cookies and Web Storage. The headers below (COOP, COEP, CORP) decide which documents share a process and which resources may be embedded; they do not grant cross-origin reads.

## COOP and COEP

Previously, websites using shared memory for [inter thread communication](https://blog.logrocket.com/understanding-sharedarraybuffer-and-cross-origin-isolation/) could load cross-origin content without permission. These websites could interact with window pop-ups that are not of the same origins, potentially causing a security breach or a loophole to gain access to user information on the website. **Cross-origin isolation** shipped in browsers in 2020 to 2021 (Chrome 88, Firefox 79). In short, it is the result of sending two HTTP headers on your top-level document (COOP and COEP). These headers enable your website to gain access to powerful web APIs such as SharedArrayBuffer and prevent outer attacks (Spectre attacks, cross-origin attacks, and the like).

Powerful features

- SharedArrayBuffer - allows `main` thread to send messages to a `worker` thread using shared memory
- performance.measureMemory()
- JS Self Profiling API
  and more to come

If you are interested in using these powerful features, you will need to opt into COOP and COEP. This isolates the top-level document process and ensures it does not share a **browsing context group** with cross-origin documents (e.g. pop ups ), preventing a set of cross-origin attacks.

### Enabling cross-origin isolation

`Cross-Origin-Opener-Policy: same-origin`

**Cross-Origin-Resource-Policy** (CORP) is set by a resource owner to say which origins may embed that resource with no-cors requests such as `<img>` or `<script>`: `same-origin`, `same-site` or `cross-origin` (the browser default when the header is absent). It does not grant cross-origin reads (that is CORS); it lets a server stop other sites embedding its resources, which is a defence against Spectre-style side-channel reads.

```http
Cross-Origin-Resource-Policy: same-origin
```

COEP requires every resource your page loads to either pass a CORS check or carry a CORP header that permits your origin; anything else is blocked from loading. `Cross-Origin-Embedder-Policy: credentialless` (Chrome 96, Firefox 119) is an easier alternative that loads cross-origin resources without credentials instead of requiring CORP.

`Cross-Origin-Embedder-Policy: require-corp`

## Deprecated

- X-XSS-Protection
  The core issue exploited by XSS attacks is the browser’s inability to distinguish between scripts that are intended to be part of your application and the ones that have been maliciously injected by a third-party. This header toggled the browser's built-in reflected XSS filter. The filter was removed from Chrome 78 (2019) and Safari 15.4, never existed in Firefox, and introduced side-channel bugs of its own, so the only value worth sending is `0`, or omit the header and use Content-Security-Policy instead.

    ```sh
    X-XSS-Protection: 0 # disable the legacy filter; use Content-Security-Policy instead
    ```

- Feature Policy
    The Permissions-Policy header replaces the existing Feature-Policy header for controlling which features and APIs can be used in the browser
