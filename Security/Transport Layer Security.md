# HTTPS
HTTPS allows you to secure the connection between 2 machines on a network, providing

* Confidentiality - your data is protected from eavesdroppers through encryption
* Integrity - data can't be changed in transit through signing
* Authenticity - You know who you are talking to through validation of the owner of the resource (e.g. website).

Having a secure HTTPS connection allows a site to have:

* Valid [TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) certificate: The connection to the site is using a valid, trusted server certificate.
* Secure TLS connection: The connection to the site is using a strong protocol version and cipher suite.
* Secure Resources: All resources on the page are served securely.

## SSL Certificate

After a [key pair](https://en.wikipedia.org/wiki/Public-key_cryptography) is generated, the public key needs to be distributed for public usage. A certificate adds identity to a public key. The certificate, in addition to containing the public key, contains additional information such as issuer, what the certificate is supposed to be used for, and other types of metadata.

* A **CER** file is used to store X.509 certificate. The file contains information about certificate owner and public key. The file extensions .CRT and .CER are interchangeable. Certificates should be in an ASCII format such as PEM, CER, or DER. A CER file can be in binary (ASN.1 DER) or encoded with Base-64 with header and footer included (PEM).

* **PFX** files Personal Exchange Format, is a PKCS12 file. This contains a variety of cryptographic information, such as certificates, root authority certificates, certificate chains and private keys. It’s cryptographically protected with passwords to keep private keys private and preserve the integrity of the root certificates.

* Windows uses **PVK files** to store private keys for code signing in various Microsoft products. PVK is proprietary format

### Certificate thumbprint

A thumbprint, much like an [SSH Key fingerprint](https://superuser.com/questions/421997/what-is-a-ssh-key-fingerprint-and-how-is-it-generated) that identifies the public key of a host to connect to, **identifies the public key of the certificate**. The thumbprint is almost certainly contained in the signature of the request to identify the certificate that can be used to verify the signature.

## How does HTTPS work?

In order to achieve the security guarantees mentioned above, the TLS protocol specifies:

Browser ----------------> website (e.g. google.com)

The website presents the browser with its certificate. To verify the authenticity of the certificate, a certificate is itself signed by a certificate authority (CA) using CA's private or secret key .

![certificate](https://latex.codecogs.com/gif.latex?Certificate%20%3DSign_C_A_s_S_K%20%28dnsName%3ApublicKey%29)

*CA -> Certificate Auhtority  
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

Depending upon the nature of your website and how much do users need to trust your website, you can pay anything from $5 to thousands of dollars for a certificate. What’s the difference?

* How reputable is the certificate authority (CA)? If they have weak cryptography or a deficient implementation of SSL or TLS, they  get hacked, you get hacked!
* How well does the CA check you are who you say you are?

* **Domain Validation or DV Certificates** Gives assurance that we are talking to the domain we think we are but provides no guarantees about the owner of the domain and whether they are good guys. Usually for personal websites and small forums without sensitive data. On viewing the certificate (Mozilla) no organisation is mentioned under *Issued to* section of the certificate. e.g.
  * Organisation (O) `<Not Part Of Certificate>`

* **Organization Validation or OV Certificates** Checking of ownership as well as domain, additional vetting of the organization and individual applying for the certificate. On viewing the certificate (Mozilla) organisation name is listed on the certificate. e.g.
  * Organisation (O) `Mozilla Corporation`

* **Extended Validation or EV Certificates** Gives assurance that we are talking to the organisation we think we are. They cost money, because they require the certificate authority to check who you are. When the site has EV, the organisation name and the country of origin is displayed along with the URL in the browser (Chrome & Firefox) address bar. E-commerce and banking websites handling credit/debit card and financial transactional data.

Getting an EV certificate is [costly and not easy](https://www.troyhunt.com/journey-to-an-extended-validation-certificate/). You are probably going to pay more than 3 times for and EV certificate as compared to a normal one and you need a legal entity that can own the certificate i.e. a registered business under the laws of the country that you are operating in.

If your login page page is served over http but the login form posts to https, is it secure? Not really. You cannot have confidence that the login form that has been served over http hasn't been modified by a **man in the middle** by the time it gets to the end user in! Your traffic could still be intercepted before and after HTTPS connection begins and ends!