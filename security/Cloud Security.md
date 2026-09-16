# Cloud Security

Overall view of the control domains reviewed and assessed for public cloud adoption. Over time new controls can be added to attain a maturity level optimal for the organisational needs.

The frameworks below are easy to confuse because they all talk about "controls". They sit at different layers and answer different questions. Read them as a stack.

| Layer | Question it answers | Frameworks |
|---|---|---|
| Threat model | What do attackers do? | MITRE ATT&CK, ENISA threat taxonomy |
| Function model | What must a security programme do? | NIST CSF 2.0 |
| Control catalogue | Which controls, stated precisely? | NIST SP 800-53, CSA Cloud Controls Matrix, ISO/IEC 27002 |
| Configuration baseline | How is this system set up safely? | CIS Benchmarks |
| Provider assurance | Can I trust this provider? | CSA STAR and CAIQ, NCSC cloud security principles, SOC 2 and ISO 27001 reports |

## Threat models

* MITRE ATT&CK classifies adversary behaviour by tactic and technique: how attackers get in, move laterally, escalate privileges, evade defences and exfiltrate data. It has a cloud matrix. It is not a list of controls. Its use is to check coverage: for each technique that applies to you, which control prevents it and which detection would see it.
* ENISA, the European Union Agency for Cybersecurity, publishes a threat taxonomy and an annual threat landscape report. Both are a checklist of threat categories to walk through when you build a risk register.

## Function model: NIST CSF

The NIST Cybersecurity Framework (CSF) organises a security programme into functions. CSF 2.0 (2024) has six: Govern, Identify, Protect, Detect, Respond and Recover. Govern was added in 2.0 and covers strategy, roles, policy and supply chain risk. Under each function sit categories and subcategories that describe outcomes, not controls.

The functions matter because they force even coverage. A programme that is all Protect and no Detect or Respond is lopsided, and the CSF makes that visible.

The CSF has no control catalogue of its own. Each subcategory maps to controls in NIST SP 800-53, ISO/IEC 27002 and the CSA CCM. Keep the two apart: the CSF says a detection capability must exist, SP 800-53 says which audit and monitoring controls make it exist.

## Control catalogues

* NIST SP 800-53 is the US federal control catalogue, organised into control families (access control, audit and accountability, system and communications protection, and so on). It is the most thorough catalogue and the heaviest to implement in full. Organisations select a baseline (low, moderate, high) rather than everything.
* The Cloud Security Alliance (CSA) is a non-profit that publishes cloud-specific security guidance. Its Cloud Controls Matrix (CCM) is a control set written for cloud services, with mappings to ISO 27001, SP 800-53 and PCI DSS so one assessment can be reused against several standards.
* ISO/IEC 27001 and its control set 27002, SOC 2 and PCI DSS are covered in [Standards and Compliance](Standards%20and%20Compliance.md).

## Configuration baseline: CIS Benchmarks

The Center for Internet Security (CIS) Benchmarks are consensus configuration guides for operating systems, databases, Kubernetes and each cloud provider's account settings. Where a control catalogue says "harden the host", a benchmark says which settings and what value. CIS establishes the initial baseline and supports continuous posture management against it.

Each benchmark has two profiles. Level 1 meets minimum and essential security requirements with little effect on function. Level 2 is defence in depth for situations where security is paramount and some functionality can be lost. CIS also publishes hardened VM images built to those profiles, available in the cloud marketplaces.

## Provider assurance

* CSA STAR (Security, Trust, Assurance and Risk) is a public registry where cloud providers document their security and privacy controls. A customer reads the registry before procurement instead of sending their own questionnaire.
* The CAIQ (Consensus Assessments Initiative Questionnaire) is the yes/no questionnaire that a provider answers against the CCM. The completed CAIQ is what gets uploaded to STAR. So CCM is the control set, CAIQ is the self-assessment against it, STAR is where it is published.
* The UK NCSC's [cloud security principles](https://www.ncsc.gov.uk/collection/cloud/the-cloud-security-principles) are fourteen principles for choosing a provider. They apply to platforms and to SaaS and are the shortest useful checklist for a procurement conversation.

## Technical controls checklist

A technical set of controls to complete the more abstract type of controls above. A checklist to assess your cloud application security footprint for running cloud based applications. The family column is the spine: identity, network, data, detection, response.

| Family | Requirement | Description |
|---|---|---|
| Identity | Access control | Access to cloud production resources requires an identity with assigned authorised actions, following least privilege |
| Network | Network security | The offering can define and maintain network security groups for network access control and segmentation |
| Network | Intrusion detection and prevention | An IDS inspects traffic for patterns that match known attacks and raises an alert. An IPS does the same inline and can drop the packet, so it stops the attack rather than reporting it |
| Data | Cryptography | Controls for data in transit and data at rest, for both the product and the supporting infrastructure |
| Data | Data access and confidentiality | No public access to object storage buckets; data at rest encrypted with a managed key service; access and usage monitored for audit and troubleshooting |
| Data | Catalogue, integrity, retention, recovery | Every service that stores data has an owner and a classification, integrity checks, a retention period and a recovery target that is monitored |
| Detection | Malware detection and response | An active system detects malware, removes an infection automatically and reports its operational status |
| Detection | Vulnerability management | Resources are assessed for vulnerabilities, missing patches and misconfiguration according to an agreed procedure |
| Detection | Security information and event monitoring (SIEM) | All security logs are consolidated so indicators or evidence of compromise can be found in one place |
| Response | Patch management | Vulnerabilities found are remediated within an agreed time |
| Response | Standard operating procedures | Daily operations and exception handling are written down and kept current |
| Response | Penetration test | A third party tests the offering to find weaknesses before general availability |

The data rows are both preventive and detective. Preventive stops the bucket being public; detective notices when someone makes it public anyway.

## Tool categories

Several [cloud security tool categories](https://www.uptycs.com/blog/whats-the-difference-between-casb-cwpp-cspm-and-cnapp) go into securing cloud applications and workloads. Each has its own focus and they are used together.

* CSPM (cloud security posture management) reads the provider's configuration through its APIs and flags drift from a benchmark: a public bucket, a wide-open security group, a user without MFA.
* CWPP (cloud workload protection platform) protects what runs: VMs, containers and functions, with vulnerability scanning and runtime detection.
* CASB (cloud access security broker) sits between users and SaaS to enforce policy on what data goes where.
* CNAPP (cloud-native application protection platform) is the vendor bundle of CSPM and CWPP with code-to-cloud context.

The choice and combination depend on the security requirements and cloud architecture of the organisation.

Prowler (`prowler-cloud/prowler`) and ScoutSuite (`nccgroup/ScoutSuite`) are open-source CSPM scanners that assess an account against CIS and other benchmarks; the AWS assessment tooling that uses them is in [AWS](../cloud/aws/README.md).

## SIEM and SOAR

Security information and event management (SIEM) and security orchestration, automation and response (SOAR) complement each other but are not the same thing. A SIEM helps identify and analyse security incidents. A SOAR lets you respond to those incidents in an automated way.

Firewalls, network appliances and intrusion detection systems produce more event data than a team can read. A SIEM collects it and correlates events into incidents. It needs regular tuning to tell normal from anomalous, and the tuning competes for the analysts who should be triaging alerts.

A SOAR takes those incidents and runs playbooks against them: gather context, open a case, isolate a host, notify. Manual response steps become workflow, which is how a small team keeps up with alert volume.

Provider implementations: AWS Security Hub and GuardDuty are described in [AWS](../cloud/aws/README.md); Microsoft Defender for Cloud and Microsoft Sentinel in [Azure security services](../cloud/azure/Tenants%2C%20Subscriptions%20and%20RBAC.md#security-services).

## How to rederive this

* Ask what layer a document sits at: threat, function, control, configuration or assurance. Two documents at different layers do not compete.
* A function model has no controls; a control catalogue has no priorities. You need one of each.
* A benchmark is a control made concrete for one product. If it names a setting and a value, it is a benchmark.
* Assurance is someone else's evidence about their controls. STAR, SOC 2 and ISO certificates are read, not implemented.
* CSPM reads configuration, CWPP watches workloads, SIEM reads logs, SOAR acts on incidents.

## Sources

* NIST Cybersecurity Framework 2.0 (February 2024)
* NIST SP 800-53 Rev 5, Security and Privacy Controls for Information Systems and Organizations
* Cloud Security Alliance: Cloud Controls Matrix, STAR registry, CAIQ
* CIS Benchmarks and CIS Hardened Images, Center for Internet Security
* MITRE ATT&CK, Enterprise and Cloud matrices
* ENISA Threat Landscape reports
* NCSC, The cloud security principles
* Uptycs, "What's the difference between CASB, CWPP, CSPM and CNAPP"
