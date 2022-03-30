# Securing azure services

Public internet access to your resources is not desirable. Locking down access to azure services is required for allowing traffic only from your virtual network or known IPs.

## Virtual Network service endpoints

Virtual Network (VNet) service endpoints allow you to [secure your critical Azure service](https://docs.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview) resources by restricting access to the resources only via your virtual networks. Traffic from your VNet to the Azure service always remains on the Microsoft Azure backbone network.

Endpoints extend your virtual network private address space. The endpoints also extend the identity of your VNet to the Azure services over a direct connection. 

## Securing Data

Microsoft [recommends using server-level IP firewall rules](https://docs.microsoft.com/en-us/azure/sql-database/sql-database-firewall-configure#recommendation) when you have many databases that have the same access requirements and you don't want to spend time configuring each database individually.

One must explicitly **whitelist the IP addresses** that will be allowed access to a SQL Azure DB or add existing virtual networks to provide access to all databases in the dbserver.

* Allow access to Azure services ON: allows communications from all Azure IP addresses and all Azure subnets. These Azure IPs or subnets might not be owned by you. This ON setting is probably more open than you want your SQL Database to be.
* Allow access to Azure services OFF: most secure configuration

[Automatically configure](https://docs.microsoft.com/en-us/azure/sql-database/sql-database-firewall-configure#manage-server-level-ip-firewall-rules-using-azure-cli) firewall rules using the Azure   cli or REST api.

```sh
# Set server firewall -> add the following rule to

# provide access to any IP:
0.0.0.0 to 255.255.255.255
1.1.1.1 to 255.255.255.255

# give access to a single IP:
2.222.224.12 to 2.222.224.12
```
