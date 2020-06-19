# Cross Site Scripting

Cross-site scripting (also known as XSS) is a web security vulnerability that allows an attacker to run malicious scripts while a user visits or interacts with a vulnerable website or app. The malicious script can originate from various sources:

* Reflected XSS: the malicious script comes from the current HTTP request itself passed in the query url.
* Stored (persistent or second-order) XSS: the malicious script comes from the website's database and can be executed repeatedly.
* DOM-based XSS: the vulnerability exists in client-side code rather than server-side code

XSS allows an attacker to circumvent the same origin policy, which is designed to segregate different websites from each other.

## Preventing XSS attacks

* Always validate un-trusted data i.e. all input fields. XSS vulnerabilities come from a [lack of data escaping](https://blog.sqreen.com/reflected-xss/) user inputs.

    ```javascript
    html_escape('is a > 0 & a < 10?')
    // equivalent unicode escaped form
    => is a &gt; 0 &amp; a &lt; 10?
    ```

    Validation filters can be evaded if they are just looking for script tags in the input. e.g. such a filter can be circumvented by using an IMG tag for executing javascript

    ```javascript
    <IMG SRC="javascript.alert('XSS');">
    ```

    OWASP [XSS Filter Evasion cheat sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet) has more examples of filter evasion techniques.
* Flag Cookies as **Http only**. Reduce the attack surface by preventing javascript access to sensitive cookies, otherwise scripting attack can get access to user session info in the cookie and perform operations as a logged in user. Flagging cookies as Http only can be read by the server as usual but are not accessible to client javascript.
* Treat everything as suspicious. Even DNS records can be infected by XSS attacks.