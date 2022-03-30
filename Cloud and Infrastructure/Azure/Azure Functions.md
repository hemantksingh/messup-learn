# Azure Functions

Azure functions hosting options

* [Consumption plan](https://docs.microsoft.com/en-in/azure/azure-functions/functions-scale#consumption-plan) is the default hosting plan and offers:
  * Pay only when your functions are running
  * Scaling the functions dynamically depending on workload

* Premium plan - automatically scales based on demand using pre-warmed workers which run applications with no delay after being idle
  * runs on more powerful instances
  * connects to virtual networks
* App service plan runs your functions within an app service plan at regular app service plan rates
  * best for long running scenarios, with existing underutilized VMs that are already running other app service instances
  * predictive scaling and costs are required

On either plan, a function app requires a general Azure Storage account for operations such as managing triggers and logging function executions.

App service plan for functions and the app service plan for webapps cannot be in the same resource group?

## Development

* dotnet-sdk 2.2
* azure-functions-core-tools

```sh
# create a dotnet functions project (collection of projects i.e. functionapp?)
func init starterfunctionapp --worker-runtime dotnet

# build, restore packages in ./starterfunctionapp.csproj
func extensions install

# create new function
func new --template "Http Trigger" --name starterhttptrigger --language C#

# run function locally
func host start

```

## Deployment to azure

* azure cli

```sh
$resourceGroup=playground
$storageName=starterappstorage
$functionApp=starterapp

# create an azure resource group
az group create --name $resourceGroup --location westeurope

# create an azure storage account in the resource group.
az storage account create \
  --name $storageName \
  --location westeurope \
  --resource-group $resourceGroup \
  --sku Standard_LRS

# create a serverless function app in the resource group.
az functionapp create \
  --name $functionApp \
  --storage-account $storageName \
  --consumption-plan-location westeurope \
  --resource-group $resourceGroup

# source: manage function app deployment via source control
# config-zip: deploy using the kudu zip push deployment for a function app
az functionapp deployment source config-zip \
  -g $resourceGroup \
  -n $functionApp \
  --src <zip_file_path>

# update a function app's settings (app config) - https://docs.microsoft.com/en-in/cli/azure/functionapp/config/appsettings?view=azure-cli-latest#az-functionapp-config-appsettings-set
az functionapp config appsettings set [--ids]
                                      [--name]
                                      [--resource-group]
                                      [--settings]
                                      [--slot-settings]
                                      [--subscription]

```