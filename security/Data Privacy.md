---
title: "Data Privacy"
summary: "What makes data personally identifiable, how fingerprinting tracks you without cookies, and what GDPR demands, including when data leaves the EU or UK."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "Peter Eckersley, How Unique Is Your Web Browser?, EFF Panopticlick, PETS 2010"
  - "ICO, A guide to lawful basis"
  - "GDPR Article 83; Data Protection Act 2018; Data (Use and Access) Act 2025"
  - "CJEU, C-311/18 Schrems II (16 July 2020)"
  - "Commission Decision 2021/914 (new SCCs); ICO, International Data Transfer Agreement and Addendum (2022)"
  - "Commission Decision 2023/1795 (EU-US Data Privacy Framework)"
tags: [data-privacy, pii, gdpr, fingerprinting, international-transfers, pci-dss]
---
# Data Privacy

## Personally identifiable information (PII)

Any data that could potentially identify a specific individual. e.g. Name, email address, Social Security Number, National Insurance Number.

There are always grey areas when classifying a piece of data as PII or not. Everything can be considered PII in the right frame of reference

* A work email address is personal data just like a personal one. There is no GDPR exemption for staff. What differs is the lawful basis: employers rarely rely on consent, because an employee cannot freely refuse. They use contract, legal obligation or legitimate interests instead.
* A lot of individual data points e.g. (DOB) by themselves are not PII but when linked to other data points e.g. individual's Name become PII. If data is accessible along with other piece of data it can be classified as PII
  * Company registration number by itself is not PII - it is public data but if it is accessed along with list of names and the company they work for it can be PII.
  * Address linked to a user is PII, not by itself
  * IP address along with browser fingerprinting can potentially leak PII.

### Device/Browser fingerprinting

Fingerprints can be used to fully or partially identify individual users or devices even when cookies are turned off. Fingerprinting is done by capturing information about

* your browser type and version
* your operating system
* installed fonts
* time zone
* language
* screen resolution and various other active settings.
* how your machine renders a hidden canvas or WebGL scene, or processes an audio signal. Small differences in GPU and drivers make the output distinctive.

Because your browsing history is connected to your fingerprint rather than cookies, you can be tracked in incognito mode too.

* The often quoted figure comes from the EFF Panopticlick study (Eckersley, 2010): of browsers with Java or Flash enabled, 94% were uniquely identifiable, meaning no two had the same set of attributes. Flash and Java applets are gone, so the number is history. Plugin lists were the strongest signal then; canvas, WebGL, audio and fonts have taken their place.
* The large majority of sites use this data to personalise the advertisements and information that they serve up to you.
  * To stop users sharing credentials for paid subscriptions
  * News service can serve upto 10 articles for free to a user based on their fingerprint
  * Voting mechanism may use fingerprinting to record duplicate votes
* Fingerprints can be used in a constructive way to combat fraud or credential hijacking, by checking that a user who logs into a specific site is likely the legitimate user.

Device fingerprinting is used to track duplicate devices/hosts by capturing information such as

* OS installation date
* device drivers
* IP address and hostname

## General Data Protection Regulation (GDPR)

A game changer in how companies have to process PII. In force across the EU since May 2018.

In the UK the law is UK GDPR, a copy of the EU text kept after Brexit, plus the Data Protection Act 2018, which replaced the DPA 1998 and fills in the parts GDPR leaves to member states. The Data (Use and Access) Act 2025 amended both. The regulator is the [ICO](https://ico.org.uk).

The principles:

* Lawfulness, fairness and transparency
* Purpose limitation
* Data minimisation
* Accuracy
* Storage limitation
* Integrity and confidentiality - obligation to avoid data breaches
* Accountability - companies must be able to show they comply. The maximum fine is EUR 20 million or 4% of global annual turnover, whichever is higher. The UK GDPR cap is GBP 17.5 million or 4%.

Every use of personal data needs a lawful basis: most often consent, contract, legal obligation or legitimate interests.

The data subject (individual) also gets rights under the law:

* The right to be informed
* The right of access
* The right of rectification
* The right to erasure
* The right to restrict processing
* The right to data portability
* The right to object
* Rights in relation to automated decision making and profiling

## International transfers

Personal data may leave the EU or UK only if the destination gives essentially equivalent protection. Two routes: an adequacy decision for the whole country, or a contract between sender and receiver.

On 16 July 2020 the Court of Justice of the EU ruled in Data Protection Commissioner v Facebook Ireland and Schrems (C-311/18), known as Schrems II. It struck down the EU-US Privacy Shield, then the main route to the US, because US surveillance law gave EU citizens no effective remedy. It kept Standard Contractual Clauses (SCCs) valid but told exporters to check whether the destination's law undermines them.

What followed:

* June 2021: the Commission published new SCCs (Decision 2021/914) built for the post-Schrems world.
* 2022: the UK issued its own contract, the International Data Transfer Agreement (IDTA), plus an Addendum to the EU SCCs.
* 10 July 2023: the Commission adopted the EU-US Data Privacy Framework (DPF) adequacy decision (Decision 2023/1795). US companies self-certify and EU data can flow to them without SCCs.
* 3 September 2025: the General Court dismissed the first challenge to the DPF, Latombe v Commission (T-553/23). The appeal to the Court of Justice (C-703/25 P) is pending.

So today the DPF is the route for the US; SCCs or the IDTA cover every other country without adequacy. If the appeal goes the way of Schrems II, expect the same scramble as 2020.

## Controls

For card numbers, PCI DSS is a contractual industry standard from the PCI Security Standards Council, founded by the five card brands (Visa, Mastercard, American Express, Discover, JCB), not a regulation; processors such as Worldpay, PayPal and Stripe must comply with it, not write it. See [Standards and Compliance](Standards%20and%20Compliance.md).

* Data masking shows part of a value and hides the rest (the last four digits of a card). It is redaction with no key and no way back, which suits logs, test data and support screens. It is not encryption, see [Cryptography Basics](Cryptography%20Basics.md).

## Sources

* Peter Eckersley, [How Unique Is Your Web Browser?](https://coveryourtracks.eff.org/static/browser-uniqueness.pdf), EFF Panopticlick, PETS 2010 (the 94% figure)
* ICO, [A guide to lawful basis](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/) (why employers do not rely on consent)
* GDPR Article 83 (fines); Data Protection Act 2018; Data (Use and Access) Act 2025
* CJEU, C-311/18 Schrems II (16 July 2020)
* Commission Decision 2021/914 (new SCCs); ICO, International Data Transfer Agreement and Addendum (2022)
* Commission Decision 2023/1795 (EU-US Data Privacy Framework)
* General Court, T-553/23 Latombe v Commission (3 September 2025); appeal C-703/25 P
* [PCI Security Standards Council](https://www.pcisecuritystandards.org/)
