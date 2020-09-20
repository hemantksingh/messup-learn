# Kubernetes cli

## kubectl

Kubernetes client to deploy and manage applications on Kubernetes cluster

```sh
kubectl cluster-info

# get the config, context (you can have multiple contexts for multiple clusters) and users info
kubectl config view

# list all the kubernetes apis resources
kubectl api-resources

# nodes
kubectl get nodes

# scroll through the node information
kubectl describe nodes | more

# service
kubectl get svc <service-name>
kubectl get svc <service-name> -o wide
kubectl get svc <service-name> -o yaml

kubectl edit svc <service-name>

kubectl delete svc <service-name>

# deployment
kubectl get deployment <deployment-name>

# get coredns (cluster dns service that enables service discovery) deployment info
kubectl describe deployment coredns -n kube-system | more

kubectl apply -f deployment.yaml # create based on the YAML file

kubectl delete deployment <deployment-name>

# replica sets
kubectl get replicasets
kubectl describe replicasets

# get fully qualified domain name for a service (performs a named lookup on the service)
kubectl run -it --rm nwutils --restart=Never --image nbrown/nwutils -- nslookup <service-name>

# get fully qualified domain name for a service running in a specific namespace
kubectl run -it --rm nwutils --restart=Never --image nbrown/nwutils -n ingress-haproxy -- nslookup http-svc

# get all resources with label query 'app.kubernetes.io/name=ingress-nginx'
kubectl -n <namespace> get -l app.kubernetes.io/name=ingress-nginx all

```

## pod networking

```sh
# get node IPAddress, PodCIDR and the running pods
kubectl describe node <nodename> | more

# get ip configuration for a running pod
kubectl -n <namespace> exec -it <podname> ip addr

# The following result shows the IP address of the individual Pod - 10.244.0.31. That's being allocated from the PodCIDR range on the node that this individual Pod is running on
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
3: eth0@if35: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    link/ether ba:0d:12:8a:3b:5c brd ff:ff:ff:ff:ff:ff
    inet 10.244.0.31/24 scope global eth0
       valid_lft forever preferred_lft forever

# get IP routing table for a running pod
kubectl -n <namespace> exec -it <podname> route
# The following result shows a default route, which sends all information out to 10.244.0.1 (the IP address of the bridge crbr0 inside of that node). When traffic wants to leave the Pod, it's going to hit this default route and then get forwarded to the interface crbr0, which will then forward it on to the node network. And then the node network will route the traffic based on the destination address in the packet
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.244.0.1      0.0.0.0         UG    0      0        0 eth0
10.244.0.0      *               255.255.255.0   U     0      0        0 eth0

```

## Expose a service for external access

Using NodePort: https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/

## Configuration best practices

https://kubernetes.io/docs/concepts/configuration/overview/