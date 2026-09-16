# TLS

HTTPS is HTTP inside TLS, which gives a connection three properties, each from a different primitive (table in [Cryptography Basics](../security/Cryptography%20Basics.md)):

* Confidentiality: your **data is private**. Symmetric encryption under a key only the two ends know.
* Integrity: your **data hasn't changed** in transit. Each record carries a MAC under that key; in TLS 1.3 encryption and MAC come from one AEAD cipher, AES-GCM or ChaCha20-Poly1305.
* Authenticity: you know **who** you are talking to. The server proves it holds the private key a certificate authority has tied to its DNS name.

## Where TLS sits

TLS wraps HTTP transparently: in the four-layer model of [Network Layers](Network%20Layers.md) it is an application-layer protocol over TCP, invisible to everything below. HTTP/3 is the exception: QUIC builds TLS 1.3 into the transport (see [HTTP](../web%20and%20apis/HTTP.md)).

## Versions

* 1.0 and 1.1: deprecated by RFC 8996 (2021), disabled in every major browser.
* 1.2 (2008): still common and only as good as its configuration, since it allows RSA key transport and older ciphers alongside ephemeral Diffie-Hellman and AEAD.
* 1.3 (RFC 8446, 2018): the target. Only AEAD ciphers, only ephemeral key exchange (forward secrecy is mandatory), one round trip, and everything after the server's first message is encrypted, certificate included. 0-RTT resumption puts a returning client's data in its first message; it can be replayed, so accept only idempotent requests there.
* 2025: the hybrid post-quantum group X25519MLKEM768 (X25519 with ML-KEM) is becoming the default key exchange in browsers and OpenSSL 3.5, so traffic recorded today stays safe from a future quantum computer.

## The handshake, rederived for TLS 1.3

Browser ----------------> website (e.g. `example.com`)

The client speaks first: its versions and cipher suites plus an **ephemeral key share**, a fresh Diffie-Hellman public value for this connection only.

The server replies with its own key share, its certificate chain, a **signature over the handshake so far** by the certificate's private key, and a Finished message, an HMAC over the transcript that catches any alteration.

Each side combines its private value with the other's public value; both get the same secret, never sent, and derive session keys from it and the transcript. The client verifies the certificate and signature, sends its own Finished, and data flows.

The certificate's key **signs**; it never encrypts the session secret. Both sides contribute to the secret, so neither chooses it alone.

Browsers ship the trusted CAs' public keys to check certificates:

`cert = Sign_CA(dnsName, publicKey)` and `Verify_CA_pk(cert) = ok?`

### Why RSA key transport was removed

Up to 1.2 the browser could instead pick a random secret and encrypt it to the certificate's public key, `c = E_pk(secret)` and `secret = D_sk(c)`, then encrypt the traffic under it, `c = E_secret(plaintext)`.

One long-term key then protects every session ever made under that certificate: whoever recorded traffic and later gets the key (break-in, court order, Heartbleed) reads all of it. Ephemeral Diffie-Hellman discards its private values at close, so a leaked key allows impersonation in future but not reading the past. That is **forward secrecy**, mandatory in 1.3 since RSA key transport is gone; RSA survives only for signatures.

## What the certificate proves

The handshake signature proves the server holds the private key; the certificate proves that key belongs to the name the client typed. The client checks that the hostname is in the Subject Alternative Names, the time is within validity, the signature chain leads through an intermediate CA to a root in its trust store, and nothing in it is revoked.

Intact chain, wrong name: a real server, just not the one asked for. That is the name-mismatch warning. Requesting, encoding, renewing and revoking them is in [TLS Certificates](TLS%20Certificates.md).

## Server Name Indication

IPv4 addresses are scarce, so one address hosts many names, and the server must pick a certificate before HTTP starts and the `Host` header arrives. **Server Name Indication** (SNI, RFC 6066) fixes this: the client puts the hostname in its first message and the server picks the matching key and chain.

The cost: the hostname travels in clear text, so an observer sees which site you visit. **Encrypted Client Hello** (ECH) is being deployed to close that gap.

## Mutual TLS

Rather than only the server identifying itself, clients can also identify themselves with certificates. The server asks for one in the handshake and validates it against its configured root CAs. Only if the certificate is valid, and only if its name or DN is in the server's list of trusted identities, is the client deemed trustworthy. It is presented per handshake, so per connection, not per request.

[Proxy authentication](https://search-guard.com/elasticsearch-proxy-authentication-certificates/) delegates authentication and authorisation to a proxy in front of a service; mutual TLS is how proxy and service trust each other. A service mesh does the same in Kubernetes: each pod's sidecar holds a short-lived certificate with a SPIFFE workload name and speaks mutual TLS to the others ([Kubernetes](../platform/Kubernetes.md)).

Traditionally **IP based trust** was used instead, a list of IPs the server trusts; that breaks down where services come and go without fixed IPs.

## How to rederive this

* How do strangers share a key? Diffie-Hellman, signed with a key the client already trusts, else a man in the middle runs DH with each side.
* What if the server's key leaks later? Recorded sessions encrypted under it are readable, so 1.3 kept only ephemeral DH.
* What must the server know to pick a certificate? The hostname, before HTTP, so SNI goes in clear and ECH follows.
* When can a client certificate be checked? Where the server's is, in the handshake, so per connection.

## Sources

* RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3 (2018).
* RFC 8996, Deprecating TLS 1.0 and TLS 1.1 (2021).
* RFC 6066, TLS Extensions: Extension Definitions (Server Name Indication).
* Mozilla, Server Side TLS guidelines (wiki.mozilla.org/Security/Server_Side_TLS).
* Cloudflare Learning Center, "What happens in a TLS handshake?", and the Cloudflare blog on post-quantum key agreement.
* SPIFFE project, spiffe.io.
