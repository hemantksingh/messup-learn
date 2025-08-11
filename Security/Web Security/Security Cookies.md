# HTTP Cookies

An [HTTP cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) is a small piece of data that a server sends to the user's web browser. Because the underlying HTTP protocol is stateless, it is typically used to tell the server if two requests came from the same browser. The stateless nature of HTTP means, each request from your browser is completely separate from others, so if the server needs a way to keep track of what request belongs to what visitor, it does so by storing a small bit of information in a cookie.

Cookies mainly used for three purposes: help the user in providing a much more targeted and customized experience tailored to the user. Like

* Session management: user logins, shopping carts
* Personalization: User preferences, themes and other settings e.g. showing the weather or news in the user's home town
* Tracking: Recording and analyzing user behavior

## Cooke creation

A web server specifies a cookie to be stored by sending an HTTP header called Set-Cookie. The format of the Set-Cookie header is a string as follows (parts in square brackets are optional):
`Set-Cookie: <em>value</em>[; expires=<em>date</em>][; domain=<em>domain</em>][; path=<em>path</em>][; secure]`

## Cookie restrictions

Cookies can have security and privacy implications for the user. There are a number of restrictions placed on cookies in order to prevent abuse and protect both the browser and the server from detrimental effects

* Only a limited number of cookies are available for each domain. IE 8 has a maximum of 50 cookies per domain as. Firefox also has a limit of 50 cookies while Opera has a limit of 30 cookies. Safari and Chrome have no limit on the number of cookies per domain.
* Because cookies are sent with every request, their size should be kept to a minimum. Ideally, only an identifier should be stored in a cookie with the data stored by the app. The maximum size for all cookies sent to the server has remained the same since the original cookie specification: 4 KB. Anything over that limit is truncated and won’t be sent to the server.

To ensure that cookies are sent securely and are not accessed by unintended parties or scripts, they can be configured with the following attributes:

```javascript
// Most web servers like Apache, Nginx, IIS, NodeJs.Express have the ability to set cookies
// Express.js example
app.use(session({
    cookie: {
        // A cookie with the `Secure` attribute is only sent to the server over HTTPS, not with HTTP
        secure: process.env.NODE_ENV === 'production', // dev environments often use HTTP locally
        httpOnly: true, // Prevents the cookie being accessible via JS - `document.cookie' cannot read HttpOnly cookies
        sameSite: 'strict' // Cookie only sent with same-site requests, JS on same domain can still access non-HttpOnly cookies regardless of SameSite
    }
})
```

## Cookies and advertising

Cookies are used by online advertisers to track the websites you visit.

Because cookies are always sent back to the site that originated them, an advertiser's cookie will be sent back to them from every web site you visit that is also using that same advertiser. This allows the advertiser to track the sites you visit, and send targeted advertising based on the types of sites that you visit.

This does not mean that advertisers can read the cookies from the web site you are visiting—they can only read their own cookies, but because the advertising Javascript is embedded in the page, they will know the URL you are visiting. These cookies are considered third-party cookies, because they are not set by the actual page you are visiting, and they can generally be blocked without causing any serious problems.

## Cookies and local storage

Cookies and local storage serve different purposes. Cookies are primarily for data required **server-side**, local storage can only be read by the **client-side**, therefore cookies are restricted to small data volumes (4 Kb), while localStorage can store up to 10mb per domain. So the question is, in your app, who needs this data - the client or the server?

| Exploit          | Local Storage                                                                     | Cookies |
| ---------------- | ----------------------------------------------------------------------------------|-------- |
| XSS              | Malicious scripts can access data. Malicious JS injection can be prevented by CSP | `HTTPOnly` prevents JS access, limiting XSS attacks |
| SessionFixation  | Bound to a single origin                                                          | Can be bound to a single origin by using `SameSite`, however can still be sent to subdomains, meaning requests from `login.mysite.com` to `cdn.mysite.com` would be considered a same-site request. It relies on the fact that wildcard cookies can be set by a subdomain and, that those cookies may affect other subdomains|
| CSRF             | Not sent by the browser with each HTTP request, therefore not applicable | Mainly server bound, all cookies for a domain are sent by the browser with HTTP requests to the server, therefore require CSRF protection |
| Support          | Not supported by anything before: IE 8, Firefox 3.5, Safari 4, Chrome 4           | Legacy support (it's been around forever) |
