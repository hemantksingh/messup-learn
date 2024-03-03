# IAM

Identity and Access Management is used for

* 'I' stands for authentication and 'AM' stands for authorization - managing users and their access to AWS resources, allowing administrators to define **who can do what**
* issuing identities
  * IAM user - identity for humans using **long term access credentials** e.g. username and password or long term credentials for programmatic access
  * AWS services - identity for non-human resources e.g. EC2 instance, Lambda, SageMaker, Glue crawler, ECS task etc
  * IAM principal - is an identity in IAM, can be an IAM user, IAM role or an AWS service, something that can make API calls to other AWS services
  * IAM role - is an identity that you can create in your account that has specific permissions (similar to a Service Principal in Azure or Service Account in GCP). An IAM role is similar to an IAM user, in that it is an AWS identity with permission policies that determine what the identity can and cannot do in AWS. Instead of being uniquely associated with one person, a [role can be assumed](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html) by anyone who needs it. Also, a role does not have standard long-term credentials such as a password or access keys associated with it. Instead, when you assume a role, it provides you with **temporary security credentials** for your role session.
* monitoring and auditing access to specific resources e.g. by enabling AWS Cloud Trail
* federate access into AWS by integrating with corporate identity providers like Microsoft Active Directory when the users have identities defined outside of AWS
<img src="../../Images/aws-federated-identity.png" title="AWS federated identity" width="600" height="400"/>

|Users (Who)            |Groups (Who)       |Roles (Who)    | Policies (What) |
|:---------------------|:------------------|:--------------|:---------------|
|Specific individual, can receive logins |Collection of users by function such as administrator, developer etc |Collection of policies that you can use to access AWS resources e.g. a role with DB Read, DB Write permissions |Low level permissions to resources (Allow/Deny). There are mainly 2 ways to control access to resources  <ul><li>**Identity policy** - Issue an identity (role) and define who (the IAM principal) can assume that identity and what they can do with the resource in question. Such a policy is attached to a user, group or role specifying what the principal can do with the resource e.g. get items from an Amazon DynamoDB table</li><li>**Resource policy** - Define the access control directly at the AWS resource (e.g. S3 buckets, KMS Keys) itself as opposed to the IAM principal making the call and specify who can access the resource and do what. Unlike an identity-based policy, a resource-based policy specifies who (which principal - mandatory in a resource based policy) can access that resource. Not all resources allow you to define resource based policies e.g. dynamodb</li></ul>|

## IAM Roles

* IAM Roles can be used for delegated access on behalf of the signed in user e.g. an IAM Role can be assigned to an EC2 instance to allow the instance to work on the signed in user's behalf and access another AWS resource e.g. S3 bucket. This means you don't have to provide credentials to the EC2 instance for programmatic access to S3.

You generally have two [ways to use a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios.html): interactively in the IAM console, or programmatically with the AWS CLI, Tools for Windows PowerShell, or API.

* IAM users in your account using the IAM console can [switch to a role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html) to temporarily use the permissions of the role in the console. The users give up their original permissions and take on the permissions assigned to the role. When the users exit the role, their original permissions are restored.

* An application or a service offered by AWS (like Amazon EC2) can assume a role by requesting temporary security credentials for a role with which to make programmatic requests to AWS. You use a role this way so that you don't have to share or maintain long-term security credentials (for example, by creating an IAM user) for each entity that requires access to a resource.

## IAM Policies

IAM Policies are generally applied to Groups as opposed to individual users. AWS pre-defines some IAM policies for common tasks. These are useful for setting up permissions for human roles that have common sets of coarse grained actions that they want to do. A [policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html) can be granted to a specific resource (with an `arn`) or all resources of a particular type (with a wildcard `"*"`)

* Not explicitly allowed == implicitly denied
* Explicit deny > everything else
* Only attached policies have effect
* AWS joins all applicable policies, e.g. EC2 admin access attached to devs and S3 admin access attached to devs, AWS will join these together but an explicit deny in one and an Allow in another will result in a Deny

Root Account: The account created when you first set up your AWS account and which has complete admin access. This should be secured with MFA and not meant to be used to log in day to day

New Users: No permissions when first created

### Amazon Resource Names (ARNs)

* Uniquely identify AWS resources
* Required when you need to specify a resource unambiguously across all of AWS, such as in IAM policies, Amazon Relational Database Service (Amazon RDS) tags, and API calls
* Format: `arn:partition:service:region:account_id`
  * partition: aws|aws-cn (AWS China)
  * service: s3|ec2|rds
  * region: us-east-1|eu-central-1
  * account_id: 123456789012

```json
// full admin access, allow the action of everything on every resources
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",  // Allow or deny
            "Action": "*",      // What can (or can't) you do?        
            "Resource": "*"     // What can (or can't) you do it to?
        }
    ]
}

// allow dynamodb read and query access on 'mytable'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "dynamodb:BatchGetItem",
              "dynamodb:GetItem",
              "dynamodb:Query"
            ]
            "Resource": [
              "arn:aws:dynamodb:eu-west-1:111122223333:table/mytable"
            ]
        }
    ]
}
```

### Permission boundaries

* Controls maximum permissions an IAM policy can grant
* Prevents privilege escalation or unnecessarily broad permissions e.g. you do not want developers to get full admin access to the AWS console, you may only want them to create roles to be used with EC2 instances, lambda functions etc.
