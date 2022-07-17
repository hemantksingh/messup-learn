# What is a Certificate?

In order to secure communication between two devices or machines the following three things are required:

1. Unique Identity - each device needs to have a unique identity. Like a username provides identity to a person a device can be identified by a unique id or IP address
2. Identity is independently verifiable - An external authority should be able to attest the identity of the device by signing the device identity and providing a means of verifying that signed identity to others (e.g. by using a X.509 certificate).
3. Verifiable identity is easily accessible and renewable - The verifiable identity should be easy to obtain, renew and revoke.

A public key or [digital certificate](https://certbot.eff.org/docs/what.html) (formerly called SSL certificate) provides 1 and 2 above but is not so great at 3. The certificate includes information about the key, information about the server identity, and the digital signature of the certificate issuer.

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
     -days 356 -nodes \
     -subj '/CN=Demo Cert Authority'

# The applicant creates a private key and CSR for the CA to generate and sign a certificate for the applicant
$ openssl req -new -nodes -newkey rsa:4096 \
	-out applicant.csr \
	-keyout applicant.key \
	-subj '/CN=demo.applicant.com/O=applicant-org'

# The CA can approve the CSR or request further information and generates a certificate (public key) for the applicant
$ openssl x509 -req -sha256 -days 365 \
	-in applicant.csr \
	-CA ca.crt -CAkey ca.key \
	-set_serial 01 \
	-out applicant.crt
```
### Certificate encoding formats

Multitude of server and device types that allow an SSL to be installed and configured require the digital certificate file to be encoded and formatted in a certain way. There are various [certificate encoding formats](https://www.ssls.com/knowledgebase/what-are-certificate-formats-and-what-is-the-difference-between-them/) depending upon whether they are Base64 (ASCII) encoded or in binary format.

#### Base64 (ASCII)

* **PEM**
  * .pem - the most common format for an X.509 certificate. This is a (Privacy-enhanced Electronic Mail) Base64 encoded DER certificate, enclosed between “—–BEGIN CERTIFICATE—–” and “—–END CERTIFICATE—–
  * .crt - you can inspect a certificate `openssl x509 -in admin.crt -text -noout | more`
* **PKCS#7**
  * .p7b
  * .p7s

#### Binary

* **DER**
  * .der
  * .cer
* **PKCS#12**
  * .pfx - an archive file format for storing several cryptographic objects. A .pfx file must contain the end-entity certificate (issued for your domain), a matching private key, and may optionally include an intermediate certification authority (a.k.a. CA Bundle). All this is wrapped up in a single file which is then protected with a pfx password.  (end entity certificate, intermediate certificates, root authority certificates and private key) in a single file.
  * .p12

* Windows uses **PVK files** to store private keys for code signing in various Microsoft products. PVK is proprietary format

## Self signed certificates

As mentioned above a certificate can be self signed or requested from a known global Certificate Authority (CA). Self signed certificates do not go through the independent **identity vetting** process, therefore understandably they cannot be implicitly trusted and are not fit for public usage. However they may be used in development and test environments, provided:

* The self-signed certificate is trusted by importing it into the host's certificate store. On a Linux host 'trustung' the certificate is different and distro dependent On Windows this can be done using:
  * [Powershell](https://docs.microsoft.com/en-us/dotnet/core/additional-tools/self-signed-certificates-guide#with-powershell) `Import-PfxCertificate  -FilePath certificate.pfx -CertLocation 'Cert:\LocalMachine\Root' -Password 'password'`
  * `dotnet dev-certs https --trust`
* You create your own private/internal CA that can issue certificates and add trust in your browsers for that CA

In both of these cases, the key point is that the general public will not accept self signed certificates, which is by design — there is no reason that everyone else should believe the contents of your self signed certificates. So developers have to take some action to modify their browsers’ trust behavior in order to accept something that’s not publicly-trusted.

Alternatively, you can purchase a public domain name from somewhere like https://www.namecheap.com/, get it registered and then get a publicly-trusted certificate for it, even if it is for development purposes.

## Certificate thumbprint

A thumbprint, much like an [SSH Key fingerprint](https://superuser.com/questions/421997/what-is-a-ssh-key-fingerprint-and-how-is-it-generated) (that identifies the public key of a host to connect to) **identifies the public key of the certificate**. The thumbprint is almost certainly contained in the signature of the request to identify the certificate that can be used to verify the signature.

## SSL certificate for multiple domains

The **Subject Alternative Name** (SAN) field lets you specify additional host names (sites, IP addresses, common names, etc.) to be protected by a single SSL Certificate, such as a Multi-Domain (SAN) or Extend Validation Multi-Domain Certificate. To [request an SSL certificate that supports multiple domains](http://www.jasinskionline.com/technicalwiki/%28X%281%29S%28fdjqoj45vcgk5z225tt5qaey%29%29/Print.aspx?Page=Requesting-an-SSL-Certificate-for-Multiple-Domains), you need to generate a Certificate Signing Request (CSR) for SANs.

[SAN certificates are different from wildcard certificates](https://opensrs.com/blog/2012/09/san-and-wildcard-certificates-whats-the-difference). While wildcard certificates allow for unlimited subdomains to be protected with a single certificate, a SAN cert allows multiple domain names to be protected with a single certificate.

## Server hosting multiple TLS certificates

Due to a [shortage of IPv4 addresses](https://en.wikipedia.org/wiki/IPv4_address_exhaustion) it doesn't make sense to host a single site per IP address. **Server Name Indication** (SNI) allows a server to safely host multiple TLS Certificates for multiple sites, all under a single IP address. The Internet Protocol version 4 (IPv4) has roughly 4 billion IP addresses. But, there are already more than 4 billion internet connected computers worldwide, so we are facing a shortage of IPv4 addresses. The anticipated shortage has been the driving factor in creating and adopting several new technologies, including network address translation (NAT), Classless Inter-Domain Routing (CIDR), and IPv6.

SNI is an [extension to the TLS protocol](https://www.globalsign.com/en/blog/what-is-server-name-indication). The client specifies which hostname they want to connect to using the SNI extension in the TLS handshake. This allows a server (for example Apache, Nginx, or a load balancer such as HAProxy) to select the corresponding private key and certificate chain that are required to establish the connection from a list while hosting all certificates on a single IP address.

## Certificate Revocation List (CRL)

A Certificate Revocation List (CRL) is a list of digital certificates that have been revoked by the issuing Certificate Authority (CA) before their scheduled expiration date and should no longer be trusted.
