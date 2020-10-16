# DevOps capabilites

The union of people, processes and products to enable continuous delivery of value to end users.

People who can work with clients to shape and oversee engagements that are primarily infra/ops oriented

* Transforming infra/ops departments (i.e. reorganising them and getting them to adopt agile practices across the department, bridging silos and adopt DevOps culture by having **cross functional teams** capable of **building, running and supporting their apps**.

* People who know what it's like to shape and manage Cloud migrations strategies, who can talk to a client about the impact of moving to cloud on their budgeting **moving from CapEx to OpEx** (e.g moving from owning a car to renting a car), managing technical budgets and pros and cons of adoption of IAAS, PAAS or FAAS.

* Product specialist equivalent? The answer to these gaps may not be Principal Technologists. Product specialists may not be true technologists, not PMs, not BAs, not CPs but may run serious infra/ops engagements, alongside a technologist and other roles.

* Non-technical roles, e.g. BA, QA, UX, have a different experience from devs, in that they don't typically lead teams, or work with others of their own sort except with very large engagements. But it feels to me like DevOps becoming a different thing, not because it's technical, but because it's becoming the central focus of certain types of engagements (e.g. cloud migration)

## DevOps tooling

Picking the right tools for the right job is crucial while adopting DevOps practices. In principle it is preferable to keep infrastructure provisioning separate from configuration management and application deployment.

### CI/CD best practices and principles

Adopting Infra as Code approaches to delivering infrastructure

* separattion of concern
    * separation of infrastructure provisioning & configuration management - are you managing snowflake or ephemeral servers? think cattle not pets
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
   * modularise reusable scripts to prevent duplication
* security baked into your pipeline 
    * no secrets in source code
    * store secrets in a vault not in auto-generated files on a CI server
    * run with least privileges
    * run code securty scans

### Infrastructure Provisioning

Infrastructure setup primarily requires provisioning

* Storage
* Servers or Compute services in cloud
* Networking

OS installation abd patches, CPU and memory config, associated disks and network setup are infrastructure provisioning tasks that tools like *Terraform and Cloudformation* can provide.

### Configuration Management

Installing application runtimes, copying and modifying files or setting environment variables are examples of configurations tasks that are implemented using configuration management (CM) tools. *Chef, Ansible, Puppet and SaltStack* are popular, open-source examples of such tools.

Using CM tools to provision infrastructure for a few environments and regions is simple enough. But using CM tools to provision multiple environments in different regions with different accounts can lead to complex code that is unmaintainable and hard to extend. Therefore keeping [configuration management separate from provisioning](https://www.thoughtworks.com/insights/blog/why-configuration-management-and-provisioning-are-different) helps in separation of concerns.

For example Terraform could be a good option for configuring IAAS but Ansible is a good fit for PAAS based solutions. A [combination of terraform and ansible](https://www.reddit.com/r/devops/comments/8co4pr/ansible_and_terraform) is a good option where you provision your VMs and the network using terraform and configure those VMs using ansible.

### Application deployment

***Chef*** and ***Puppet*** are configuration management tools. They work by describing the state that a system should be in, and they take steps to ensure systems are in that state. For example, imagine you were managing 30 web servers. Rather than using remote desktop to configure them all, installing Windows components, enabling features, and so on, you could use Puppet or Chef to specify:

* All web servers should have IIS configured with the Windows Authentication module enabled
* MSMQ should be installed and running
* A folder at C:\Logs should exist and be writable by a given user account

**Octopus Deploy**, by contrast, is a **release automation tool** for deploying .NET apps. Octopus doesn't work on "desired state"; rather, it's an orchestration tool that runs steps in a very specific order. Octopus is ideal for Blue Green deployments that look like this:

* Redirect load balancer to a "down for maintenance" site
* Remove web servers from load balancer
* Stop application servers
* Backup and upgrade the database
* Start application servers
* Add web servers back to load balancer

Puppet/Chef work well if you can describe your automation in terms of a checklist, and order/time isn't important. Octopus works well when order matters. You can't update the web application before migrating the database, for example, or there will be chaos.

You could have Octopus use PowerShell to perform your infrastructure provisioning and configuration management tasks, and many people do. But for infrastructure automation and provisioning of new systems, using Puppet, if you already have the skills, would make a better choice: the workflows are much more designed for that.

Use Puppet to provision the infrastructure and ensure everything is ready (automation that system administrators might need), and use Octopus for the continuous delivery of your applications on top of those systems.