# DNS

A client machine is usually configured automatically to the name server of your ISP for domain name resolution. When you set DNS on your computer, you manually override the DNS servers provided by the DHCP server in your router.

When you manually set DNS servers on your router, you manually override DNS servers provided to the router by the DHCP server at your ISP.

When your computer connects to your router, it usually gets [configured](https://www.quora.com/What-is-the-difference-between-setting-your-DNS-choice-on-your-Windows-compare-to-setting-it-on-your-router) by DHCP. That means the computer tells the router "Here I am at ________ MAC address, tell me my IP address, my netmask, my default gateway, and my DNS server". The router acts as the DHCP server.

To perform a DNS query you can use `nslookup hemantkumar.net` to find the IP address of hemantkumar.net

You can trace the route of a network call - `tracert` on Windows `traceroute` on MAC

## DNS Caching

DNS servers cache the records so that if the same server is looked up the results can be retrieved quicker. Your local machines also cache this information.

Each DNS record carries a TTL (Time To Live, in seconds). It tells any caching resolver, whether the stub resolver on your machine, a corporate or public resolver, or your ISP's, how long it may serve the record before querying again. In practice, if a resolver has the current IP address for your website cached for 24 hours, it won't check for a DNS update for your domain until that 24 hours has passed even if you made a DNS change for that domain 5 minutes ago.

On the other hand, someone in another city may be using an Internet Service Provider that hasn't made a query for your domain's DNS settings recently. That person will get the new DNS information right away (and thus be shown your new website right away) because the Internet Service Provider did not cache the information previously.

If your site is going to look exactly the same from one server to another, this is probably not a big deal for you. But if you're "launching" a new site, or if you have a live email address at your domain, you may want to first lower your TTL before making any other DNS changes. This can help you avoid a lengthy period where web traffic and email are going to two servers at once.

You can find out the (remaining) TTL of any given DNS record with the dig command on a MAC:

`dig hemantkumar.net`

On Windows `ipconfig /displaydns` lists the local DNS cache and `ipconfig /flushdns` clears it. On a Mac clear it with `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.

It is possible to raise and lower the TTL (Time To Live) value for your domains with your DNS provider.

On a machine you can override DNS by modifying the `hosts` file `/etc/hosts` on a MAC and `windows\system32\drivers\etc\hosts` on Windows.

## DNS Record Types

**A record** turns a name into an IP address.

**NS record** names the authoritative name servers for a zone (delegation).

`nslookup -type=NS hemantkumar.net` or `dig NS hemantkumar.net`

**MX record** determines Mail Exchange server

`nslookup -type=MX hemantkumar.net` or `dig MX hemantkumar.net`

**CNAME record** determines the canonical name used for aliasing one name to another. For example you may want to access hemantkumar.net through www.hemantkumar.net as well.

`nslookup -type=CNAME www.hemantkumar.net` or `dig CNAME www.hemantkumar.net`

**AAAA record** Quad A IPv6 version of an A record. Turns a name into an IPv6 address.

`nslookup -type=AAAA google.com` or `dig AAAA google.com`

**SOA record** Start Of Authority. One per zone, names the primary name server and the zone's serial number and refresh timers.

**TXT record** free text attached to a name. Used for SPF, DKIM and DMARC mail policies and for domain ownership checks.

**PTR record** the reverse of an A or AAAA record. Turns an IP address back into a name.

**SRV record** locates a service by name, giving the host and port to use, for example for SIP or LDAP.

**CAA record** lists which certificate authorities may issue TLS certificates for the domain.
