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
  * Always on, flow based monitoring to provide realtime notifications of DDOD attacks

### Cloud Trail

* CCTV monitoring for your AWS account. Logs API calls made to your AWS account and stores them in S3
* not for RDP/SSH connections

### Guard Duty

* Centralized threat detection service that uses ML to continuously monitor for malacious behaviour. It receives feeds from 3rd parties like Proofpoint and Crowdstrike about known malacious domains and IP addresses.
* Allows you to monitor CloudTrail logs, VPC flow logs and DNS logs
* Anomaly detection by learning what normal behaviour looks like in your account and alerts of any abnormal malacious behaviour


### Macie

* Monitors S3 buckets, uses ML and pattern matching to discover sensitive data stored in S3
* Uses AI to recognise if your S3 objects contain sensitive data such as PII (Personally Identifiable Information), PHI and financial data
* Great for frameworks like HIPPA and GDPA
* Alerts you about public and unencrypted buckets, buckets shared with AWS accounts outside of those defined in your AWS organization. Alerts can be
  * filtered and serached in your AWS console
  * sent to Amazon EventBridge and integrated with your SIEM system
  * integreated with AWS Security Hub for a broader analysis of your organization's security posture
  * integrated with other AWS services, such as Step functions to take remediatory action

### Inspector

* Automated security assessmet service that helps improve the security and compliance of applications deployed on AWS
* Automatically assesses applications for vulnerabilites or deviations from best practices by inspecting the network and EC2 instances, e.g. whehter port 22 has been left open on your security group. It can perform
  * network assessment - network configuration analysis to check for ports reachable from outside VPC, inspector agent not required
  * host assessment - Vulnerable software (CVE), host hardening using CIS Benchmarks, inspector agent is required
* Assessment findings are reported based on severity

### Key Management Service (KMS)

* Create and control encryption keys used to encrypt your data
* Integrates with EBS, S3 and RDS and other services to encrypt your data with the encryption keys you manage
* Provides centralized control over the lifecycle and permissions of your keys

#### AWS KMS Keys

AWS KMS keys (KMS keys) are the primary resource in AWS KMS. You can use a KMS key to encrypt, decrypt, and re-encrypt data. It can also generate data keys that you can use outside of AWS KMS. Typically, you'll use symmetric KMS keys, but you can create and use asymmetric KMS keys for encryption or signing. AWS KMS key is a logical representation of an encryption key. It contains the key material used to encrypt and decrypt data. The key material for a KMS key can be

  * generated by default, within AWS KMS. The key material cannot be extracted, exported or viewed. Also, you cannot delete this key material; you must delete the KMS key. The key material for the KMS key is genereated within HSMs managed by AWS KMS.
  * imported from your own key management infrastructure into a KMS key
  * created in the **AWS CloudHSM** cluster associated with an [AWS KMS custom key store](https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html). When you create an AWS KMS key in a custom key store, AWS KMS generates and stores non-extractable key material for the KMS key in an AWS CloudHSM cluster that you own and manage. When you use a KMS key in a custom key store, the cryptographic operations are performed in the HSMs in the cluster.

A **Hardware Security Module (HSM)** is a physical computing device containing one or more secure cryptoprocessor chips that safegaurds and manages digital keys and performs encryption and decryption functions. The default AWS KMS key store is a shared service and protected by FIPS 140-2 validated cryptographic module but if your security requirement mandates a dedicated HSM, certified at FIPS 140-2 Level 3 with full control of underlying hardware you can opt for a custom key store.

* AWS KMS keys can be rotated automatically every year, provided that those keys were generated within AWS KMS HSMs.
* Automatic key roation is not supported for imported keys, assymetric keys or keys generated in an AWS CloudHSM cluster using the AWS KMS custom key store
* There are 3 ways to control permissions to KMS keys
  * Using the key policy (resource based policy attached to the KMS key) - the full scope of access to the KMS key is defined in a single document (the key policy)
  * Using IAM policies (policies attached to IAM identity) in combination with the key policy - manage all the permissions for your IAM identities in IAM
  * Using grants in combinations with the key policy - enables you to allow access to the KMS key in the key plocu as well as allow users to delegate their access to others
