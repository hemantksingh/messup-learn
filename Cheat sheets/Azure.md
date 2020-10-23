# Azure

Use Azure cli and azurerm module for interacting with the azure cloud APIs.

## Getting resources

```sh
# List all the resources of a particular type
az <resource> list -g <resource-group>

# Get examples queries for a query that returns a list []
az disk list --query-examples
# Get a resource field when the result is a list '[]' using JMESPath query string. See http://jmespath.org/
az disk list -g <resource-group> --query "[].name"
# Get multiple fields
az disk list -g <resource-group> --query "[].[name, id]"


# Get examples queries for a query that returns a single instance
az account show --query-examples
# Get a resource filed when the result is a single instance. e.g current subscription name
az account show --query name
# On az login you may log into one of the subscriptions that you have access to by default. To set a specific default subscription
az account set -s <subname or subid> # e.g. az account set -s "Visual Studio Enterprise Subscription"

```

## Create a service principal

[Creating a service principal](https://docs.microsoft.com/en-us/cli/azure/ad/sp?view=azure-cli-latest#az-ad-sp-create-for-rbac) creates an app registration in:
Azure Active Directory -> App registrations and assigns a default role `Contributor`.

```sh
az ad sp create-for-rbac -n starter-agent
{
  "appId": "80d805ac-1973-487a-b152-9da5b9b0bb77",
  "displayName": "starter-agent",
  "name": "http://starter-agent",
  "password": "<guid>",
  "tenant": "<tenant-id>"
} # appId is the same as clientId

# Create with a specific role, Default role is: Contributor
az ad sp create-for-rbac -n starter-agent --role Owner

# Create with customised access to resources.
az ad sp create-for-rbac -n starter-agent --scopes /subscriptions/<subscription-id>

# Space separated list of scopes the service principal's role assignment applies to. Defaults to the root of the current subscription.
az ad sp create-for-rbac -n starter-agent --scopes \
/subscriptions/<subscription-id>/resourceGroups/<resource_group1> \
/subscriptions/<subscription-id>/resourceGroups/<resource_group2> \


# Show details of sp
az ad sp show --id http://starter-agent

# or
az ad sp show --id <appId>

```
### Get existing service principal configuration

```powershell
function Get-AzureServicePrincipal ([Parameter(mandatory = $true)][string] $spName) {

    Write-Host "Getting details for service principal '$spName'"
    $appId =  az ad sp list --display-name $spName --query '[0].appId' -o tsv
    
    if([string]::IsNullOrWhiteSpace($appId)) {
        throw "No service principal found with name '$spName'"
    }
    
    $account = az account show | ConvertFrom-Json
    Write-Host "Updating credentials for service principal '$spName'"
    $newSecret = az ad app credential reset --id $appId `
        --append --credential-description "auto-generated" `
        --year 1 `
        --query 'password' -o tsv
    
    return @{
        clientId        = $appId
        clientSecret    = $newSecret
        tenantId        = $account.tenantId
        subscriptionId  = $account.id
    }
}
```

## Create app registration

```sh
az_ad_create_apps() {
    apps="$1"; tenant="$2"; suffix="$3"
    sort <(for app in "${apps[@]}" ;
        do app="$app-$suffix";
        appId=$(az ad app create --display-name $app \
            --identifier-uris https://$tenant.onmicrosoft.com/$app \
            --homepage https://localhost:44321 \
            --reply-urls https://localhost:44321 \
            | jq -r '.appId')
        appSecret=$(az ad app credential reset --id $appId \
                --append --credential-description default \
                --years 1 \
                --query 'password' -o json);
        echo "Created app \"$app\" with clientId \"$appId\" and secret $appSecret";
   done)
}

az_ad_delete_apps() {
    apps="$1"; tenant="$2"; suffix="$3"
    sort <(for app in "${apps[@]}" ;
        do app="$app-$suffix";
        appId=$(az ad app list --display-name $app --query [].appId -o tsv);
        if [[ -z "$appId" ]] ; then
            echo "No app '$app' found. Nothing deleted!"
        else
            az ad app delete --id $appId
            echo "Deleted app \"$app\" with id $appId";
        fi
    done)
}

apps=('beta-abc-us' 'beta-def-us'); tenant=kalibrate; suffix=kalibratepricing;
az_ad_create_apps $apps $tenant $suffix
az_ad_delete_apps $apps $tenant $suffix
```

Powershell

```powershell
$tenant='kalibrate';
$app='beta-abc-us-suffix';
az ad app create --display-name $app `
  --identifier-uris https://$tenant.onmicrosoft.com/$app `
  --homepage https://localhost:44321 `
  --reply-urls https://localhost:44321
```

### Add api permission

`az ad app permission grant --id <appId> --api <apiAppId>`

## Azure keyvault

```sh

# List all vaults
az keyvault list

# Add secret to a vault
az keyvault secret set -n <secret-name> --value <secret-value> --vault-name <vault-name> --tags 'foo=bar' 'lol=cat'

# Show a secret in a vault
az keyvault secret show -n <secret-name> --vault-name <vault-name>

# Delete a secret in a vault
az keyvault secret delete -n <secret-name> --vault-name <vault-name>

# Show all secrets in a vault
az keyvault secret list --vault-name <vault-name>
```

## ACR

`az acr login -n <container-registry>`

## AKS

```sh
# Get access credentials for a managed Kubernetes cluster.
az aks get-credentials --resource-group <resource-group> --name <aks-cluster-name>

# Enable the kube-dashboard addon for the cluster
az aks enable-addons --addons kube-dashboard -g <resource-group> -n <aks-cluster-name>

# Install kubectl
az aks install-cli
```
