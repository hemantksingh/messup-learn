# Phase 3 report: cloud/aws/EKS.md

File rewritten: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/cloud/aws/EKS.md (about 782 prose words after the owner's tighten pass; target 600 to 800). Not committed. No other file touched.

## (a) Question the page answers

What does AWS manage for me in EKS, what is still mine, and where do pod IP addresses come from? The first paragraph answers all three in plain words; sections then cover the ownership split (managed node groups, Fargate, Auto Mode), IAM-to-RBAC authentication via access entries, pod networking with the VPC CNI and the three fixes for IP exhaustion, version lifecycle, a rederivation section and sources.

## (b) Kept from the original

- The opening observation that running a cluster means management, patching, security, isolation and scaling (reworded as the setup for what AWS takes off you).
- The Fargate isolation passage, nearly verbatim: a dedicated right-sized VM per pod, no two pods share a VM, no shared OS so container escapes stop at the VM boundary, AWS updates the VM OS. All still true.
- The Fargate limitations: no DaemonSets so agents become sidecars, no image cache so slower start, no GPU or instance-type choice. Reframed as consequences of having no nodes, and the log-routing gap filled (see (d)).
- The "value of Fargate is not paying the hidden cost of operations" sentence with its blog link, now on one line (fixing the BROKEN split URL) and marked `> Own view:` because it is a judgement.
- The "one to over 200 IPs per node" observation, kept as "a handful to a couple of hundred", now explained by the ENI and warm-pool mechanism.
- The "many small clusters of at most 100 nodes" preference, kept as `> Own view:` in the owner's words only. The reasons (blast radius, separate upgrade cadence) and the "not a limit" note are stated neutrally outside the blockquote, since the owner did not write them.

## (c) Dropped and why

- "The largest CIDR block for any VPC is /16" and "the /16 VPC size cannot be changed or switched" (WRONG, audit L26-28). Replaced by: a /16 is the largest single block, but a VPC can have several.
- "Each pod will consume an IP address from the whole VPC CIDR block" (WRONG). Pods draw from the subnet of the ENI they sit on, not from the VPC as a whole.
- "Maximum 100 worker nodes" stated as a constraint (OPINION, L28). Now marked as preference with a link to the quotas page; no ceiling asserted.
- "EKS Node Managed" and "control node" terminology (STALE, L5-7). Now "managed node groups" and "control plane".
- The binary Fargate-vs-managed-nodes framing (STALE). Replaced by three modes including Auto Mode.
- The "monitoring has to run in sidecars, no option" framing (STALE, L20). Fargate's built-in Fluent Bit log router is now mentioned.
- After the owner's tighten pass: the aws-auth lock-out explanation, the multi-AZ control plane detail, the "first-class VPC citizen" sentence, and one rederive bullet were cut as detail beyond the question.
- The truncated sentence at L22 (BROKEN in overlaps audit).
- Splunk and Datadog product names: catalogue, not concept.

## (d) Added, with sources

- Control plane runs across several availability zones; upgrades happen when you trigger them. EKS User Guide, cluster architecture and "Update cluster Kubernetes version".
- Managed node groups: you pick instance types and AMI, AWS handles join, drain and rolling update; OS patching is still yours via new AMIs. EKS User Guide, "Managed node groups".
- Fargate built-in Fluent Bit log router. EKS User Guide, "Fargate logging" (aws-observability namespace).
- EKS Auto Mode since December 2024: AWS manages nodes, Karpenter-based scaling and core add-ons; you choose node pools. AWS News Blog, re:Invent 2024 launch; EKS User Guide, "Auto Mode".
- Authentication: kubectl presents a signed AWS request as bearer token, verified via STS; access entries map IAM principals to Kubernetes groups or EKS access policies; aws-auth ConfigMap is legacy and lock-out prone because it was editable only from inside the cluster. EKS User Guide, "Grant IAM users access to Kubernetes with EKS access entries" and "Cluster authentication"; EKS Best Practices Guide, Identity and Access Management.
- VPC CNI mechanism: secondary private IPs on extra ENIs, one per pod; ENIs per node and IPs per ENI depend on instance type, so max pods per node does too; warm pool of pre-assigned addresses is why nodes hold more IPs than running pods. EKS Best Practices Guide, Networking, "Amazon VPC CNI"; amazon-vpc-cni-k8s README (WARM_IP_TARGET, WARM_ENI_TARGET).
- Secondary CIDR blocks including 100.64.0.0/10, and custom networking placing pod ENIs in subnets from that range while nodes stay in the original subnet; the reason 100.64.0.0/10 is chosen (RFC 6598 shared address space, will not collide with corporate plan). VPC User Guide, "VPC CIDR blocks"; EKS Best Practices Guide, "Custom networking".
- Prefix delegation: /28 prefix (16 addresses) per ENI slot; also recovers the density lost when custom networking takes the primary ENI out of pod use. EKS Best Practices Guide, "Prefix mode for Linux".
- IPv6 clusters must be chosen at creation; existing IPv4 clusters cannot be switched. EKS User Guide, "IPv6 for clusters, pods and services".
- Version lifecycle: three Kubernetes minors a year; about 14 months standard support, then paid extended support, then forced control-plane upgrade; upgrade order control plane, nodes, add-ons. EKS User Guide, "Kubernetes version lifecycle" and release calendar. Exact extended-support length and price deliberately left out (brief rule 4).
- "Clusters with thousands of nodes are ordinary": no number asserted; link to the EKS service quotas page.

## (e) Diagrams for Phase 5

The old page had no image. One diagram would carry the networking section: `images/eks-pod-addressing.drawio.svg`. One worker node in subnet 10.0.1.0/24 with its primary ENI holding the node address; two secondary ENIs in a 100.64.x.0/24 subnet from the VPC's secondary CIDR, each ENI showing a /28 prefix slot with pods hanging off the addresses inside it. Label where each address comes from (node: original subnet; pods: secondary CIDR via custom networking; prefix delegation: 16 addresses per slot). Alt text: "EKS node with its own address in the node subnet and pods drawing addresses from /28 prefixes on ENIs in a secondary 100.64.0.0/10 subnet".

## (f) Open questions for the owner

1. Does the "several small clusters, around 100 nodes each" preference still hold? It is preserved as `> Own view:`; if the team has moved on, delete the blockquote.
2. Is Auto Mode the mode you would recommend by default today? The page presents the three modes neutrally and does not pick one. A one-line `> Own view:` would fit if you have a position.
3. Out of scope for this page: `fundamentals/platform/Kubernetes.md` has a "Managing kubernetes clusters" section (line 203) with no link to EKS, and the overlaps audit (Group 3) asked for a "Managed Kubernetes" paragraph there linking EKS and a future Azure AKS page (the AKS kubenet text at lines 102 to 104 of Kubernetes.md still contradicts the no-NAT rule stated at line 90). Whoever rewrites Kubernetes.md should add the cross-link.
4. Pod-to-AWS identity (IRSA and EKS Pod Identity) is the opposite direction from what this page covers and is not mentioned. If you want it, it fits as a short section under authentication or as a paragraph in `cloud/aws/Identity.md`.
