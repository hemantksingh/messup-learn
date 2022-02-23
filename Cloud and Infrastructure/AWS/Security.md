# AWS Security


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
