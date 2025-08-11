# Networking

VPC or Virtual Private Cloud is a logically isolated part of the AWS cloud, think of it as a virtual  data center in the cloud. You can leverage multiple layers of security, including security groups and network ACLs to help control access to Amazon EC2 instances in each subnet. The inbound and outbound connectivity to your VPC via the internet gateway or a VPN is established via three main lines of defense:

* Routing tables - whether there is a route in or out to the internet. A **router** is required to create subnets and routes traffic between different subnets. A public subnet requires a route out to the internet (via an internet gateway) and a mapping to a public IP. This allows any EC2 instances within this subnet to reach out to the internet and be publicly available. **1 subnet always spans 1 Availability Zone**
  * An **internet gateway** allows resources within your public subnet to access the internet, and the internet to access said resources. **You can only have 1 internet gateway per VPC**. To allow access to the internet, a route is defined in the route table with the destination as `0.0.0.0/0` and the target as the internet gateway. To allow communication between subnets another route is defined with destination as CIDR block for VPC and target `local`. Example of a route table for a public subnet, with routes for both IPv4 and IPv6.
    |Destination              |Target      |Description     |
    |:------------------------|:-----------|:---------------|
    |`10.0.0.0/16`            |`local`     | IPv4 traffic bound to your VPC, stays within your VPC|
    |`2001:db8:1234:1a00::/56`|`local`     | IPv6 traffic bound to your VPC, stays within your VPC|
    |`0.0.0.0/0`              |`igw-id`    |All IPv4 traffic (`0.0.0.0/0`), except for traffic within the VPC (`10.0.0.0/16`) is routed to the internet gateway|
    |`::/0`                   |`igw-id`    |All IPv6 traffic (`::/0`), except for traffic within the VPC is routed to the internet gateway|

  * A **NAT Gateway** allows resources in a private subnet to access the internet (think yum updates, external database connections, wget calls, OS patch, etc). It only works one way. The internet at large cannot get through your NAT to your private resources unless you explicitly allow it. The NAT Gateway is provisioned inside the public subnet to allow routing traffic from the private subnet. To allow access to the internet from the private subnet, a route is defined with the destination as `0.0.0.0/0` and the target as the NAT gateway. Example of a route table for one of the private subnets, with routes for both IPv4 and IPv6.
    |Destination              |Target          |Description     |
    |:------------------------|:---------------|:---------------|
    |`10.0.0.0/16`            |`local`         | IPv4 traffic bound to your VPC, stays within your VPC|
    |`2001:db8:1234:1a00::/56`|`local`         | IPv6 traffic bound to your VPC, stays within your VPC|
    |`0.0.0.0/0`              |`nat-gateway-id`|All IPv4 traffic (`0.0.0.0/0`), except for traffic within the VPC (`10.0.0.0/16`) is routed to the nat gateway|
    |`::/0`                   |`eigw-id`       |All IPv6 traffic (`::/0`), except for traffic within the VPC is routed to the egress-only internet gateway|
    |`s3-prefix-list-id`      |`s3-gateway-id` |Traffic destined for Amazon S3 routed to the gateway VPC endpoint|

  * **VPC Endpoints**: A lot of the services within AWS do not run within a VPC e.g. S3, DynamoDb, API Gateway, CloudWatch. By default, communications to and from these services use the HTTPS protocol, which protects network traffic by using SSL/TLS encryption. Connectivity to these services from your VPC can be established by allowing a route out to the internet or if you have stricter security policies relating to data being transmitted over the public internet, a more secure option is a [VPC endpoint](https://docs.aws.amazon.com/whitepapers/latest/aws-privatelink/what-are-vpc-endpoints.html) where traffic between an Amazon VPC and a supported service does not leave the Amazon network. This can be done via
    * **Gateway VPC endpoints** - target specific IP routes in an Amazon VPC route table in the form of a `prefix-list` used for traffic destined to massive scale services like DynamoDb, S3.
      * App calls S3 -> Route table intercepts -> Direct to AWS backbone
      * DNS stays the same: You call s3.amazonaws.com but traffic gets redirected
      * Free: No hourly charges, just data transfer charges
    * **Interface VPC endpoints** - enable you to privately connect your VPC to supported AWS services like API Gateway, CloudFormation, CloudWatch etc, services hosted by other AWS customers and partners in their own Amazon VPCs and supported AWS Marketplace partner services, powered by [PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) 
      * App calls EC2 API -> DNS resolves to private IP -> ENI (Elastic Network Interface) forwards to service
      * Enables instances in your VPC to not require an internet gateway, NAT gateway or public IP to communicate with other AWS services.
* Network ACLs - act as a firewall for controlling traffic in and out of one or more subnets, so any instance in the subnet with an associated NACL will follow rules of NACL. Each subnet in your VPC must be associated with a NACL. If not done explicitly the subnet is automatically associated with the default NACL. You can associate a NACL with multiple subnets, however **a subnet can be associated with only 1 NACL**. You may setup NACLs with rules similar to your security group to add another layer of security to your VPC
  * by default, a custom NACL denies all outbound and inbound traffic whereas the default NACL allows all outbound and inbound traffic
  * can be used to block specific IP addresses
  * are stateless, therefore explicit rules are enforced for inbound and outbound traffic

* Security Groups - virtual stateful firewalls for EC2 instances and the last line of defense.
  * by default everything is blocked
  * [security groups are tied to an instance whereas Network ACLs are tied to the subnet](https://medium.com/awesome-cloud/aws-difference-between-security-groups-and-network-acls-adc632ea29ae)
  * security groups are stateful - this means any changes applied to an incoming rule will be automatically applied to the outgoing rule. e.g. If you allow an incoming port 80, the outgoing port 80 will be automatically opened.
![aws-vpc.png](../../Images/aws-vpc.png "AWS VPC Setup")

## Troubleshooting inbound network connectivity

While accessing your ec2 instance from the browser, if you get a

* timeout - it is probably because there is no inbound route defined in your route table or network ACL
* *ERR connection refused* - means you are able to get through to the EC2 instance but it is not serving the requested HTTP page.

## VPC

* [VPC with public and private subnets](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario2.html) to host your public facing web apps in the public subnet and the database servers in the private subnet. You can set up security and routing so that the web servers can communicate with the database servers.

* [VPC with public and private subnets and AWS Site-to-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario3.html) to run a multi-tiered application with a scalable web front end in a public subnet, and to house your data in a private subnet that is connected to your on-premises network by an IPsec AWS Site-to-Site VPN connection. A VPN or Virtual Private Network connection between your corporate data center and your VPC allows you to leverage the AWS Cloud as an extension of your corporate data center.

* [VPC with a private subnet only and AWS Site-to-Site VPN access](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Scenario4.html) to extend your network into the cloud using Amazon's infrastructure without exposing your network to the internet.

### Elastic Network Interfaces

* Elastic Network Interface (ENI)s are virtual network cards you can attach to your EC2 instances. They are used to enable network connectivity for your instances, and having more than one of them connected to your instance allows it to communicate on two different subnets. You’re already using them if you’re running on EC2—the default interface, `eth0`, is attached to an ENI that was created when you launched the instance, and is used to handle all traffic sent and received from the instance. You’re not limited to just one network interface though—attaching a secondary network interface allows you to **connect your EC2 instance to two networks at once**. A common use case for ENIs is the creation of management networks. This allows you to have public-facing applications like web servers in a public subnet but lock down SSH access down to a private subnet on a secondary network interface.

### AWS PrivateLink

Opening services in a VPC to another VPC, sharing applications across VPCs within the AWS ecosystem be it within the same company or between companies and partners using AWS. In a multi tenant system if you have a VPC per customer then connecting 1000s of VPCs to your service VPC may not scale well. AWS PrivateLink allows you to expose a service VPC to tens, hundreds or thousands of customer VPCs.

* Doesn't require VPC peering, no route tables, NAT gateways, internet gateways, or public IP addresses.
* Requires a Network LB on the service VPC and an Elastic Network Interface on the customer VPC
* Can also provide [API Gateway private endpoints](https://aws.amazon.com/blogs/compute/introducing-amazon-api-gateway-private-endpoints/), securely exposing REST APIs only to the other services and resources inside your VPC, or those connected via Direct Connect to your own data centers.

## Connecting AWS to On-Premise Data Centres

AWS VPCs can be connected to on-premise networks via [Virtual Private Gateway or Transit Gateway](http://www.differencebetween.net/technology/difference-between-virtual-private-gateway-and-transit-gateway/)

### Virtual Private Gateway

managed gateway endpoint for VPC for Site to Site VPN connection using VPN and AWS Direct Connect
does not introduce any extra latency but can end up increasing complexity with scale

### Transit Gateway

* Network transit hub that connects multiple VPCs and on-premise networks via VPNs or Direct Connect links
offers a simpler design and allows you to easily connect VPCs, AWS accounts and on-premise networks to a central hub
* simplifies your network by stopping complex peering relationships, experiences a slight delay but infrastructure is streamlined and scalable

### AWS Direct Connect

AWS Direct Connect bypasses the public Internet and establishes a secure, dedicated connection from your infrastructure into AWS. This dedicated connection occurs over a standard 1 GB or 10 GB Ethernet fiber-optic cable with one end of the cable connected to your router and the other to an AWS Direct Connect router. AWS has established these Direct Connect routers in large collocation facilities across the world, providing access to all AWS regions. With established connectivity via AWS Direct Connect, you can access your Amazon VPC and all AWS services.

AWS Direct Connect is a great option for businesses that are seeking secure, ultra-low latency connectivity into AWS. While provisioning AWS Direct Connect can sometimes be more involved, it is worth it once the connectivity is established the because of the ease of predictable network performance and 60% cost savings.

### AWS-manged VPN

AWS-managed VPN is a hardware IPsec VPN that enables you to create an encrypted connection over the public Internet between your Amazon VPC and your private IT infrastructure. The VPN connection lets you extend your existing security and management policies to your VPC as if they were running within your own infrastructure.

VPN is a great connectivity option for businesses that are just getting started with AWS. It is quick and easy to setup. Keep in mind, however, that VPN connectivity utilizes the public Internet, which can have unpredictable performance and despite being encrypted, can present security concerns.