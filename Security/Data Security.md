# Data Security


## Personally identifiable information (PII)

Any data that could potentially identify a specific individual. e.g. Name, email address, Social Security Number, National Insurance Number.

There are always grey areas when classifying a piece of data as PII or not. Everything can be considered PII in the right frame of reference
* Personal email address is always PII but there is an exemption in GDPR for staff email addresses. Companies are able to process employee data without explicit GDPR consent from employees.
* A lot of individual data points e.g. (DOB) by themselves are not PII but when linked to other data points e.g. individual's Name become PII. If data is accessible along with other piece of data it can be classified as PII 
  * Company registration number by itself is not PII - it is public data but if it is accessed along with list of names and the company they work for it can be PII.
  * Address linked to a user is PII, not by itself
  * IP address along with device/browser fingerprinting can potentially leak PII. Fingerprints can be used to fully or partially identify individual users or devices even when cookies are turned off. Fingerprinting is used to collect information about your browser type and version, as well as your operating system, active plugins, time zone, language, screen resolution and various other active settings. The large majority of sites use this data to personalize the advertisements and information that they serve up to you. Fingerprints can be used in a constructive way to combat fraud or credential hijacking, by checking that a user who logs into a specific site is likely the legitimate user.
   
## General Data Protection Regulation (GDPR)

A game changer in how companies have to process PII. It replaced the Data Protection Act in the UK

* Lawfulness, fairness and transparency
* Purpose limitation
* Data minimization
* Accuracy
* Storage limitation
* Integrity and confidentiality - obligation to avoid data breaches
* Accountability - companies are now accountable to [ICO](https://ico.org.uk) and can be punished with a maximum fine of 20m or 4% of their revenue

The data subject (individual) also gets rights under the law:

* The right to be informed
* The right of access
* The right of rectification
* The right to erasure
* The right to restrict processing
* The right to data portability
* The right to object
* Rights to in relation to automated decision making and profiling

## Payment Card Industry Data Security Standard (PCI DSS)

Regualtionput inplace by payment processors, e.g. Visa, Mastercard, Worldpay, PayPal, Stripe

* Payment Card Industry - Data Security Standard
* Strict industry regulations for handling card numbers
* Includes segregated networks, vulnerability management, access control, monitoring and testing and policy
