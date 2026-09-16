# Endpoint Security

Securing endpoints in an enterprise has traditionally relied on antivirus software, which is suitable if you have a limited number of devices to protect and a small budget. At the other end, endpoint detection and response (EDR), for example CrowdStrike Falcon, suits numerous devices and a larger budget.

EDR provides real-time anomaly detection and alerting, forensic analysis and endpoint remediation. It is also preferable if you need to monitor your endpoint security from a higher vantage point.

Endpoint protection platforms (EPPs) are designed to detect and block threats at device level. Typically this includes antivirus, anti-malware, data encryption, personal firewalls, intrusion prevention (IPS) and data loss prevention (DLP). An EPP sits in the middle in capability and scale and is often combined with EDR: the EPP blocks what it recognises, the EDR records and investigates what got past it.

XDR (extended detection and response) widens EDR beyond the endpoint to correlate identity, email, network and cloud signals. MDR (managed detection and response) is EDR or XDR operated for you by a vendor's analysts.

[Choosing an EDR or EPP or both](https://www.esecurityplanet.com/endpoint/antivirus-vs-epp-vs-edr/#how-to-choose) will depend upon the size of your organisation and the sensitivity of the data that you deal with.

## Antivirus

Antivirus software scans a computer for malware such as worms, trojans, adware and ransomware using three types of detection:

* Signature comparison monitors a device for evidence of known threats and blocks them from taking further action
* Heuristic analysis examines new programs for suspicious code or behaviour by comparing it to viruses already known from a heuristic database
* Integrity checking inspects system files for evidence of corruption

## Malware triage

VirusTotal is an antivirus aggregator. It [inspects a submitted file or URL with over 70 antivirus engines](https://support.virustotal.com/hc/en-us/articles/115002126889-How-it-works) and URL and domain blocklists, and can catch what the user's own antivirus missed. Since 2024 it is part of Google Threat Intelligence. The [public API](https://docs.virustotal.com/reference/overview) exposes the same data as the site.

### Reading a VirusTotal result

The API gives static analysis data about a file. That is not a reputation by itself. Living-off-the-land binaries are legitimate, signed system tools that attackers misuse, and they come back clean. Other sources help establish reputation: [capa](https://github.com/mandiant/capa) reports what a binary is capable of, [Manalyze](https://github.com/JusticeRage/Manalyze) does static analysis of PE files, [CyberGordon](https://cybergordon.com/) queries many reputation sources for a hash, IP or domain. Sandboxes that run the file and report its behaviour: [any.run](https://any.run/) and [Hybrid Analysis](https://www.hybrid-analysis.com/).

[Interpreting the scan result](https://security.stackexchange.com/questions/231161/how-to-interpret-virustotal-virusscan-scan) requires you to consider your risk appetite.

* Do you trust some scanners more than others?
* Check the malware names to see if the results are serious. [not-a-virus](https://encyclopedia.kaspersky.com/knowledge/riskware/) means the file is not malicious in itself, only that it can be misused.
* Only trust files that have been around for a while? Look at the first submission date. If it is before the software you are testing was released, it is probably recycled malware.
* Make sure the file type is what it claims to be.
* Look at the other names used for the file. If they refer to something unrelated, it is likely renamed malware. Names like update.exe, test.pdf or random letters can usually be ignored.
* Is the file signed with a valid signature, with a valid code signer and counter signers?
* Check behaviour: files read, deleted and written, registry actions. See if it is going where it does not need to be.
* Community score can be useful but take it with a grain of salt. Comments are more useful than the votes.

One approach: based on the fraction of engines that flag the file, calculate a graded reputation score using the [two point form](https://math.stackexchange.com/questions/1417845/higher-the-percentage-lower-the-value) of a line, so a higher detection percentage gives a lower reputation.

### Hunting with YARA

Threat hunting is searching for attackers already inside who got past the endpoint defences, rather than waiting for an alert.

[YARA](https://yara.readthedocs.io/en/stable) is an independent open-source pattern-matching tool that malware researchers use to identify and classify samples. With YARA you can

* describe malware families (or anything else) by textual or binary patterns
* turn those descriptions into indicators of compromise (IOCs): artefacts on a network or OS that indicate an intrusion with high confidence

VirusTotal [Livehunt](https://support.virustotal.com/hc/en-us/articles/360001315437) runs your YARA rules against the stream of files VirusTotal analyses and notifies you on a match: a constant flow of malware classified by family, new malware flying under the industry's radar, and a way to track threat actors.

## Neighbouring disciplines

Vulnerability management and privileged access management are separate disciplines, not parts of endpoint protection. A vulnerability is only a potential problem: it matters when an attacker can reach it and exploit it, so the work is prioritising what to fix now and what to defer, not counting findings.

## How to rederive this

* Antivirus recognises; EDR records and lets you investigate what was not recognised.
* A signature is a hash. Changing one byte defeats it, so heuristics and behaviour analysis must exist.
* A clean static verdict is not a reputation. Legitimate signed tools are the attacker's favourite tools.
* A YARA rule is a description of a family; running it against a feed turns a description into a detector.

## Sources

* eSecurity Planet, "Antivirus vs EPP vs EDR"
* VirusTotal documentation: How it works, API, Livehunt
* YARA documentation; mandiant/capa README
* security.stackexchange.com, "How to interpret VirusTotal scan"
