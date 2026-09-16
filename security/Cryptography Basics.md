# Cryptography Basics

Ask two things of a primitive: who holds the key, and can it be reversed.

## The four properties

* **Confidentiality**: only the intended reader can read it.
* **Integrity**: it has not changed since it was written.
* **Authenticity**: it came from the party it claims to.
* **Non-repudiation**: the sender cannot deny it later; a third party can check the proof.

| Security Goal         | Hash | MAC       | Digital Signature| Encryption               |
|:----------------------|:-----|:----------|:-----------------|:-------------------------|
|Integrity              |  Yes |    Yes    |   Yes            |   No                     |
|Authentication         |  No  |    Yes    |   Yes            |   No                     |
|Confidentiality        |  No  |    No     |   No             |   Yes                    |
|Non-repudiation        |  No  |    No     |   Yes            |   No                     |
|**Kind of keys**       | none | symmetric | asymmetric       | symmetric or asymmetric  |

A MAC or signature is computed over plaintext and hides nothing; only encryption gives confidentiality. AEAD modes (AES-GCM, ChaCha20-Poly1305) combine encryption with a MAC, so one operation gives confidentiality, integrity and authenticity.

## Symmetric encryption

Encryption is two-way: scrambled so it can be unscrambled later. Symmetric means one shared key for both directions. AES and ChaCha20 are fast, so they carry bulk data: card numbers that must be read back later (unlike passwords), TLS traffic, disk encryption.

Encryption alone gives no integrity: tampered ciphertext decrypts to different plaintext rather than failing, and in a stream or counter mode one flipped ciphertext bit flips the same plaintext bit.

Nor does it solve **key distribution**: the key needs a channel that is already secure, and every pair of parties needs its own.

## Asymmetric encryption

A key pair: the public key is published, the private key never leaves its owner. The public key encrypts what only the private key can decrypt, and verifies what only the private key could have signed. Key distribution becomes trust that a public key belongs to who you think; [certificates](../networking/TLS%20Certificates.md) answer that.

Asymmetric operations are orders of magnitude slower than AES, and RSA can only encrypt something smaller than its own key. So it agrees a symmetric key and signs, and bulk data goes under the symmetric key. [TLS](../networking/TLS.md) does this: ephemeral Diffie-Hellman for key agreement, a signature for authentication. TLS 1.3 removed encrypting the session key with the server's RSA public key.

RSA and elliptic curve (ECC) are the key pairs in common use. OpenPGP (PGP, GnuPG) is a message format, not an algorithm: RSA or ECC for keys, AES for the body.

## Hashing

A hash is a one-way function from data of any length to a fixed-length value, usually shown as hexadecimal. A cryptographic hash has three properties:

* **preimage resistance**: given a hash, it is infeasible to find any input that produces it. This is what makes it one-way.
* **second-preimage resistance**: given an input, it is infeasible to find a different input with the same hash. Any change to the input changes the hash.
* **collision resistance**: it is infeasible to find any two inputs with the same hash. Collisions exist, there are more inputs than outputs (the pigeonhole principle); nobody can find one.

No key, so integrity only: anyone can compute it. It detects change only if the digest reaches you by a path the attacker cannot touch. Signatures sign the hash, not the message, so two documents with one digest share one valid signature.

SHA-256 and other general-purpose hashes are fast, for integrity checks, content addressing and signing. Hash-table hashes only need to spread inputs evenly; no collision resistance in the cryptographic sense. A checksum is a hash used to detect accidental errors: necessarily a hash, but not every hash is a checksum.

> Own view: if you can afford the computational cost, a cryptographically strong hash code is a good checksum.

## MAC and HMAC

A MAC is a short tag over the message with a shared key; HMAC builds one from a hash. The receiver recomputes it; a match means the message is intact and came from a key holder. No non-repudiation: the receiver holds the same key, so a third party cannot tell which of the two made the tag.

The same message and key always give the same HMAC, so a captured message could be replayed. A **nonce** (one-time value) or timestamp goes in the authenticated message and the receiver rejects a repeat. The nonce does not change the MAC algorithm.

## Digital signatures

Hash the message, apply the private key to the digest; anyone with the public key can verify. One party holds the private key, so a valid signature proves that party produced the message, to a third party, not just the receiver: non-repudiation, which a MAC cannot give. It holds only while the private key stays private and the verifier trusts the binding of key to identity.

## Password hashing is a different job

A password is only checked, never read back, so hash it. The attacker has stolen the table and guesses offline: the user pays one hash per login, the attacker one per guess. So password hashes are deliberately slow and memory-hard; memory-hard because GPUs and ASICs have cheap compute but expensive memory.

A **salt** is a random value, unique per password, mixed in before hashing and stored next to the hash. Two users with the same password get different hashes, which defeats precomputed (rainbow) tables, and each guess costs the attacker one account, not the whole table.

Use a dedicated password hashing function, not plain SHA-256. OWASP Password Storage Cheat Sheet, as of 2024: Argon2id (19 MiB memory, 2 iterations, parallelism 1) first; scrypt (N=2^17, r=8, p=1) if Argon2id is unavailable; bcrypt (work factor 10 or more) for legacy systems; PBKDF2-HMAC-SHA256 with 600,000 iterations where FIPS compliance is required.

![Password creation: the password and a random salt go through the hash and the salt is stored with the hash. Verification: the entered password and the stored salt go through the same hash and the result is compared with the stored hash](../images/password-hashing.png "Password hashing with a per-password salt")

## Encoding is not encryption

Encoding changes the representation of data. No key and anyone can reverse it, so none of the four properties. Base64 turns binary into ASCII that survives text-only channels; URL encoding does the same for characters that mean something in a URL.

## Controls that are not cryptography

**Data masking** (the last four digits of a card) is redaction (no key, no way back), see [Data Privacy](Data%20Privacy.md); **backups** protect availability, not one of the four properties.

## How to rederive this

* Who holds the key: nobody (hash), both (MAC, symmetric), one (signature, asymmetric). Nobody means no authentication; both means no non-repudiation; one gives both.
* Reversible with a key: encryption. Not reversible: integrity at most. Reversible without a key: encoding, nothing.
* Decryption does not fail on tampering, so integrity needs a MAC; AEAD is both.
* Asymmetric is slow and size-limited, so it carries keys and signatures, never data.
* A password is only checked, so hash it; the attacker guesses offline, so slow and salted.

## Sources

* Ferguson, Schneier and Kohno, *Cryptography Engineering* (hash properties, MAC vs signature, why to use AEAD)
* OWASP Password Storage Cheat Sheet (algorithm choice and parameters)
* NIST SP 800-57 Part 1, *Recommendation for Key Management* (which key type gives which security service)
* RFC 8446, TLS 1.3 (removal of RSA key transport)
* The table began from an Auth0 post, [How secure are encryption, hashing, encoding and obfuscation](https://auth0.com/blog/how-secure-are-encryption-hashing-encoding-and-obfuscation/), corrected here
