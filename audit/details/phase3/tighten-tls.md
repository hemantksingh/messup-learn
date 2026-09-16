# Tighten report: TLS.md and TLS Certificates.md

Nothing committed. Two files edited, both under /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/networking/.

## TLS.md

Word count (code fences excluded; the page has none): 1,514 before, 998 after. Target 900 to 1,000. Every fact, link (6), section, heading and the Sources block are intact; no em or en dashes; British spelling.

Note: 998 is the top of the band, not the low end. Getting lower needed dropping facts (RFC numbers, cipher names, the 0-RTT replay caveat, the post-quantum bullet, the mTLS per-connection correction), so I stopped here.

### Cut, by category

Sentences restating the previous sentence or another section:
- Intro: "A hash cannot give confidentiality and encryption cannot prove identity, so TLS needs all three" (rederive bullet said the same) and "The handshake exists to get two strangers from no shared secret to..." (the handshake section shows it).
- Intro first sentence's gloss ("so that nobody on the network can read or change the traffic, and so that the client knows...") which the three bullets then say.
- Handshake: "The certificate is the CA's statement that a public key belongs to a name" (said again in "What the certificate proves"); kept the formula and its lead-in.
- "What the certificate proves": "an expired certificate or an untrusted chain produces a similar warning for a different reason".
- "How to rederive this": cut from 5 bullets to 4 (brief allows at most 5); dropped the primitives bullet, which restated the intro's three bullets. Each survivor is now one line, a question prompt with its answer. These are working prompts, not rhetorical questions, and match the owner's own question headings in practice/Testing Strategy.md.

Explanatory asides a reader can infer:
- "Where TLS sits": SMTP/LDAP aside, "HTTP hands its bytes to TLS, TLS encrypts them into records and hands the records to TCP". Now one sentence plus the Network Layers link, plus the HTTP/3 exception with its link.
- RSA section: "exactly as today"; "instead of discouraging them"; "Everything after that was symmetric encryption..." folded into the formula sentence.
- SNI: "even though the rest is encrypted"; "from the ones it holds".
- Mutual TLS: "every request on that connection inherits the identity"; "the client presents it"; IP-based trust cut to one sentence as the assignment allowed, dropping "you told the server which IPs..." and "A certificate travels with the workload; an IP does not".

Connective filler and lead-ins:
- "Two things fall out of this."; "The version matters because it changes the mechanism."; "Because IPv4 addresses are scarce... But it has to..."; "Rather than..." kept (owner's).

Long parenthetical lists of products:
- SNI: "(Apache, Nginx, HAProxy, a cloud load balancer)".

Shorter words, merged clauses:
- "Server Name Indication ... is a TLS extension that fixes this" to "fixes this"; "the current time is inside the validity period" to "the time is within validity"; "when the connection closes" to "at close"; "made with" to "by"; "one round trip instead of two" to "one round trip"; version bullets lose the repeated "TLS" prefix; "(a break-in, a court order, a Heartbleed-style bug)" to "(break-in, court order, Heartbleed)"; "As of 2025 the key exchange is changing again" folded into the "2025:" bullet.

### Tempted to cut but kept

- "Traditionally **IP based trust** was used instead..." : owner's sentence from the pre-rewrite page (rule 7 / rule 2), so shrunk to one sentence rather than deleted.
- "Only if the certificate is valid, and only if its name or DN is in the server's list of trusted identities, is the client deemed trustworthy": owner's sentence, kept verbatim.
- The [Proxy authentication](search-guard) sentence and "Rather than only the server identifying itself...": owner's, kept.
- "Browser ----------------> website (e.g. `example.com`)" and the Sign_CA / Verify_CA_pk formulas: owner's, kept.
- "Both sides contribute to the secret, so neither chooses it alone" and "The certificate's key signs; it never encrypts the session secret": the two corrections of the old page's RSA-transport model, kept.
- "It is presented per handshake, so per connection, not per request": correction of the old "for every request" claim, kept.
- The 0-RTT replay caveat, the X25519MLKEM768 bullet, RFC numbers and years, AES-GCM / ChaCha20-Poly1305: facts, kept.
- The Sources section: byte-identical.

## TLS Certificates.md

One edit. The "> Own view:" blockquote (was line 121) that the owner did not write is replaced by one neutral sentence, no blockquote:

"A DV certificate covers everything the browser needs; OV or EV are worth paying for only when a customer or a compliance regime asks for them."

Nothing else in the file was touched (the replacement was done as a single exact-string substitution asserted to match once).
