# Endpoint Security

Securing endpoints in an enterprise has traditionally relied on antivirus software which is suitable if you have a limited number of devices that need protection and a small budget to protect them. On the other end, endpoint detection and response (EDR) e.g. [Crowdstrike Falcon](https://www.crowdstrike.co.uk/endpoint-security-products/crowdstrike-falcon-faq/#:~:text=CrowdStrike%20is%20the%20pioneer%20of,via%20a%20single%20lightweight%20agent.) may be your best option for securing numerous devices with a larger budget.

EDR provides real-time anomaly detection and alerting, forensic analysis and endpoint remediation capabilities. It is also preferable if you need to monitor your endpoint security from a higher vantage point.

Endpoint protection platforms (EPPs) are designed to detect and block threats at device level. Typically, this includes antivirus, anti-malware, data encryption, personal firewalls, intrusion prevention (IPS) and data loss prevention (DLP). It is somewhat in the middle in terms of capabilities and scale and are often combined with EDR to create the perfect endpoint security cocktail.

[Chosing an EDR or EDP or both](https://www.esecurityplanet.com/endpoint/antivirus-vs-epp-vs-edr/#how-to-choose) will depened upon the size of your oranization and the sensitivity of the data that you deal with.

## Anti virus

Typical antivirus software scans a user’s computer for malware such as worms, trojans, adware, ransomware, and others. It accomplishes this by using three types of detection:

- Signature comparison, which monitors a device for evidence of known threats and blocks them from taking further action
- Heuristic analysis, which examines new programs for suspicious source code or behavior by comparing it to viruses that are already known from a heuristic database
- Integrity checking, which inspects system files for evidence of corruption

### VirusTotal

VirusTotal is antivirus aggregator that [inspects items with over 70 antivirus scanners](https://support.virustotal.com/hc/en-us/articles/115002126889-How-it-works) and URL/domain blacklisting services and can check for viruses that the user's on antivirus may have missed. It can notify Anti virus software vendors of files flagged by other scans but passed by their own engine to help improve their software and by extension VT's own capability.

VirusTotal's aggregated data is the output of many different

- antivirus engines
- website scanners
- file and URL analysis tools - discriminate between malware sites, phishing sites, suspicious sites, etc
- user contributions

The file and URL characterization tools that are aggregated cover a wide range of purposes: heuristic (shortcut approximations) engines, known-bad signatures, metadata extraction, identification of malicious signals, etc

#### Interpretting the VirusTotal Scan

The [VirusTotal Public API](https://developers.virustotal.com/v3.0/reference#overview) based on the  http://jsonapi.org/ specification provides the aggregated antivirus scanning and URL/domain balcklisting services.

Most AV vendoes work on signature based technology that relies on hash value of a file. The VT API provides static analysis data about a file but is not sufficient by itself to provide reputation https://www.cynet.com/attack-techniques-hands-on/what-are-lolbins-and-how-do-attackers-use-them-in-fileless-attacks/. In addition to VT, other sources can be used to establish reputation of an application:

- https://github.com/fireeye/capa
- https://github.com/JusticeRage/Manalyze
- https://cybergordon.com/

Other useful sites that can run the application and perform analysis in a sandbox environment:
- https://any.run/
- https://www.hybrid-analysis.com/

An [overview of the VT scan](https://www.reddit.com/r/antivirus/comments/gozqc1/understanding_virustotal_results_it_is_not/) can help in understanding each section of the scan result. [Interpreting the VT scan result](https://security.stackexchange.com/questions/231161/how-to-interpret-virustotal-virusscan-scan) requires you to consider your risk appetite.

- do you trust some scanners more than others?
- check the malware names to see if the results are serious e.g. [not-a-virus](https://encyclopedia.kaspersky.com/knowledge/riskware/) is a helpful clarification that the file isn't malicious in and of itself, just that it can be (mis)used
- only trust files that may have been around for a while? Look at the first submission date, if it's before the date that the software or file you're testing was actually released, it's probably recycled malware
- make sure the file type is what it claims to be. 
- look at the other names used for the file, if they refer to something completely unrelated, it's likely renamed malware (though names like update.exe, test.pdf, or a series of random letters, can usually be ignored)
- file is signed with a valid signature - valid code signer, counter signers
- check behaviour - look at the files read, deleted, written, the registry actions, see if it's going where it doesn't need to be
- community score - can be useful but the score needs to be taken with a grain of salt.  Comments tend to be of more useful than just the votes.

Based on the VT fraction percentage, a graded reputation score can be calculated using [two point form](https://math.stackexchange.com/questions/1417845/higher-the-percentage-lower-the-value)

#### Malware hunting

[Threat hunting](https://www.crowdstrike.com/cybersecurity-101/threat-hunting/) is the practice of proactively searching for cyber threats that are lurking undetected in a network. Cyber threat hunting digs deep to find malicious actors in your environment that have slipped past your initial endpoint security defenses.

VT's [YARA](https://yara.readthedocs.io/en/stable) is a tool aimed at (but not limited to) helping malware researchers to **identify and classify malware** samples. With YARA you can 
- create descriptions of malware families (or whatever you want to describe) based on textual or binary patterns
- automatically create IOCs (Indicators of Compromise): artifact observed on a network or OS that with high confidence indicates a computer intrusion

[Livehunt](https://support.virustotal.com/hc/en-us/articles/360001315437) allows you to hook into the stream of files analyzed by VirusTotal and get notified whenever one of them matches a certain rule written in the YARA language. By matching the submitted files with YARA you should be able to

- get a constant flow of malware files classified by family
- discover new malware flying under the industry's radar
- collect files written in a given language or packed with a specific run-time packer
- create heuristic rules to detect suspicious files
- track threat actors, and, in general, enjoy the benefits of YARA's versatility acting on the huge amount of files processed by VirusTotal every day

## Vulnerability Management

When originally deployed, [vulnerability management](https://en.wikipedia.org/wiki/Vulnerability_management) companies acted almost like antivirus vendors in that they tried to get their scanners to uncover as many potential threats as possible. They would even brag about being able to detect more vulnerabilities hiding in testbeds than their competitors. The trouble with that logic is that unlike viruses and other types of malware, vulnerabilities are only potentially a problem. For a vulnerability to be truly dangerous, it must be accessible to an attacker and relatively easy to exploit. So, a vulnerability sitting on an internal resource isn’t much of a potential threat, nor is one that requires additional components like secure access to other network services. Knowing what is truly dangerous is important so that you can plan what to fix now, and what to put off until later or even ignore.

Traditional anti-virus solutions that rely on block listing malware are insufficient to protect today’s systems from the plethora of threats. Security vendors have evolved endpoint protection solutions to include

* firewalls
* host-based intrusion prevention solutions
* even proactive application protection capabilities in order to defend against the evolving threat landscape.

[Retina](https://www.beyondtrust.com/blog/entry/the-retina-protection-agent/) was Beyond Trust's vulnerability management offering that scanned corporate networks and devices and report on all of the security vulnerabilities, zero-day vulnerabilities, and misconfigurations on a host, and provide advanced protection capabilities that co-exist with your existing anti-virus vendor. This layered approach allows you to augment your current anti-virus investment with a tool that can provide vulnerability information for patch management processes and regulatory compliance initiatives. However Retina has been [end of lifed](https://www.beyondtrust.com/vulnerability-management) and for vulnerability management needs, BeyondTrust recommend customers to work with strategic partner Tenable.

### Tenable

Tenable is well known in the industry for creating security dashboards for any environment. They bring that same diagnostic technology to their vulnerability management program, Tenable.io. This platform is managed in the cloud, so it has a small footprint inside a protected organization. It uses a combination of active scanning agents, passive monitoring and cloud connectors to search for vulnerabilities. Tenable.io then applies machine learning, data science and AI to predict which fixes need to be made first before an attacker can exploit them.

One of the biggest strengths of Tenable.io is the fact that it uses both the dashboard and its customized reports to show vulnerabilities in a way that anyone can understand. Whether someone is a developer, part of the operations team or a member of IT security, they can easily comprehend the warnings generated by Tenable.io. In a way, Tenable.io provides vulnerability management to everyone with no specialized training or expertise required.

## Asset and Account discovery

With networks spread across cloud, virtual, mobile and on-premises environments, blind spots are likely to arise. If they do, attackers could exploit those oversights to conceal their malicious activity. IT personnel can defend against these nefarious individuals by gaining visibility over their organization’s networks. They can start by leveraging what’s known as [asset discovery](https://www.tripwire.com/state-of-security/security-data-protection/security-controls/what-is-asset-discovery).

 Separate from vulnerability scans, [BeyondTrust asset discovery](https://www.beyondtrust.com/password-safe/features/discovery) scans assets (web, mobile, cloud, virtual) in your network to discover privileged user accounts, shared accounts, and service accounts.

### Priveleged account discovery

- [BeyondTrust Privileged Identity](https://www.beyondtrust.com/privileged-identity/features/discovery-pi) auto-discovers privileged accounts and shows you where they are used — on a real-time, continuous basis.
