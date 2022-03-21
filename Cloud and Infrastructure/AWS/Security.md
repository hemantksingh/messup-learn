# AWS Security

## DDOS

* SYN flood attack - A TCP connection requires 3 way handshake between the client and the server
  * Client -> SYN packet -> Server
  * Server -> SYN-ACK -> Client
  * Client -> ACK -> Server
  * The client overwhelms ther server by sending SYN packets without sending ACK, crossing the number of TCP connections the server can support 
* [NTP amplification attack](https://www.cloudflare.com/en-gb/learning/ddos/ntp-amplification-ddos-attack/#:~:text=An%20NTP%20amplification%20attack%20is,the%20target%20and%20its%20surrounding) - The Network Time Protocol is designed to allow internet connected devices to synchronize their internal clocks, and serves an important function in internet architecture. By exploiting the monlist command enabled on some NTP servers, an attacker is able to multiply their initial request traffic, resulting in a large response. This command is enabled by default on older devices, and responds with the last 600 source IP addresses of requests which have been made to the NTP server. NTP server functionality is exploited in order to overwhelm a targeted network or server with an amplified amount of UDP traffic, rendering the target and its surrounding infrastructure inaccessible to regular traffic. An amplification attack exploits disparity in bandwidth cost between an attacker and the targeted web resource. By sending small queries that result in large responses, the malicious user is able to get more from less. NTP amplification, much like DNS amplification, can be thought of in the context of a malicious teenager calling a restaurant and saying “I’ll have one of everything, please call me back and tell me my whole order.” When the restaurant asks for a callback number, the number given is the targeted victim’s phone number. The target then receives a call from the restaurant with a lot of information that they didn’t request.
* Layer 7 attacks -  Web server receives a flood of GET/POST requests

### AWS Shield

There are 2 tiers of AWS Shield

* Standard
  * All AWS customers benefit from the automatic protections of AWS Shield Standard, at no additional charge. 
  * Provides DDOS protection against SYN/UDP floods, reflection attacks and other layer 3 and layer 4 attacks when used with CloudFront and Route53
* Advanced
  * Protection against larger & more sphisticated attacks targeting applications running on EC2, ELB, CloudFront AWS Global Accelerator and Route 53 resources
  * Always on, flow based monitoring to provide realtime notifications of DDOS attacks

### Cloud Trail

* CCTV monitoring for your AWS account. Logs API calls made to your AWS account and stores them in S3
* not for RDP/SSH connections

### Guard Duty

* Centralized threat detection service that uses ML to continuously monitor for malacious behaviour. It receives feeds from 3rd parties like Proofpoint and Crowdstrike about known malacious domains and IP addresses. It is used for threat detection, not for protocol compliance
* Allows you to monitor CloudTrail logs, VPC flow logs and DNS logs
* Anomaly detection by learning what normal behaviour looks like in your account and alerts of any abnormal malacious behaviour 

### Macie

* Monitors S3 buckets, uses ML and pattern matching to discover sensitive data stored in S3
* Uses AI to recognise if your S3 objects contain sensitive data such as PII (Personally Identifiable Information), PHI and financial data
* Great for frameworks like HIPPA and GDPA compliance
* Alerts you about public and unencrypted buckets, buckets shared with AWS accounts outside of those defined in your AWS organization. Alerts can be
  * filtered and serached in your AWS console
  * sent to Amazon EventBridge and integrated with your SIEM system
  * integreated with AWS Security Hub for a broader analysis of your organization's security posture
  * integrated with other AWS services, such as Step functions to take remediatory action

### Inspector

* Automated security assessment by performing vulnerability scans to help improve the security and compliance of applications deployed on AWS
* Automatically assesses applications for vulnerabilites or deviations from best practices by inspecting the network and EC2 instances, e.g. whehter port 22 has been left open on your security group. It can perform
  * network assessment - network configuration analysis to check for ports reachable from outside VPC, inspector agent not required
  * host assessment - Vulnerable software (CVE), host hardening using CIS Benchmarks, inspector agent is required
* Assessment findings are reported based on severity

### AWS Config

AWS Config is a service that enables you to assess, audit, and evaluate the configurations of your AWS resources. 
* continuously monitors and records your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations.  
* review changes in configurations and relationships between AWS resources, dive into detailed resource configuration histories, and determine your overall compliance against the configurations specified in your internal guidelines. 
* enables you to simplify compliance auditing, security analysis, change management, and operational troubleshooting

### Trust Advisor

* Provides recommendations that help you follow AWS best practices. Trusted Advisor evaluates your account by using checks. These checks identify ways to optimize your AWS infrastructure, improve security and performance, reduce costs, and monitor service quotas. You can then follow the check recommendations to optimize your services and resources.

### Access Analyser 

Access Analyzer helps you identify the resources in your organization and accounts, such as Amazon S3 buckets or IAM roles, shared with an external entity
* validates IAM policies against policy grammar and best practices
* generates IAM policies based on access activity in your AWS CloudTrail logs

### Systems Manager

* Allows you to select a resource group and view its recent API activity, resource configuration changes, related notifications, operational alerts, software inventory, and patch compliance status. It lets you take action on each resource group depending on your operational needs. 
* Systems Manager provides a central place to view and manage your AWS resources, so you can have complete visibility and control over your operations.

### Key Management Service (KMS)

* Create and control encryption keys used to encrypt your data
* Integrates with EBS, S3 and RDS and other services to encrypt your data with the encryption keys you manage
* Provides centralized control over the lifecycle and permissions of your keys

#### AWS KMS Keys

AWS KMS keys (KMS keys) are the primary resource in AWS KMS. You can use a KMS key to encrypt, decrypt, and re-encrypt data. It can also generate data keys that you can use outside of AWS KMS. Typically, you'll use symmetric KMS keys, but you can create and use asymmetric KMS keys for encryption or signing. AWS KMS key is a logical representation of an encryption key. It contains the key material used to encrypt and decrypt data. The key material for a KMS key can be

  * generated by default, within AWS KMS. The key material cannot be extracted, exported or viewed. Also, you cannot delete this key material; you must delete the KMS key. The key material for the KMS key is genereated within shared HSMs managed by AWS KMS.
  * imported from your own key management infrastructure into a KMS key
  * created in the **AWS CloudHSM** cluster associated with an [AWS KMS custom key store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html). When you create an AWS KMS key in a custom key store, AWS KMS generates and stores non-extractable key material for the KMS key in an AWS CloudHSM cluster that you own and manage. When you use a KMS key in a custom key store, the cryptographic operations are performed in the HSMs in the cluster.

A **Hardware Security Module (HSM)** is a physical computing device containing one or more secure cryptoprocessor chips that safegaurds and manages digital keys and performs encryption and decryption functions. The default AWS KMS key store is a shared service and protected by FIPS 140-2 validated cryptographic module but if your security requirement mandates a dedicated HSM, certified at FIPS 140-2 Level 3 with full control of underlying hardware you can opt for a custom key store.

* AWS KMS keys can be rotated automatically every year, provided that those keys were generated within AWS KMS HSMs.
* Automatic key roation is not supported for imported keys, assymetric keys or keys generated in an AWS CloudHSM cluster using the AWS KMS custom key store
* There are 3 ways to control permissions to KMS keys
  * Using the key policy (resource based policy attached to the KMS key) - the full scope of access to the KMS key is defined in a single document (the key policy)
  * Using IAM policies (policies attached to IAM identity) in combination with the key policy - manage all the permissions for your IAM identities in IAM
  * Using grants in combinations with the key policy - enables you to allow access to the KMS key in the key plocu as well as allow users to delegate their access to others

### Secrets Manager

Secrets manager is a service that securely stores, encrypts and rotates your database credentials, SSH keys, API keys and other secrets.
* Encryption in transit and at rest using KMS
* Automatic credentials rotation. When enabled secrets manager will rotate credentials immediately, therefore before enabling credential rotation make sure all your application instances are configured to use SecretsManager
* Fine-grained access control using IAM policies
* Costs money

### Parameter Store

* a capability of AWS Systems Manager, provides secure, hierarchical storage for configuration data management and secrets management
* store data such as passwords, database strings, Amazon Machine Image (AMI) IDs, and license codes as parameter values. You can store values as plain text or encrypted data. 
* Free, but limited to 10000 parameters with no key rotation
* Uses KMS in the backend

