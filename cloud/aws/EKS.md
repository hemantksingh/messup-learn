---
title: "EKS"
summary: "What AWS runs and what you still own on EKS, why pods run out of IP addresses, and how IAM becomes the cluster authenticator."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "AWS, EKS User Guide and EKS Best Practices Guide"
  - "Kubernetes documentation: cluster networking model"
tags: [aws, eks, kubernetes, fargate, vpc-cni, iam]
---
# EKS

Running Kubernetes yourself means patching, securing, scaling and upgrading machines and the software on them. EKS takes the control plane off you: AWS runs the API server and etcd, patches them and upgrades them when you ask. The worker nodes stay yours unless you pick a mode that hands more over. Pod IPs come from your VPC. By default every pod gets a real address from its node's subnet, which is why running out of addresses is the classic EKS problem.

## What AWS runs and what you own

The control plane is always AWS's. Workers come in three forms.

* **Managed node groups.** EC2 instances in an auto scaling group. You choose instance types and the AMI. AWS joins nodes, drains pods and rolls instances on update. Patching the OS is still yours, mostly by rolling to a newer AMI.
* **Fargate.** No nodes to see or patch. Fargate allocates a dedicated, right-sized virtual machine to run any given pod. No two pods share a VM or an operating system, so a container escape stops at the VM boundary. With no nodes there are no DaemonSets: node agents become sidecars, and logs leave through the built-in Fluent Bit log router. Images are not cached, so pods start slower. No GPUs.
* **EKS Auto Mode** (since December 2024). AWS also manages the nodes: launching, replacing, Karpenter-based scaling, and the core add-ons (networking, DNS, storage, load balancing). You write pod specs and choose node pools.

> Own view: default to the option with the least management overhead, especially for an early-stage business where go-to-market is the primary goal. Today that is Auto Mode, or Fargate where a VM per pod is worth its start-up cost. The main value is not paying the [hidden cost of operations](https://aws.amazon.com/blogs/containers/saving-money-pod-at-time-with-eks-fargate-and-aws-compute-savings-plans/) for the nodes.

## Authentication

Kubernetes has no user database. It trusts whatever authenticator is configured (see [Kubernetes Security](../../platform/Kubernetes%20Security.md)). In EKS that is IAM. `kubectl` sends a signed AWS request as its bearer token and the cluster verifies it with STS. An **access entry** then maps the IAM principal, usually an [IAM role](Identity.md), to Kubernetes groups or to an EKS access policy such as cluster admin. RBAC takes over from there. The older `aws-auth` ConfigMap did the same mapping inside the cluster and is legacy.

## Pod networking with the VPC CNI

Kubernetes requires that every pod can reach every other pod without NAT (see [Kubernetes](../../platform/Kubernetes.md)). The AWS VPC CNI does this the direct way. It attaches extra [elastic network interfaces](VPC%20Networking.md) to each node and assigns secondary private IPs to them, one per pod.

![One worker node (an EC2 instance) drawn as a dashed box. Its primary ENI takes one address, 10.0.1.10, from the node subnet 10.0.1.0/24 in the VPC's primary CIDR. Two secondary ENIs sit in the pod subnet 100.64.1.0/24, which comes from the VPC's secondary CIDR 100.64.0.0/10; each ENI slot is delegated one /28 prefix of 16 addresses (100.64.1.16/28 and 100.64.1.32/28) and pods hang off addresses inside it, for example 100.64.1.17, .18 and .19, with the rest of the prefix as a warm pool. The node keeps its address in the original subnet; only the pod ENIs move to the secondary range. Addresses are examples.](../../images/eks-pod-addressing.drawio.svg "Where an EKS pod address comes from: secondary CIDR and prefix delegation")

The cost is addresses. ENIs per node and IPs per ENI depend on the instance type, so max pods per node does too. The plugin also pre-assigns a warm pool of IPs, so one node can hold from a handful to a couple of hundred addresses, most idle. A small subnet runs out of IPs long before it runs out of compute.

A /16 is the largest single IPv4 block a VPC can hold, but a VPC can hold several. The fixes stack:

* **Secondary CIDR with custom networking.** Add a second range to the VPC, commonly from 100.64.0.0/10 because that shared address space will not collide with the corporate IPv4 plan. Tell the CNI to put pod ENIs in subnets from that range. Nodes stay in the original subnet; pods draw from the new one.
* **Prefix delegation.** The CNI assigns a /28 prefix (16 addresses) per ENI slot instead of one address, so the same ENIs carry far more pods.
* **IPv6 clusters.** Pods get globally unique IPv6 addresses and exhaustion goes away. Chosen at cluster creation; an IPv4 cluster cannot be switched.

## Version lifecycle

Kubernetes ships three minor releases a year. EKS gives each about 14 months of standard support, then paid extended support, then upgrades the control plane for you. Upgrades are routine work: control plane first, then nodes and add-ons. Dates are in the [EKS release calendar](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html).

Cluster size is a trade-off, not a limit: several small clusters keep the blast radius small and upgrade on their own cadence, one large cluster is less to run. Clusters with thousands of nodes are ordinary; see the [quotas](https://docs.aws.amazon.com/eks/latest/userguide/service-quotas.html).

## How to rederive this

* The control plane is the same for every customer, so the provider runs it. Workers vary by workload, so they stay with you until you opt out of them.
* Fargate is a VM per pod. Anything that assumes a shared node (DaemonSets, image cache, GPUs) cannot exist there.
* Pods need NAT-free reachability. Real VPC addresses give it, but a subnet is finite. Exits: more IPv4 space, denser use of it, or IPv6.
* IAM already knows who you are. The cluster only needs a mapping from principal to RBAC subject: the access entry.

## Sources

* AWS, EKS User Guide and EKS Best Practices Guide.
* Kubernetes documentation: cluster networking model.
