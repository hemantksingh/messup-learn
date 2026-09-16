# Phase 5 content edits (2026-09-16)

Six files edited, nothing committed. Repo: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn

## web and apis/HTTP Caching.md

`/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/web and apis/HTTP Caching.md`

* Replaced the `cacheable-content.jpg` embed with a three-row table (Content, Examples, Cacheability): static (images, CSS, simple HTML) easy to cache; dynamic (blog posts, status pages, some API data) micro-cacheable for seconds; user-specific (shopping cart, account data) do not cache at shared caches. Surrounding text untouched.

## platform/Kubernetes Security.md

`/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/platform/Kubernetes Security.md`

* Replaced the `default-cluster-roles.png` embed with a one-sentence lead, a four-row table (Role, Scope, Can, Cannot) and a two-sentence note on why `edit` can read Secrets and `view` cannot, with a link to the Kubernetes RBAC docs (user-facing roles).
* Verified against the live docs text. One correction to the brief: the docs do not say `edit` or `view` cannot *view* resource quotas. The docs say `admin` cannot write resource quotas or the namespace itself; `edit` cannot view or modify Roles and RoleBindings (and, being a subset of admin, cannot write quotas); `view` cannot view Roles, RoleBindings or Secrets. The table follows the docs. It also carries the docs' detail that `cluster-admin` in a RoleBinding controls the namespace object itself.
* The five `# ` matches in this file are shell comments inside `sh` fences, not headings. One real H1.

## networking/Network Layers.md

`/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/networking/Network Layers.md`

* Replaced the `network-admin-tools.jpg` embed (Julia Evans zine, copyrighted) with a 13-row table, one line per tool, "tool, question it answers", in plain words: ping, dig or nslookup, ss (netstat), ip (ifconfig), tcpdump, wireshark, traceroute or mtr, nc (netcat), nftables or iptables, iw, ethtool, tc, arp.
* `osi.gif` embed left in place for the Phase 5 redraw. Nothing else changed.

## security/Standards and Compliance.md

`/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/security/Standards and Compliance.md`

* H1 changed from "Compliance" to "Standards and Compliance" (matches the filename and the inbound link from Cloud Security).
* Removed the `windows-schannel.png` embed and its blank line. The Schannel paragraph never referred to the picture, so no clause was added. Nothing else changed.

## security/Data Privacy.md

`/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/security/Data Privacy.md`

Rewritten per the audit findings for the old `Security/Data Security.md` lines 1 to 78. Owner's PII explanation and examples kept. About 990 prose words (excluding headings and Sources). One H1 "Data Privacy". No "Own view" text.

* Staff email: removed the false "GDPR exemption". Now: work email is personal data; employers rely on contract, legal obligation or legitimate interests, not consent.
* Fingerprinting: the 94% figure attributed to EFF Panopticlick (Eckersley, 2010) and marked as history since Flash and Java applets are gone; canvas, WebGL, audio and fonts added as the modern vectors (both in the attribute list and the bullet). "Active plugins" bullet replaced by "installed fonts".
* UK law: UK GDPR plus the Data Protection Act 2018 (replaced DPA 1998), amended by the Data (Use and Access) Act 2025. Replaced the wrong "It replaced the Data Protection Act".
* Fines: EUR 20 million or 4% of global annual turnover, whichever is higher; UK cap GBP 17.5 million.
* Added one line on lawful bases. Fixed "minimization" to "minimisation" and the "Rights to in relation to" typo.
* "Schrems II" section renamed "International transfers" and brought up to date: Schrems II (16 July 2020), new SCCs (June 2021, Decision 2021/914), UK IDTA and Addendum (2022), EU-US Data Privacy Framework adequacy (10 July 2023, Decision 2023/1795), Latombe v Commission dismissed by the General Court (3 September 2025, T-553/23), appeal C-703/25 P pending. Checked by web search today: the appeal was lodged 31 October 2025 and no judgment has been reported. The old en-dash on this page is gone with the rewrite.
* PCI DSS: its own section removed. One sentence remains at the top of `## Controls` (industry standard from the PCI SSC, founded by the five card brands, not a regulation by processors) with a link to `Standards%20and%20Compliance.md`.
* `## Controls` also holds a one-line data masking note that agrees with Cryptography Basics line 78 (shows part, hides the rest, no key, no way back) and links back to `Cryptography%20Basics.md`.
* Added `## Sources` as a bullet list matching the Cryptography Basics and Cloud Security pages. The two external links (EFF PDF, ICO lawful basis guide) return 200.

## platform/Configuration Management.md

`/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/platform/Configuration Management.md`

* H1 changed from "Ansible" to "Configuration Management".
* One opening sentence added: configuration management is declaring the desired state of machines and having a tool converge them to it; Ansible is the tool this page uses as the example.
* "control server" changed to "control node" (both occurrences).
* Where push over SSH is first described, added a clause: WinRM for Windows hosts, and `ansible-pull` inverts the model so each node fetches and applies a playbook from git.
* "Ansible in practice" section and the `ansible-components.png` embed kept. Nothing else changed. Noticed but left alone under "change nothing else": "deployements" typo on line 5.

## Verification (all six files)

* Exactly one H1 per file (Kubernetes Security's extra `# ` lines are shell comments inside fences).
* Every code fence opening line carries a language tag; no bare fences.
* No en-dash or em-dash (U+2013, U+2014) in any of the six. The owner's ` - ` separator style is untouched.
* All relative links resolve: `Standards%20and%20Compliance.md` and `Cryptography%20Basics.md` from Data Privacy; `../images/osi.gif` and `../images/ansible-components.png` still exist.
* No filler phrases ("In practice", "worth noting", "Importantly") and no "Own view" text added.
* `git status`: six modified files, nothing staged or committed.
