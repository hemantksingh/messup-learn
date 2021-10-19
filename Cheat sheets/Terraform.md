# Terraform workflow

### terraform init 

Pulls down the module(s) being referenced in your configuration, as well as add the provider plugin e.g. azurerm. It also initializes the .terraform directory: a local cache where terraform retains some files it will need for subsequent operations against this configuration. Its contents are not intended to be included in version control.

### terraform plan

Identify the changes that terraform will apply based on your configuration

Pass inline variables

`terraform plan -var client_id=$AZURE_CLIENT_ID -var client_secret=$AZURE_CLIENT_SECRET -out my.tfplan # output the plan to a file 'my.tfplan'`

Pass variables as file

`terraform plan -var-file="terraform.example.tfvars" -out my.tfplan`

### terraform apply

`terraform apply "my.tfpan" # apply the plan`

## Defining resources

```sh
resource "<type>" "<terraform_identifier>" { # or variable name
  name     = "resourceGroup1"
  location = "West US"
}

# Usage
resource "azurerm_resource_group" "rg1" {
  name     = "resourceGroup1"
  location = "West US"
}
```