# Cryptography Basics

## Techniques

Data security involves [three key properties](https://auth0.com/blog/how-secure-are-encryption-hashing-encoding-and-obfuscation/): confidentiality, integrity and authenticity.

| Security Goal         | Hash | MAC       | Digital Signature| Encryption               |
|:----------------------|:-----|:----------|:-----------------|:-------------------------|
|Integrity              |  Yes |    Yes    |   Yes            |   No                     |
|Authentication         |  No  |    Yes    |   Yes            |   No                     |
|Confidentiality        |  No  |    No     |   No             |   Yes                    |
|Non-repudiation        |  No  |    No     |   Yes            |   No                     |
|**Kind of keys**       | none | symmetric | asymmetric       | symmetric or asymmetric  |

A MAC or a digital signature is computed over plaintext and hides nothing. Only encryption provides confidentiality. AEAD modes (AES-GCM, ChaCha20-Poly1305) combine encryption with a MAC so one operation gives confidentiality, integrity and authenticity.

### Data masking

Hiding sensitive information to prevent unintentional leakage

### Data backups

Redundant storage for maintaining copies of data

### Encryption

Encryption is a two-way function where information is scrambled in such a way that it can be unscrambled later. You encrypt information with the intention of decrypting it later.

Encryption dates back to at least 1900 BC after the discovery of a tomb wall with non-standard hieroglyphs chiseled into it.

* The ancient Egyptians used a simple form of encryption.
* Caesar used a primitive shift cipher that changed letters around by counting forward a set number of places in the alphabet. It was extraordinarily useful though, making any information intercepted by Caesar’s opponents practically useless.

Modern encryption algorithms:

* AES Advanced Encryption Standard
* RSA Rivest-Shamir-Adlemen
* ECC Elliptic Curve Cryptography
* AEAD modes: AES-GCM, ChaCha20-Poly1305

OpenPGP (PGP, GnuPG) is a message format, not an algorithm. It uses RSA or ECC for keys and AES for the message body.

Usage

* Store sensitive data that must be retrieved (unlike passwords); e.g., credit card information.
* Protect network traffic; e.g., Wi-Fi Protected Access, Transport Layer Security, Virtual Private Networking.
* Protect data within storage media in the event of physical theft; e.g., full disk encryption.

### Hashing

Hashing is a one-way function where data is mapped to a fixed-length value. Hashing is primarily used for performing integrity checks on data. A **hash** is a fixed-length code, generally shown as hexadecimal, that represents a dataset e.g a file. A cryptographic hash is designed to have three properties:

* **preimage resistance** - given a hash, it is infeasible to find any input that produces it. This is what makes the function one-way.
* **second-preimage resistance** - given an input, it is infeasible to find a different input with the same hash. In practice any change to the input changes the hash.
* **collision resistance** - it is infeasible to find any two inputs with the same hash. Collisions always exist, because there are more possible inputs than outputs (the pigeonhole principle). The property is that nobody can find one.

General-purpose cryptographic hashes such as SHA-256 are designed to be fast. Non-cryptographic hashes used in hash tables only need to spread inputs evenly to keep collisions rare; they offer no collision resistance in the cryptographic sense.

Usage

* A **checksum** is necessarily a hash, however not all hashes are checksums (one's used in hash tables) but if you can afford the computational cost, a cryptographically strong hash code is a good checksum. A cryptographic hash is designed to be computationally infeasible to reverse, whereas a checksum is designed to detect data integrity errors and often to be fast to compute.

* **Password hashing** uses a "Salt" - a random value, unique per password, that is combined with the password before hashing and stored alongside the hash. Two users with the same password get different hashes, which defeats precomputed (rainbow) tables. Unlike general-purpose hashes, password hashes are designed to be slow and memory-hard so that brute force is expensive. Use a dedicated password hashing function, not plain SHA-256. OWASP Password Storage Cheat Sheet recommendations as of 2024: Argon2id (19 MiB memory, 2 iterations, parallelism 1) as the first choice; scrypt (N=2^17, r=8, p=1) if Argon2id is unavailable; bcrypt (work factor 10 or more) for legacy systems; PBKDF2-HMAC-SHA256 with 600,000 iterations where FIPS compliance is required.  

  ![password-hashing.png](../../images/password-hashing.png "Password Hashing")

* **Hash-based Message authentication codes (HMACs)** are keyed hashes. Sender and receiver share a secret key; the receiver recomputes the HMAC and, if it matches, knows the message is intact and came from a holder of the key. Hashing the same message with the same key always gives the same HMAC, so a captured message could be replayed. To prevent this a **nonce** (one-time value) or timestamp is included in the message that is authenticated; the receiver rejects a repeated nonce. The nonce does not change the MAC algorithm itself.

### Encoding

Encoding is the process of converting data from one form to another and has nothing to do with cryptography. It guarantees none of the 3 cryptographic properties of confidentiality, integrity, and authenticity because it involves no secret and is completely reversible. Encoding methods are considered public and are used for data handling when data is sent over the wire. Base64 is a way to encode binary data into an ASCII character set known to pretty much every computer system, in order to transmit the data without loss or modification of the contents.
