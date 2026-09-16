---
title: "DevOps and Delivery"
summary: "What DevOps means beyond the acronym, which metrics tell you delivery is improving, and why deployment and release are separate acts."
kind: concept
status: current
last_reviewed: 2026-09-16
sources: []
tags: [devops, dora-metrics, ci-cd, feature-flags, continuous-delivery]
---
# DevOps and Delivery

In the [SRE book by Google](https://sre.google/workbook/how-sre-relates/) DevOps is defined as a loose set of practices, guidelines, and culture designed to break down silos in IT development, operations, networking, and security. Articulated by John Willis, Damon Edwards, and Jez Humble, CA(L)MS—which stands for Culture, Automation, Lean (as in Lean management; also see continuous delivery), Measurement, and Sharing—is a useful acronym for remembering the key points of DevOps philosophy.

DevOps and SRE have a lot in common.  *SRE is defined as the class that implements the DevOps interface*.

## DevOps capabilities

People who can work within organizations to bring people, processes and products together to enable continuous delivery of value to end users. What that looks like as a role (transforming infra/ops departments, shaping cloud migrations, CapEx to OpEx, change and incident management) is in [Roles and Hiring](../practice/Roles%20and%20Hiring.md).

## DevOps Metrics

Collecting performance and operational metrics in your continuous integration/continuous delivery (CI/CD) pipeline is important to

* measure your return (or quantify the value) on investment in DevOps automation
* identify opportunities to improve efficiency in software delivery capabilities

The [devops metrics](https://docs.aws.amazon.com/solutions/latest/devops-monitoring-dashboard-on-aws/devops-metrics-list.html) are similar to the DORA metrics. DORA has five keys since 2021:

* lead time for changes
* deployment frequency
* failed deployment recovery time (called mean time to restore, MTTR, until the 2023 report). Do not confuse it with RTO: RTO is an agreed maximum time to restore after a disaster, set in advance, whereas MTTR is a measured mean over real incidents.
* change failure rate
* reliability (added in 2021)

Although there is value in understanding where a team is spending time, whether it be on product innovation or keeping the lights on, the above metrics measure a specific part of the value stream - the engineering effort. Just measuring the number of deployments per day, number of incidents, number of work in progress items in isolation of the wider business context can be an exercise in vanity. To measure the end-to-end flow of a software value stream, flow metrics can be used alongside DORA metrics.

### Reference Implementation

AWS reference implementation of a DevOps monitoring solution

* <https://aws.amazon.com/blogs/mt/automate-capture-analysis-ci-cd-metrics-using-aws-devops-monitoring-dashboard-solution/>

DevOps metrics using Grafana

* <https://github.com/Justus-e/DevOpsMetrics>
* Apache dev lake (uses Grafana dashboards) <https://www.darraghoriordan.com/2022/10/16/report-on-dora-metrics-apache-dev-lake/>

## DevOps tooling

The [SRE Workbook](https://sre.google/workbook/how-sre-relates/) puts it this way:

> There is no good way to manage a service that has one tool for the SREs and another for the product developers, behaving differently (and potentially catastrophically so) in different situations. The more divergence you have, the less your company benefits from each effort to improve each individual tool.

Picking a similar tool set for Application developers, Operations, Network and Security teams is crucial to be successful at DevOps.

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

OS installation and patches, CPU and memory config, associated disks and network setup are infrastructure provisioning tasks that tools like *Terraform, OpenTofu, CloudFormation, AWS CDK, Bicep and Pulumi* can provide.

### Configuration Management

Installing application runtimes, copying and modifying files or setting environment variables are examples of configurations tasks that are implemented using configuration management (CM) tools. *Chef, Ansible, Puppet and SaltStack* are popular examples of such tools. Ansible is open source; Chef, Puppet and SaltStack are source-available or ship as commercial builds, so check the licence before assuming open source.

Using CM tools to provision infrastructure for a few environments and regions is simple enough. But using CM tools to provision multiple environments in different regions with different accounts can lead to complex code that is unmaintainable and hard to extend. Therefore keeping [configuration management separate from provisioning](https://www.thoughtworks.com/insights/blog/why-configuration-management-and-provisioning-are-different) helps in separation of concerns.

Configuration management tools (Chef, Puppet, Ansible) describe the desired state of a machine and converge it to that state on every run. Deployment orchestration tools (Octopus Deploy, Spinnaker, Argo CD) instead run an ordered sequence of steps to move an application version through environments. Use the first to make servers ready, the second to deliver applications onto them.

A blue/green deployment keeps two identical production environments. Deploy the new version to the idle one, test it there, then switch traffic to it at the load balancer or DNS. Keep the old environment running until you are sure, because switching back is the rollback.

## Separate deployment from release

**Deployment** puts an artefact on servers and checks it runs. **Release** reveals a feature to users. Keeping the two apart lets you deploy small changes often without turning anything on, roll a feature back by switching it off rather than redeploying, and show a feature to a few users before everyone. The mechanics are **feature flags** (toggle per user segment or percentage), **canary** or ring-based rollouts (a slice of traffic first), and **dark launches** (the code path runs, the result is hidden). Deploy, watch it stay stable, then widen the release: a segment, a random percentage, everyone.
