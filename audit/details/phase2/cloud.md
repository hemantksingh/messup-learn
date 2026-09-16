# Phase 2 corrections: cloud (6 files), 2026-09-16

Nothing committed. Only the six assigned files were touched (`git status` also shows modified files under `fundamentals/` and `practice/`; those are not mine). Every edit was a targeted replacement of a sentence with a finding against it; untouched paragraphs were not re-emitted. All six files: exactly one H1, no em-dashes, every fence tagged, trailing newline present. Both JSON policies in Identity.md parse with `json.loads`. The Phase 1 "Locking down network access to Azure services" section is byte-identical to before. No web verification was needed; every High replacement fact was supplied by the parent and most are marked verified in `audit/details/aws.md`.

## cloud/aws/Identity.md

- was: H1 "IAM" → now: "AWS Identity and Access Management"
- was: "'I' stands for authentication and 'AM' stands for authorization" → now: "Identity = who (authentication), Access Management = what they may do (authorization)"
- was: "AWS services - identity for non-human resources e.g. EC2 instance, Lambda..." → now: "IAM roles for workloads" bullet: workloads get identity by assuming a role (instance profile, Lambda execution role, ECS task role); the service appears only as a service principal in the trust policy
- was: "AWS Cloud Trail" → now: "AWS CloudTrail"
- was: `<img src=... title=... width= height=>` with no alt → now: Markdown image with descriptive alt text and the same title
- was: Roles = "Collection of policies that you can use to access AWS resources" → now: "An identity with a trust policy (who may assume it) and attached permission policies (what it may do)"
- was: "Not all resources allow you to define resource based policies e.g. dynamodb" → now: "e.g. EC2 instances (DynamoDB tables do, since March 2024)"
- was: "IAM Policies are generally applied to Groups..." → now: same sentence plus "For human access, prefer IAM Identity Center with permission sets over IAM users and groups altogether"
- was: four evaluation bullets → now: fifth bullet added: identity and resource policies grant, SCPs, RCPs (Nov 2024), session policies and permission boundaries only restrict, request must pass every applicable type, link to the AWS policy evaluation logic page
- was: "Root Account ... should be secured with MFA" → now: MFA on root mandatory for management accounts since 2024; centralized root access (Nov 2024) lets you remove root credentials from member accounts
- was: ARN format `arn:partition:service:region:account_id`, partitions aws|aws-cn → now: `arn:partition:service:region:account-id:resource-id` (or `resource-type/resource-id`), partitions aws|aws-cn|aws-us-gov, plus a resource example and the S3 empty-segment case
- was: one `json` fence holding two policies with `//` comments and a missing comma → now: two valid `json` fences, comments moved into prose above each block, comma added after the `Action` array

## cloud/aws/Key Management.md

- was: "Key deletion for customer managed key is instantaneous" → now: scheduled with a mandatory 7 to 30 day waiting period (default 30), unusable while pending, cancellable; still disable first and test
- was: "rotated automatically every year" → now: automatic rotation with a period configurable 90 to 2560 days (default 365) since April 2024, plus on-demand rotation
- was: "Automatic key rotation is not supported for imported keys..." → now: same, plus "On-demand rotation of imported key material is supported since June 2025"
- was: "Service managed keys e.g. (S3 default encryption)" / "Customer managed key where customers generate the key material" → now: the three AWS categories: customer managed keys (KMS-generated material by default, import or custom key store as alternatives), AWS managed keys (`aws/s3`, visible, read-only key policy, cannot delete), AWS owned keys (invisible, no key policy; S3 default encryption SSE-S3 uses these). Lead-in "Different types of key material are allowed in KMS" reworded to match, since the categories are about who controls the key, not material type
- was: "disable the CMK first" → now: "disable the KMS key first" (no other "CMK" occurrences existed)
- was: custom key store = CloudHSM only → now: fourth key-material bullet for External Key Stores (XKS, 2022) with material held outside AWS behind an XKS proxy
- was: "FIPS 140-2 validated ... FIPS 140-2 Level 3" → now: FIPS 140-3 Level 3 for both the default KMS HSMs and CloudHSM; the shared-vs-dedicated contrast is kept, the validation-level contrast is dropped because it no longer exists
- added: one paragraph on envelope encryption (4 KB limit per call, data key returned in plaintext and encrypted, plaintext copy discarded, encrypted copy stored with the data, KMS key never leaves the HSM)
- added: trailing newline (file had none)

## cloud/aws/VPC Networking.md

- was: H1 "Networking" → now: "AWS VPC Networking"
- was: "A router is required to create subnets" → now: every VPC has an implicit router; you never create one, you only edit its route tables
- was: "by default everything is blocked" → now: a new security group denies all inbound and allows all outbound
- was: "stateful - any changes applied to an incoming rule will be automatically applied to the outgoing rule ... outgoing port 80 will be automatically opened" → now: return traffic for an allowed connection is permitted without a rule in the other direction; rules are not mirrored; port 80 example deleted and replaced with the correct statement
- was: NACL "stateless, therefore explicit rules are enforced for inbound and outbound traffic" → now: both directions need explicit rules, a reply only gets out if an outbound rule allows it
- was: timeout "no inbound route defined in your route table or network ACL" → now: security group listed first, then route table, then NACL
- was: "standard 1 GB or 10 GB Ethernet fiber-optic cable" → now: dedicated ports 1, 10, 100 or 400 Gbps (400 since July 2024); hosted connections 50 Mbps to 25 Gbps; unit Gbps
- was: "predictable network performance and 60% cost savings" (plus stray "the") → now: "predictable network performance"; figure removed, not replaced
- was: "### AWS-manged VPN" / "AWS-managed VPN is a hardware IPsec VPN" → now: "### AWS Site-to-Site VPN" / "AWS Site-to-Site VPN is a managed IPsec VPN"
- was: "Requires a Network LB on the service VPC" → now: NLB or Gateway Load Balancer; PrivateLink Resource Gateway (Dec 2024) shares an individual resource without a load balancer
- was: gateway endpoints "Free: No hourly charges, just data transfer charges" → now: no hourly charge and no data processing charge for the endpoint
- was: "the default interface, `eth0`" → now: "`eth0` or `ens5` depending on the AMI"; the two em-dashes in that same sentence became a colon and a comma
- was: VGW "does not introduce any extra latency" / TGW "experiences a slight delay" → now: "adds little latency" / "adds a small amount of latency as an extra hop"
- added: trailing newline (file had none)

## cloud/aws/Messaging.md

- was: H1 "Asynchronous messaging" → now: "AWS Messaging: SNS, SQS and EventBridge"
- was: "AWS provides 3 alternatives for messaging:" → now: "AWS offers many messaging services; this note covers three:"
- was: "If the consumer is down " (truncated) → now: completed: SNS retries per the subscription's delivery policy and can send messages that still fail to a subscription dead-letter queue (an SQS queue)
- was: "SNS messages are sent once regardless of the consumer availability" → now: SNS is push based with per-subscription retries and optional subscription DLQ; it does not persist messages for polling, SQS does
- was: "if the lambda fails the message is lost" (and the opener "if you do not care about lost messages") → now: Lambda retries async invocations twice, then on-failure destination or Lambda DLQ if configured, plus the SNS subscription DLQ; lost only if none are set up. Opener now reads "if Lambda's built-in retries are enough for you"
- was: "Message Bus (topic)" → now: "Event Bus"
- was: "EventBridge Pipes provide many out of the box integrations ... Datadog, PagerDuty, Shopify" → now: three bullets: partner event sources (SaaS to bus), API destinations (bus to external HTTP), Pipes (Dec 2022, point-to-point source, filter, enrich, target)
- added: one bullet on ordering and filtering (standard = best-effort order, at-least-once; SQS FIFO and SNS FIFO topics = ordering within a message group plus deduplication; SNS filter policies on attributes and, since 2022, payload)
- added: trailing newline

## cloud/aws/Disaster Recovery.md

- was: "RPO - Data recovery back to the point prior to the disaster or Point In Time Recovery (PITR)" → now: maximum acceptable data loss expressed as time between last recoverable point and the incident; PITR is a feature that helps meet a low RPO, not the definition
- was: "RTO - Amount of time it takes to get your system operation after a disaster" → now: maximum acceptable time between disaster and system operational again; a target, not a measurement. Not in the parent's per-file list, applied from the README "Cloud" bullets (shared Medium WRONG with DevOps and Delivery)
- was: "PRD/STG factor = Row Count in PRD / Row Count in STG ... >= 1 ... at least 0.60" → now: STG/PRD = STG rows / PRD rows, ideal 1.0, aim for at least 0.60, labelled "a personal heuristic, not an AWS guideline"
- was: "granularity down to the second in the last 35 days" → now: recovery window configurable from 1 to 35 days (default 35). The "system backup ... retains it for 35 days" line was left, it is still correct
- was: "RTO/PTO" → now: "RTO/RPO"
- was: only active/active and generic active/passive → now: four-strategy list added after that sentence (backup and restore, pilot light, warm standby, multi-site active/active) with what each trades off
- was: "deployed in a redundant region costs you no money" → now: costs little at idle; fixed-cost components (provisioned concurrency, Route 53 health checks, CloudWatch alarms) still bill
- was: "automatically span across all availability zones" → now: "span multiple availability zones"
- was: global tables sentence with no replication model → now: "multi-active: every replica accepts writes, last-writer-wins by default, since 2025 multi-Region strong consistency is an option at the cost of higher write latency" ("multi-master" only appears in the drawio label, not the text)
- was: "Write requests for the replication storage (per million units)" + data transfer → now: replicated write request units per replica region, storage per replica region, inter-region data transfer

## cloud/azure/Tenants, Subscriptions and RBAC.md

- was: "Azure isolation allows distributing the cost of shared azure resources among multiple customers, preventing the risk of sharing" → now: Azure is multi-tenant (cost spread); isolation is what stops that sharing becoming a risk
- was: "Azure AD" / "Azure Active Directory" throughout → now: "Microsoft Entra ID (formerly Azure AD)" on first use with the note that the `az ad` CLI group did not change, then "Entra ID"; headings "### Azure AD" → "### Entra ID", "### IAM for Active Directory" → "### IAM for Entra ID". "AD authentication" → "Entra authentication"
- was: bare-metal / Windows Firewall bullet → now: dropped (historical Microsoft statement not needed for the tenant model)
- was: "#### Transferring subscription to a different tenant" directly under H1 → now: H2
- was: "2 roles that get automatically assigned ... Account Admin ... Service Admin" → now: Account Administrator (billing role, not RBAC) plus Azure RBAC Owner at subscription scope; Service Administrator and Co-Administrator retired 31 Aug 2024
- was: "Transferring ... means the account admin and service admin change to the target tenant" → now: transfer does not by itself change the billing Account Administrator; RBAC role assignments, managed identities etc. are deleted and have to be recreated in the target directory. Did not state who becomes Owner after transfer (would be inventing)
- was: `![azuread-subscription.png]` / `![tenant-transfer.png]` with the copy-pasted title "AzureAD and Subscription Association" / `![access-patterns.png]` / `![azure-role-assignment.png]` → now: descriptive alt text on all four; tenant-transfer title is now "Transferring a subscription between tenants"
- was: "It [Azure AD] can be configured at different levels e.g. for a particular resource group, app service, storage account or the Azure subscription" → now: the directory is tenant-wide; Azure RBAC role assignments are what get scoped to management group, subscription, resource group or resource
- was: Managed Identities = system assigned only → now: system-assigned (lives and dies with one resource) and user-assigned (standalone, shareable, outlives the resources) with "no secret to store or rotate"
- was: portal click-path "select your account in the top-right corner -> My permissions -> ..." → now: `az role assignment list --subscription <subscription-id> --all --output table` in a `bash` fence, plus the direct "Subscriptions -> Access control (IAM)" path
- was: v1.0 token endpoint only → now: v1.0 and v2.0 endpoints listed, v2.0 recommended (scopes instead of resource identifier, personal accounts)
- trivial typos fixed: permiter, ensureing, resourecs, SQl, manging, subsctiption
- untouched: Phase 1 "Locking down network access to Azure services" section (byte-identical)

## Skipped deliberately

- Disaster Recovery: export of the `AWS.drawio` "Serverless DR" page and embedding it (High BROKEN) needs a diagram tool, not a text edit. Split/rename of the generic RTO/RPO section (CLASSIFY) skipped per instructions.
- Disaster Recovery / Identity / Azure: adding "Diagram source: AWS.drawio / AzureAd.drawio" lines under images was not in the parent's list.
- Key Management: multi-Region keys, HMAC keys and default key policy statement (Medium STALE "missing features"); parent listed only envelope encryption, so only that was added.
- Identity: `aws-iso*` / `aws-eusc` partitions omitted; parent listed three partitions.
- VPC Networking: tables nested inside list items (Low BROKEN). They sit two levels deep inside a list that continues after them (NAT Gateway, VPC Endpoints), so pulling them out splits the list. Not a small change; left.
- VPC Networking: VGW/TGW bullet normalisation L75-82 (Low BROKEN) and the "VPC_Scenario2/3/4" wizard framing (Low STALE) not listed; only the latency wording was softened.
- VPC Networking: `![aws-vpc.png]` filename-as-alt has no finding against it; left.
- Azure: H1 "Azure" now mismatches the new filename (Low BROKEN); not in the parent's list, left for the owner to decide the convention.
- Azure: portal click-paths "List all the SPs: -> Select Role Assignments -> ..." (L76-78) describe the screenshot and had no finding; left.
- Messaging: SNS FIFO archive/replay (2024) not added; parent asked only for ordering and filtering.
- No DUPLICATE findings exist against any of the six files, so no cross-links were added.
- No CLASSIFY findings were applied anywhere.
