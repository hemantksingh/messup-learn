# TLS Certificates

In order to secure communication between two devices or machines the following three things are required:

1. Unique Identity - each device needs to have a unique identity. Like a username provides identity to a person a device can be identified by a unique id or IP address
2. Identity is independently verifiable - An external authority should be able to attest the identity of the device by signing the device identity and providing a means of verifying that signed identity to others (e.g. by using a X.509 certificate).
3. Verifiable identity is easily accessible and renewable - The verifiable identity should be easy to obtain, renew and revoke.

A public key or [digital certificate](https://certbot.eff.org/docs/what.html) (formerly called SSL certificate) provides 1 and 2 above. Point 3 used to be the weak spot; since 2015 the ACME protocol (Let's Encrypt, certbot) automates issue and renewal, see [Validity limits and automation](#validity-limits-and-automation) below. The certificate includes information about the key, information about the server identity, and the digital signature of the certificate issuer.

## Certificate generation

After a [key pair](https://en.wikipedia.org/wiki/Public-key_cryptography) is generated, the public key needs to be distributed for public usage. A certificate adds identity to a public key. 

A certificate can be self signed or requested from an independent Certificate Authority (CA) that verifies your identity (the process is known as **identity vetting**), creates the certificate and signs it for it to be used in clients that trust the CA.

A [certificate signing request (CSR)](https://www.globalsign.com/en/blog/what-is-a-certificate-signing-request-csr) is a message sent from an applicant to a Certificate Authority to apply for a digital identity certificate. A CSR is created and sent to the CA to be signed and generate a certificate for your domain. It usually contains the public key that will be included in your certificate, identifying information such as a common name (CN), organization (O), country (C), key type and key length. The CA will use the data from the CSR to create your certificate. The CSR may be accompanied by other credentials or proofs of identity required by the certificate authority, and the certificate authority may contact the applicant for further information. The certificate, in addition to containing the public key, contains additional information such as issuer, what the certificate is supposed to be used for and other types of metadata.

A trusted CA will own their CA key and certificate but you can [create your own CA key and certificate with OpenSSL](https://docs.docker.com/engine/security/protect-access/#create-a-ca-server-and-client-keys-with-openssl) as shown below

```sh
# Generate the CA key and certificate
$ openssl req -x509 -sha256 -newkey rsa:4096 \
     -out ca.crt \
     -keyout ca.key \
     -days 365 -nodes \
     -subj '/CN=Demo Cert Authority'

# The applicant creates a private key and CSR for the CA to generate and sign a certificate for the applicant.
# Browsers ignore the CN and require a Subject Alternative Name (Chrome 58, 2017), so a CSR without one
# produces a certificate no browser will accept.
$ openssl req -new -nodes -newkey rsa:4096 \
	-out applicant.csr \
	-keyout applicant.key \
	-subj '/CN=demo.applicant.com/O=applicant-org' \
	-addext "subjectAltName=DNS:demo.applicant.com"

# The CA can approve the CSR or request further information and generates a certificate (public key) for the applicant.
# -copy_extensions copy (OpenSSL 3) carries the SAN from the CSR into the certificate; older versions need -extfile.
$ openssl x509 -req -sha256 -days 365 \
	-in applicant.csr \
	-CA ca.crt -CAkey ca.key \
	-set_serial 01 \
	-copy_extensions copy \
	-out applicant.crt
```
### Certificate encoding formats

Multitude of server and device types that allow an SSL to be installed and configured require the digital certificate file to be encoded and formatted in a certain way. There are various [certificate encoding formats](https://www.ssls.com/knowledgebase/what-are-certificate-formats-and-what-is-the-difference-between-them/) depending upon whether they are Base64 (ASCII) encoded or in binary format.

#### Base64 (ASCII)

* **PEM**
  * .pem - the most common format for an X.509 certificate. This is a (Privacy-enhanced Electronic Mail) Base64 encoded DER certificate, enclosed between `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----`
  * .crt - you can inspect a certificate `openssl x509 -in admin.crt -text -noout | more`
* **PKCS#7**
  * .p7b
  * .p7s

#### Binary

* **DER**
  * .der
  * .cer
* **PKCS#12**
  * .pfx - an archive file format for storing several cryptographic objects. A .pfx file must contain the end-entity certificate (issued for your domain), a matching private key, and may optionally include an intermediate certification authority (a.k.a. CA Bundle). All this is wrapped up in a single file which is then protected with a pfx password. OpenSSL 3 (2021) writes PKCS#12 with AES-256-CBC and PBKDF2; older importers that only understand the legacy RC2/3DES/SHA-1 encoding need the file created with `openssl pkcs12 -export -legacy`.
  * .p12

* Windows uses **PVK files** to store private keys for code signing in various Microsoft products. PVK is proprietary format

## Self signed certificates

As mentioned above a certificate can be self signed or requested from a known global Certificate Authority (CA). Self signed certificates do not go through the independent **identity vetting** process, therefore understandably they cannot be implicitly trusted and are not fit for public usage. However they may be used in development and test environments, provided:

* The self-signed certificate is trusted by importing it into the host's certificate store. On a Linux host trusting the certificate is different and distro dependent. On Windows this can be done using:
  * [Powershell](https://docs.microsoft.com/en-us/dotnet/core/additional-tools/self-signed-certificates-guide#with-powershell) `Import-PfxCertificate -FilePath certificate.pfx -CertStoreLocation 'Cert:\LocalMachine\Root' -Password (ConvertTo-SecureString 'password' -AsPlainText -Force)`
  * `dotnet dev-certs https --trust`
* You create your own private/internal CA that can issue certificates and add trust in your browsers for that CA

In both of these cases, the key point is that the general public will not accept self signed certificates, which is by design — there is no reason that everyone else should believe the contents of your self signed certificates. So developers have to take some action to modify their browsers’ trust behavior in order to accept something that’s not publicly-trusted.

Alternatively, you can purchase a public domain name from somewhere like https://www.namecheap.com/, get it registered and then get a publicly-trusted certificate for it, even if it is for development purposes. The certificate itself is free from an ACME CA such as Let's Encrypt (see [Validity limits and automation](#validity-limits-and-automation)).

## Certificate thumbprint

A thumbprint (or fingerprint) is the SHA-1 or SHA-256 hash of the **whole DER-encoded certificate**, so it identifies that exact certificate and changes on every renewal. It is not a hash of the public key. The hash of the SubjectPublicKeyInfo (SPKI) is a separate value and is what certificate pinning uses, because it survives a renewal that keeps the same key; that is the closer analogue of an [SSH key fingerprint](https://superuser.com/questions/421997/what-is-a-ssh-key-fingerprint-and-how-is-it-generated).

## SSL certificate for multiple domains

The **Subject Alternative Name** (SAN) field lets you specify additional host names (sites, IP addresses, common names, etc.) to be protected by a single SSL Certificate, such as a Multi-Domain (SAN) or Extend Validation Multi-Domain Certificate. To [request an SSL certificate that supports multiple domains](http://www.jasinskionline.com/technicalwiki/%28X%281%29S%28fdjqoj45vcgk5z225tt5qaey%29%29/Print.aspx?Page=Requesting-an-SSL-Certificate-for-Multiple-Domains), you need to generate a Certificate Signing Request (CSR) for SANs.

Every publicly trusted certificate is a SAN certificate today, because browsers ignore the CN. The useful distinction is [multi-domain versus wildcard](https://opensrs.com/blog/2012/09/san-and-wildcard-certificates-whats-the-difference): a wildcard (`*.example.com`) covers unlimited subdomains at one level, a multi-domain certificate lists several unrelated names, and one certificate can carry both.

## Server hosting multiple TLS certificates

Due to a [shortage of IPv4 addresses](https://en.wikipedia.org/wiki/IPv4_address_exhaustion) it doesn't make sense to host a single site per IP address. **Server Name Indication** (SNI) allows a server to safely host multiple TLS Certificates for multiple sites, all under a single IP address. The Internet Protocol version 4 (IPv4) has roughly 4 billion IP addresses. But, there are already more than 4 billion internet connected computers worldwide, so we are facing a shortage of IPv4 addresses. The anticipated shortage has been the driving factor in creating and adopting several new technologies, including network address translation (NAT), Classless Inter-Domain Routing (CIDR), and IPv6.

SNI is an [extension to the TLS protocol](https://www.globalsign.com/en/blog/what-is-server-name-indication). The client specifies which hostname they want to connect to using the SNI extension in the TLS handshake. This allows a server (for example Apache, Nginx, or a load balancer such as HAProxy) to select the corresponding private key and certificate chain that are required to establish the connection from a list while hosting all certificates on a single IP address.

## Validity limits and automation

Publicly trusted certificates have had a maximum lifetime of 398 days since Sep 2020. CA/Browser Forum ballot SC-081v3 (Apr 2025) shortens this in steps: 200 days from 15 Mar 2026, 100 days from 15 Mar 2027 and 47 days from 15 Mar 2029, and the period for which a domain validation can be reused falls to 10 days. Renewing by hand is not workable at that cadence, so automate with the ACME protocol: Let's Encrypt and ZeroSSL issue free certificates, `certbot` or your load balancer's built-in ACME client renews them, the DNS-01 challenge works for hosts that are not reachable from the internet, and wildcards cost nothing.

## Certificate Revocation List (CRL)

A Certificate Revocation List (CRL) is a list of digital certificates that have been revoked by the issuing Certificate Authority (CA) before their scheduled expiration date and should no longer be trusted.

CRLs grew too large to download on every connection, so **OCSP** (Online Certificate Status Protocol) let a client ask the CA about one certificate at a time, at the cost of latency and of leaking browsing history to the CA. **OCSP stapling** fixes both by having the server fetch the signed OCSP response and attach it to the TLS handshake. In practice browsers now rely on aggregated revocation lists pushed by the vendor (Chrome CRLSets, Firefox **CRLite**) rather than live checks; the CA/Browser Forum made OCSP optional for CAs in 2023 and Let's Encrypt ended its OCSP service in 2025, publishing only CRLs. Short certificate lifetimes (see above) also reduce how much revocation matters.
