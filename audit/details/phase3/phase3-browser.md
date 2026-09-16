# Phase 3 report: Browser Security Model

Files edited (not committed):
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Browser Security Model.md (full rewrite; old name Security/Web Security/Security Cookies.md, old H1 "HTTP Cookies")
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Security Headers.md (only the "## Same-Origin Policy and CORS" section and its two subsections replaced by a two-sentence pointer; COOP/COEP/CORP untouched)

Not touched: Cross Site Request Forgery.md, Cross Site Scripting.md (both already link to ./Browser%20Security%20Model.md). No other page linked to the removed Security Headers anchors.

Final word count: 1,398 by raw `wc -w`; 1,374 with table pipes removed; 1,220 words of prose (excluding the two code blocks, the table and Sources). The first draft was 2,340; the owner's brevity feedback arrived mid-task and the page was tightened to the low end of the target. "How to rederive this" is 4 bullets. No "> Own view:" block: the owner's "who needs this data, the client or the server?" is stated neutrally as a sentence, not as a question. Each related page is linked exactly once: CSRF from the same-origin policy section, XSS from the Web Storage section (as the brief asked), Security Headers from the CORS section.

## (a) Question the page answers

What does the browser let a page do, and how do cookies and storage fit into that? Answered in the first paragraph: a page can send and embed almost anything but read only its own origin (same-origin policy); cookies are older and attach by host and path regardless of who started the request; Web Storage is origin-locked.

## (b) Kept from the original

From Security Cookies.md:
- "HTTP is stateless ... so the server can tell two requests came from the same browser" and the three uses (session management with logins and shopping carts, personalisation, tracking).
- The advertiser explanation (third-party cookie returned from every embedding site; the script knows the URL; it cannot read the embedding site's cookies), rewritten and followed by the 2020 to 2025 browser changes.
- "Who needs this data, the client or the server", now a neutral closing sentence of the Web Storage section.
- The cookies vs localStorage comparison, turned from an exploit table into the requested scope/size/sent/expiry/script-access table. The corrected content of its XSS, CSRF and SessionFixation rows survives as prose (HttpOnly, CSRF via cookies riding along, cookie tossing from a sibling subdomain).

From Security Headers.md (moved here, corrected):
- The mybank.com / evil.example.com sentence.
- The "restricts reading cross-origin responses, not embedding them" paragraph including the fonts exception and canvas taint.
- The Access-Control-* header block (owner's five lines, comments shortened, plus Access-Control-Allow-Credentials).
- The foo.com / bar.com three-step CSP-then-SOP list, already corrected in Phase 2, tightened.

## (c) Dropped and why

- IE8 / Firefox 50 / Opera 30 / "Chrome no limit" cookie counts: 2009 facts, two of the browsers are dead, the Chrome claim was false. Replaced with RFC 6265 minimums and "around 150 to 180 per domain".
- "4 KB for all cookies, anything over is truncated": wrong on both points. Replaced.
- The `<em>`-tagged Set-Cookie line: replaced with the full attribute list in an `http` fence.
- The express-session snippet: dropped. It was incomplete (no `require`, no `secret`) and, once completed, cost about 75 words for three attributes the bullets already cover. Under the low-end word target it did not earn its place. Easy to restore if the owner wants it (see (f)).
- The localStorage browser-support row (IE8, Firefox 3.5, Safari 4, Chrome 4): irrelevant in 2026.
- "SameSite binds a cookie to a single origin": wrong, SameSite is site-scoped; the page now says so and explains why the subdomain gap exists.
- "Malicious JS injection can be prevented by CSP": CSP mitigates; the XSS page covers CSP so this page does not repeat it.
- From Security Headers: the Wikipedia origin definition, the Stack Overflow Postman link, and the "for large websites with multiple subdomains ... you may need to relax" paragraph (generic filler; the point survives as one sentence).

## (d) Added, with sources

- Origin vs site definitions, eTLD+1 and the public suffix list (`alice.github.io` vs `bob.github.io`); "current browsers also compare the scheme" (schemeful same-site). Source: MDN "Same-origin policy", web.dev "Schemeful Same-Site".
- Which rules use which principal (SOP and Web Storage origin-scoped; `Domain` and `SameSite` site-scoped; cookies ignore port). Source: RFC 6265 section 8.5, MDN cookies.
- Cross-origin `fetch()` is sent but the response withheld without CORS; preflight triggers (non-simple method, non-safelisted header, non-form Content-Type), `OPTIONS` with `Access-Control-Request-*`, credentials need `Access-Control-Allow-Credentials: true` and a non-wildcard origin. Source: MDN "Cross-Origin Resource Sharing", Fetch standard.
- Full Set-Cookie attribute list with `Max-Age`, `HttpOnly`, `SameSite`, `Partitioned`; `Max-Age` wins over `Expires`; host-only cookies when `Domain` is absent; `Domain` can only name the setting host or a parent within its site; `Secure` cookies cannot be set or overwritten from HTTP. Source: RFC 6265 sections 4.1.2 and 5.3, RFC 6265bis "Leave Secure Cookies Alone".
- Limits: RFC 6265 section 6.1 minimums (50 per domain, 4096 bytes per cookie); reject not truncate (RFC 6265bis storage model); browsers cap around 150 to 180 per domain (audit figure, marked approximate).
- SameSite Strict/Lax/None semantics; Chrome 80 (February 2020) Lax default with the two-minute Lax+POST exception; Firefox and Safari not defaulting to Lax; `None` requires `Secure`; Lax gaps (same-site subdomains, top-level GET). Source: web.dev "SameSite cookies explained", RFC 6265bis section 5.5. Written differently from the CSRF page's paragraph so the two do not duplicate.
- Cookie tossing mechanics (site-wide `Domain`, `Cookie` header carries no attributes) and the `__Host-` and `__Secure-` prefix rules. Source: RFC 6265bis section 4.1.3.
- Session fixation and the fix (regenerate the session id at login and privilege change; never accept a server-unknown id). Source: OWASP Session Management Cheat Sheet.
- Third-party cookies today: Safari ITP full block 2020; Firefox Total Cookie Protection default 2022; Chrome 1% trial January 2024, user-choice plan July 2024, dropped April 2025; CHIPS `Partitioned` and Storage Access API. Source: Chrome Privacy Sandbox posts "A new path for Privacy Sandbox on the web" (July 2024) and "Next steps for Privacy Sandbox and tracking protections in Chrome" (April 2025); the audit's dates agree.
- Web Storage: origin-scoped not domain-scoped, roughly 5 to 10 MB per origin, never sent, no HttpOnly equivalent, sessionStorage per tab. Source: MDN "Web Storage API".
- Security Headers pointer sentence: COOP/COEP/CORP decide process sharing and embedding, not reads.

## (e) Diagrams for Phase 5

The old page had no images and none were added. One diagram would help: `origin-vs-site.drawio.svg`, showing `https://login.mybank.com`, `https://cdn.mybank.com`, `http://mybank.com` and `https://mybank.com:8443` as separate origin boxes inside one site boundary, with labels for which rule sits on which boundary (same-origin policy and Web Storage on the origin box; cookie `Domain` and `SameSite` on the site boundary; port ignored by cookies). Embed under "Origins and sites".

## (f) Open questions for the owner

1. The express-session snippet was dropped for length. If you want a code example back, the completed version (with `require('express-session')` and `secret`) is about 75 words and fits under "Session fixation" or "Set-Cookie". Say which.
2. "Current browsers also compare the scheme" (schemeful same-site) is stated without dates. Fine to keep as is, or cut if you consider it too fine a point.
3. The "150 to 180 per domain" cap is approximate and browser-specific. Keep as a rough figure, or cut and leave only the RFC minimums.
4. The page says nothing about `document.domain`, `postMessage` or cross-window DOM access. Intentional, to stay on the reading/sending question. Add if you want a fuller "what a page can do" answer.
