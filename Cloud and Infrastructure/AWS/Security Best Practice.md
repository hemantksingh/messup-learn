# Security Best Practice

The [AWS security docs](https://docs.aws.amazon.com/security/) provide the list of best practices for all the services in each category of AWS services.

What are the common security mistakes customers make, how to fix them, and why they are important?

## How do I make my account secure?

An AWS Account creates a logical boundary to provide isolation environment by enforcing permissions that prevent cross account access

* Therefore resources present in one account cannot access resources provisioned in another account unless explicitly allowed via a trust relationship
* AWS Accounts also provide cost boundaries for reporting and billing purposes
* AWS also enforces service limits at the AWS account level e.g. you can only have 100 S3 buckets within an account by default

AWS has a primary set of services to help customers maintain a strong security posture over their AWS accounts

- AWS Security Hub - organization aware **continual account assessment** for things like:
  - AWS foundational security practice
  - CIS Benchmarks
  - PCI DSS compliance
- [AWS Security Assessment Tool](https://github.com/awslabs/aws-security-assessment-solution) - asses **point in time** security posture, leverages ScoutSuite and Prowler to run a point in time security check on your AWS account
- Amazon GuardDuty - like an IDS system, not IPS
- AWS Config - audit and evaluate AWS resource configurations
- AWS Well-Architected reviews - less technical, more broader security assessment

## How do I protect my keys?

Different types of key material are allowed in KMS

- **Service managed keys** e.g. (S3 default encryption) are never seen by the customer and therefore they are not allowed to create a key policy on a service managed key

- **Customer managed key** where customers generate the key material and are responsible for managing the key and the key material

- Key deletion for customer managed key is instantaneous and can be destructive, therefore it is advisable to disable the CMK first before deleting it  
