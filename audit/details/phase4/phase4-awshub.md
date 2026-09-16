# Phase 4 report: cloud/aws/README.md (AWS hub)

File edited: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/cloud/aws/README.md (only file touched; not committed).

## (a) Question the page answers

What is in the AWS folder, and what is the one mental model that ties AWS security together? Answer given: every action is an API call that IAM authenticates and authorises; the same three controls (IAM, KMS, VPC) apply to every service; the account is the isolation boundary; shared responsibility says which half is yours; the five Well-Architected control areas (identity, detection, infrastructure protection, data protection, incident response) organise the service families.

## (b) Word counts

Counted with `sed '/^```/,/^```/d' | grep -v '^\s*|' | wc -w` (includes headings and link syntax):
- before: 1594
- after: 1135

Prose only (excluding headings, the six index bullets, the image line and the Sources bullets): about 898, inside the 600 to 900 target.

## (c) What was cut and why

- Per-service marketing descriptions (Detective, Security Hub, GuardDuty, Inspector, Macie, Access Analyzer, CloudTrail, Config, Shield, Systems Manager, Secrets Manager, Parameter Store as H4 catalogue entries): vendor copy; replaced by two or three sentences per control area naming services as examples.
- AWS Config rules table with the "Alerted" column: undefined column, snapshot of one environment, not general knowledge.
- Prowler, ScoutSuite, Security Monkey descriptions: duplicated fundamentals/security/Cloud Security.md; now one sentence naming the AWS Security Assessment Tool (which the trimmed Cloud Security.md line 78 points back to) and linking Cloud Security for the tools. Security Monkey (archived) dropped entirely.
- Systems Manager under Data Protection: an operations service, misfiled; only Parameter Store kept (one sentence, linking Secrets Management).
- Well-Architected reviews and Trusted Advisor bullets: not security fundamentals; Well-Architected survives only as the named source of the five categories.
- Config "can be costly" dzone link: opinion with a third-party link, no concept.
- Inspector Classic's network/host assessment split and "inspector agent required" lines: describes a product that ended support in May 2026.
- GuardDuty "feeds from Proofpoint and Crowdstrike": stale vendor detail (audit L62).
- "Security Best Practices" H2 and the rhetorical question "What are the common security mistakes...": filler.

## Corrections applied (every WRONG, STALE, INCONSISTENT finding against the page)

Index lines were checked against the sibling pages as they stand today (KMS scheduled deletion, stateful security groups, four DR strategies, fan out and DLQs, permission boundaries and ARN format all present).

- S3 bucket quota "100 by default": replaced by "service quotas are enforced per account (most are adjustable)"; no number.
- Security Hub: now "Security Hub CSPM (the original Security Hub, renamed in 2025)" plus the new unified Security Hub, GA December 2025, correlating CSPM, GuardDuty and Inspector findings (verified against the December 2025 announcement; Macie is not listed there).
- Inspector: current service (SSM agent or agentless EBS snapshot scanning; EC2, ECR images, Lambda); Inspector Classic end of support May 2026 stated once.
- "known vulnerabilities such as zero day": dropped the contradiction; Inspector described as known CVEs, GuardDuty as unusual behaviour.
- "HIPPA and GDPA" to HIPAA and GDPR.
- "Analyser" to "Access Analyzer" (product spelling).
- "Guard Duty" to "GuardDuty".
- Shield Standard: applies to every AWS customer at no charge; Advanced is the paid tier. Dropped "when used with CloudFront and Route53" as the condition.
- Parameter Store: per Region limit on the standard tier, paid Advanced tier; no number.
- WAF and Network Firewall added to infrastructure protection.
- H1 changed from "AWS Security" to "AWS" (per assignment).

## (d) What was moved where

Nothing moved to another page. Content dropped rather than relocated, because every dropped item already exists at fundamentals/security/Cloud Security.md (tools), fundamentals/security/Secrets Management.md (Secrets Manager vs Parameter Store trade offs) or the vendor docs.

## (e) Inbound links changed

None needed. Filename unchanged. `grep -rn "README.md#" fundamentals cloud practice` finds no inbound link to any removed anchor. The one inbound link, fundamentals/security/Secrets Management.md line 15 ("The AWS pair is in the AWS hub"), still holds: Secrets Manager and Parameter Store are both named under Data protection.

Outbound links added (targets verified to exist today):
- ../../fundamentals/security/Cloud%20Security.md#tool-categories. The concurrent Phase 4 trim of Cloud Security.md renamed the tools heading to "## Tool categories"; I checked the working tree and used the new anchor. If that page is later renamed to Standards and Compliance, update this link.
- ../../fundamentals/security/Web%20Application%20Risks.md#ddos-protection (working tree heading is now "### DDoS protection", line 109; anchor unchanged).
- ../../fundamentals/security/Secrets%20Management.md

Needed change in a page I did not edit: fundamentals/security/Cloud Security.md line 78 links to this hub with the text "AWS Security"; the H1 is now "AWS", so the link text should become "AWS" or "AWS hub".

## (f) Diagrams for Phase 5

- Redraw images/aws-security-patterns.png as images/aws-security-patterns.drawio.svg: three controls around a generic AWS resource. IAM: who may call the API. VPC: which network path reaches it. KMS: which key encrypts its data. Optionally a CloudTrail strip underneath labelled "every call logged" to connect controls to detection. The wiki plan left the IAM/KMS/VPC icon triad in AWS.drawio page "IAM" as "second file or dropped"; recommend it becomes this hub's diagram. Alt text is already written in the embed; the Sources bullet "Diagram source: AWS.drawio" should be updated to the new file name when the PNG is deleted.
- No tables to build.

## (g) Open questions for the owner

1. H1 is "AWS" as assigned, but rule 7 says H1 equals filename ("README"). Deliberate override for a hub page; confirm this is the convention for cloud/azure too.
2. The sentence "Hence the usual advice: many small accounts under one organisation" is my addition, stated neutrally. Keep, or drop if you do not hold that view.
3. Detection runs about nine sentences over two paragraphs, more than the brief's two or three per category. The Fix list forces most of it (Security Hub CSPM plus the unified Security Hub, current Inspector, the zero-day correction, GuardDuty alerts only). Deliberate; the GuardDuty and Config examples are the first thing to cut if it should be shorter.
4. Incident response mentions EventBridge rules invoking Lambda or Step Functions; this is standard AWS guidance, not from the old page. Fine as a neutral statement, but flagging since it is new text.
5. No `> Own view:` block: the old page held no stance sentences.
