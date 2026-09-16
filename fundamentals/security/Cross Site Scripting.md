# Cross Site Scripting

Cross-site scripting (also known as XSS) is a web security vulnerability that allows an attacker to run malicious scripts while a user visits or interacts with a vulnerable website or app. The malicious script can originate from various sources:

* Reflected XSS: the malicious script comes from the current HTTP request itself passed in the query url.
* Stored (persistent or second-order) XSS: the malicious script comes from the website's database and can be executed repeatedly.
* DOM-based XSS: the vulnerability exists on the client-side, possibly from an injected malicious JS from an untrusted source as opposed to coming from the server.

XSS allows an attacker to circumvent the same origin policy, which is designed to segregate different websites from each other.

## Preventing XSS attacks

* Encode untrusted data for the context it is rendered into (HTML body, attribute, JavaScript, URL, CSS) at output time. This **context-aware output encoding** is the primary defence; XSS vulnerabilities come from a [lack of data escaping](https://blog.sqreen.com/reflected-xss/) when user input is written into a page. Input validation is defence in depth and cannot be relied on alone.

    ```text
    html_escape('is a > 0 & a < 10?')
    // equivalent HTML entity encoded form
    => is a &gt; 0 &amp; a &lt; 10?
    ```

    Validation filters can be evaded if they are just looking for script tags in the input. e.g. such a filter can be circumvented by using an IMG tag with an event handler for executing javascript

    ```html
    <img src=x onerror=alert(1)>
    ```

    OWASP [XSS Filter Evasion cheat sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet) has more examples of filter evasion techniques.
* Flag Cookies as `HttpOnly`. Reduce the attack surface by preventing javascript access to sensitive cookies, otherwise scripting attack can get access to user session info in the cookie and perform operations as a logged in user. Flagging cookies as Http only can be read by the server as usual but are not accessible to client javascript. Cookie attributes are covered in [Browser Security Model](./Browser%20Security%20Model.md).
* Treat everything as suspicious. Any untrusted data source rendered into HTML, including DNS TXT records or log lines, can carry an XSS payload.
* Other mitigations, each of which limits the damage when encoding is missed:
  * A strict [Content-Security-Policy](./Security%20Headers.md#content-security-policy) using nonces or hashes and `'strict-dynamic'`, so injected inline script does not run.
  * Trusted Types (Chromium), which make dangerous DOM sinks such as `innerHTML` accept only sanitised values.
  * Framework auto-escaping in templates (React, Angular, Razor), and avoiding the raw-HTML escape hatches.
  * DOMPurify to sanitise any HTML that genuinely must be rendered from untrusted input.
  * `X-XSS-Protection` is deprecated and should be set to `0` or omitted; see [Security Headers](./Security%20Headers.md#deprecated).
