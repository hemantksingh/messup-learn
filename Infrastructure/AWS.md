# AWS

## IAM

Identity and Access management for manging users and their access to AWS resources

|Users                  |Groups                         |Roles                     |
|:---------------------:|:------------------------------|:-------------------------:|
|A physical person      |Functions such as administrator, developer etc |Internal usage within AWS |

IAM policies are generally applied to Groups as opposed to individual users.

Root Account: The account created when you first set up your AWS account and which has complete admin access. This should be secured with MFA and not meant to be used to log in day to day.

New Users: No permissions when first created

## Networking

VPC or Virtual Private Cloud is a logically isolated part of the AWS cloud, think of it as a virtual data center in the cloud. You can leverage multiple layers of security, including security groups and network ACLs to help control access to Amazon EC2 instances in each subnet. [Security groups are tied to an instance whereas Network ACLs are tied to the subnet](https://medium.com/awesome-cloud/aws-difference-between-security-groups-and-network-acls-adc632ea29ae). Network ACLs are applicable at the subnet level, so any instance in the subnet with an associated NACL will follow rules of NACL. You can block specific IP addresses using NACL.

![aws-vpc.png](../Images/aws-vpc.png "Ansible Components")

One subnet is always in one Availability Zone. You can create

* [VPC with public and private subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html) to host your public facing web apps in the public subnet and the database servers in the private subnet. You can set up security and routing so that the web servers can communicate with the database servers.

* [VPC with public and private subnets and AWS Site-to-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario3.html) to run a multi-tiered application with a scalable web front end in a public subnet, and to house your data in a private subnet that is connected to your network by an IPsec AWS Site-to-Site VPN connection. A VPN or Virtual Private Network connection between your corporate data center and your VPC allows you to leverage the AWS Cloud as an extension of your corporate data center.

* [VPC with a private subnet only and AWS Site-to-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario4.html) to extend your network into the cloud using Amazon's infrastructure without exposing your network to the internet.

### AWS-manged VPN

AWS-managed VPN is a hardware IPsec VPN that enables you to create an encrypted connection over the public Internet between your Amazon VPC and your private IT infrastructure. The VPN connection lets you extend your existing security and management policies to your VPC as if they were running within your own infrastructure.

VPN is a great connectivity option for businesses that are just getting started with AWS. It is quick and easy to setup. Keep in mind, however, that VPN connectivity utilizes the public Internet, which can have unpredictable performance and despite being encrypted, can present security concerns.

### AWS Direct Connect

AWS Direct Connect bypasses the public Internet and establishes a secure, dedicated connection from your infrastructure into AWS. This dedicated connection occurs over a standard 1 GB or 10 GB Ethernet fiber-optic cable with one end of the cable connected to your router and the other to an AWS Direct Connect router. AWS has established these Direct Connect routers in large colocation facilities across the world, providing access to all AWS regions. With established connectivity via AWS Direct Connect, you can access your Amazon VPC and all AWS services.

AWS Direct Connect is a great option for businesses that are seeking secure, ultra-low latency connectivity into AWS. While provisioning AWS Direct Connect can sometimes be more involved, it is worth it once the connectivity is established the because of the ease of predictable network performance and 60% cost savings.