# HTTPS

HTTPS allows you to secure the connection between 2 machines on a network, providing

* Confidentiality - your **data is private** and protected from eavesdroppers through encryption
* Integrity - your **data hasn't changed** in transit, achieved through signing
* Authenticity - you know **who** you are talking to through validation of the owner of the resource (e.g. website).

Having a secure HTTPS connection allows a site to have:

* Valid [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) certificate: The connection to the site is using a valid, trusted server certificate.
* Secure TLS connection: The connection to the site is using a strong protocol version and cipher suite.
* Secure resources: All resources on the page are served securely.

## What is a Certificate?

In order to secure communication between two devices or machines the following three things are required:

1. Unique Identity - each device needs to have an identity. Like a username provides identity to a person this could be a unique id or IP address
2. Identity is independently verifiable - An external authority should be able to attest the identity of the device by signing the device identity and providing a means of verifying that signed identity (e.g. X.509 certificate) to others
3. Verifiable identity is easily accessible and renewable - The verifiable identity should be easy to obtain, renew and revoke.

A public key or [digital certificate](https://certbot.eff.org/docs/what.html) (formerly called SSL certificate) provides 1 and 2 above but is not so great at 3. The certificate includes information about the key, information about the server identity, and the digital signature of the certificate issuer.

### Certificate generation

After a [key pair](https://en.wikipedia.org/wiki/Public-key_cryptography) is generated, the public key needs to be distributed for public usage. A certificate adds identity to a public key. 

A certificate can be self signed or requested from an independent Certificate Authority (CA) that verifies your identity, creates the certificate and signs it for it to be used in clients that trust the CA.

A [certificate signing request (CSR)](https://www.globalsign.com/en/blog/what-is-a-certificate-signing-request-csr) is a message sent from an applicant to a Certificate Authority to apply for a digital identity certificate. A CSR is created and sent to the CA to be signed and generate a certificate for your domain. It usually contains the public key that will be included in your certificate, identifying information such as a common name (CN), organization (O), country (C), key type and key length. The CA will use the data from the CSR to create your certificate. The CSR may be accompanied by other credentials or proofs of identity required by the certificate authority, and the certificate authority may contact the applicant for further information. The certificate, in addition to containing the public key, contains additional information such as issuer, what the certificate is supposed to be used for and other types of metadata.

```sh
# Create a CSR
openssl -req mydomain.csr -new -newkey rsa:2048 -nodes -keyout mydomain.key
```

Certificate can be in [various formats](https://knowledge.digicert.com/generalinformation/INFO4448.html) depending upon whether they are Base64 ASCII encoded or in binary format.

* A **CER** file is used to store X.509 certificate. The file contains information about certificate owner and public key. The file extensions .CRT and .CER are interchangeable. A CER file can be binary (ASN.1 DER) or Base-64 encoded with header and footer included (PEM). **PEM** being the most common format used for an X.509 certificate.

* **PFX/P12/PKCS#12** The PKCS#12 or PFX/P12 format is a binary format for storing the server certificate, intermediate certificates, root authority certificates, [certificate chains](https://knowledge.digicert.com/solution/SO16297.html) and the private key in one encryptable file. It is cryptographically protected with passwords to keep private keys private and preserve the integrity of the root certificates.

* Windows uses **PVK files** to store private keys for code signing in various Microsoft products. PVK is proprietary format

### Certificate thumbprint

A thumbprint, much like an [SSH Key fingerprint](https://superuser.com/questions/421997/what-is-a-ssh-key-fingerprint-and-how-is-it-generated) that identifies the public key of a host to connect to, **identifies the public key of the certificate**. The thumbprint is almost certainly contained in the signature of the request to identify the certificate that can be used to verify the signature.

### SSL certificate for multiple domains

The Subject Alternative Name (SAN) field lets you specify additional host names (sites, IP addresses, common names, etc.) to be protected by a single SSL Certificate, such as a Multi-Domain (SAN) or Extend Validation Multi-Domain Certificate. To [request an SSL certificate that supports multiple domains](http://www.jasinskionline.com/technicalwiki/%28X%281%29S%28fdjqoj45vcgk5z225tt5qaey%29%29/Print.aspx?Page=Requesting-an-SSL-Certificate-for-Multiple-Domains), you need to generate a Certificate Signing Request (CSR) for SANs.

[SAN certificates are different from wildcard certificates](https://opensrs.com/blog/2012/09/san-and-wildcard-certificates-whats-the-difference). While wildcard certificates allow for unlimited subdomains to be protected with a single certificate, a SAN cert allows multiple domain names to be protected with a single certificate.

### Server hosting multiple TLS certificates

Server Name Indication (SNI) allows a server to safely host multiple TLS Certificates for multiple sites, all under a **single IP address**. This is helpful because there is a [shortage of IPv4 addresses](https://simple.wikipedia.org/wiki/Main_Page).   The Internet Protocol version 4 (IPv4) has roughly 4 billion IP addresses. But, there are already more than 4 billion internet connected computers worldwide, so we are facing a shortage of IPv4 addresses. The Internet Protocol version 6 (IPv6) should fix this problem, offering trillions of addresses, but there is still some existing network equipment that does not support IPv6.

SNI is an [extension to the TLS protocol](https://www.globalsign.com/en/blog/what-is-server-name-indication). The client specifies which hostname they want to connect to using the SNI extension in the TLS handshake. This allows a server (for example Apache, Nginx, or a load balancer such as HAProxy) to select the corresponding private key and certificate chain that are required to establish the connection from a list while hosting all certificates on a single IP address.

### Certificate Revocation List (CRL)

A Certificate Revocation List (CRL) is a list of digital certificates that have been revoked by the issuing Certificate Authority (CA) before their scheduled expiration date and should no longer be trusted.

## How does HTTPS work?

The TLS protocol is implemented as a transparent wrapper around the HTTP protocol. It doesn't really fit into the OSI model but from a conceptual level it can be thought to [sit between HTTP and TCP](https://security.stackexchange.com/questions/93333/what-layer-is-tls), therefore between layer 4 and 7. In order to achieve the security guarantees mentioned above, the TLS protocol specifies:

Browser ----------------> website (e.g. google.com)

The website presents the browser with its certificate. To verify the authenticity of the certificate, a certificate is itself signed by a certificate authority (CA) using CA's private or secret key .

![certificate](https://latex.codecogs.com/gif.latex?Certificate%20%3DSign_C_A_s_S_K%20%28dnsName%3ApublicKey%29)

*CA -> Certificate Authority  
SK -> Secret Key*

Web browsers come with a list of public keys of most commonly used CA's in order to verify certificates.

![verify](https://latex.codecogs.com/gif.latex?Verify_C_A_s_P_K%28m%2Ccertificate%29%3D%20ok%3F)

*PK -> Public Key  
m -> message*

On establishing the validity of the certificate, the web browser then generates a new secret key and encrypts it with the websites public key so that the secret can be shared with the website using asymmetric key cryptography.

Encryption ![encryption](https://latex.codecogs.com/gif.latex?E_p_k%28p%29%3Dc) and Decryption ![decryption](https://latex.codecogs.com/gif.latex?D_s_k%28c%29%3Dp)

*pk -> website's public key  
sk -> website's secret key  
p -> new secret key in plain text  
c -> cipher text*

The [key exchange is vital to secure data transfer](https://www.jscape.com/blog/key-exchange#:~:text=The%20two%20most%20popular%20key,of%20the%20Internet%2C%20especially%20businesswise) between communicating parties. All further communication between the web browser and the website is encrypted with the shared secret key (only known to the 2 communicating parties) using symmetric key encryption. The two most popular key exchange algorithms are RSA (Rivest–Shamir–Adleman) and Diffie-Hellman (now known as Diffie-Helmlman-Merkle).

Encryption ![encryption](https://latex.codecogs.com/gif.latex?E_s_k%28p%29%3Dc) and Decryption ![decryption](https://latex.codecogs.com/gif.latex?D_s_k%28c%29%3Dp)

*sk -> secret key
p -> plain text
c -> cipher text*

## How do you decide the type of SSL certificate

Depending upon the nature of your business and how much users need to trust your website, you can pay anything from $5 to thousands of dollars for a certificate. What’s the difference?

* How reputable is the certificate authority (CA)? If they have weak cryptography or a deficient implementation of SSL or TLS, they  get hacked, you get hacked!
* How well does the CA check you are who you say you are?

* **Domain Validation or DV Certificates** Gives assurance that we are talking to the domain we think we are but provides no guarantees about the owner of the domain and whether they are good guys. Usually for personal websites and small forums without sensitive data. On viewing the certificate (Mozilla) no organisation is mentioned under *Issued to* section of the certificate. e.g.
  * Organisation (O) `<Not Part Of Certificate>`

* **Organization Validation or OV Certificates** Checking of ownership as well as domain, additional vetting of the organization and individual applying for the certificate. On viewing the certificate (Mozilla) organisation name is listed on the certificate. e.g.
  * Organisation (O) `Mozilla Corporation`

* **Extended Validation or EV Certificates** Gives assurance that we are talking to the organisation we think we are. They cost money, because they require the certificate authority to check who you are. When the site has EV, the organisation name and the country of origin is displayed along with the URL in the browser (Chrome & Firefox) address bar. E-commerce and banking websites handling credit/debit card and financial transactional data.

Getting an EV certificate is [costly and not easy](https://www.troyhunt.com/journey-to-an-extended-validation-certificate/). You are probably going to pay more than 3 times for and EV certificate as compared to a normal one and you need a legal entity that can own the certificate i.e. a registered business under the laws of the country that you are operating in.

### How to tell DV and OV certificates apart

The only way to know with confidence that a certificate is of a specific type is to know the practices of each CA. **Certificate Transparency (CT)** helps businesses by making certificate information publicly available. In X.509 the way an issuer is supposed to express something like this is via the Certificate Policies extension which is defined in RFC 5280. This allows a CA to express a unique identifier called Object Identifier (OID) in their certificates that maps to a document that describes its practices associated with this certificate.

#### What is an Object Identifier (OID)

Object Identifiers (OIDs) are used to define policies for processing certificates defined by the X.509 specification. Signatures that do not conform to the specified policies are deemed invalid. Root object identifiers are issued to individuals or organizations by national registration authorities. e.g. on the certificate issued to https://hemantkumar.net Policy Identifier=2.23.140.1.2.1 which belongs to [CA-Browser Forum](https://www.alvestrand.no/objectid/submissions/2.23.140.1.2.1.html)

```
[1]Certificate Policy:
     Policy Identifier=2.23.140.1.2.1
[2]Certificate Policy:
     Policy Identifier=1.3.6.1.4.1.44947.1.1.1
     [2,1]Policy Qualifier Info:
          Policy Qualifier Id=CPS
          Qualifier:
               http://cps.letsencrypt.org
```

The [OID can be used programmatically](https://unmitigatedrisk.com/?p=203) to make trust decisions about a certificate or to differentiate the user interface in an application based on what type of certificate is being used.
