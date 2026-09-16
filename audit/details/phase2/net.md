# Phase 2 corrections: networking (DNS, Network Layers, Local IPC)

Applied 2026-09-16. Nothing committed. Only the three assigned files were written.
Note: `git status` also shows other modified files under `fundamentals/security`, `fundamentals/web and apis`, `cloud/aws` and `fundamentals/networking/TLS Certificates.md`; those are from other agents working in the same tree and were not touched here.

## fundamentals/networking/DNS.md

- was: H1 "# DNS configuration" → now: "# DNS".
- was: "TTL is the value that determines how long your current DNS settings are cached with Internet Service Providers ... if your Internet Service Provider has the current IP address ... cached for 24 hours" → now: "Each DNS record carries a TTL (Time To Live, in seconds). It tells any caching resolver, whether the stub resolver on your machine, a corporate or public resolver, or your ISP's, how long it may serve the record before querying again. In practice, if a resolver has ... cached for 24 hours ...".
- was: "On windows `ipconfig /displaydns` provides you local DNS cache stats" → now: "On Windows `ipconfig /displaydns` lists the local DNS cache and `ipconfig /flushdns` clears it. On a Mac clear it with `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`."
- was: "### DNS Record Types" (H3 nested under DNS Caching) → now: "## DNS Record Types" (H2).
- was: "**NS record** determines the name server used." → now: "**NS record** names the authoritative name servers for a zone (delegation)."
- was: interactive nslookup fragments split across inline code spans (`nslookup` / `set type=NS` / `hemantkumar.net`, and the MX, CNAME, AAAA variants without the `nslookup` entry) → now: one non-interactive line per record type, e.g. "`nslookup -type=NS hemantkumar.net` or `dig NS hemantkumar.net`" (same for MX, CNAME www.hemantkumar.net, AAAA google.com).
- was: only A, NS, MX, CNAME, AAAA listed → now: one-line entries added for SOA, TXT (SPF, DKIM, DMARC, ownership checks), PTR, SRV and CAA in the existing "**X record**" style.

Skipped (deliberately):
- Lines 19 and 21 keep the "Internet Service Provider" framing. They are not wrong once the TTL definition is fixed, and no finding was raised against them.
- The CLASSIFY part of the record-types finding beyond promote-and-extend: nothing to move.

## fundamentals/networking/Network Layers.md

- was: H1 "# OSI Model" → now: H1 "# Network Layers"; the existing OSI bullet list is now under a new "## OSI Model" H2 so it keeps its label alongside the existing "## TCP/IP" H2. (This one H2 is a consequence of the H1 rename; flagging it as the only heading change not literally enumerated.)
- added (Group 10, layering convention): one four-sentence paragraph directly under the H1: this wiki uses the four-layer TCP/IP model; TLS and SSH are treated as application-layer protocols in it; OSI numbers appear only in the L4/L7 load-balancer vocabulary; the seven OSI layers are listed for reference.
- was: "Transport - Guarantee end to end delivery of data. Ensure all packets of data arrive at the destination." → now: "Transport - End to end delivery of data between processes, addressed by ports. Reliable with TCP or best-effort with UDP."
- was: "Network - Finds the destination network, the shortest route not physical distance but shortest time" → now: "Network - Finds the destination network and chooses a path using the routing protocol's metric (hop count, cost, bandwidth or policy), not physical distance".
- was: "SSH (has encryption, therefore uses part of the Presentation layer)" (TCP/IP bullet) → now: "SSH (has encryption)".
- was: "Both telnet and ssh are application layer protocols in the OSI model. As it allows login and encryption SSH uses part of the Presentation layer too." (SSH section) → now: "Both telnet and ssh are application layer protocols."
- was: "a port assigned dynamically between 8000 to 65535" → now: "a port assigned dynamically from the ephemeral range, 49152-65535 by IANA convention (Windows, macOS) or 32768-60999 by default on Linux".
- was: "Firewalls make decisions based on the port number.`" (stray backtick) → now: trailing backtick removed.
- was: "Uses physical address (48 bit hexadecimal layer) also called the MAC address that is physically permanently burnt into a network interface card." → now: "Uses a physical address, the MAC address, a 48-bit value written as six hex octets. It is assigned by the factory but can be changed in software, and modern operating systems randomise the Wi-Fi MAC per network."
- was: "Median Access Control" → now: "Media Access Control".
- was: TCP paragraph implied HTTP is always TCP → now: sentence added: "HTTP/1.1 and HTTP/2 use TCP; HTTP/3 uses QUIC over UDP."
- was: "waits for the client to say what it wants - `GET /index.html`" → now: "... what it wants. HTTP/1.1 needs the version and a `Host` header followed by a blank line:" plus a fenced `http` block containing `GET /index.html HTTP/1.1`, `Host: hemantkumar.net`, blank line.
- was: "`telnet telnet gmail-smtp-in.l.google.com 25`" → now: "`telnet gmail-smtp-in.l.google.com 25`".
- was: "RSA fingerprint - is based on the hosts public key ..." → now: "Host key fingerprint - a SHA-256 hash of the host's public key ... OpenSSH defaults to Ed25519 host keys."
- was: "Port scanning on a MAC is available under Network Utilities. `netstat` can be used to determine which processes are listening on which ports" → now: "Network Utility was removed from macOS in Big Sur. Use `nmap` or `nc -zv host port` to scan ports. To see which processes are listening on which ports use `lsof -iTCP -sTCP:LISTEN` on a Mac or `ss -ltnp` on Linux; `netstat` also works on both."

Skipped (deliberately):
- CLASSIFY: moving "## Making Http requests" and "## Network Admin Tools" to a cheat sheet / Network Tools page. Later phase, per instructions.
- STALE/Low: old curl protocol list. Low confidence and not a typo.
- BROKEN/Medium: image alt text equals filename (osi.gif, network-admin-tools.jpg). Not in the task's fix list and images are handled in a later phase; paths left untouched as instructed.
- Audit's alternate H1 wording "Network Layers (OSI and TCP/IP)": task wording "Network Layers" used instead.

## fundamentals/networking/Local IPC.md

- was: H1 "# Interprocess communication" → now: "# Local IPC" (task wording; the audit's "Interprocess Communication" predates the Phase 1 rename).
- was: "which makes them **faster and lighter than IP sockets**. So if you plan to communicate with processes on the same host, this is a better option than IP sockets." → now: "which, as the StackOverflow answer above puts it, usually makes them **faster and lighter than IP sockets**. So ... this is usually the better option, though loopback TCP is portable and fine for many applications."
- was: "Named pipes allow impersonation - ability of connected clients to use their oen permissions on remote servers. High privilege attacks can impersonate the caller and find information disclosed from the pipe." → now: "Named pipes allow impersonation - the pipe server thread can adopt the security context of the connected client (`ImpersonateNamedPipeClient`). The classic attack is a low privilege process creating a pipe with a predictable name so that a high privilege client connects to it and is impersonated. Clients can limit this by connecting with the `SECURITY_IDENTIFICATION` or `SECURITY_ANONYMOUS` impersonation level. Servers should create pipes with `FILE_FLAG_FIRST_PIPE_INSTANCE` so that creation fails if a pipe with that name already exists." (also absorbs the "oen" typo)
- was: "So in essence a pipe with a default security descriptor can only be accessed by the LocalSystem account." → now: "So with the default security descriptor any local user can read from the pipe, and only LocalSystem, Administrators and the creating owner have full control. Supply an explicit security descriptor when creating the pipe if that is too permissive." (now agrees with the preceding paragraph)
- was: link "https://docs.microsoft.com/en-us/aspnet/core/grpc/interprocess?view=aspnetcore-5.0" → now: "https://learn.microsoft.com/aspnet/core/grpc/interprocess"; bullet added: ".NET 8 and later support gRPC over Windows named pipes as well as Unix domain sockets."
- added (DUPLICATE finding, cross-reference only): "For gRPC as an API style rather than as a transport, see the [gRPC section of API Styles](../web%20and%20apis/API%20Styles.md#grpc)." API Styles.md itself was not edited.

Skipped (deliberately):
- Nothing else was raised against this file. The "Windows 10 build 17063" AF_UNIX paragraph had no finding and was left as is.

## Checks run
- `git status`: my changes are confined to DNS.md, Network Layers.md and Local IPC.md; other modified paths belong to parallel agents.
- The `### gRPC` heading in API Styles.md still exists (line 76), so the `#grpc` anchor resolves.
- Exactly one H1 per file; no em-dashes in any of the three files; the only new code fence is tagged `http`; image paths unchanged.
