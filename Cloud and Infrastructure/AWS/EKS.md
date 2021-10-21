# Elastic Kubernetes Service (EKS)

Running a Kubernetes cluster requires management, patching, security, isolation, scaling, etc.

EKS Fargate - allows deploying containers on a kubernetes cluster without thinking about infrastructure where the control and worker nodes (group of VMs) are managed by AWS

EKS Node Managed - the control node is always managed by AWS workload and worker node management is the customer's responsibility, you are responsible for securing and patching them, even if that is simplified by replacing instances using the updated AMIs that AWS provides

The main supposed [value of Fargate](https://aws.amazon.com/blogs/containers/saving-money-pod-at-time-with-eks-fargate-and-aws-compute-savings-plans/
) is not having to pay for the hidden costs of operations.

## EKS Fargate or Managed Node

* Fargate allocates a dedicated right sized virtual machine to run any given pod. At any point in time, no two pods will run on the same VM. With Fargate, you get the packaging and flexibility advantages of using containers with the security advantages of running code within the hard boundaries of a virtual machine.
* Kubernetes pods running on Fargate do not share the same operating system thus mitigating the problems associated with containers escapes.
* With Fargate, AWS is responsible for delivering security related operational tasks such as updating the operating systems of the virtual machines used to run pods

### Fargate limitations

* DaemonSets (ensures all nodes in your K8 cluster run a copy of a pod as a background processes or daemon) typically used for running agents for node monitoring e.g. sending node info to prometheus, log collection  e.g. fluentd or logstash are not supported in EKS Fargate so monitoring and observability tools like Splunk, Datadog have to run in sidecar containers in each pod instead of a DaemonSet per node.
* EKS Fargate does not cache container images on nodes therefore pod start time can be long
* Specific hardware support such as GPUs or pick a particular instance type for fine tune deployment EKS Node Managed cluster
