# Terminology

## Tasks

An AzDo [task](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/tasks?view=azure-devops&tabs=yaml) is the building block for defining automation in a pipeline.

job  
  -> task1  
  -> task2  
  -> task3

All tasks run in a sequence, one after the other. To run the same set of **tasks in parallel** on multiple agents, or to run some tasks without using an agent, see [jobs](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/phases?view=azure-devops&tabs=yaml)

### Custom tasks

Some built-in tasks are provided to enable fundamental build and deployment scenarios. You can also create your own [custom task](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/tasks?view=azure-devops&tabs=yaml#custom-tasks).

### YAML schema

https://dev.azure.com/hemantk/_apis/distributedtask/yamlschema?api-version=5.1

In addition, Visual Studio Marketplace offers a number of extensions; each of which, when installed to your subscription or collection, extends the task catalog with one or more tasks. Furthermore, you can write your own custom extensions to add tasks to Azure Pipelines.

## Manage extensions

[Install extensions](https://docs.microsoft.com/en-us/azure/devops/marketplace/get-tfs-extensions?view=azure-devops-2019) (tasks) from visual studio marketplace. 

[Uninstall or disable extensions](https://docs.microsoft.com/en-us/azure/devops/marketplace/uninstall-disable-extensions?view=azure-devops&tabs=browser) that you no longer need.

### Agentless job
Tasks that can be handled by the azure devops services e.g. a manual intervention task where someone has to approve something

## Release Pipeline Definition

Defines the steps required to get the artifact from the artifact location and install the artifact.
You create a release to kick off a stage (e.g. development) defined in your release pipeline.

## Release Agent

Runs the tasks defined in the Release pipeline definition in a sequence. An agent may live in an agent pool. Agent pools can be managed by MS or customized with agents that run on-premise or in your own cloud subscription.

## Deployment group

Set of predefined machines in a n/w segment normally on-prem but it could also be in the cloud.

## Release Pipelines

You can define a combined build and release pipeline using a YAML file checked into source control. This is done by defining stages

### Pipeline permissions

Permissions in a release pipeline can be configured using the Security dropdown by placing users in the appropriate groups in your team project. Permissions can also be set for individual Stage and agent pool.

### Approvals

Use the **Four eyes principle** for approvals: two individuals approve an action before it can be taken.

Approvals by multiple users, can be configured for a Stage in the release pipeline.

### Gates

Gates are evaluated post deployment e.g. start monitoring the application 5 minutes post deployment and send alerts if a metric goes above threshold.

### Environment

A deployment environment, like kubernetes to deploy your application to.

### Built in variables

`$(Release.EnvironmentName)` - built in variable in pipelines that gets you the name of the 'Stage' that you're currently in.