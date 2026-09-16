---
title: "Network Layers"
summary: "The four layer TCP/IP model this wiki uses, mapped against OSI, with the protocols and PDUs at each layer."
kind: concept
status: current
last_reviewed: 2026-09-16
sources: []
tags: [network-layers, osi, tcp-ip, tcp, udp, ssh]
---
# Network Layers

Layering convention for this wiki: pages use the four-layer TCP/IP model (application, transport, internet, network access). TLS and SSH are treated as application-layer protocols in that model. OSI layer numbers appear only in the L4/L7 load-balancer vocabulary. The seven OSI layers below are listed for reference.

## OSI Model

* Application - Email, web browser, twitter, facebook
* Presentation - Encryption, compression, translation of encodings (ASCII & EBCDIC) between different OS
* Session - Authenticate and establish a session.
* Transport - End to end delivery of data between processes, addressed by ports. Reliable with TCP or best-effort with UDP.
* Network - Finds the destination network and chooses a path using the routing protocol's metric (hop count, cost, bandwidth or policy), not physical distance
* Data Link - Finds the physical device on the network.
* Physical - Cables, voltages, frequencies, bits transfer rates

![Two columns of network layers. The OSI model's seven layers (application, presentation, session, transport, network, data link, physical) on the left; the TCP/IP model's four layers on the right, with application spanning the top three OSI layers, transport and internet matching one OSI layer each, and network access spanning data link and physical. Each TCP/IP layer lists its protocol data unit (data; segment or datagram; packet; frame) and example protocols (HTTP, TLS, SSH, SMTP; TCP, UDP; IP, ICMP; Ethernet, Wi-Fi). A caption says this wiki uses the four-layer model and counts TLS and SSH as application layer.](../images/network-layers.drawio.svg "OSI and TCP/IP layers")

## TCP/IP

PDU - Protocol data unit

* Application layer - Http, SMTP, Telnet (does not have encryption), SSH (has encryption) are all application level protocols.

* Transport layer - TCP, UDP. Application and transport layer addressing use ports to identify services. A web server listens for http traffic on port 80 and https traffic on 443. A client (browser) also gets a port assigned dynamically from the ephemeral range, 49152-65535 by IANA convention (Windows, macOS) or 32768-60999 by default on Linux. Firewalls make decisions based on the port number.

* Internet layer - Internet protocol, Internet Control Message Protocol (used in ping), Address Resolution Protocol. Internet layer PDU is a **packet**. Internet layer uses IP addresses.

* Network access layer - Ethernet, Fiber optics, copper cables, RJ45, RJ48. PDU is **frames** (for the Data Link) and **bits** (for the Physical layer). Uses a physical address, the MAC address, a 48-bit value written as six hex octets. It is assigned by the factory but can be changed in software, and modern operating systems randomise the Wi-Fi MAC per network. There is a sub layer in the Data Link called Media Access Control.

### TCP

The receiver sends an acknowledgement, therefore it is useful in cases where data loss is unacceptable for example loading an http page. HTTP/1.1 and HTTP/2 use TCP; HTTP/3 uses QUIC over UDP. PDU for TCP is a **segment**.

### UDP

The receiver does not send any acknowledgement and the data is sent without the overhead of establishing a connection. UDP is useful in video streaming. PDU for UDP is a **datagram**.

## Making Http requests

### Curl

Tool to transfer data from or to a server, using one of the supported protocols (DICT, FILE, FTP, FTPS, GOPHER, HTTP, HTTPS, IMAP, IMAPS, LDAP, LDAPS, POP3, POP3S, RTMP, RTSP, SCP, SFTP, SMTP, SMTPS, TELNET and TFTP). Practically speaking its a multipurpose tool built off libcurl to communicate with these protocols. In short, you can use curl to script something that sends data to a system or receive data.

### Telnet

*Unencrypted* terminal protocol, whose client just happens to be useful in testing other applications since it speaks '*raw*' tcp. Sensitive data sent over telnet is susceptible to *packet sniffing*. Connect to your web server through tcp protocol on the port 80

`telnet hemantkumar.net 80` establishes a connection with the host on port 80 and the web server on hemantkumar.net waits for the client to say what it wants. HTTP/1.1 needs the version and a `Host` header followed by a blank line:

```http
GET /index.html HTTP/1.1
Host: hemantkumar.net

```

`telnet gmail-smtp-in.l.google.com 25` connect to the gmail server at port 25 (SMTP or mail traffic is on port 25)

If the host uses ssl you can use **Openssl**

`openssl s_client -connect www.thoughtworks.com:443`

### SSH

Secure shell is the same as telnet but with encryption to allow network services to operate securely over an unsecured network. Both telnet and ssh are application layer protocols.

* Host key fingerprint - a SHA-256 hash of the host's public key for easy identification of the host you are connecting to. OpenSSH defaults to Ed25519 host keys. You can generate the fingerprint for a public key using `ssh-keygen -lf /path/to/key.pub`
* `~/.ssh/known_hosts` - public keys of the ssh hosts that you connect to

## Network Admin Tools

Network Utility was removed from macOS in Big Sur. Use `nmap` or `nc -zv host port` to scan ports. To see which processes are listening on which ports use `lsof -iTCP -sTCP:LISTEN` on a Mac or `ss -ltnp` on Linux; `netstat` also works on both.

| Tool | Question it answers |
|---|---|
| `ping` | Can I reach this host, and how long does a round trip take? |
| `dig` or `nslookup` | What does DNS say this name resolves to, and which server answered? |
| `ss` (`netstat`) | Which sockets are open or listening on this machine, and which process owns them? |
| `ip` (`ifconfig`) | What interfaces, addresses and routes does this machine have? |
| `tcpdump` | What packets are actually going over this interface right now? |
| `wireshark` | Same as tcpdump, but decoded and searchable in a GUI. What is inside these packets? |
| `traceroute` or `mtr` | Which hops does traffic take to get there, and where is it slow or dropped? |
| `nc` (netcat) | Is this port open, and what happens if I send raw bytes to it? |
| `nftables` or `iptables` | Which firewall and NAT rules is the kernel applying to this traffic? |
| `iw` | What is the state of this wireless interface and which networks can it see? |
| `ethtool` | What speed, duplex and link state is this wired interface negotiating? |
| `tc` | How is the kernel shaping, delaying or dropping traffic on this interface? |
| `arp` | Which MAC address does this IP map to on the local network? |