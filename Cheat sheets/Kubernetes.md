# Kubernetes cli

`kubectl` is the kubernetes client to deploy and manage applications on Kubernetes cluster. The full official kubernetes cheat sheet is available here https://kubernetes.io/docs/reference/kubectl/cheatsheet/


## Kubectl context and configuration

https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-context-and-configuration

```sh
# get the config, context (you can have multiple contexts for multiple clusters) and users info
kubectl config view

# get config in raw format (without redactions)
kubectl config view --raw

# list all the kubernetes apis resources
kubectl api-resources

```

## Viewing, finding resources

https://kubernetes.io/docs/reference/kubectl/cheatsheet/#viewing-finding-resources

```sh

# get nodes with increased verbosity
kubectl get nodes -v 6

# scroll through all the nodes info
kubectl describe nodes | more

# get node IPAddress, PodCIDR and the running pods
kubectl describe node <nodename> | more

# get coredns (cluster dns service that enables service discovery) deployment info
kubectl describe deployment coredns -n kube-system | more

# get all resources with label query 'app.kubernetes.io/name=ingress-nginx'
kubectl -n <namespace> get -l app.kubernetes.io/name=ingress-nginx all
```

## Creating objects

https://kubernetes.io/docs/reference/kubectl/cheatsheet/#creating-objects


You can create deployment based on [here doc](https://stackoverflow.com/questions/2953081/how-can-i-write-a-heredoc-to-a-file-in-bash-script) directly from the command line using `stdin` or define yaml manifests

`kubectl apply -f deployment.yaml`

## Pod networking

```sh

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

# get fully qualified domain name for a service (performs a named lookup on the service)
kubectl run -it --rm nwutils --restart=Never --image nbrown/nwutils -- nslookup <service-name>

# get fully qualified domain name for a service running in a specific namespace
kubectl run -it --rm nwutils --restart=Never --image nbrown/nwutils -n ingress-haproxy -- nslookup http-svc

```

## Configuration best practices

https://kubernetes.io/docs/concepts/configuration/overview/