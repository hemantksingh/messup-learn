# Phase 3 report: fundamentals/networking/IP Addressing.md

File: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/networking/IP Addressing.md (was Networking/IPRouting.md). Not committed.

Final word count after the owner's tighten pass (`wc -w`): 1,199 for the whole file, 1,129 for the body without the Sources list. Target was 900 to 1,200. Checks: one H1 "IP Addressing", sections at H2, no dashes, no filler phrases, British spelling, no `> Own view:` blocks, every fence tagged, all three relative links resolve, no bitbucket or personal-domain URLs remain.

## (a) Question the page answers

How do IP addresses, subnets and the boundaries between them actually work: where the network/host split sits, how a host decides between sending directly and via the gateway, how the layer-3 subnet relates to the layer-2 VLAN, and what NAT, the DMZ and IPv6 do to the boundary.

## (b) Kept from the original

- The partition-divides-a-room analogy; hosts in a subnet talk directly and a router carries traffic between subnets. The old "router is required to create subnets" wording was dropped (a router is needed for subnets to talk, not to exist).
- The worked example `192.168.21.17` with `/24`: network `192.168.21.0`, host `.17`, mask `255.255.255.0`, and the owner's "logically AND ... the zeros get rid of the host part `17`" explanation. Checked correct. The mask is now derived from the prefix (24 ones, 8 zeros) rather than from "class C".
- The CIDR sentence: `/24` means the first 24 bits are the network part.
- The correct VLAN facts: a VLAN is a layer-2 segment made on switches, subnets are layer 3, and "same VLAN and same subnet, or a router forwards between subnets", with the example corrected to `10.10.20.3/24` and `10.10.20.4/24`.
- NAT as address rewriting at the border so private ranges can be reused.
- DMZ: "neither as secure as the internal network nor as insecure as the public internet" and the origin of the name.

## (c) Dropped and why

- Both bitbucket image embeds (`classful_networks.jpg`, `vlan_switch.gif`): 404, alt text was the filename. The mask bit pattern is now a `text` fence; the VLAN/ARP picture is prose. See (e).
- The pasted DigitalOcean paragraph ("TCP/IP addressing allows you to connect together networks ... three main classes") and the pasted VLAN definition: verbatim third-party text, rewritten in own words.
- "Three main classes" and "default subnet mask for a class C address" as current fact (STALE): classes are now history, CIDR since 1993, "default class C mask" explained as the old name for `/24`.
- "VLAN ... resolves MAC addresses to IP addresses" (WRONG): replaced with ARP mapping IP to MAC.
- "netmask must be equal or smaller" and the `10.10.20.0/24` host example (WRONG): replaced by the each-host-applies-its-own-mask rule, a correct host pair, and an explicit statement that `10.10.20.0` is the network address.
- "Unsolicited traffic is blocked ... NAT prevents outsiders identifying devices" as fact (OPINION): reframed as a side effect of the translation table, with port forwarding, UPnP and hairpinning as the gaps.
- External links to the DigitalOcean and iplocation.net tutorials: replaced by RFC sources.
- After the owner's feedback, also cut: the `/28` mask worked example (kept only the host count), the classful D/E classes and the "wasted addresses" motivation, the cosmetic-separation elaboration (shortened), the cloud-DMZ aside, and the fifth rederive bullet.

## (d) Added, with sources

- Network address (host bits all zero) and broadcast address (all one) are not hosts; usable hosts `2^(32-n) - 2`: 254, 65,534, 14 for /24, /16, /28. Kurose and Ross ch. 4; RFC 4632.
- Mask derived from the prefix as ones then zeros. Arithmetic.
- Classful history: A/B/C at 8/16/24 bits; CIDR RFC 1519 (1993), now RFC 4632. RFC 4632 sections 1 and 2.
- Forwarding decision: AND destination with own mask, on-link vs route table; longest-prefix match; `0.0.0.0/0` as zero-length prefix. Kurose and Ross ch. 4.
- Mismatched-mask example (`.3/25` vs `.200/24`): one direction goes via the gateway and works only if the router forwards back onto the same link. Derived from the rule; corrected after review so it does not claim an outright failure.
- Gateway is a configured router address; AWS implicit router with a reserved address per subnet. Existing VPC Networking page and AWS VPC docs.
- ARP: broadcast "who has X", unicast reply, IP to MAC. RFC 826.
- VLAN membership is per port, the 802.1Q tag carries the VLAN number between switches, a VLAN bounds broadcasts; one-VLAN-one-subnet derived from ARP being a broadcast. Kurose and Ross ch. 6.
- RFC 1918 ranges. RFC 1918 section 3.
- SNAT, DNAT, PAT/NAPT; port forwarding is DNAT. RFC 2663.
- NAT drop of unsolicited inbound as a table side effect; port forwarding, UPnP, hairpinning. RFC 2663 and the audit finding.
- Docker default bridge and cloud NAT gateway named as the same mechanism, closing the inbound link from Containers.md.
- DMZ as firewall rules on both boundaries; defence in depth linked to the security principles page.
- IPv6: 128 bits, `/64` per link, no NAT needed for address sharing, link-local `fe80::/10`, Neighbour Discovery replaces ARP, dual stack. RFC 4291 and RFC 4861 (both added to Sources).

## (e) Diagrams for Phase 5

Both old images were dead. Neither should be redrawn as it was.

1. Replaces `classful_networks.jpg` (old: classful A/B/C table). Draw `ipv4-prefix-and-mask.drawio.svg`: `192.168.21.17` as four octets in binary, a bracket over the first 24 bits labelled "network part (/24)" and over the last 8 labelled "host part", the mask `255.255.255.0` underneath as ones and zeros, and the AND result `192.168.21.0` below. Optional second panel: fixed class boundaries at bits 8, 16 and 24 beside one arbitrary CIDR boundary, to illustrate the history section.
2. Replaces `vlan_switch.gif` (old: hosts on a switch split into VLANs). Draw `vlan-subnet-arp.drawio.svg`: one switch with two VLANs (VLAN 10 carrying `10.10.20.0/24`, VLAN 20 carrying `10.10.30.0/24`); an ARP broadcast from `10.10.20.3` reaching every port in VLAN 10 and stopping at the VLAN boundary; a router (or layer-3 switch) between the two subnets. Label: "ARP maps IP to MAC; the VLAN is where the broadcast stops".
3. Optional, new: `nat-translation-table.drawio.svg`: private hosts on the left, NAT router holding a small table (private address:port to public address:port), internet on the right; one outbound flow rewritten, one reply matched to a row, one unsolicited inbound packet with no row marked "dropped". Only if Phase 5 has capacity.

## (f) Open questions for the owner

- The page says the gateway is "a configured router address on the subnet" and does not claim every network has an implicit one; that is only true of cloud networks. Confirm this is the intended stance.
- The file is 1,199 words by `wc -w`, near the top of the range. If it should go lower, the mismatched-mask example (about 45 words) and the PAT/DNAT bullets are the first candidates; every remaining section is one the outline asked for.
- Containers.md links here with the text "NATted" inside a stray `**`; that page is out of scope for this assignment but the link now lands on a real NAT section.
