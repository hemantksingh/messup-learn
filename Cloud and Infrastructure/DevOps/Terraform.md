# Terraform

Tool to automate the deployment of your infrastructure across multiple clouds, both public and private. This enables Infrastructure as code to provision and manage any cloud, infrastructure or service.

* uses HCL - Hashicorp configuration language
* supports comments
* arguably more human readable
* resource addressing (referencing) is intuitive

## Terraform on Microsoft Azure

You can run terraform directly in the azure cloud shell, which has the `azcli` and terraform both installed.  

## Arm and Terraform

![arm-terraform.png](../../Images/arm-terraform.png "Arm Terraform")

## Providers

A provider is responsible for understanding API interactions and exposing resources. Providers generally are an IaaS (e.g. Alibaba Cloud, AWS, GCP, Microsoft Azure, OpenStack), PaaS (e.g. Heroku), or SaaS services (e.g. Terraform Cloud, DNSimple, Cloudflare). There are 3 Azure providers in Terraform

* Azure - Used to interact with Azure public cloud, Azure gov cloud or one of the sovereign clouds. It uses the Azure Resource Manager (Azure RM) API.
* Azure Stack - On premise extension of Microsoft Azure. It uses the same ARM API, but some of the versions and resources are different.
* Azure Active Direcory - Explicitly deals with Azure AD

Providers have:

* Version: Terraform providers are versioned, allows you to specify the version of the provider to use
* Data sources: Information that you can pull from the provider about your target environments. e.g. get a list of marketplace images or get an existing virtual network that's already been provisioned or subscription details of the target subsciption
* Resources: e.g. create an Azure VM in a Vnet that you got from the data sources.
* Modules: help deploy common configurations for that provider. These modules can be found on public terraform registry: `registry.terraform.io`
* Authentication:
    * azcli
    * managed service identity - a VM running in azure under managed identity
    * service principal with client secret
    * service principal with client certificate

```sh
    provider "azurerm" {
        version         = "~> 1.0" # stay in the 1 major version 1.x
        alias           = "networking" # allows you to create multiple instances of the same provider
        subscription_id = var.subscription_id
        cliend_id       = var.client_id
        client_secret   = var.client_secret
    }
```

## Remote state

Terraform stores state about your managed infrastructure and configuration. This state is used by Terraform to map real world resources to your configuration, keep track of metadata, and to improve performance for large infrastructures.

This state is stored by default in a local file named `terraform.tfstate`, but it can also be stored remotely, which works better in a team environment.

A [backend](https://www.terraform.io/docs/backends/index.html) in Terraform determines how state is loaded and how an operation such as apply is executed. This abstraction enables non-local file state storage, remote execution, etc. e.g. when commands like plan, apply or destroy are running terraform puts a lock on the state file to ensure it can only be modified in isolation.

A backend like Azure blob storage supports locking

```sh
backend "azurerm" {
    storage_account_name = "storestate"
    container_name       = "terraform-state"
    key                  = "prod.terraform.tfstate"
    access_key           = "access_key"
}
```

## Provisioners

[Provisioners](https://www.terraform.io/docs/provisioners/index.html) can be used to model specific actions on the local machine or on a remote machine in order to prepare servers or other infrastructure objects for service.

Provisioners are a Last resource and be used with caution. An example of running a local provisioner on the machine that terraform is running on, rather than running the provisioner on a remote VM.

```sh
resource "null_resource" "post_config" {

    depends_on = [azurerm_role_assignment.vnet]

    provisioner "local-exec" {
        command = <<EOT
    echo "export TF_VAR_my_vnet_id=${module.vnet-my.vnet_id}" >> file.txt
    EOT
    }
}
```

## Workspaces

The persistent data stored in the backend belongs to a workspace. Initially the backend has only one workspace, called "default", and thus there is only one Terraform state associated with that configuration.

Certain backends support multiple named workspaces, allowing multiple states to be associated with a single configuration. This can possibly also be achieved using different state files for the same configuration stored in the same backend.

## Modules

A module is a container for multiple resources that are used together. Modules can be used to create lightweight abstractions, so that you can describe your infrastructure in terms of its architecture, rather than directly in terms of physical objects.

Using a standard [module structure](https://www.terraform.io/docs/modules/index.html#module-structure) is recommended for reusable modules. Terraform tooling is built to understand the standard module structure and use that structure to generate documentation, index modules for the module registry, and more.
