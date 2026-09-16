# Phase 4 report: Infrastructure as Code (TRIM)

File edited: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Infrastructure as Code.md` (old name `Cloud and Infrastructure/DevOps/Terraform.md`). No other page edited. Nothing committed.

## (a) Question the page answers

What does infrastructure as code give me, how does Terraform's model work, and where does state fit?

Sections in order: what IaC gives you (declared end state, plan then apply, drift) · Terraform's model (provider, resource, data source, module, variables/locals/outputs, with Providers, Resources and data sources, Modules as H3) · State (remote state and locking, workspaces) · Workflow: init, plan, apply · Provisioners · ARM templates and Terraform · Terragrunt · Licence · How to rederive this · Sources.

## (b) Prose word counts

Counted with `awk '/^```/{f=!f;next} !f' | grep -v '^|' | wc -w` (fences and table rows excluded; headings, bullets and Sources included).

| | Before | After | Target |
|---|---|---|---|
| Infrastructure as Code | 1,404 | 1,399 | 1,100 to 1,400 |

The count barely moved because the brief's required additions (IaC intro with drift, outputs, state explanation, ARM table sentence, licence, 1.x sentence, rederive, Sources) roughly equal the cuts.

## (c) What was cut, by category

**Pasted or unattributed text**
- The six intro bullets ending "The last part of this article goes into this feature in detail" (external article paste). Rewritten as the owner-voice "What infrastructure as code gives you" list plus one HCL paragraph.
- HashiCorp-doc paraphrases that were near verbatim: "A provider is responsible for understanding API interactions and exposing resources", "A module is a container for multiple resources ... lightweight abstractions", "Terraform stores state ... map real world resources ... improve performance", "A backend determines how state is loaded and how an operation such as apply is executed", "Terraform CLI workspaces are associated with a specific working directory", "The persistent data stored in the backend belongs to a workspace", "Provisioners can be used to model specific actions", and the workflow intro about "plugins called providers ... application programming interfaces (APIs)". All rewritten in short plain sentences.

**Wrong or stale (audit findings, all now absent)**
- "Open source project with a community of thousands of contributors" replaced by the Licence section (BSL 1.1 August 2023, OpenTofu fork, Terraform Cloud is HCP Terraform).
- Provider snippet with `version = "~> 1.0"` inside `provider`, `cliend_id` typo and no `features {}`: replaced by a `terraform { required_providers {...} }` block plus `provider "azurerm" { features {} ... }` with `client_id` spelled right.
- `terraform apply "my.tfpan"` is now `terraform apply my.tfplan`.
- `null_resource` is now `terraform_data`; `depends_on` and `local-exec` kept; heredoc changed to `<<-EOT` so the indented closing marker is valid.
- Hard-coded `access_key = "access_key"` in the backend replaced by `use_azuread_auth = true`; the bare `backend` block is now wrapped in `terraform { }` so it is valid HCL; a sentence says to use `ARM_ACCESS_KEY` or `-backend-config` if a key is unavoidable.
- "managed service identity" is now "managed identity"; `azcli` is now "Azure CLI (`az`)".
- Three-provider list replaced by one sentence naming `azurerm`, `azuread` (keeps its name though the product is Entra ID), `azapi`, `azurestack` (minimal).
- "Passing variables to modules" reasoning ("variables are initialized before any parsing") corrected to: a variable default must be a literal; compute in a `local` and pass the local. Original discuss.hashicorp link kept.
- "At present, the dependency lock file tracks only provider dependencies" reduced to "pins provider versions but not module versions" with no time qualifier.
- Terragrunt closing clause "terraform plans are based on diffs as opposed to a complete state refresh" dropped (plan still refreshes by default). The owner's first half, "Terraform has probably evolved to fill the gap in functionality that terragrunt once provided", kept verbatim as `> Own view:` (verified against `git show HEAD`).
- Workspaces limitation stated neutrally: all workspaces of one configuration share one backend, so every environment's state lands in one store; HashiCorp's advice for separate backends is separate root configurations. "Unfortunately" removed.

**Structure and formatting**
- H1 changed from `# Terraform` to `# Infrastructure as Code`.
- Every HCL fence retagged `hcl` (4 blocks); shell commands in `sh`. The dev/qa/prod list left its fence and is a normal list.
- "Arm and Terraform" section (heading with no ARM content, plus the slide embed) replaced by "ARM templates and Terraform": one 8-row markdown table built from `arm-terraform.png` plus one sentence that Bicep is the current ARM language.
- `![arm-terraform.png](../../images/arm-terraform.png)` embed removed. The PNG file is left in `images/` for Phase 5 to delete.

**Product detail and asides cut for budget**
- `TF_LOG=DEBUG` debugging tip.
- Provider `alias` sentence.
- Cloud Shell has `az` and `terraform` installed.
- Terragrunt bullet tree (per-environment `terragrunt.hcl`, tfvars StackOverflow link, `-var-file="common.tfvars" -var-file="$env.tfvars"` alternative) compressed to three sentences plus the own view.
- Module structure sentence reduced to the link.
- Terraform Cloud, DNSimple, Cloudflare, Heroku, Alibaba examples in the provider definition.

**Added (only what the brief or a fix required)**
- IaC opening with declared end state, plan before apply, repeatability, drift.
- Outputs and locals in the model list.
- Two paragraphs on what state is and why plan needs it (configuration vs state = your change; state vs API = drift), and why state is sensitive.
- One sentence naming `moved` blocks, `import` blocks and the test framework as things to look up. No versions.
- `## How to rederive this` (4 bullets) and `## Sources`.

## (d) What was moved where

Nothing moved to another page. The ARM slide's content moved from an image into a table on the same page.

## (e) Inbound links changed

None. `grep -rn -i "Terraform.md\|Infrastructure%20as%20Code\|Infrastructure as Code.md" fundamentals cloud practice README.md` returned nothing; no page links to this one.

Suggestion, not done (out of scope): `fundamentals/platform/DevOps and Delivery.md` line 85 names "Terraform, OpenTofu, CloudFormation, AWS CDK, Bicep and Pulumi" in plain text and could link to `Infrastructure%20as%20Code.md`.

## (f) For Phase 5

- Table: the ARM template to Terraform mapping is already a markdown table on the page (8 rows). `images/arm-terraform.png` (60 KB slide) is no longer embedded anywhere and can be deleted.
- Diagram to draw, `images/iac-state-map.drawio.svg`: three boxes, Configuration (HCL), State (`terraform.tfstate`, resource address to real id), Real infrastructure (API). Two arrows labelled as the two comparisons plan makes: configuration vs state = "your change", state vs API = "drift". Embed under `## State`.
- Optional: a small remote-state picture, two engineers, one locked blob in a storage account, one lease. Probably not worth a file; the text carries it.
- Link check: all `www.terraform.io/docs/...` and `learn.hashicorp.com` URLs on the page were swapped for `developer.hashicorp.com` equivalents; `registry.terraform.io`, `discuss.hashicorp.com`, `terragrunt.gruntwork.io`, the HashiCorp BSL blog post and `opentofu.org` remain.

## (g) Open questions for the owner

1. The ARM to Terraform slide is titled "Terraform for the Azure Admin" and the page attributes it by that title only. It looks like Ned Bellavance's Pluralsight course of that name; confirm the author so Sources can name them.
2. The provider snippet carries `version = "~> 4.0"` because a version constraint is the point of `required_providers`. If you would rather have no version on the page (rule 4), replace it with `version = "~> X.0"` and a comment.
3. The backend example includes `resource_group_name`. Confirm it matches how your state storage account is addressed, or drop it.
4. Cut for budget, restore if you want them back: the `TF_LOG` tip, the provider `alias` sentence, "Cloud Shell has `az` and `terraform` installed", and your `-var-file="common.tfvars" -var-file="$env.tfvars"` alternative to Terragrunt.
5. The dev/qa/prod workspaces list and the `terraform workspace -h` fence are kept as you wrote them; the section could be halved if you no longer use CLI workspaces.
