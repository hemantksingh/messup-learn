# Azure

Use Azure cli and azurerm module for interacting with the azure cloud APIs.

## Subscription details

```sh
# Get current subscription
az account show

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
