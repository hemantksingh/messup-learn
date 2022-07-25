# AWS CLI

The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) is used to interact with AWS services from your command line shell.

In order to configure the AWS CLI you will need an AWS account and your AWS credentials

```bash
$ aws configure
```

The configuration process stores your

* credentials in a file at `~/.aws/credentials` on MacOS and Linux, or `%UserProfile%\.aws\credentials` on Windows
* config e.g. aws default profile, region at `~/.aws/config`

## Getting resources

```bash

# Get specific fields in a query that returns a list 
$ aws iam list-users --output text --query 'Users[*].[UserName,Arn,CreateDate,PasswordLastUsed,UserId]'

$ aws schemas list-schemas --registry-name aws.events --output text --query 'Schemas[*].[SchemaName,SchemaArn,LastModified,VersionCount]'

# Export the list to a file
$ aws schemas list-schemas --registry-name aws.events --output text --query 'Schemas[*].[SchemaName,SchemaArn,LastModified,VersionCount]' > aws_events.csv

# Filtering 
$ aws events list-rules --event-bus-name default --query 'Rules[?State==`ENABLED`]'

```
