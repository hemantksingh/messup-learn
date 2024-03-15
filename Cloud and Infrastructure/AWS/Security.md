# AWS Security

Fundamentally there are a few patterns that can be used to secure all your AWS services.

* Control your cloud infrastructure: [AWS IAM](./Security%20-%20IAM.md)
  * Every AWS service uses IAM to authenticate and authorize API calls
  * How to make authenticated API calls to AWS from human and non human IAM identities
* Control your data: [AWS KMS](./Security%20-%20KMS.md)
* Control your network: [Amazon VPC](./Security%20-%20Networking.md)

![aws-security-patterns.png](../../Images/aws-security-patterns.png "AWS Security Patterns")

## Security Best Practices

The [AWS security docs](https://docs.aws.amazon.com/security/) provide the list of best practices for all the services in each category of AWS services. e.g. [AWS IAM security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

What are the common security mistakes customers make, how to fix them, and why they are important?

### How do I make my account secure?

An AWS Account creates a logical boundary to provide isolation environment by enforcing permissions that prevent cross account access

* Therefore resources present in one account cannot access resources provisioned in another account unless explicitly allowed via a trust relationship
* AWS Accounts also provide cost boundaries for reporting and billing purposes
* AWS also enforces service limits at the AWS account level e.g. you can only have 100 S3 buckets within an account by default

AWS has a primary set of services to help customers maintain a strong security posture over their AWS accounts

* AWS Security Hub - is a Cloud Security Posture Management (CSPM) tool that assesses your security alerts and security posture across all your accounts and regions at the organization level. It can **continually assess your accounts** for things like:
  * AWS foundational security practice
  * CIS Benchmarks
  * PCI DSS compliance
* Amazon Detective - key tool for an incident’s root cause analysis, which can help in a thorough investigation of security incidents.
* Amazon GuardDuty - an Intrusion Detection system (IDS) which can detect threats like compromised accounts, unauthorized access, and data exfiltration based on unexpected/unusual activity.
* AWS Config - audit and evaluate AWS resource configurations
* AWS Well-Architected reviews - less technical, more broader security assessment
* AWS Trusted Advisor - can Provide recommendations that help you follow AWS best practices. Trusted Advisor evaluates your account by using checks. These checks identify ways to optimize your AWS infrastructure, improve security and performance, reduce costs, and monitor service quotas. 

If an organisation has not implemented any of the above services, there may be a need to conduct a rapid security assessment of the cloud environment. [AWS Security Assessment Tool](https://github.com/awslabs/aws-security-assessment-solution) helps in assessing **point in time** security posture of the deployed AWS environment. It leverages ScoutSuite and Prowler to run a point in time security check on your AWS account.

## AWS Security Services

AWS provides a [range of services](https://aws.amazon.com/products/security/?nc=sn&loc=2) to secure your workloads and applications in the cloud. These services are broadly categorized into:

### Detection and Response

#### Amazon Detective

* Automatically collects and analyzes data from various sources like AWS CloudTrail logs, Amazon VPC Flow Logs, Amazon EKS audit logs, Amazon GuardDuty findings, AWS Security Hub findings, and other integrated AWS security services.

* Creates a graph model of your AWS environment, which shows the relationships between your resources, users, and accounts. This graph model can help identify the root cause of a security incident.

#### AWS Security Hub

* Single pane of glass for all your AWS accounts that identifies gaps in your security coverage
* Automating and enforcing organisation wide security policies and centralise security alerts e.g. control for checking automation of secrets rotation.
* Can automate response and remediation actions to improve Mean time to resolution (MTTR)
* AWS Security Hub is integrated with AWS CloudTrail, a service that provides a record of actions taken by a user, role, or an AWS service in Security Hub. CloudTrail captures API calls for Security Hub as events

#### Guard Duty

* Automated scans for *active intrusion* attempts. **Threat detection** service that uses ML to continuously monitor for malicious behavior. It receives feeds from 3rd parties like Proofpoint and Crowdstrike about known malicious domains and IP addresses.
* Detects anomalies by learning what normal behavior looks like in your account and alerts of any abnormal malicious behavior
  * IAM users and AWS accounts credentials being used in a suspicious way, such as from IP addresses associated with known malicious actors
  * EC2 instances trying to mine cryptocurrency or communicate with IP addresses and domains associated with known malicious actors
  * container workloads in EKS
  * storage - S3 policy allowing public read access
* Allows you to monitor CloudTrail logs, VPC flow logs and DNS query logs for potential threats.
* What Guard Duty is not?
  * It only alerts about an unusual activity, therefore it is **not an Intrusion Prevention System (IPS)**. You could build your actions on top of GuardDuty alerts with AWS Lambda, but it is not part of the service itself.
  * It is **different from Inspector** as it is assessing *unusual/unexpected* behavior whereas Inspector scans your EC2 instances and network for *known* security vulnerabilities such as zero day. Inspector doesn't scan behavior, just known and new security vulnerabilities based on an up to date database.

#### Inspector

* Automated scans for *potential known* vulnerabilities and reports on them based on severity.
* Automatically assesses applications for vulnerabilities or deviations from best practices by **inspecting the network and EC2 instances**, e.g. whether port 22 has been left open on your security group. It can perform
  * network assessment - network configuration analysis to check for ports reachable from outside VPC, inspector agent not required
  * host assessment - Vulnerable software (CVE), host hardening using CIS Benchmarks, inspector agent is required

#### Macie

* Monitors S3 buckets, uses ML and pattern matching to discover sensitive data stored in S3
* Uses AI to recognize if your S3 objects contain sensitive data such as PII (Personally Identifiable Information), PHI and financial data
* Great for frameworks like HIPPA and GDPA compliance
* Alerts you about public and unencrypted buckets, buckets shared with AWS accounts outside of those defined in your AWS organization. Alerts can be
  * filtered and searched in your AWS console
  * sent to Amazon EventBridge and integrated with your SIEM system
  * integrated with AWS Security Hub for a broader analysis of your organization's security posture
  * integrated with other AWS services, such as Step functions to take remediatory action

### Identity and Access Management

#### IAM Access Analyser

Access Analyzer lets you identify unintended access to your resources and data. It helps you identify the resources in your organization and accounts, such as Amazon S3 buckets or IAM roles, shared with an external entity.

IAM Access Analyzer identifies resources shared with external principals by using logic-based reasoning to analyze the resource-based policies in your AWS environment.

* validates IAM policies against policy grammar and best practices
* generates IAM policies based on access activity in your AWS CloudTrail logs

### Compliance and Auditing

#### AWS CloudTrail

* CCTV monitoring for your AWS account. Keeps a record of actions taken - Who, what, when and where
* Logs API calls made to your AWS account and stores them in S3
* not for RDP/SSH connections

#### AWS Config

* service that enables you to assess, audit, and evaluate the configurations of your AWS resources. An older alternative was Security Monkey <https://github.com/Netflix/security_monkey>
* continuously monitors and records your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations
* this is achieved by enabling AWS Config rules in one or multiple of your AWS accounts (enabling across multiple accounts [can be costly](https://dzone.com/articles/we-turned-off-aws-config)) to check for your configuration settings against best practices or your desired/approved settings like:

  | AWS Config Rule | Alerted |
  | ----------------|:-------:|
  | acm-certificate-expiration-check         | Yes |
  | ec2-instances-in-vpc                     | Yes |
  | ec2-volume-inuse-check                   | Yes |
  | encrypted-volumes                        | Yes |
  | restricted-ssh                           | Yes |
  | iam-root-access-key-check                | Yes |
  | iam-password-policy                      | Yes |
  | iam-user-no-policies-check               | Yes |
  | lambda-function-settings-check           | Yes |
  | db-instance-backup-enabled               | Yes |
  | rds-snapshots-public-prohibited          | Yes |
  | rds-storage-encrypted                    | Yes |
  | dynamodb-throughput-limit-check          | No  |
  | s3-bucket-public-read-prohibited         | Yes |
  | s3-bucket-public-write-prohibited        | Yes |
  | s3-bucket-replication-enabled            | Yes |
  | s3-bucket-server-side-encryption-enabled | Yes |
  | s3-bucket-ssl-requests-only              | No  |
  | s3-bucket-logging-enabled                | Yes |
  | s3-bucket-versioning-enabled             | Yes |
  | cloudtrail-enabled                       | Yes |
  
### Network and Application Protection

#### AWS Shield

Prevention of [DDOS attacks](../../Security/Web%20Security/Web%20Application%20Security.md#ddos-protection) There are 2 tiers of AWS Shield

* Standard
  * All AWS customers get the automatic protections of AWS Shield Standard, at no additional charge
  * Provides DDOS protection against SYN/UDP floods, reflection attacks and other layer 3 and layer 4 attacks when used with CloudFront and Route53
* Advanced
  * Protection against larger & more sophisticated attacks targeting applications running on EC2, ELB, CloudFront AWS Global Accelerator and Route 53 resources
  * Always on, flow based monitoring to provide realtime notifications of DDOS attacks

### Data Protection & Privacy

#### Systems Manager

* Allows you to select a resource group and view its recent API activity, resource configuration changes, related notifications, operational alerts, software inventory, and patch compliance status. It lets you take action on each resource group depending on your operational needs
* Systems Manager provides a central place to view and manage your AWS resources, so you can have complete visibility and control over your operations

#### Secrets Manager

Secrets manager is a service that securely stores, encrypts and rotates your database credentials, SSH keys, API keys and other secrets

* Encryption in transit and at rest using KMS
* Automatic credentials rotation. When enabled secrets manager will rotate credentials immediately, therefore before enabling credential rotation make sure all your application instances are configured to use SecretsManager
* Fine-grained access control using IAM policies
* Cross account access
* Costs money

#### Parameter Store

* a capability of AWS Systems Manager, provides secure, hierarchical storage for configuration data management and secrets management
* store data such as passwords, database strings, Amazon Machine Image (AMI) IDs, and license codes as parameter values. You can store values as plain text or encrypted data
* Free, but limited to 10000 parameters with no key rotation
* Uses KMS in the backend
