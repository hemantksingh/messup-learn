# HTTPS

HTTPS allows you to secure the connection between 2 machines on a network, providing

* Confidentiality - your **data is private** and protected from eavesdroppers through encryption
* Integrity - your **data hasn't changed** in transit, achieved through signing
* Authenticity - you know **who** you are talking to through validation of the owner of the resource (e.g. website).

Having a secure HTTPS connection allows a site to have:

* Valid [TLS certificate](./TLS%20Certificates.md): The connection to the site is using a valid, trusted certificate.
* Secure TLS connection: The connection to the site is using a strong protocol version and cipher suite.
* Secure resources: All resources on the page are served securely.

## How does HTTPS work?

The TLS protocol is implemented as a transparent wrapper around the HTTP protocol. It doesn't really fit into the OSI model but from a conceptual level it can be thought to [sit between HTTP and TCP](https://security.stackexchange.com/questions/93333/what-layer-is-tls), therefore between layer 4 and 7. In order to achieve the security guarantees mentioned above, the TLS protocol specifies:

Browser ----------------> website (e.g. google.com)

The website presents the browser with its certificate. To verify the authenticity of the certificate, a certificate is itself signed by a certificate authority (CA) using CA's private or secret key .

![certificate](https://latex.codecogs.com/png.latex?Certificate=Sign_C_As_S_K(dnsName:publicKey))

*CA -> Certificate Authority  
SK -> Secret Key*

Web browsers come with a list of public keys of most commonly used CA's in order to verify certificates.

![verify](https://latex.codecogs.com/png.latex?Verify_C_As_P_K(m,certificate)=ok?)

*PK -> Public Key
m -> message*

On establishing the validity of the certificate, the web browser then generates a new secret key and encrypts it with the websites public key so that the secret can be shared with the website using asymmetric key cryptography.

Encryption ![encryption](https://latex.codecogs.com/png.latex?E_p_k(p)=c) and Decryption ![decryption](https://latex.codecogs.com/png.latex?D_s_k(c)=p)

*pk -> website's public key  
sk -> website's secret key  
p -> new secret key in plain text  
c -> cipher text*

The [key exchange is vital to secure data transfer](https://www.jscape.com/blog/key-exchange#:~:text=The%20two%20most%20popular%20key,of%20the%20Internet%2C%20especially%20businesswise) between communicating parties. All further communication between the web browser and the website is encrypted with the shared secret key (only known to the 2 communicating parties) using symmetric key encryption. The two most popular key exchange algorithms are RSA (Rivest–Shamir–Adleman) and Diffie-Hellman (now known as Diffie-Helmlman-Merkle).

Encryption ![encryption](https://latex.codecogs.com/png.latex?E_s_k(p)=c) and Decryption ![decryption](https://latex.codecogs.com/png.latex?D_s_k(c)=p)

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
