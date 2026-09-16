# Phase 3 report: TLS.md (and the two permitted edits to TLS Certificates.md)

Files changed (not committed):

- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/networking/TLS.md (full rewrite, 1,514 words including headings and Sources; body about 1,400)
- /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/networking/TLS Certificates.md (SNI section removed; `## Certificate types` appended; nothing else touched)

## (a) The question the page now answers

How does HTTPS give confidentiality, integrity and authenticity, and where do certificates fit? The first paragraph answers it: symmetric AEAD encryption for confidentiality and integrity, a certificate-backed signature over the handshake for authenticity, and the handshake exists to get two strangers to a shared key with the server verified. The page then rederives the TLS 1.3 handshake, explains why RSA key transport was removed (forward secrecy), what the certificate check actually proves, SNI, mutual TLS, and ends with `## How to rederive this` and `## Sources`.

## (b) Kept from the original

- The three-bullet triad with the owner's bold phrasing ("data is private", "data hasn't changed", "who you are talking to"), corrected so integrity is attributed to the MAC/AEAD tag rather than to signing.
- "The TLS protocol is implemented as a transparent wrapper around the HTTP protocol" and the sits-between-HTTP-and-TCP intuition.
- The `Browser ----------------> website` arrow.
- The owner's formula notation, now inline code: `cert = Sign_CA(dnsName, publicKey)`, `Verify_CA_pk(cert) = ok?`, `c = E_pk(secret)`, `secret = D_sk(c)`, `c = E_secret(plaintext)`.
- The observation that browsers ship with the CAs' public keys.
- The mutual TLS paragraph (validate against configured root CAs, DN list, proxy authentication link) and the whole IP-based trust paragraph, lightly tightened.
- From TLS Certificates.md, the owner's SNI sentences (IPv4 scarcity motivation, client names the host in the handshake, server picks the key and chain; Apache, Nginx, HAProxy as examples), moved into TLS.md.
- In the new `## Certificate types` section of TLS Certificates.md: the two "how reputable is the CA / how well does the CA check" questions, the DV/OV/EV descriptions with the `<Not Part Of Certificate>` and `Mozilla Corporation` examples, the Troy Hunt link, the RFC 5280 Certificate Policies explanation, the OID example block, and the unmitigatedrisk.com link about programmatic use of OIDs.

## (c) Dropped and why

- Lines 9-13 ("Valid TLS certificate / Secure TLS connection / Secure resources"): DevTools Security-panel phrasing, not a concept; nothing was lost that the rest of the page does not say.
- The security.stackexchange "what layer is TLS" link and "between layer 4 and 7": replaced by the wiki's own layering convention with a link to Network Layers.md.
- The RSA-key-transport handshake description (line 35) and "The two most popular key exchange algorithms are RSA ... and Diffie-Hellman" (line 44): WRONG for TLS 1.3. Replaced by the ECDHE-plus-signature derivation, with RSA key transport kept only as a historical paragraph explaining forward secrecy. The jscape.com key-exchange link went with it.
- All six latex.codecogs.com images: replaced by inline code as the brief asked.
- "$5 to thousands of dollars": DV is free via ACME; reworded in the moved section.
- "EV ... displayed along with the URL in the browser (Chrome & Firefox) address bar": STALE since 2019; corrected in the moved section.
- "The client sends a TLS client certificate for every request": WRONG; now "once per handshake, so once per connection, not once per HTTP request".
- The NAT/CIDR/IPv6 tangent in the old SNI section: belongs to IP Addressing.md, and the globalsign SNI link is replaced by RFC 6066.
- `hemantkumar.net` in the OID example: personal data rule; replaced with `example.com` and labelled a snapshot from an older Let's Encrypt certificate.
- In TLS Certificates.md, `## Server hosting multiple TLS certificates` is removed in full; grep shows no inbound links to that anchor.

## (d) Added, with sources

- Integrity comes from the AEAD tag, not from signing; AES-GCM and ChaCha20-Poly1305: RFC 8446 section 9.1 (mandatory cipher suites), matches the table already in Cryptography Basics.md.
- TLS as application-layer over TCP in the TCP/IP model: the convention stated in Network Layers.md line 3. QUIC carrying TLS 1.3 for HTTP/3: RFC 9000/9001, already stated in HTTP.md.
- TLS 1.0/1.1 deprecated by RFC 8996 (March 2021). TLS 1.2 is RFC 5246 (2008).
- TLS 1.3 (RFC 8446, August 2018): one round trip, AEAD only, ephemeral key exchange only, encrypted handshake after ServerHello including the certificate, 0-RTT. The 0-RTT replay caveat is RFC 8446 section 8 and appendix E.5.
- Hybrid post-quantum X25519MLKEM768 becoming the default in major browsers and OpenSSL 3.5 "as of 2025": brief's wording; Chrome 131 and Firefox 132 (late 2024) and the OpenSSL 3.5 release notes (April 2025). No browser version numbers in the page.
- Handshake details: the server's signature is CertificateVerify over the transcript hash; Finished is an HMAC over the transcript; keys are derived from the DH secret and the transcript (RFC 8446 sections 4.4.3, 4.4.4, 7.1).
- Forward secrecy argument and "RSA survives in 1.3 only as a signature algorithm": RFC 8446 section 1.2 (removed static RSA and DH key exchange) and section 4.2.3.
- Certificate checks (SAN match, validity window, chain to a trust-store root, revocation): RFC 5280 and RFC 6125. The "CN is ignored" fact is already on TLS Certificates.md.
- SNI is RFC 6066 section 3; it is sent in clear text in ClientHello. Encrypted Client Hello is the IETF draft (draft-ietf-tls-esni) deployed by Cloudflare, Firefox and Chrome; the page says only "being deployed".
- Mutual TLS is per connection: RFC 8446 section 4.4.2 (Certificate in the handshake); post-handshake client authentication (section 4.6.2) is still per connection, so the simplification holds.
- SPIFFE and service-mesh sidecars: spiffe.io and the existing Service Mesh section of fundamentals/platform/Kubernetes.md (linked).
- In TLS Certificates.md: Safari 12 (2018), Chrome 77 and Firefox 70 (2019) removed the EV indicator, so the page says "all removed by the end of 2019" without ordering (Apple, Chromium and Mozilla release notes; the audit's "Safari followed" had the order wrong); CA/Browser Forum reserved policy OIDs 2.23.140.1.2.1 (DV), 2.23.140.1.2.2 (OV), 2.23.140.1.1 (EV) from the CA/B Forum Baseline Requirements and EV Guidelines; Certificate Transparency from RFC 6962 and the Chrome/Safari CT policies. The "three times the price" remark is attributed to Troy Hunt (2018). The advice to buy OV/EV only when a checklist demands it is marked `> Own view:`.
- The audit's Let's Encrypt-OID-removed claim was marked Unverified, so the page does not assert it; the OID block is labelled a snapshot from an older certificate.

## (e) Diagrams for Phase 5

- New: `tls-1-3-handshake.drawio.svg`, a sequence diagram: ClientHello (versions, cipher suites, key share, SNI) -> ServerHello (key share) + {Certificate, CertificateVerify, Finished} encrypted -> client Finished -> application data. Label the arrow where the server signs the transcript with the certificate's private key, and the point where both sides derive keys. This replaces the six removed formula images.
- Optional: `certificate-chain.drawio.svg`, leaf signed by intermediate signed by root, root in the browser trust store; could be shared with TLS Certificates.md. The existing `digital-signature.drawio.svg` planned for Cryptography Basics covers the sign/verify primitive, so this one should show only the chain.
- No existing images were embedded in either page, so nothing was removed.

## (f) Open questions for the owner

1. TLS.md is 1,514 words against a 900 to 1,200 target (within the allowed third). The candidates to cut if you want it shorter are the "Where TLS sits" paragraph (could be one sentence plus the link) and the IP-based trust paragraph at the end of Mutual TLS.
2. The search-guard.com proxy authentication link was kept because it carries the owner's sentence about delegating auth to a proxy; it is a vendor blog and could be replaced by a link to Load Balancing and Proxies.md if that page covers the pattern.
3. TLS Certificates.md line 80 still contains an em-dash and smart quotes from the original text; out of scope for this assignment (Phase 2 corrected that page) but worth a one-line fix in Phase 5's sweep.
4. The `## Certificate types` section is appended at the end of TLS Certificates.md, after revocation. If you prefer it directly after `## Certificate generation` (where CA vetting is first mentioned), that is a pure move.
5. The page says ECH is "being deployed" without naming who; if you want a source line, Cloudflare's 2023 ECH announcement and the Firefox 118 release notes are the ones to cite.
6. The `> Own view:` block in Certificate types (buy OV or EV only when a checklist or compliance regime demands it) is my draft from the brief's "EV has little practical security value", not a sentence you wrote. Confirm, reword or delete it.
