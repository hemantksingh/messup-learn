# Kubernetes

Kubernetes runs many containers across many machines without anyone placing them, restarting them or rewiring the network by hand. Applications needn't care about the infrastructure they run on. You say what you want and the cluster makes it so and keeps it so.

## The idea: desired state and reconciliation

You write the desired state in a manifest: what should exist, not the steps to get there. A controller compares that with the actual state and acts on the difference. Then it does it again. Forever.

This one loop explains most of Kubernetes. A node dies and three pods vanish; the controller sees "want 3, have 0" and creates three elsewhere. When it cannot get there it keeps trying and writes the reason into the object's status, which `kubectl describe` shows.

## Architecture

A control plane decides. Nodes do.

**Control plane.** The API server is the only door: everything talks to it and nothing writes to the store directly. Behind it is `etcd`, a key-value store and the only stateful component of the cluster; back it up and run it as an odd-numbered quorum. The scheduler picks a node for each new pod from resource requests, affinity rules and taints. The controller manager runs the reconciliation loops, such as the ReplicaSet controller. The term is "control plane", not "master".

**Nodes.** The `kubelet` registers the node, watches the API server for pods assigned to it and asks the container runtime to start them. Its authenticated API is on port 10250; the old read-only port 10255 is disabled by default. `kube-proxy` makes Service IPs route to pod IPs (below). The runtime ([Containers](Containers.md)) is `containerd` or `CRI-O`, spoken to through the Container Runtime Interface (CRI). Docker Engine support went with the dockershim in Kubernetes 1.24; Docker itself uses containerd underneath. `rkt` is dead.

## Workload objects

You rarely create a pod by hand. You create a higher-level object and its controller creates the pods.

| Object | What it is for |
|---|---|
| Pod | One or more containers sharing a network namespace and volumes. The unit of scheduling. Never moved, only replaced. |
| ReplicaSet | Keeps N identical pods running. Almost always owned by a Deployment. |
| Deployment | Stateless services. Owns ReplicaSets and rolls between them for updates and rollbacks. |
| StatefulSet | Pods with a stable name and their own volume (databases, brokers). `db-0` stays `db-0` and gets its disk back. |
| DaemonSet | One pod per node: log shippers, node agents, CNI plugins. |
| Job, CronJob | Run to completion, once or on a schedule. |

Just like a VM is the unit of deployment in the VMware world and a container in the Docker world, the pod is the unit of deployment and scaling in Kubernetes. Containers in a pod share an IP and network namespace (so they talk over `localhost`), IPC and volumes; each keeps its own cgroup for CPU and memory limits. A small "pause" container holds the network namespace for the life of the pod, so application containers can restart without the pod losing its IP. A pod works like a small VM.

## Networking model

Kubernetes ships no network implementation, only three rules that a Container Network Interface (CNI) plugin must satisfy:

* Every pod gets its own IP address.
* All pods can communicate with all other pods without NAT, whichever node they are on.
* All nodes can communicate with all pods (and vice versa) without NAT, and the IP a pod sees itself as is the IP others see it as.

So there is no port mapping between pods; they find each other by real IPs registered in DNS. Inside a node each pod has a virtual ethernet pair, `eth0` in the pod and the other end on a bridge in the node's namespace. Across nodes there are two ways to keep the rules:

* **Routed.** Each node owns a block of pod addresses (its `PodCIDR`) and the node's or the cloud's route table says "10.244.1.0/24 lives on node B". `kubenet` works this way; in Azure the routes are User Defined Routes the platform maintains. Pods do talk pod-IP to pod-IP; the route table is just how a packet finds the right node.
* **Overlay.** Pod packets travel in a node-to-node tunnel (VXLAN, for example), so the underlying network only routes between nodes.

### Services

Pods die and their IPs change. A Service is a stable virtual IP, DNS name and port in front of the pods its label selector matches; moving the label is how blue-green and canary deployments work.

* **ClusterIP** (the default) is reachable only inside the cluster. The other types build on it.
* **NodePort** opens the same port on every node and forwards to the ClusterIP.
* **LoadBalancer** asks the cloud for a load balancer per Service, pointed at the NodePorts: one public IP and one bill per Service.

External traffic therefore goes cloud LB, node, Service, pod, and the client's source IP is lost unless `externalTrafficPolicy: Local` limits each node to its own pods. This is why Ingress controllers and gateways send traffic straight to pod endpoints.

Cluster DNS (CoreDNS) names every Service `<service>.<namespace>.svc.cluster.local`. `kube-proxy` makes the Service IP work with iptables, IPVS or nftables rules that rewrite the destination to a chosen pod; eBPF CNIs such as Cilium do this without kube-proxy.

### Seeing pod networking from inside a pod

The rules above are easiest to believe once you have looked at a pod's own view of the network. Commands after `--` run inside the container; many minimal images lack `ip` and `route`, so use a debug image such as `nicolaka/netshoot` if they are missing.

```sh
kubectl -n <namespace> exec -it <pod> -- ip addr
```

```text
3: eth0@if35: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
    inet 10.244.0.31/24 scope global eth0
```

The pod's address (`10.244.0.31`) comes from the `PodCIDR` of the node it runs on (`kubectl describe node <node>` shows it).

```sh
kubectl -n <namespace> exec -it <pod> -- ip route
```

```text
default via 10.244.0.1 dev eth0
10.244.0.0/24 dev eth0 scope link
```

The default route points at `10.244.0.1`, the node-side bridge (`cbr0` with kubenet; CNI plugins name it differently). Traffic leaving the pod hits that bridge, then the node's routing table decides where it goes next. Service names resolve through the cluster DNS:

```sh
kubectl run -it --rm dbg --restart=Never --image nicolaka/netshoot -- nslookup <service>.<namespace>.svc.cluster.local
```

### Ingress and Gateway API

Services are layer 4; HTTP routing by host or path, and TLS termination, need layer 7. The **Ingress** object describes those rules, but Kubernetes has no built-in controller that acts on Ingress objects, and this is by design. You deploy a third-party Ingress controller: a reverse proxy ([Load Balancing and Proxies](Load%20Balancing%20and%20Proxies.md)) that watches Ingress objects and reconfigures itself.

Ingress took a lowest-common-denominator approach. Controllers filled the gaps with annotations, a stopgap that grew into incompatible dialects, so an Ingress written for one controller does not port to another.

The successor is the **Gateway API**, GA since October 2023. A **GatewayClass** names an implementation. A **Gateway** is a listener with addresses and TLS settings, owned by the platform team. An **HTTPRoute** attaches routing rules to a Gateway from the application team's own namespace. Annotations become typed fields, so routes are portable.

In March 2026 the Kubernetes project retired `ingress-nginx`, the controller about half of clusters ran: no more releases or security patches. Maintained implementations include Envoy Gateway, Cilium, Traefik and NGINX Gateway Fabric.

### TLS with cert-manager

cert-manager is an operator that manages TLS certificates: Certificate and Issuer custom resources, certificates from an ACME CA such as Let's Encrypt or an internal CA, renewal before expiry. The private key and X.509 certificate for a host reach the gateway or ingress controller as a Kubernetes Secret, and the controller uses the SNI extension of TLS to present the right certificate to each client. Certificates and Secrets are namespaced, so define the Certificate in the namespace of the Gateway or Ingress that serves it. ACME itself is in [TLS Certificates](../networking/TLS%20Certificates.md#validity-limits-and-automation).

## Configuration and storage

A **ConfigMap** holds configuration and a **Secret** holds credentials. Both are mounted into pods as files or environment variables, so one image runs everywhere. Secrets are base64-encoded, not encrypted; see [Kubernetes Security](Kubernetes%20Security.md).

A pod's filesystem dies with it. State that must survive is claimed through a **PersistentVolumeClaim**, and a StorageClass provisions a matching PersistentVolume. The claim outlives the pod.

## Packaging and extension

**Helm** is the package manager. A chart is templated manifests plus a `values.yaml`; Helm merges the two and applies the result as a named release it can upgrade and roll back. Charts come from repositories or OCI registries; the old `stable` repository is archived.

```sh
helm repo add <repo> <url>
helm search repo <chart>
helm install <release> <repo>/<chart>
helm install <release> oci://<registry>/<chart>   # from an OCI registry, no repo add needed
```

**Operators** go further. A Custom Resource Definition teaches the API server a new kind, and an operator is a controller for that kind: the same loop, now encoding how to install, back up and upgrade one application. Helm installs; an operator keeps managing.

## Running it

**Locally.** `kind`, `k3d` and `minikube` (docker driver) run a cluster as Docker containers; Docker Desktop bundles a single-node cluster. Development only.

**Self-managed.** `kubeadm` bootstraps a cluster on your own machines. Install a runtime and a CNI plugin, then:

```sh
kubeadm init                          # first control-plane node; prints the join command
kubeadm join <control-plane-host>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

**Managed.** EKS, AKS and GKE run the control plane for you; see [EKS](../../cloud/aws/EKS.md). AKS now defaults to Azure CNI Overlay; kubenet is legacy there. Deciding between a managed service and self-hosting should be a considered one: self-hosting means patching, upgrading, adding nodes and keeping the control plane highly available, forever.

### Production readiness checklist

Questions to have an answer for before a cluster carries production traffic:

* How do we scale the cluster, both node count and node size?
* How do we upgrade the control plane and the node pools, and how often? Kubernetes releases three times a year with roughly fourteen months of support each.
* How do we grow storage and subnets when they run out?
* How do we roll out application updates, and how do we roll them back?
* How do we see and respond to latency and errors?
* How is access to resources regulated per role? (See Kubernetes Security.)
* What are the pod security, resource limit and disruption budget defaults?
* How is the cluster backed up and restored?

## Service mesh and serverless

A service mesh moves mutual TLS, retries, timeouts and request telemetry out of application code into the platform. The data plane is a sidecar proxy in every pod or, in ambient mode, a per-node proxy; a control plane pushes policy to it. Istio and Linkerd are CNCF graduated projects and emit traces with OpenTelemetry.

Serverless on Kubernetes means scale-to-zero and request-driven scaling for containers. Knative, a CNCF project, provides that on a standard cluster. Underneath it is still pods, plus an autoscaler that counts requests and a router that holds them while a pod starts.

## How to rederive this

* Desired state in the API server, the single door, with etcd the single store; controllers compare and correct. For any object, find the controller and what it compares.
* Pods die and get new IPs, so a Service sits in front. Services are layer 4, so HTTP routing needs Ingress, now Gateway API.
* Three networking rules, no NAT: either real routes per node or a tunnel between nodes.
* Anything with its own lifecycle is a CRD plus a controller: the same loop on a new kind.

## Sources

* Kubernetes docs, Concepts: <https://kubernetes.io/docs/concepts/>.
* Burns, Beda, Hightower and Evenson, *Kubernetes: Up and Running*, 3rd ed., O'Reilly, 2022.
* Gateway API: <https://gateway-api.sigs.k8s.io/>.
* Kubernetes blog on the ingress-nginx retirement: <https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/> and <https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/>.
* cert-manager docs: <https://cert-manager.io/docs/>.
