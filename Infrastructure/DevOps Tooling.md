# DevOps tooling

Picking the right tools for the right job is crucial while adopting DevOps practices. In principle it is preferable to keep infrastructure provisioning separate from configuration management and application deployment.

## Infrastructure Provisioning

Infrastructure setup primarily requires provisioning

* Storage
* Servers or Compute services in cloud
* Networking

OS installation abd patches, CPU and memory config, associated disks and network setup are infrastructure provisioning tasks that tools like *Terraform and Cloudformation* can provide.

## Configuration Management

Installing application runtimes, copying and modifying files or setting environment variables are examples of configurations tasks that are implemented using configuration management (CM) tools. *Chef, Ansible, Puppet and SaltStack* are popular, open-source examples of such tools.

Using CM tools to provision infrastructure for a few environments and regions is simple enough. But using CM tools to provision multiple environments in different regions with different accounts can lead to complex code that is unmaintainable and hard to extend. Therefore keeping [configuration management separate from provisioning](https://www.thoughtworks.com/insights/blog/why-configuration-management-and-provisioning-are-different) helps in separation of concerns.

For example Terraform could be a good option for configuring IAAS but Ansible is a good fit for PAAS based solutions. A [combination of terraform and ansible](https://www.reddit.com/r/devops/comments/8co4pr/ansible_and_terraform) is a good option where you provision your VMs and the network using terraform and configure those VMs using ansible.

## Application deployment

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