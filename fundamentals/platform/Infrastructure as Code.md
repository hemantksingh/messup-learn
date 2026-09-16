# Infrastructure as Code

What does infrastructure as code give me, how does Terraform's model work, and where does state fit?

Infrastructure as code (IaC) means describing servers, networks and services in files, then letting a tool make the real environment match the files. Terraform is the example here. OpenTofu and Pulumi follow the same model; CloudFormation and Bicep declare the same way but keep no separate state file.

## What infrastructure as code gives you

You declare the end state you want, not the steps to reach it. The tool works out the steps.

* The description lives in version control. A change to infrastructure is a diff, a review and a commit.
* You see changes before they happen. The tool prints the difference between declared and real; nothing changes until you accept it.
* The same files build the same environment again. Dev, test and prod come from one description with different inputs.
* Drift becomes visible. Drift is the gap that opens when someone changes a resource by hand. The next comparison shows it and the tool can put it back.

Terraform reads its own syntax, HCL (HashiCorp configuration language), and also accepts JSON. It builds a dependency graph from the references between resources, creates or destroys them in the right order, and works on independent resources in parallel. A failure in one resource stops only the resources that depend on it.

Will Brock's [terraform playlist](https://www.youtube.com/playlist?list=PL8HowI-L-3_9bkocmR3JahQ4Y-Pbqs2Nt) is a good resource for learning terraform.

## Terraform's model

* **Provider**: a plugin that knows one API. Terraform itself knows nothing about Azure or AWS; the provider translates HCL blocks into API calls. Each is versioned and published on the [registry](https://registry.terraform.io/browse/providers).
* **Resource**: one object the provider manages, such as a virtual network.
* **Data source**: a read-only lookup of something that exists already, such as a marketplace image or a network another team provisioned.
* **Module**: a folder of configuration used as a unit. It takes inputs and returns outputs.
* **Variables, locals and outputs**: variables are the inputs to a configuration or module, locals are values computed from them, and outputs are what it hands back, for example an id another module needs.

### Providers

The Azure providers are `azurerm` for resources through the Azure Resource Manager API, `azuread` for Entra ID (the provider keeps its old name), `azapi` for resources that `azurerm` does not cover yet, and `azurestack`, which is minimally maintained. A provider authenticates with the Azure CLI (`az`), with a managed identity when Terraform runs inside Azure, or with a service principal using a client secret or certificate.

Pin the provider in a `required_providers` block. The `provider` block then holds its settings. For `azurerm` an empty `features {}` block is mandatory.

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0" # stay within one major version
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}
```

### Resources and data sources

A resource block names a type, a label that is local to your configuration, and the arguments the provider needs.

```hcl
resource "<type>" "<terraform_identifier>" {
  name     = "resourceGroup1"
  location = "West US"
}

# Usage
resource "azurerm_resource_group" "rg1" {
  name     = "resourceGroup1"
  location = "West US"
}
```

Other blocks refer to it as `azurerm_resource_group.rg1.name`. That reference is also the dependency: Terraform creates the group before anything that mentions it. A data source has the same shape with `data` in place of `resource`, and reads instead of creating.

### Modules

As teams and operations scale you want to organise your infrastructure resources into meaningful groups by keeping their configurations separate. A module groups resources that change together. It lets you describe infrastructure in terms of its architecture (a frontend, a database) rather than one physical object at a time.

Generally it is advisable to **avoid preemptively creating modules** and only do it after seeing patterns emerging. Eventually you may end up with a structure like:

* application
  * modules
    * frontend
    * backend
    * database

Reusable modules follow the standard [module structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure).

**Passing values to modules.** A variable's default must be a literal; it cannot reference a resource. If a module input has to be computed, compute it in a `local` and pass the local in. Locals are evaluated during plan, so they can hold references. An example is [here](https://discuss.hashicorp.com/t/passing-values-in-existing-variables-to-modules/4803/3).

## State

State is the map between what you declared and what exists. For every resource block Terraform records the real object's id and its last known attributes. Plan reads three things: the configuration, the state and the live API. Configuration against state tells it what you changed. State against the API tells it what drifted. Without state Terraform could not know which real object a block refers to, and it would have to query everything on every run.

By default state is a local file named `terraform.tfstate`. It holds every attribute, including secrets the provider returned, so treat it as sensitive.

### Remote state and locking

In a team a local file fails in two ways: two people hold different copies, and two people apply at once. A [backend](https://developer.hashicorp.com/terraform/language/backend) tells Terraform where state lives. A remote backend fixes the first problem. Locking fixes the second: when plan, apply or destroy run, Terraform takes a lock on the state so one operation at a time can change it. Azure blob storage locks through blob leases.

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "storestate"
    container_name       = "terraform-state"
    key                  = "prod.terraform.tfstate"
    use_azuread_auth     = true
  }
}
```

`use_azuread_auth` uses the identity Terraform already has. Never put a storage access key in this block; if you must use one, pass it through `ARM_ACCESS_KEY` or `-backend-config`.

### Workspaces

```sh
terraform workspace -h
```

CLI workspaces let one configuration hold several state files in the same working directory. One configuration, multiple states:

* `dev.tfstate`
* `qa.tfstate`
* `prod.tfstate`

The state stored in the backend belongs to a workspace. A backend starts with one workspace called `default`. All workspaces of one configuration share that one backend, so every environment's state lands in the same storage account and container. If separate environments need separate backends or credentials, HashiCorp's advice is separate root configurations; [workspaces are not the tool for system decomposition](https://developer.hashicorp.com/terraform/language/state/workspaces#using-workspaces).

## Workflow: init, plan, apply

`terraform init`

* downloads the providers (for example `azurerm`) and the modules the configuration references
* creates the `.terraform` directory, a local cache that stays out of version control
* creates or updates `.terraform.lock.hcl`, which pins provider versions but not module versions

`terraform plan` shows what Terraform will change. Save the plan to a file so that apply does exactly what you reviewed.

```sh
# inline variables, plan written to my.tfplan
terraform plan -var client_id=$AZURE_CLIENT_ID -var client_secret=$AZURE_CLIENT_SECRET -out my.tfplan

# variables from a file
terraform plan -var-file="terraform.example.tfvars" -out my.tfplan

# apply the saved plan
terraform apply my.tfplan
```

Newer language features worth looking up are `moved` blocks, `import` blocks and the built-in test framework.

## Provisioners

[Provisioners](https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax) run a script on the local machine or on a remote one after Terraform creates a resource. They are a last resort: Terraform cannot plan what a script will do, cannot undo it, and cannot see drift in its result. Prefer cloud-init, a configuration management tool or a provider resource. If you need one, attach it to a `terraform_data` resource, which replaces `null_resource`. This one runs on the machine running Terraform rather than on a remote VM:

```hcl
resource "terraform_data" "post_config" {
  depends_on = [azurerm_role_assignment.vnet]

  provisioner "local-exec" {
    command = <<-EOT
      echo "export TF_VAR_my_vnet_id=${module.vnet-my.vnet_id}" >> file.txt
    EOT
  }
}
```

## ARM templates and Terraform

On Azure the native IaC format is the ARM template. The concepts map one to one. Adapted from the *Terraform for the Azure Admin* slide:

| ARM template | Terraform |
|---|---|
| JSON | HCL |
| Parameters | Variables |
| Variables | Locals |
| Resources | Resources |
| Functions | Functions |
| Nested templates | Modules |
| Explicit dependency (`dependsOn`) | Automatic dependency from references |
| Refer by `reference()` or `resourceId()` | Refer by resource or data source |

Bicep is the current language for ARM; it compiles to ARM JSON and replaces writing templates by hand.

## Terragrunt

Terragrunt is a thin wrapper that generates Terraform configuration before calling Terraform. A `terragrunt.hcl` per environment names the module to run and its inputs, and inherits the remote state block from a root file found with [find_in_parent_folders()](https://terragrunt.gruntwork.io/docs/reference/built-in-functions/#find_in_parent_folders). It removes repetition across environments and keeps one state file per module.

> Own view: Terraform has probably evolved to fill the gap in functionality that terragrunt once provided.

## Licence

Terraform moved from the MPL 2.0 to the Business Source License 1.1 in August 2023. It is source-available, not open source. OpenTofu is the open-source fork under the Linux Foundation and reads the same configuration. Terraform Cloud, HashiCorp's hosted service, is now HCP Terraform.

## How to rederive this

* Files describe what you want, the API describes what exists, and something must remember which real object each block refers to. That is state.
* Plan is a three-way comparison: configuration against state shows your change, state against the API shows drift.
* Two people and one state file means stale copies or concurrent writes, so state must be remote and locked.
* Anything Terraform cannot plan, undo or compare it cannot manage, which is why provisioners are a last resort.

## Sources

* HashiCorp, [Terraform language documentation](https://developer.hashicorp.com/terraform/language)
* HashiCorp, [Infrastructure as Code tutorial](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/infrastructure-as-code)
* *Terraform for the Azure Admin* slide (ARM to Terraform mapping)
* Gruntwork, [Terragrunt documentation](https://terragrunt.gruntwork.io/docs/)
* HashiCorp, [BSL announcement](https://www.hashicorp.com/blog/hashicorp-adopts-business-source-license); [OpenTofu](https://opentofu.org)
