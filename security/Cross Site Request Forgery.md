# Cross Site Request Forgery

[Understanding Cross Site Request Forgery](http://www.troyhunt.com/2016/03/understanding-csrf-video-tutorial.html)

An attack that involves forcing a victim to send an HTTP request to a destination without their knowledge or intent in order to perform an action on their behalf. It often takes advantage of the fact that the victim is authenticated. The browser attaches the session cookie automatically to every request that matches its domain and path, so the server treats the forged request as authenticated. How cookies are created and scoped is covered in [Browser Security Model](Browser%20Security%20Model.md).

e.g. you go to securepuppies.com & rather than just displaying cute puppies the site might also POST to facebook on your behalf using the authenticated facebook session in your browser, if facebook doesn't prevent against CSRF. The attacker may use XSS vulnerability or **social engineering** to trick you to go to securepuppies.com & execute the script/html that performs these unintended actions. The html is usually obfuscated somewhere in the original page and might be hidden in an iframe. It is usually done with one of the following techniques:

* Sending an unsolicited email with HTML content
* Planting an exploit URL or script on pages that are likely to be visited by the victim while they are on other legitimate sites.

[CSRF Prevention](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet)

State change operations (POST,PUT) that are predictable and make it easy for the attacker to predict a request pattern, allow the attacker to forge a request on the user's behalf. e.g. changing password could be a form action that needs 2 parameters 'new password' & 'confirm password', a POST operation and the URL at which this action is performed. In order to prevent against CSRF we need to add some unpredictability and this is achieved by adding an anti **CSRF token** to the requested form. The server does this by including a hidden input field with a common name such as "CSRFToken" to the form as well as the Cookie.

```html
<form action="/transfer.do" method="post">
  <input type="hidden" name="CSRFToken" 
  value="OWY4NmQwODE4ODRjN2Q2NTlhMmZlYWE...
  wYzU1YWQwMTVhM2JmNGYxYjJiMGI4MjJjZDE1ZDZ...
  MGYwMGEwOA==">
  …
</form>
```

While processing this form, the server checks for the presence of this token along with the Cookie to determine if it is a valid request. CSRF tokens need to be secret, otherwise attacker would have the missing piece required to forge a request. There are two common token patterns. The **synchronizer token** is generated per session (or per request) and stored server side; the server compares the submitted value with the stored one. The **double-submit cookie** sends the token both in a cookie and in the form field and checks that the two match, so the server stores nothing. A naive double-submit is weak: an attacker who controls any sibling subdomain can set a cookie for the parent domain (cookie tossing) and so supply both halves without needing XSS. OWASP therefore recommends the **signed double-submit cookie**, where the token is an HMAC over the session id with a server-side key, so an attacker cannot mint a matching pair.

Cross-Site Scripting is not necessary for CSRF to work. However, any cross-site scripting vulnerability can be used to defeat token defenses. This is because an XSS payload can simply read any same-origin page using a XMLHttpRequest and obtain the generated token from the response, and include that token with a forged request. As the [OWASP CSRF Prevention cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) puts it: "This technique is exactly how the MySpace (Samy) worm defeated MySpace's anti-CSRF defenses in 2005, which enabled the worm to propagate."

## SameSite and other defences

The `SameSite` cookie attribute stops the browser attaching a cookie to most cross-site requests. Chromium has treated cookies without a `SameSite` attribute as `Lax` since Chrome 80 (Feb 2020), with a two-minute "Lax+POST" exception for freshly set cookies; Firefox and Safari do not default to Lax, so set the attribute explicitly. `SameSite=None` requires `Secure`. `SameSite=Lax` still allows top-level GET navigations and does not protect against a sibling subdomain, because subdomains are the same site. Servers can also check the `Sec-Fetch-Site` request header (Fetch Metadata) and reject `cross-site` values on state-changing routes. OWASP keeps tokens (synchronizer or signed double-submit) as the primary defence, with SameSite and `Sec-Fetch-Site` checks as defence in depth.
