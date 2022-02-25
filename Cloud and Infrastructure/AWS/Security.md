# AWS Security

## DDOS

* SYN flood attack - A TCP connection requires 3 way handshake between the client and the server
  * Client -> SYN packet -> Server
  * Server -> SYN-ACK -> Client
  * Client -> ACK -> Server
  * The client overwhelms ther server by sending SYN packets without sending ACK, crossing the number of TCP connections the server can support 
* [NTP amplification attack](https://www.cloudflare.com/en-gb/learning/ddos/ntp-amplification-ddos-attack/#:~:text=An%20NTP%20amplification%20attack%20is,the%20target%20and%20its%20surrounding) - The Network Time Protocol is designed to allow internet connected devices to synchronize their internal clocks, and serves an important function in internet architecture. By exploiting the monlist command enabled on some NTP servers, an attacker is able to multiply their initial request traffic, resulting in a large response. This command is enabled by default on older devices, and responds with the last 600 source IP addresses of requests which have been made to the NTP server. NTP server functionality is exploited in order to overwhelm a targeted network or server with an amplified amount of UDP traffic, rendering the target and its surrounding infrastructure inaccessible to regular traffic. An amplification attack exploits disparity in bandwidth cost between an attacker and the targeted web resource. By sending small queries that result in large responses, the malicious user is able to get more from less. NTP amplification, much like DNS amplification, can be thought of in the context of a malicious teenager calling a restaurant and saying “I’ll have one of everything, please call me back and tell me my whole order.” When the restaurant asks for a callback number, the number given is the targeted victim’s phone number. The target then receives a call from the restaurant with a lot of information that they didn’t request.

## Guard Duty

* Centralized threat detection service that uses ML to continuously monitor for malacious behaviour. It receives feeds from 3rd parties like Proofpoint and Crowdstrike about known malacious domains and IP addresses.
* Allows you to monitor CloudTrail logs, VPC flow logs and DNS logs
* Anomaly detection by learning what normal behaviour looks like in your account and alerts of any abnormal malacious behaviour


## Macie

* Monitors S3 buckets, uses ML and pattern matching to discover sensitive data stored in S3
* Uses AI to recognise if your S3 objects contain sensitive data such as PII (Personally Identifiable Information), PHI and financial data
* Great for frameworks like HIPPA and GDPA
* Alerts you about public and unencrypted buckets, buckets shared with AWS accounts outside of those defined in your AWS organization. Alerts can be
  * filtered and serached in your AWS console
  * sent to Amazon EventBridge and integrated with your SIEM system
  * integreated with AWS Security Hub for a broader analysis of your organization's security posture
  * integrated with other AWS services, such as Step functions to take remediatory action


## Inspector

* Automated security assessmet service that helps improve the security and compliance of applications deployed on AWS
* Automatically assesses applications for vulnerabilites or deviations from best practices by inspecting the network and EC2 instances, e.g. whehter port 22 has been left open on your security group. It can perform
  * network assessment - network configuration analysis to check for ports reachable from outside VPC, inspector agent not required
  * host assessment - Vulnerable software (CVE), host hardening using CIS Benchmarks, inspector agent is required
* Assessment findings are reported based on severity
