# Cross Site Request Forgery

[Understanding Cross Site Request Forgery](http://www.troyhunt.com/2016/03/understanding-csrf-video-tutorial.html)

An attack that involves forcing a victim to send an HTTP request to a destination without their knowledge or intent in order to perform an action on their behalf. It often takes advantage of the fact that the victim is authenticated. **AuthCookie** keeps a user authenticated as they make requests across the site, so that a user does not have to log in with each request. It is sent to the server as part of each request in the Cookie header after a user is logged in to let the server know who the user is. The Cookie is sent automatically to the server by the browser if it is valid for the domain and the path and if it hasn't expired. This makes the server treat it as an authenticated request.

e.g. you go to securepuppies.com & rather than just displaying cute puppies the site might also POST to facebook on your behalf using the authenticated facebook session in your browser, if facebook doesn't prevent against CSRF. The attacker may use XSS vulnerability or **social engineering** to trick you to go to securepuppies.com & execute the script/html that performs these unintended actions. The html is usually obfuscated somewhere in the original page and might be hidden in an iframe. It is usually done with one of the following techniques:

* Sending an unsolicited email with HTML content
* Planting an exploit URL or script on pages that are likely to be visited by the victim while they are on other legitimate sites.

[CSRF Prevention](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet)

State change operations (POST,PUT) that are predictable and make it easy for the attacker to predict a request pattern, allow the attacker to forge a request on the user's behalf. e.g. changing password could be a form action that needs 2 parameters 'new password' & 'confirm password', a POST operation and the URL at which this action is performed. In order to prevent against CSRF we need to add some unpredictability and this is achieved by adding an anti **CSRF token** to the requested form. The server does this by including a hidden input field with a common name such as "CSRFToken" to the form as well as the Cookie.

```<form action="/transfer.do" method="post">
  <input type="hidden" name="CSRFToken" 
  value="OWY4NmQwODE4ODRjN2Q2NTlhMmZlYWE...
  wYzU1YWQwMTVhM2JmNGYxYjJiMGI4MjJjZDE1ZDZ...
  MGYwMGEwOA==">
  …
  </form>```

While processing this form, the server checks for the presence of this token along with the Cookie to determine if it is a valid request. CSRF tokens need to be secret, otherwise attacker would have the missing piece required to forge a request. The token is generated as a pair with the session token stored in the Cookie header. They are a cryptographic pair, you can see them but cannot tell whats inside them. The only way an attacker can set both  the CSRF token in the form field and the Cookie in a request is if they perform a XSS attack to inject their own arbitrary cookie. This is a separate risk and needs to be accounted for separately. Even in this case the attacker might not be able to do much because once you are authenticated the cookie gets keyed to your username. If the cookie and the form field are both keyed to your username and your identity comes from the **AuthCookie** then the attacker is out of luck, they can't generate the right form field and the right cookie for your username, if they could they have just hijacked your user session and you have a different problem.

Cross-Site Scripting is not necessary for CSRF to work. However, any cross-site scripting vulnerability can be used to defeat token defenses. This is because an XSS payload can simply read any page on the site using a XMLHttpRequest and obtain the generated token from the response, and include that token with a forged request. This technique is exactly how the MySpace (Samy) worm defeated MySpace's anti CSRF defenses in 2005, which enabled the worm to propagate.