## DMZ or Demilitarized zone

A physical or logical subnet that exposes an organisation's external-facing services to a usually larger and untrusted network, usually the internet. It acts as a gateway to the public Internet, is neither as secure as the internal network, nor as insecure as the public internet.

* Adds an additional layer of security to an organisation's local area network (LAN)
* The name is derived from the term "demilitarized zone", an area between nation states in which military operation is not permitted.

## Subnet

Subnets divide a network into smaller network just as a partition divides a room into smaller rooms. A subnet is a collection of computers (identified by a range of IP addresses) that can talk to each other using TCP/IP without having to go through a router. A **router** routes traffic between different subnets and is required to create subnets.

[TCP/IP addressing](https://www.digitalocean.com/community/tutorials/understanding-ip-addresses-subnets-and-cidr-notation-for-networking) allows you to connect together networks of different sizes and systems of different types. These networks are arbitrarily defined into three main classes. IP addresses are typically made of two separate components. One part identifies the host (computer), the other part identifies the network (required for routing purposes) to which it belongs.

### Subnet mask

A [subnet mask](https://www.iplocation.net/subnet-mask) separates the IP address into the network and host addresses. For instance, for class C addresses, the first 3 bytes are used to describe the network. For the address `192.168.21.17`, the `192.168.21` portion describes the network and the `17` describes the host. To create the mask we use a number and then **logically AND** that with the IP address. Therefore in a class C address to preserve the network part, you AND the IP address with `255.255.255.0`. The AND operation with the last zero in `255.255.255.0` gets rid of the host part `17` therefore `255.255.255.0` is the default subnet mask for a class C address.

![classful_networks.jpg](https://bitbucket.org/repo/7XoEpd/images/313561612-classful_networks.jpg)

### CIDR Notation

Classless Inter-Domain Routing, or CIDR, was developed as an alternative to traditional subnetting. The idea is that you can add a specification in the IP address itself to determine the number of significant bits that make up the routing or networking portion.

For example, we could express that the IP address `192.168.21.17` is associated with the subnet mask `255.255.255.0` by using the CIDR notation of `192.168.21.17/24`. This means that the first 24 bits (or the first 3 bytes, considering an IP address is 4 bytes) of the given IP address are considered significant for network routing.

## VLAN

A virtual local area network (VLAN) is a logical group of workstations, servers and network devices that appear to be on the same LAN despite their geographical distribution. VLANs work by applying tags to network frames and handling these tags in networking systems – creating the appearance and functionality of network traffic that is physically on a single network but acts as if it is split between separate networks. In this way, VLANs can keep network applications separate despite being connected to the same physical network, and without requiring multiple sets of cabling and networking devices to be deployed. VLANs are created to provide segmentation and assist in issues like security, network management and scalability.

Subnet operates on the Network layer while VLAN operates on the **Data Link layer**. It resolves MAC addresses to IP addresses. Network **switches** allow the implementation of VLANS. Therefore in order for 2 computers that are both part of the same VLAN (they are both connected to the same switch) to talk to each other over TCPIP, either:

* They must also be part of the same subnet. This means their network address must be the same and the netmask must be equal or smaller. So, a computer with an interface with an IP address of `10.10.20.0/24` can talk to a computer with an interface with an IP address of `10.10.20.4/24` with no issues.

* A router needs to exist between both computers that can forward traffic between subnets.

![vlan_switch.gif](https://bitbucket.org/repo/7XoEpd/images/460685639-vlan_switch.gif)

## Network Address Translation

Networks can be isolated from one another, and they can be bridged and translated to provide access between distinct networks. Network Address Translation allows the addresses to be rewritten when packets traverse network borders to allow them to continue on to their correct destination. This allows the same IP address to be used on multiple, isolated networks while still allowing these to communicate with each other if configured correctly.

Each computer on your network is allocated an address only known to the router. It doesn’t represent you out on the internet. Instead, the router has its own internet address and that communicates with the outside world. The NAT system prevents outsiders from identifying the addresses of individual devices on the network. Unsolicited traffic is blocked before it ever reaches local network devices. This enables a local-area network to use one set of IP addresses for internal traffic and a second set of addresses for external traffic.

A NAT Gateway is located where the LAN meets the Internet and it makes all necessary IP address translations.