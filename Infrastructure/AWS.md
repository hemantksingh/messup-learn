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

VPC or Virtual Private Cloud is a logically isolated part of the AWS cloud, think of it as a virtual  data center in the cloud. You can leverage multiple layers of security, including security groups and network ACLs to help control access to Amazon EC2 instances in each subnet. The inbound and outbound connectivity to your VPC via the internet gateway or a VPN is established via three main lines of defense:

* Routing tables - whether there is a route in or out to the internet
* Network ACLs - acts as a firewall for controlling traffic in and out of one or more subnets, so any instance in the subnet with an associated NACL will follow rules of NACL. Each subnet in your VPC must be associated with a NACL. If not done explicitly the subnet is automatically associated with the default NACL. You can associate a NACL with multiple subnets, however a subnet can be associated with **only 1 NACL** You may setup NACLs with rules similar to your security group to add another layer of security to your VPC
  * by default, a custom NACL denies all outbound and inbound traffic whereas the default NACL allows all outbound and inbound traffic
  * can be used to block specific IP addresses
  * are stateless, therefore explicit rules are enforced for inbound and outbound traffic
* Security Groups - virtual firewalls for EC2 instances and the last line of defense.
  * by default everything is blocked
  * [security groups are tied to an instance whereas Network ACLs are tied to the subnet](https://medium.com/awesome-cloud/aws-difference-between-security-groups-and-network-acls-adc632ea29ae)
  * security groups are stateful - if you send request from your isntance, the response traffic for that request is allowed to flow in regardlesss of inbound security rules

![aws-vpc.png](../Images/aws-vpc.png "AWS VPC Setup")

* A **router** routes traffic between different subnets and is required to create subnets.
* A public subnet requires a route out to the internet (via an internet gteway) and a mapping to a public IP. This allows any EC2 instances within this subnet to reach out to the internet and be publicly available. **1 subnet always spans 1 Availability Zone**
* An internet gateway allows routes out to the internet, therefore allowing resources within your public subnet to access the internet, and the internet to access said resources. **You can only have 1 internet gateway per VPC**
  * To allow access to the internet a route is defined in the route table with the destination as `0.0.0.0/0` and the target as the internet gateway.
  * To allow communication between subnets another route is defined with destination as CIDR block for VPC and target `local`
* A NAT Gateway allows resources in a private subnet to access the internet (think yum updates, external database connections, wget calls, OS patch, etc). It only works one way. The internet at large cannot get through your NAT to your private resources unless you explicitly allow it. The NAT Gateway is provisioned inside the public subnet to allow routing traffic from the private subnet.
  * To allow access to the internet from the private subnet, a route is defined with the destination as `0.0.0.0/0` and the target as the NAT gateway

You can create

* [VPC with public and private subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html) to host your public facing web apps in the public subnet and the database servers in the private subnet. You can set up security and routing so that the web servers can communicate with the database servers.

* [VPC with public and private subnets and AWS Site-to-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario3.html) to run a multi-tiered application with a scalable web front end in a public subnet, and to house your data in a private subnet that is connected to your network by an IPsec AWS Site-to-Site VPN connection. A VPN or Virtual Private Network connection between your corporate data center and your VPC allows you to leverage the AWS Cloud as an extension of your corporate data center.

* [VPC with a private subnet only and AWS Site-to-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario4.html) to extend your network into the cloud using Amazon's infrastructure without exposing your network to the internet.

### AWS-manged VPN

AWS-managed VPN is a hardware IPsec VPN that enables you to create an encrypted connection over the public Internet between your Amazon VPC and your private IT infrastructure. The VPN connection lets you extend your existing security and management policies to your VPC as if they were running within your own infrastructure.

VPN is a great connectivity option for businesses that are just getting started with AWS. It is quick and easy to setup. Keep in mind, however, that VPN connectivity utilizes the public Internet, which can have unpredictable performance and despite being encrypted, can present security concerns.

### AWS Direct Connect

AWS Direct Connect bypasses the public Internet and establishes a secure, dedicated connection from your infrastructure into AWS. This dedicated connection occurs over a standard 1 GB or 10 GB Ethernet fiber-optic cable with one end of the cable connected to your router and the other to an AWS Direct Connect router. AWS has established these Direct Connect routers in large colocation facilities across the world, providing access to all AWS regions. With established connectivity via AWS Direct Connect, you can access your Amazon VPC and all AWS services.

AWS Direct Connect is a great option for businesses that are seeking secure, ultra-low latency connectivity into AWS. While provisioning AWS Direct Connect can sometimes be more involved, it is worth it once the connectivity is established the because of the ease of predictable network performance and 60% cost savings.

### VPC Endpoints

A VPC Endpoint enables you to privately connect your VPC to supported AWS services and VPC endpoint services powered by PrivateLink without requiring an internet gateway, NAT device, VPN connection or AWS Direct Connect.

Traffic between your VPC and other service does not leave the Amazon internal network.

Instances in your VPC do not require public IP addresses to communicate with resources in the service.

### AWS PrivateLink

Opening services in a VPC to another VPC, Sharing applications across VPCs. In a multi tenant system if you have a VPC per customer then connecting 1000s of VPCs to your service VPC may not scale well. AWS PrivateLink allows you to expose a service VPC to tens, hundreds or thousands of customer VPCs.

* Doesn;t require VPC peering, no route tables, NAT gateways, internet gateways, etc.
* Requires a Network LB on the service VPC and an Elastic Network Interface on the customer VPC
