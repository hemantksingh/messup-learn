# Tighten report: fundamentals/security/Cryptography Basics.md

No code fences on this page, so every count below is fences-excluded by definition.

## Word counts

| Measure | Before | After |
|---|---|---|
| Whole file | 1,646 | 1,245 |
| Without the table | 1,579 | 1,178 |
| Prose only: no table, no image line, no Sources (this matches the assignment's "about 1,460") | 1,458 | 1,057 |

Result: 1,057 on the assignment's measure. Under the 1,100 ceiling, but above the 800 to 900 target. I could not reach 900 without dropping a fact or an owner sentence, which rule 2 forbids. The fixed parts alone are about 330 words: the four-property bullets (40), the owner's AEAD paragraph (33), the owner's three hash-property bullets (65), the Own view (17), the OWASP parameter sentence (50), five rederive bullets (70), headings and title (30), plus the two asymmetric links' sentences. What remains is one terse sentence per fact.

To get to 900 the caller would have to authorise cutting some of these (each is a fact or owner text, listed roughly in order of least loss):

* the one-sentence opener (13 words; rederive bullet 1 says the same)
* "It holds only while the private key stays private and the verifier trusts the binding of key to identity" (20)
* "TLS traffic, disk encryption" and "(unlike passwords)" from the symmetric examples (owner examples, 6)
* "The nonce does not change the MAC algorithm" (owner sentence, 8)
* the stream/counter-mode bit-flip clause (18)
* "RSA and elliptic curve (ECC) are the key pairs in common use" (owner listed both, 11)
* "content addressing" (2)
* "Memory-hard because GPUs and ASICs have cheap compute but expensive memory" (11)
* the four-property bullets, since the table names the rows (40)

## What was cut, by category

Named by the rewriter as candidates, all cut:
* the Caesar paragraph, whole; kept only the two facts inside it ("one shared key for both directions"; AES and ChaCha20 are fast so carry bulk data) and the owner's usage examples
* the git content-addressing example; "content addressing" stays as a use
* "Controls that are not cryptography" down to one sentence with the Data Privacy link; heading kept

Restatements:
* opener cut from five sentences to one; the other four were rederive bullets 1 and 2 in substance
* "The private key does the reverse: decrypt, and sign" (already said by the previous sentence)
* "So asymmetric cryptography does two jobs" restated as "So it agrees a symmetric key and signs"
* "the opposite of SHA-256" in the password section (SHA-256 is called fast in Hashing and "not plain SHA-256" follows two sentences later)
* "so it cannot say who sent a message" (follows from "integrity only")
* "That is non-repudiation, the one property a MAC cannot supply" folded into the previous sentence
* "The key turns the Authentication row from No to Yes" (the table says it)
* "whoever can alter the file can alter a digest next to it" (restates "a path the attacker cannot touch")
* "Asymmetric cryptography exists for this" at the end of Symmetric (the next heading is Asymmetric)
* "AEAD modes add a MAC so tampering is caught first" in Symmetric (the owner's AEAD paragraph under the table and rederive bullet 3 say it)
* "Key distribution becomes a different problem: not a secret channel, but ..." cut to "becomes trust that a public key belongs to who you think"

Connective filler and lecture voice:
* "You can tell which property a primitive gives by asking", "In practice", "That is symmetric encryption", "have the shape of it", "Hashing is a one-way function where", "is designed to have", "To prevent this", "for the same reason", "So password hashes are ... " kept as the one "so" per paragraph

Product lists:
* "traffic in TLS, Wi-Fi and VPNs, full disk encryption against theft" to "TLS traffic, disk encryption"
* "RSA and elliptic curve cryptography (ECC) are the two key-pair families in common use" to "RSA and elliptic curve (ECC) are the key pairs in common use"

Explanatory asides:
* "Encoding ... has nothing to do with cryptography" (the heading and "none of the four properties" say it)
* "generally shown as hexadecimal" kept, "where data of any length is mapped" shortened
* "Hash the message, then apply ..." made one sentence with "anyone with the public key can verify"

Links: "see [TLS Certificates]" and "See [the TLS page]" became inline links on "certificates" and "TLS"; same five targets, same count.

Rederive bullets: still five, each one line, each shortened.

## Kept though tempted to cut

* Own view: restored the owner's wording "a cryptographically strong hash code is a good checksum" (HEAD has "hash code"; the rewrite had dropped "code").
* "Encryption is two-way: scrambled so it can be unscrambled later" is the owner's opening sentence on encryption, so it stays even though the intro covers reversibility.
* "The nonce does not change the MAC algorithm" is an owner sentence.
* "Hash-table hashes only need to spread inputs evenly; no collision resistance in the cryptographic sense" is the owner's sentence, kept though the checksum sentence half covers it.
* RSA can only encrypt something smaller than its own key; TLS 1.3 removed RSA key transport (RFC 8446 is in Sources for it); OpenPGP is a format not an algorithm; signatures sign the hash so a collision shares a signature; pigeonhole; stream/counter bit flip; every pair needs its own key; memory-hard because of GPUs and ASICs; salt defeats rainbow tables and makes each guess cost one account; "as of 2024"; non-repudiation holds only while the key is private and the binding trusted; Base64 and URL-encoding purposes. Each is a fact tied to a source.
* The four-property bullets and the image alt text, untouched apart from shortening the bullets.

## Checks run

Table, headings, Sources and the image line unchanged (diffed). Five links before and after, same targets; the `#encoding-is-not-encryption` anchor that Secrets Management.md links still resolves. Every number in the old page is in the new one (one duplicate "SHA-256" mention dropped). No em or en dashes. British spelling. Nothing committed.
