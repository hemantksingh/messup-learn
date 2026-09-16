# Phase 3 report: fundamentals/security/Cryptography Basics.md

File edited: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Cryptography Basics.md` (only this file; nothing committed). Length: `wc -w` gives 1,646 words including the table, alt text and Sources; 1,458 words of prose (table, image line and Sources excluded). The prose figure is inside the "target plus a third" ceiling (1,467) but above the 1,100 target; the raw `wc -w` figure is not. Cutting further would mean dropping either the Phase 2 correction text (hash properties, OWASP parameters, HMAC and nonce) or the "why can't the others do it" derivations the assignment asked for.

## (a) Question the page now answers

Which cryptographic primitive gives which property, and why can't the others do it. The opening paragraph answers with two questions (who holds the key, is the operation reversible) and one sentence per primitive; each later section derives its row of the table from that.

## (b) Kept from the original

- The owner's table, all four columns and every Phase 2 value (Confidentiality: No / No / No / Yes; Non-repudiation only for signatures; `Kind of keys` row).
- Phase 2 sentence: "A MAC or a digital signature is computed over plaintext and hides nothing ... AEAD modes (AES-GCM, ChaCha20-Poly1305) ...".
- "Encryption is a two-way function ... You encrypt with the intention of decrypting."
- Caesar's shift cipher, now used to derive "the shift is the key, both sides must know it" and the key distribution problem.
- The three encryption usage examples (card data that must be read back unlike passwords; TLS, Wi-Fi, VPN; full disk encryption against theft).
- OpenPGP is a message format, not an algorithm (Phase 2).
- The three hash-property bullets, verbatim in substance (Phase 2), including "Collisions always exist ... The property is that nobody can find one."
- "General-purpose cryptographic hashes such as SHA-256 are designed to be fast" and the hash-table vs cryptographic collision resistance sentence (Phase 2).
- The checksum remark: "a checksum is necessarily a hash, but not every hash is a checksum", with "a checksum is a hash used to detect accidental errors" added so the subset claim is grounded. The owner's heuristic "if you can afford the computational cost, a cryptographically strong hash is a good checksum" is now the page's only `> Own view:`.
- The whole password-hashing paragraph including the OWASP 2024 parameter string exactly as Phase 2 wrote it (Argon2id 19 MiB / 2 / p=1; scrypt N=2^17, r=8, p=1; bcrypt work factor 10 or more; PBKDF2-HMAC-SHA256 600,000).
- The HMAC paragraph and the nonce/timestamp replay paragraph (Phase 2).
- The Base64 explanation.
- The password-hashing image embed, now with descriptive alt text covering both halves of the picture (creation and verification).
- Data masking and backups, reduced to one short section (see (c)).

## (c) Dropped and why

- "Encryption dates back to at least 1900 BC ... tomb wall" and the Egyptian bullet: pasted history from the Auth0 post, not fundamental.
- The "Modern encryption algorithms" bullet list: AES, RSA, ECC and AEAD are now named in the sentence where each does its job, not as a catalogue. RSA is no longer expanded (the old expansion was misspelt "Adlemen").
- The "Techniques" H2 and the H3 structure: replaced by one H2 per primitive.
- The "three key properties" framing: the page now lists four, matching the table (the audit's INCONSISTENT finding).
- Data masking and backups: kept, but as a two-sentence section "Controls that are not cryptography", framed by the page's question (masking shows only part of a value and hides the rest, with no key and no way back, so it is redaction; backups protect availability, which is not one of the four properties). Masking links to Data Privacy. I did not move the text into Data Privacy because the brief restricts edits to this file. Recommendation: Data Privacy is the better home for masking; add one line there and the section here can shrink to a link.

## (d) Added, with sources

- Two-question opener (who holds the key, is it reversible) and the "How to rederive this" bullets: derivation, matches NIST SP 800-57 Part 1's mapping of key types to security services.
- Encryption alone gives no integrity; a flipped ciphertext bit in a stream or counter mode flips the same plaintext bit, hence AEAD: Ferguson, Schneier and Kohno, Cryptography Engineering (secure channel chapter).
- Key distribution: every pair needs its own key and the first key needs an already-secure channel; asymmetric changes this into trusting that a public key belongs to a party, which certificates solve: Cryptography Engineering; link to TLS Certificates.
- Asymmetric is orders of magnitude slower and RSA can only encrypt something smaller than its own key, so it carries keys and signatures, not data: Cryptography Engineering (RSA chapter).
- TLS uses ephemeral Diffie-Hellman for key agreement plus a signature for authentication; TLS 1.3 removed RSA key transport: RFC 8446. Links to ../networking/TLS.md (linked as "the TLS page" because its H1 is currently "HTTPS" and it is being rewritten this phase; no anchor used).
- Hash has no key so it cannot authenticate; it detects change only if the digest arrives by a trusted path: derivation.
- Collision resistance matters because signatures sign the hash: Cryptography Engineering (hash functions chapter).
- Content addressing example (git names objects by hash): common knowledge, no source needed.
- MAC gives no non-repudiation because the key is shared so the receiver could have made the tag: Cryptography Engineering (MAC chapter); NIST SP 800-57.
- Signature: hash then sign with the private key; proof convinces a third party; holds only while the private key is private and the key-identity binding is trusted: Cryptography Engineering (signatures chapter).
- Password hashing threat model (offline guessing; user pays once per login, attacker once per guess; memory-hardness because GPUs and ASICs have cheap compute and expensive memory; salt makes each guess cost one account): OWASP Password Storage Cheat Sheet.
- URL encoding added beside Base64 as a second encoding example: common knowledge.
- Sources section listing Cryptography Engineering, OWASP Password Storage Cheat Sheet, NIST SP 800-57 Part 1, RFC 8446 and the original Auth0 post as the origin of the table.

No WebSearch was used; every dated or numeric fact is carried over from Phase 2 (already audited) or is a definitional claim from the named books and standards.

## (e) Diagrams for Phase 5

- Redraw `images/password-hashing.png` as `password-hashing.drawio.svg` per the wiki plan, adding the "slow, memory-hard KDF" label; the current picture still matches the text so the embed stays for now.
- Draw `digital-signature.drawio.svg` (sign with private key over the hash, verify with public key) for the Digital signatures section; the orphan `images/message-signing.jpg` was not embedded. A useful variant would put MAC (shared key, both sides can produce the tag) next to signature (one private key) to picture the non-repudiation difference.

## (f) Open questions for the owner

1. Length: the page is about 340 prose words over the 1,100 target. If it must come down, the candidates are the Caesar paragraph, the content-addressing example, or the "Controls that are not cryptography" section (if masking moves to Data Privacy).
2. Should masking and backups leave this page entirely once Data Privacy has a masking line? The Data Privacy page currently has no masking content, so I did not remove them.
3. The `**Kind of keys**` row is still bold data inside the table (audit BROKEN Low). I kept it because the row is the owner's and does the work of the "who holds the key" question; it could become a plain row or a sentence.
4. The Auth0 post remains in Sources as the origin of the table. Remove it if you would rather not credit a source the table had to be corrected against.
5. `fundamentals/networking/TLS.md` still has H1 "HTTPS" and describes RSA key transport as current; this page says TLS 1.3 removed it. The TLS rewrite in this phase should resolve that; the link here is to the file, not to any claim in it.
