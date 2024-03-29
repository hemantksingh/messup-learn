# DevOps

In the [SRE book by Google](https://sre.google/workbook/how-sre-relates/) DevOps is defined as a loose set of practices, guidelines, and culture designed to break down silos in IT development, operations, networking, and security. Articulated by John Willis, Damon Edwards, and Jez Humble, CA(L)MS—which stands for Culture, Automation, Lean (as in Lean management; also see continuous delivery), Measurement, and Sharing—is a useful acronym for remembering the key points of DevOps philosophy.

DevOps and SRE have a lot in common.  *SRE is defined as the class that implements the DevOps interface*.

## DevOps capabilities

People who can work within organizations to bring people, processes and products together to enable continuous delivery of value to end users.

* Transforming infra/ops departments (i.e. reorganizing them and getting them to adopt agile practices across the department, bridging silos and adopt DevOps culture by having **cross functional teams** capable of **building, running, securing and supporting their apps**.

* People who know what it's like to shape and manage Cloud migrations strategies, who can talk to a client about the impact of moving to cloud on their budgeting **moving from CapEx to OpEx** (e.g moving from owning a car to renting a car), managing technical budgets and pros and cons of adoption of IAAS, PAAS or FAAS.

* Understand change management (e.g. CI/CD workflows, rollback and backup strategies), incident management and security auditing controls

## DevOps Metrics

Collecting performance and operational metrics in your continuous integration/continuous delivery (CI/CD) pipeline is important to

* measure your return (or quantify the value) on investment in DevOps automation
* identify opportunities to improve efficiency in software delivery capabilities

The [devops metrics](https://docs.aws.amazon.com/solutions/latest/devops-monitoring-dashboard-on-aws/devops-metrics-list.html) are similar to the DORA metrics that include measuring:

* lead time
* deployment frequency
* mean time to restore (MTTR). RTO is time taken to recover from a disaster whereas MTTR is time taken to restore a service post an incident, therefore RTO will normally be higher than MTTR.
* change fail percentage

Although there is value in understanding where a team is spending time, whether it be on product innovation or keeping the lights on, the above metrics measure a specific part of the value stream - the engineering effort. Just measuring the number of deployments per day, number of incidents, number of work in progress items in isolation of the wider business context can be an exercise in vanity. To measure the end-to-end flow of a software value stream, [flow metrics](https://www.leanix.net/en/wiki/vsm/flow-metrics#introduction) can be used alongside DORA metrics.

### Reference Implementation

AWS reference implementation of a DevOps monitoring solution

* <https://aws.amazon.com/blogs/mt/automate-capture-analysis-ci-cd-metrics-using-aws-devops-monitoring-dashboard-solution/>

DevOps metrics using Graphana

* <https://www.tutorialworks.com/devops-metrics/>
* <https://github.com/Justus-e/DevOpsMetrics>
* Apache dev lake (uses graphana dashboards) <https://www.darraghoriordan.com/2022/10/16/report-on-dora-metrics-apache-dev-lake/>

## DevOps tooling

There is no good way to manage a service that has one tool for SREs and another for the product developers, behaving differently (and potentially catastrophically so) in different situations. The more divergence you have, the less your company benefits from each effort to improve each individual tool. Picking a similar tool set for Application developers, Operations, Network and Security teams is crucial to be successful at DevOps.

### CI/CD best practices and principles

Adopting Infra as Code approaches to delivering infrastructure

* separation of concern
  * separation of infrastructure provisioning & configuration management - are you managing snowflake or ephemeral servers? think cattle not pets
  * separation of compute, networking and storage within your infrastructure as code
  * separate application build, deployment and release
  * separate code deployment from config deployment - is your config auditable & version controlled?
* build once deploy multiple times
  * build the binary package once and promote the same package to different environments
  * adopt semantic versioning for packages and add commit hash to package to tie it to the code
* dev test, prod parity
* fast feedback
  * run fastest tests early
  * ensure deployments can be run locally to get quick feedback
  * ensure all scripts are idempotent
  * ensure scripts log desired state in conditional code paths
* encapsulation and abstraction
  * ensure deployments are scriptable and decoupled from CI/CD tooling to facilitate migration & local testing
  * modularize reusable scripts to prevent duplication
* secure by default
  * security enforcement doesn't disrupt the application development and deployment pipeline
  * security baked into your pipelines
  * no secrets in source code
    * store secrets in a vault not in auto-generated files on a CI server
  * run with least privileges
  * run code security scans

### Infrastructure Provisioning

Infrastructure setup primarily requires provisioning

* Storage
* Servers or Compute services in cloud
* Networking

OS installation abd patches, CPU and memory config, associated disks and network setup are infrastructure provisioning tasks that tools like *Terraform and Cloudformation* can provide.

### Configuration Management

Installing application runtimes, copying and modifying files or setting environment variables are examples of configurations tasks that are implemented using configuration management (CM) tools. *Chef, Ansible, Puppet and SaltStack* are popular, open-source examples of such tools.

Using CM tools to provision infrastructure for a few environments and regions is simple enough. But using CM tools to provision multiple environments in different regions with different accounts can lead to complex code that is unmaintainable and hard to extend. Therefore keeping [configuration management separate from provisioning](https://www.thoughtworks.com/insights/blog/why-configuration-management-and-provisioning-are-different) helps in separation of concerns.

***Chef*** and ***Puppet*** are configuration management tools. They work by describing the state that a system should be in, and they take steps to ensure systems are in that state. For example, imagine you were managing 30 web servers. Rather than using remote desktop to configure them all, installing Windows components, enabling features, and so on, you could use Puppet or Chef to specify:

* All web servers should have IIS configured with the Windows Authentication module enabled
* MSMQ should be installed and running
* A folder at C:\Logs should exist and be writable by a given user account

Release automation tools like ***Octopus Deploy*** for deploying .NET apps across multiple environments, by contrast don't work on "desired state"; rather, it is an orchestration tool that runs steps in a very specific order. Octopus is ideal for Blue Green deployments that look like this:

* Redirect load balancer to a "down for maintenance" site
* Remove web servers from load balancer
* Stop application servers
* Backup and upgrade the database
* Start application servers
* Add web servers back to load balancer

Octopus can also use PowerShell to perform your infrastructure provisioning and configuration management tasks, but for infrastructure automation and provisioning of new systems, using Puppet, if you already have the skills, would make a better choice: the workflows are much more designed for that. Use Puppet to provision the infrastructure and ensure everything is ready (automation that system administrators might need), and use Octopus for the continuous delivery of your applications on top of those systems.
