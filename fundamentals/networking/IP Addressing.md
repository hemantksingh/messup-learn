# IP Addressing

An IP address names one interface on a network. It has two parts: a network part shared by everyone on the same link, and a host part unique on that link. A subnet is the set of addresses that share a network part. Subnets divide a network into smaller networks just as a partition divides a room into smaller rooms. Hosts inside one subnet talk directly. A router carries traffic between subnets.

## Network part, host part and the prefix length

An IPv4 address is 32 bits, written as four decimal octets. The prefix length says how many bits, from the left, are the network part. CIDR notation puts it after a slash: `192.168.21.17/24` means the first 24 bits identify the network and the last 8 identify the host.

The subnet mask writes the same split as 32 bits: ones for the network part, zeros for the host part. A `/24` is 24 ones then 8 zeros:

```text
11111111.11111111.11111111.00000000  =  255.255.255.0
```

To get the network address, logically AND the address with the mask. The zeros in the last octet get rid of the host part `17`:

```text
192.168.21.17   AND   255.255.255.0   =   192.168.21.0
```

So for `192.168.21.17/24` the network is `192.168.21.0`, the host is `.17` and the mask is `255.255.255.0`.

Two addresses in every subnet are not hosts: all host bits zero is the network address, all host bits one is the broadcast address. So a `/n` gives `2^(32-n) - 2` usable hosts: 254 for a `/24`, 65,534 for a `/16`, 14 for a `/28`. `10.10.20.0/24` is not a host; it is the network address. `10.10.20.3/24` is a host.

## Classes are history

Before 1993 the first bits of an address fixed the boundary: class A had an 8-bit network part, class B 16, class C 24. CIDR (RFC 1519, now RFC 4632) replaced the fixed boundary with an explicit prefix length. "The default class C mask" is the old way of saying `/24`.

## Direct, or via the gateway

A host sending a packet ANDs the destination with its own mask. If the result is its own network address, the destination is on-link and it delivers directly. Otherwise it picks a router from its route table. Routes match by longest prefix, so the default route `0.0.0.0/0` (a zero-length prefix, so it matches everything) is used only when nothing else does. The router it points at is the default gateway.

Two hosts talk directly only when each sees the other as on-link, because each applies its own mask. `10.10.20.3/24` and `10.10.20.4/24` share the network `10.10.20.0` and talk directly. Give `.3` a `/25` mask and `.200/24` shows the problem: `.200` sends to `.3` directly, but `.3` sends to `.200` via the gateway, which works only if the router forwards back onto the same link.

The gateway is a configured router address on the subnet. In AWS it is implicit: each VPC has a router you never create, with an address reserved in every subnet, and you edit only its route tables. See [VPC Networking](../../cloud/aws/VPC%20Networking.md).

## Layer 2 and layer 3

A subnet is a layer-3 idea. Delivery inside it happens at layer 2 with MAC addresses, so an on-link sender still needs the destination's MAC. ARP (RFC 826) gets it: the host broadcasts "who has `10.10.20.4`?" to the whole link and the owner replies with its MAC. ARP maps IP to MAC, never the other way round.

A VLAN is a layer-2 segment. A switch assigns each port to a VLAN (an IEEE 802.1Q tag carries the number between switches) and forwards a frame only to ports in that VLAN, so a broadcast stays inside it. So the usual rule: one VLAN, one subnet. A subnet spanning two VLANs breaks because ARP broadcasts do not cross; two subnets on one VLAN still hear each other, so the separation is cosmetic. A router (or a layer-3 switch) forwards between subnets.

## Private ranges and NAT

RFC 1918 sets aside `10.0.0.0/8`, `172.16.0.0/12` and `192.168.0.0/16` for private use. They are not routed on the public internet, so a reply to `192.168.1.5` would have nowhere to go.

Network Address Translation rewrites addresses at the border:

* Source NAT (SNAT): outbound, the router replaces the private source address with its own public one.
* Port address translation (PAT, or NAPT): the router also rewrites the source port, so thousands of private hosts share one public address. A table of private (address, port) to public (address, port) lets it rewrite the replies.
* Destination NAT (DNAT): inbound, the router rewrites the destination to a chosen private host. Port forwarding is DNAT.

The router can only deliver a reply it has a table entry for, so an unsolicited inbound packet is dropped. That is a side effect of the table, not a security control: port forwarding, UPnP (any program inside can open a path in) and hairpinning all punch through it. Docker's default bridge and a cloud NAT gateway are the same mechanism, see [Containers](../platform/Containers.md) and [VPC Networking](../../cloud/aws/VPC%20Networking.md).

## The DMZ

A DMZ is a subnet for an organisation's externally facing services. It is neither as secure as the internal network nor as insecure as the public internet. The name comes from the strip of land between nation states in which military operation is not permitted. What makes it work is firewall rules on both boundaries: the internet reaches the DMZ only on the published ports, and the DMZ reaches the internal network only on the connections its services need. A compromised web server then has a second boundary to cross, which is the defence in depth listed in [Security Principles and Threat Modelling](../security/Security%20Principles%20and%20Threat%20Modelling.md).

## IPv6

IPv6 addresses are 128 bits, written as eight hex groups, with the same prefix-length idea; a single link is normally a `/64`. Every host can have a globally unique address, so NAT is not needed to share one. Every interface also gives itself a link-local address in `fe80::/10` with no configuration, and Neighbour Discovery replaces ARP. Dual stack (IPv4 and IPv6 on each host) is the norm because parts of the internet still speak only one.

## How to rederive this

* Prefix length as ones then zeros is the mask. AND it with an address for the network; all host bits one is the broadcast; usable hosts are `2^(host bits) - 2`.
* AND the destination with your own mask. Same network: ARP for the MAC and send directly. Different: longest matching route, `0.0.0.0/0` last, send to that gateway.
* ARP is a broadcast and a VLAN is where broadcasts stop, so one VLAN carries one subnet.
* Private ranges are not routable, so the border rewrites addresses and ports. Replies need a table; no entry means drop, so NAT looks like a firewall without being one.

## Sources

* RFC 4632, Classless Inter-domain Routing (CIDR); obsoletes RFC 1519 (1993)
* RFC 1918, Address Allocation for Private Internets
* RFC 826, An Ethernet Address Resolution Protocol
* RFC 2663, IP Network Address Translator (NAT) Terminology and Considerations
* RFC 4291, IP Version 6 Addressing Architecture
* RFC 4861, Neighbor Discovery for IP version 6
* Kurose and Ross, Computer Networking: A Top-Down Approach, chapters 4 and 6
