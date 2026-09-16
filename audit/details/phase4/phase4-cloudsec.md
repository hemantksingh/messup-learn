# Phase 4 report: Cloud Security, Endpoint Security, Azure security services

Files edited (absolute paths, uncommitted):

* /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Cloud Security.md (rewritten as TRIM)
* /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Endpoint Security.md (rewritten as TRIM)
* /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/cloud/azure/Tenants, Subscriptions and RBAC.md (append only: `## Security services`, 3 lines including the heading; `git diff` shows 4 insertions, 0 deletions)

No other file touched. No commit.

## (a) Question each page answers

* Cloud Security: which frameworks and control families exist for securing a cloud estate, and how do they relate? Answered with a five-layer stack (threat model, function model, control catalogue, configuration baseline, provider assurance), then the owner's technical controls checklist grouped by family (identity, network, data, detection, response), then tool categories and SIEM versus SOAR.
* Endpoint Security: what protects a laptop or server at the endpoint, and how do I read a malware verdict? Answered with antivirus, EPP, EDR, XDR, MDR, then a "Malware triage" section (VirusTotal reading guide, YARA and Livehunt), then one paragraph placing vulnerability management and PAM as neighbouring disciplines.
* Tenants, Subscriptions and RBAC (appended section only): which Azure services are the CSPM and the SIEM/SOAR, and what happened to the agent workflow.

## (b) Prose word counts (code fences and table rows excluded, same awk before and after)

| Page | Before | After | Target |
|---|---|---|---|
| Cloud Security | 1,250 | 1,163 | 900 to 1,200 |
| Endpoint Security | 1,555 | 897 | 700 to 900 |
| Tenants, Subscriptions and RBAC | unchanged body | +1 paragraph (about 110 words) | at most 8 lines |

The before count for Cloud Security understates the cut: the old page carried two tables (controls checklist, AWS tool table) that the count excluded; the tool table is gone and the checklist is kept.

## (c) What was cut and why

Cloud Security

* Wrong or stale facts (rule 4): "NIST Framework ... 900 controls over 5 functions" replaced with NIST CSF 2.0 six functions as the function model and NIST SP 800-53 as the control catalogue, with the relation stated; "ENSIA" fixed to ENISA; Azure Security Center and Azure Sentinel sections removed (renamed products, deprecated agent workflow), replaced by one link to the Azure page's new section; Scout2 and toniblyx/prowler replaced by ScoutSuite (nccgroup/ScoutSuite) and Prowler (prowler-cloud/prowler).
* Contradiction: the Prowler versus ScoutSuite "superior" rows are gone; both are named neutrally as open-source CSPM scanners in one sentence.
* Catalogue and product detail (rule 2): AWS tool table (CloudMapper, PMapper, aws_public_ips, SQLMap) removed; the Azure marketplace hardened-image sentence removed.
* Misclassified: SQLMap (web SQL injection tester, not a cloud tool) removed; see (e).
* Internal or non-standard labels: "Global SOX Control Model" line removed; "SOR" (not a real acronym, duplicates SOAR) and "PRA" (never used) removed; the whole Acronyms section removed because SIEM, SOAR and SOC are now defined inline.
* Pasted passages (rule 5): the TechTarget CSA paragraph, the SIEM/SOAR paragraphs and the IDS/IPS table cell were rewritten in plain words; the Uptycs article is named inline and in Sources.
* Filler and style (rule 3): "holistic", "most thorough and holistic approach", "equitably", "industry strength", "immense amount", "precious time", "sophisticated" removed; em-dashes removed; American spellings changed.
* Image: `![asc_as.png](../../images/asc_as.png "ASC v AS")` embed removed (screenshot comparing two renamed products; alt text was the filename). The file `images/asc_as.png` is left on disk for Phase 5 to delete.

Endpoint Security

* Wrong: "EDP" fixed to EPP; "Chosing", "depened", "oranization" fixed; "VT's YARA" replaced with "independent open-source pattern-matching tool" and Livehunt described as VirusTotal running your YARA rules.
* Stale: fireeye/capa replaced with mandiant/capa; VirusTotal noted as part of Google Threat Intelligence since 2024; the dead v3.0 API link replaced with the current docs URL.
* Heading typos: "Interpretting" and "Priveleged" gone (the latter with its section).
* Vendor copy (rule 2): BeyondTrust glossary link, Retina EOL history, both Tenable.io paragraphs, BeyondTrust asset discovery and Privileged Identity paragraphs removed. Replaced by one paragraph stating vulnerability management and privileged access management are separate disciplines, keeping the owner's insight that a vulnerability matters only when reachable and exploitable.
* Pasted passages (rule 5): CrowdStrike threat-hunting definition rewritten in one sentence; VirusTotal blog "single pane of glass" integration paragraph cut; Tripwire asset-discovery paragraph cut; Cynet LOLBins link replaced by one plain sentence.
* Vendor phrasing marked OPINION: "may be your best option" and "perfect endpoint security cocktail" neutralised; the two-point-form reputation score is now prefixed "One approach:".
* Structure: VirusTotal and YARA promoted from H4 under H3 under "Anti virus" to `## Malware triage` with two H3s.

## (d) What was moved where

* Azure Security Center and Azure Sentinel content: moved (rewritten, not copied) to `cloud/azure/Tenants, Subscriptions and RBAC.md` as `## Security services`, under the current names Microsoft Defender for Cloud and Microsoft Sentinel, with the agentless-scanning correction and a link back to `../../fundamentals/security/Cloud%20Security.md`.
* AWS tool table: not moved. `cloud/aws/README.md` already names Prowler and ScoutSuite (line 42 in its current working-tree version) and now links to `Cloud Security.md#tool-categories`; that anchor exists in the new page.
* Data Control Framework bullets: folded into the Data rows of the controls checklist table on the same page.
* Nothing moved to Web Application Risks (see (e)).

## (e) Inbound links changed

None. `grep -rn` over fundamentals, cloud, practice and README.md found no existing links to `Cloud Security.md`, `Endpoint Security.md` or `asc_as.png` other than the page's own embed. Two links now point at the pages and both resolve:

* `cloud/aws/README.md:42` -> `../../fundamentals/security/Cloud%20Security.md#tool-categories` (written by another Phase 4 agent; the `## Tool categories` heading exists).
* `cloud/azure/Tenants, Subscriptions and RBAC.md:108` -> `../../fundamentals/security/Cloud%20Security.md` (mine).

Outbound links added from Cloud Security: `Standards%20and%20Compliance.md`, `../../cloud/aws/README.md`, `../../cloud/azure/Tenants,%20Subscriptions%20and%20RBAC.md#security-services`. All targets exist.

Needed change I did not make (file not in my assignment and currently modified by another agent): SQLMap belongs in the tools list of `fundamentals/security/Web Application Risks.md` (section "Web Application Security Tools", about line 40). One bullet: "SQLMap - automates detection and exploitation of SQL injection".

## (f) Diagrams and tables for Phase 5

* Diagram: the five-layer framework stack (threat model -> function model -> control catalogue -> configuration baseline -> provider assurance) with the named frameworks at each layer. The markdown table at the top of Cloud Security is the spec; draw as `images/cloud-security-framework-layers.drawio.svg`.
* Diagram, optional: EPP blocks / EDR records / XDR correlates / MDR operates, as four nested boxes, for Endpoint Security.
* Table: on the Azure page, a two-row Defender for Cloud versus Sentinel table (what it reads, what it produces, who acts) to replace the deleted `asc_as.png` screenshot.
* Delete `images/asc_as.png` (no longer embedded anywhere).

## (g) Open questions for the owner

1. `cloud/azure/Tenants, Subscriptions and RBAC.md` has H1 `# Azure`, which breaks rule 7 (H1 equals filename). The brief said change nothing else, so it is untouched. Fix in Phase 5 or by the Azure page's owner.
2. Cloud Security's checklist table has SOPs and penetration test under "Response". If the owner prefers a sixth family ("Assurance" or "Operations"), that is a one-cell change per row.
3. The "Level 1 / Level 2" CIS profile description and the "fourteen" NCSC principles are stated from memory, not re-verified (rule 9 says do not search for a fact you can omit; both are low severity). Drop the count if unwanted.
4. Endpoint Security keeps the Kaspersky "not-a-virus" link and the math.stackexchange two-point-form link because the owner's heuristics depend on them. Both are 2020-era; check they still resolve in the Phase 5 link sweep.
5. The old page's "Data Control Framework" mentioned S3 and AWS KMS by name. The table row now says "object storage buckets" and "managed key service" to stay provider-neutral; say if the AWS names should return.
