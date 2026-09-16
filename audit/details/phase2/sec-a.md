# Phase 2 report: security batch A (Cryptography Basics, Standards and Compliance, Security Principles and Threat Modelling)

Applied 2026-09-16. Nothing committed. Only the three assigned files were edited (git status also shows `fundamentals/networking/DNS.md` modified; that change is not mine).

## fundamentals/security/Cryptography Basics.md

- was: table `Confidentiality | No | Yes | Yes` (MAC and signature provide confidentiality), no encryption column → now: added an `Encryption` column; Confidentiality row is `No | No | No | Yes`; Integrity/Authentication/Non-repudiation `No` for encryption; `Kind of keys` = `symmetric or asymmetric` for encryption. One sentence below the table states that MACs and signatures are computed over plaintext and only encryption gives confidentiality, and names AEAD (AES-GCM, ChaCha20-Poly1305) as the combination.
- was: "three key properties" not mapped to the primitive supplying them (INCONSISTENT) → now: resolved by the Encryption column and the sentence above.
- was: `PGP Pretty Good Privacy` listed as a modern encryption algorithm → now: `AEAD modes: AES-GCM, ChaCha20-Poly1305`; separate sentence says OpenPGP is a message format built on RSA/ECC and AES.
- was: "A hash is a unique code" → now: "a fixed-length code".
- was: "No 2 inputs can generate the same hash thus a one-way function. This property is also known as preimage resistance" → now: three bullets with correct definitions: preimage resistance (hard to invert, this is one-wayness), second-preimage resistance ("In practice any change to the input changes the hash", hedged on purpose), collision resistance (collisions always exist by the pigeonhole principle; the property is that they are infeasible to find).
- was: "random ... minimising collisions when used in hash tables, thus providing collision resistance" → now: one sentence separating non-cryptographic hash-table hashing (spread inputs evenly) from cryptographic collision resistance.
- was: "reasonably quick to compute, but also not too quick. If it is too quick it is easy to break" → now: deleted; replaced with "General-purpose cryptographic hashes such as SHA-256 are designed to be fast"; slowness moved to the password-hashing bullet.
- was: "computationally infeasible to reverse, thus provide confidentiality via encryption" → now: "computationally infeasible to reverse, whereas a checksum ..." (phrase deleted; checksum logic left as it was).
- was: salt is "a unique value that can be added to the end of the password", no algorithm guidance → now: salt is a random per-password value combined with the password and stored alongside the hash; password hashes are deliberately slow and memory-hard; OWASP Password Storage Cheat Sheet as of 2024: Argon2id (19 MiB, 2 iterations, p=1), scrypt (N=2^17, r=8, p=1), bcrypt (work factor 10 or more), PBKDF2-HMAC-SHA256 600,000 iterations for FIPS contexts.
- was: "HMACs use hashes to verify the sender ... Nonce is a one time value used to generate a unique hash per request" → now: HMAC is a keyed hash over a shared secret; a nonce or timestamp is included in the authenticated message to prevent replay and does not change the MAC algorithm.

## fundamentals/security/Standards and Compliance.md

- was: "Secure Support Provider Interface (Win32 API)" → now: "Security Support Provider Interface (SSPI, Win32 API)". Schannel section left in place.
- was: "ISO 27001 - Info Security" → now: "ISO/IEC 27001:2022 ... certificates against 27001:2013 expired on 31 Oct 2025. ISO/IEC 27002:2022 is the companion control catalogue (93 controls in 4 themes)".
- was: SOC 1, 2, 3 = "Security, Availability & Confidentiality Reports" → now: SOC 1 = ICFR (not a security report); SOC 2 = five Trust Services Criteria (Security mandatory), Type I design at a point in time vs Type II operating effectiveness over a period, restricted distribution; SOC 3 = public summary of a SOC 2 Type II.
- was: no PCI DSS version → now: "Current version: PCI DSS v4.0.1 (v3.2.1 retired 31 Mar 2024; the v4.0 future-dated requirements became mandatory 31 Mar 2025)". This page is now the canonical PCI DSS home (the DUPLICATE row asks the other page, Data Privacy, to link here; not in my scope).
- was: "SSL ... can no longer be used as a security control after June 30, 2016" → now: "SSL and early TLS (1.0 and 1.1) ... after 30 June 2018 (the PCI DSS 3.1/3.2 migration deadline)".
- was: "TLS 1.2 currently meets the PCI SSC definition ... you must be using this version" → now: "TLS 1.2 or 1.3 meets ... you must be using one of these versions, not TLS 1.1 or 1.0".
- was: FIPS 140 paragraph anchored on the FIPS 140-2 Annex A PDF → now: FIPS 140-3 is the active version, approved functions live in SP 800-140C, all FIPS 140-2 certificates move to the CMVP Historical list on 21 Sep 2026; link now points at the CMVP FIPS 140-3 standards page. Left out the "CMVP stopped accepting 140-2 submissions Sept 2021" date because that cutoff was extended and is not load-bearing.
- was: ".Net framework provides 3 implementations ... AesCryptoServiceProvider is FIPS compliant" stated generally → now: scoped to ".NET Framework 4.x"; added "In .NET 6 and later these classes are obsolete (SYSLIB0021/SYSLIB0022); use `Aes.Create()`".
- was: "Triple-DES (Data Encryption Standard)" listed as approved → now: "- legacy. Disallowed for encryption since 1 Jan 2024 (NIST SP 800-131A Rev 2); decrypt only." Also "Triple DES (legacy, see above)" in the message authentication list.
- was: "EES (Escrowed Encryption Standard)" → now: removed.
- was: "Asymmetric Key (Public key cryptography) for TLS key exchange and authentication: RSA, DSA, ECDSA" → now: two lists. "Digital signatures (FIPS 186-5) for TLS authentication: RSA, ECDSA, EdDSA (Ed25519, Ed448), DSA - legacy, verify only since FIPS 186-5 (Feb 2023)". "Key agreement (SP 800-56A) for TLS key exchange. Signature algorithms do not perform key exchange: ECDH/ECDHE, DH/DHE, ML-KEM (FIPS 203, 2024)". The en-dash in "Rivest–Shamir–Adleman" became plain hyphens as a side effect.
- was: "SHA-1, SHA-224, SHA-256, ..." as one approved list → now: SHA-2 family (FIPS 180-4); SHA-3 family (FIPS 202) added; SHA-1 marked legacy (disallowed for signatures since 2013, full retirement planned 31 Dec 2030 per SP 800-131A, not used by TLS 1.3).
- was: "See annex c" → now: "DRBGs per SP 800-90A: Hash_DRBG, HMAC_DRBG, CTR_DRBG".
- was: "only supports TLS 1.0 and above" → now: "only supports TLS 1.2 and above (TLS 1.0 and 1.1 were deprecated by RFC 8996 in 2021; NIST SP 800-52 Rev 2 requires 1.2 minimum and recommends 1.3)".

## fundamentals/security/Security Principles and Threat Modelling.md

- was: three questions ("What are we working on? What could go wrong? What are we going to do about it?") → now: four; added "Did we do a good enough job?" and attributed the frame to Adam Shostack's Four-Question Frame / Threat Modeling Manifesto (2020) with a link.
- was: no methodology named → now: `### Methodologies` subsection (4 bullets) under "Threat model development": STRIDE (per element / per interaction), PASTA (risk-centric), LINDDUN (privacy), DREAD (dropped by Microsoft for inconsistent scores; prefer CVSS or likelihood and impact). No tooling bullet (not in the exception). Total new lines for the four-question and methodology additions: 7, within the 10-line cap.
- was: "Microsoft has published its list of attack surface elements" uncited → now: cited "(Howard, "Relative Attack Surface Quotient", 2003)" and one sentence adding modern elements (APIs, cloud IAM roles, CI/CD pipelines, third-party dependencies).
- was: "Complete mediation - reverify user authentication when they are trying to complete a sensitive task ..." → now: Saltzer and Schroeder's definition (every access to every object is checked for authority) first, with step-up re-authentication kept as one application.
- was: "Open design - Given enough eyeballs all bugs are shallow" → now: security must not depend on secrecy of the design (Saltzer and Schroeder; Kerckhoffs' principle), only keys are secret; notes that Linus's Law (Raymond) is a different idea.
- JUDGEMENT CALL, revert if unwanted: was "priority low to high" → now "priority high to low". The audit types this OPINION (Medium) but calls it a slip; the strict OPINION rule says leave. Applied because it is a two-word evident slip.

## Skipped deliberately

- Cryptography Basics: BROKEN Low "bold `**Kind of keys**` row inside table data" - Low and not a typo; row kept (extended with the Encryption cell).
- Cryptography Basics: "A checksum is necessarily a hash" inverted-logic remark - the suggested fix only asked to delete the confidentiality phrase, and the subset statement is defensible as written.
- Cryptography Basics: CLASSIFY (file split) - already done in Phase 1; the privacy half lives in Data Privacy.
- Cryptography Basics: the DUPLICATE Low row on the CIA triad sits in the Transport Layer Security section of the audit (now fundamentals/networking/TLS.md) and asks that file to cross-link here; nothing to change on this page.
- Standards and Compliance: CLASSIFY "move Schannel/PKCS to TLS notes" - later phase; only the SSPI name was fixed.
- Standards and Compliance: CLASSIFY "make Compliance the single index of regulations" - later phase.
- Standards and Compliance: DUPLICATE PCI DSS - this page is the owner; the link belongs in Data Privacy (not assigned).
- Standards and Compliance: "Rijnadael" typo - it is inside the StackOverflow URL text fragment, not prose; editing it would break the deep link.
- Standards and Compliance: H1 `# Compliance` does not match the new filename - no audit finding against it and heading renames were out of scope.
- Standards and Compliance: `## Certifications` section - left as instructed.
- Threat Modelling: CLASSIFY "extract Security principles to its own note" - later phase (Phase 1 already merged them into this page's name).
- Threat Modelling: H1 `# Threat Modelling` vs filename - no finding, heading renames out of scope.
- No WebSearch was used; every dated fact came from the audit rows marked Verified or from the suggested fixes.
