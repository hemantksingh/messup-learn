# Kubernetes

Applications needn't care about the infrastructure that they run on. Separating the infrastructure configuration and maintenance of a large cluster of machines from the application lifecycle management, reduces the friction on development of highly distributed and scalable solutions.

Kubernetes allows offloading the infrastructure concerns away from applications by using standard building blocks and provides a platform for managing applications (running in containers) at scale across machines, so developers don't need to worry about the orchestration complexity. It was originally designed by Google, now governed by the Cloud Native Computing Foundation (CNCF) and developed by Google, Red Hat, CoreOS and many others. Kubernetes aims to provide all the features needed to run Docker or Rkt-based applications including

* cluster management and scheduling
* scaling and deploying new application instances
* kube-proxy based load balancing
* DNS based service discovery
* health checks
* access control via network policies
* monitoring
* secrets management and [more](https://www.thoughtworks.com/insights/blog/macro-trends-tech-industry-nov-2018)

Kubernetes uses declarative desired state in a `manifest` file that describes what the cluster should look like rather than defining the steps to get there. Its control plane runs a reconciliation loop that constantly checks that the actual state of the cluster matches the desired state.

## Installing Kubernetes

* `minikube` - ideal for local dev kubernetes installs, similar to docker for windows or docker for mac but for kubernetes. It runs a simple, single-node Kubernetes cluster inside a virtual machine (VM).
* `kubeadm` - manually install kubernetes cluster on physical VMs. It requires some pre-reqs then

```sh
kubeadm init # spin up a new cluster

kubeadm join --token <token> # add nodes to the cluster
```
Managing a **self hosted kubernetes cluster** in production requires patching, upgrading, adding additional worker nodes etc in addition to H/A. Therefore deciding on using a manged kubernetes cloud service or self hosting a cluster should be a considered one.

## Kubernetes architecture

[Kubernetes architecture](https://github.com/spiddy/kubernetes-security-workshop/blob/master/kubernetes-architecture/architecture.md) constitutes multiple services:

### Master node

#### cluster store

only stateful component of the Kubernetes cluster - `etcd` a distributed NOSQL key value store for storing state and config of the cluster. It makes sense to back this up and deploy it in a H/A config in production.

#### controller manager

runs a number of distinct controller processes in the background to regulate the shared state of the cluster and perform routine tasks.

e.g. a replication controller controls number of replicas in a pod, endpoints controller populates endpoint objects like services and pods.

#### scheduler

helps schedule the pods on the various nodes based on resource utilization

#### api server

exposes a single api for running commands and queries on the master

### Worker Node

Kubernetes workers

* kubelet is the main kubernetes agent that registers the node with the cluster, watches the apiserver for incoming work and instantiates pods
    * **pod** is a single unit of deployment with one or more containers packaged together.
    * exposes endpoint on port: 10255 for node inspection
    * /spec /healthz /pods
* container engine (runtime) - docker or rkt
* kube-proxy - a load balancing service running across multiple pods that proxies traffic to service endpoints (pods) . e.g. if a client pod wants to communicate with a service the kube-proxy routes traffic to one of the pods associated with the service.

## Pods

Just like a VM is a single unit of deployment in the VMWare world and a container in the docker world, pods are single unit of deployment and scaling in Kubernetes world. Containers always run inside of pods. Pod is a single isolated environment with its own:

* network stack - isolated networking resources such as devices, IP4 IP6 protocol stack, ports, firewall rules etc. The shared network namespace means all the containers within the pod share the same network stack.
* kernel namespaces
* pause container -  The network namespace in a pod is implemented by a special container called the pause or the infrastructure container. When a pod is created and started, this container starts up first and sets up the network namespace for the pod. And then application containers, whether it's one or more that are running inside of that pod, will share this network namespace. This pause container enables application containers to be restarted without interrupting the network namespace inside of the pod since the network stack is initialized by the pause container rather than the application container. The pause container has the lifecycle of the pod, and so when the pod is deleted, this container would be deleted along with it.

### Container communication within a pod

All containers in a pod share the pod environment. Each container in the same pod not only **share the same IP** but also share a single network namespace, single localhost adapter, same cgroup limits and same volumes. Containers within a pod communicate with each other over the shared **localhost** interface. This effectively means a pod works like a small VM.

For communication beyond the pod the network namespace is provided with a **virtual network interface** which is allocated an IP address shared with all the containers in the pod.

This allows auto scaling, healing and rolling updates (gradual replacment of running instances of your application with newer ones) and rollbacks quite simple.

### Inter pod communication within a node

The virtual network interface of each pod is attached to a virtual **ethernet bridge** (layer 2) in the host node's network namespace. The bridge routes data packets to connected network segments by resolving IP addresses to corresponding Mac addresses. This enables pods running on the same node to communicate with each other.

### Inter pod communication across nodes

Kubernetes doesn't itself provide an inter node networking implementation but it requires 3rd party network plugins to obey some rules to provide inter node networking. These rules are:

* All pods can communicate with all other pods without Network Address Translation (NAT).
* All nodes can communicate with all containers (and vice-versa) without NAT
* The IP address that a container sees itself as, is the same IP address that others see it as.

Essentially, all pods should be able to reach all other pods running on any node by using the pods real IP address. This results in simple service discovery and application configuration. Services and pods are able to find each other using their real IPs registered in DNS or as environment variables.

By default, Docker uses **host-private networking** so containers can talk to other containers if they are on the same node. Kubernetes assumes that pods can communicate with other pods, regardless of which host they land on. Each pod is given its own cluster-private-IP address so you do not need to explicitly create links between pods or mapping container ports to host ports. This means that containers within a pod can all reach each other’s ports on localhost, and all pods in a cluster can reach each other using the pods IP without NAT.

In order to provide inter node networking Kubernetes expects 3rd party plugins that intend to provide pod networking across nodes to adhere to a specification called the **Container Networking Interface** or CNI. The CNI spec describes what a plugin must provide in order to facilitate container networking. Typically plugins implement pod to pod networking across nodes using layer 2/3 routing or **overlay networks**. An overlay network gives the appearance of a single network between the nodes in a cluster and uses tunnels or other mechanisms to move encapsulated pod network packets between the nodes.

This means a pod on one node can seamlessly communicate with a pod on another node without having to deal with any network plumbing configuration.

To provide inter node network connectivity, AKS clusters can use **kubenet** (basic networking) or **Azure CNI** (advanced networking). [AKS clusters by default use kubenet](https://docs.microsoft.com/en-us/azure/aks/configure-kubenet). With *kubenet*, only the nodes receive an IP address in the virtual network subnet. Pods can't communicate directly with each other. Instead, User Defined Routing (UDR) and IP forwarding is used for connectivity between pods across nodes. By default, UDRs and IP forwarding configuration is created and maintained by the AKS service, but you have to the option to bring your own route table for custom route management.

## Services

A way of providing stable IPs, DNS names and ports for ephemeral pods in a replication set, so that clients both external and internal to the cluster can access the pods depending upon the service type.

**Kube-proxy** exposes services onto the network by configuring IP table rules for the service on all nodes and load balances requests to the backend pods running in the cluster. Kube-proxy runs as a pod on each node in the cluster.

**Labels** and **Selectors** are used to [connect services to pods](https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/) and facilitate Blue green/canary and rolling deployments. Services define selectors that have to match the labels on the pods.

### Service API

ClusterIP exposes the service on a cluster internal IP address and is only available inside of the cluster. It's also the default service type if you don't specify one in your services configuration, and it's the foundation that the other service types are built upon. A common use case for ClusterIP is for applications or services that don't need to be accessed outside of the cluster or if we're going to provide access via other means, like ingress

The Kubernetes Service API can be used for basic layer 4 ingress requirements like [exposing services](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) for internal and external use but it has the following limitations:

* Exposing service objects using the *NodePort* type and in order to load balance service requests over cluster nodes, we'd need to manually configure external load balancer and cope with the operational overhead of cluster node failures and IP address changes.
* NodePort Service is back ended by a cluster IP service, so as traffic comes in on the NodePort ports, it will get routed to that cluster IP service.
    * This can introduce potential latency due to the network hops introduced by kube-proxy. Ingress controllers send requests directly to pod endpoints rather than to kube-proxy which would then route to Pod endpoints and perhaps even routing traffic between nodes. Node -> Service ClusterIP -> Pod. In addition, client IP addresses are lost in this exercise unless the [external traffic policy is set to local](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip) to route traffic only to pods running on the same node. This might work for you, but it would remove one of the benefits of the service API implementation, which is to load balance ingress traffic across each of the service endpoints (pods) across nodes.
* *LoadBalancer* type per service means your cloud provider provisions a load balancer and a public IP for each service. This can quickly escalate operational costs. When we access the EXTERNALIP on that cloud load balancer, that cloud load balancer is going to send its traffic to the NodePort service. The NodePort service is then going to send a traffic on to the ClusterIP service, which will then route it to an individual pod that services our deployment.

## Ingress

For advanced [host-based and path-based routing](https://dzone.com/articles/the-three-http-routing-patterns-you-should-know) of external client HTTP/S traffic (layer 7) to services running in the cluster, the [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) API allows

* named services to be externally accessible outside the cluster with externally reachable URLs
* services with load balancing (defining traffic routes to backend services)
* reliable and secure communication with SSL termination. Since containers are always coming up and going down, clients may be communicating with different containers running on different nodes on different requests. Ingress provides a consistent experience for clients over a secure reliable connection.

Ingress is a Kubernetes API object that manages the routing of external traffic to the services that are running in a cluster. Just like you would with a service object, you define the characteristics of an ingress object in a manifest. Once it's been submitted to the API Server, you'd expect Kubernetes to create the object and then start to act on what's defined using a controller, which moves the actual state towards the desired state. However, Kubernetes doesn't have its own controller that acts on ingress objects and this is by design. Instead, it relies on a cluster administrator to deploy a third-party ingress controller to the cluster. Ingress controllers need to implement the Kubernetes controller pattern, but they also need to route external traffic to cluster workloads. Essentially, this is a reverse proxy of which there are aplenty.

[Ingress Controller](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) is responsible for fulfilling the ingress with layer 7 traffic routing. It runs in a loop to get all the ingress resources running in a cluster and can dynamically configure a corresponding L7 proxy. e.g. nginx controller (maintained by Kubernetes project, written in Go) generates the `nginx.conf` file based on the ingress resources. The ingress controller runs inside the cluster.

### Limitations of the Ingress API

The ingress API in adopting a lowest common denominator approach has resulted in lack of options that other technologies require for the API to be more expressive

* Limited by design - intended to be simple and straight forward so that it can be extended by a wide range of technologies including cloud load balancers.
* Annotations stopgap - provided as a method to overcome this deficiency, resulted in explosion of disparate annotation patterns. Porting annotations from one ingress controller to another doesn't make for a good user experience.

### Ingress controller options

The Kubernetes Network Special Interest Group is likely to facilitate a consensus for a future v2 Ingress API or equivalent. With the given limitations of the ingress API your current choice for an ingress controller may not be future proof.

Currently there are 2 ways to configure ingress to your services:

* annotations used by ingress controllers like [nginx](https://git.k8s.io/ingress-nginx/README.md), [haproxy](https://haproxy-ingress.github.io/)
* custom resources used by Envoy based [Contour](https://projectcontour.io/) or [Ambassador](https://www.getambassador.io/), v2 of [Traefik](https://github.com/containous/traefik) ingress controllers. While Contour uses custom resources it also supports annotations.

A [custom resource](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources) is an extension of the Kubernetes API that is not necessarily available in a default Kubernetes installation. A **Custom Resource Definition** (CRD) file defines your own object kinds e.g. `HTTPProxy` in the case of Contour and lets the API Server handle the entire lifecycle. Deploying a CRD into the cluster causes the Kubernetes API server to begin serving the specified custom resource. Before you can start to use your custom CRD you need to register the CRD with the kubernetes api server.

[Nginx can cut websocket connections](https://vitobotta.com/2020/03/20/haproxy-kubernetes-hetzner-cloud) whenever it reloads its configuration, therefore it might be useful to deploy ingress controllers per connection type: one for http and another for websockets. Things to consider before opting for an ingress controller:

* rate limiting
* IP whitelisting
* add request and response headers
* connection queueing to prevent backends from overloading
* connection draining
* client authentication, both [nginx](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#client-certificate-authentication) and [haproxy](https://github.com/jcmoraisjr/haproxy-ingress/tree/master/examples/auth/client-certs) provide client certificate authentication using annotations in ingress rule
* support for WAF, e.g. haproxy provides [configuration of MoDSecurity](https://github.com/jcmoraisjr/haproxy-ingress/tree/master/examples/modsecurity) Web Application Firewall

## Cert manager

Defining, requesting, applying, renewing, and removing TLS certificates can be a pain, especially when you have a lot of them to manage. Cert manager is a Kubernetes operator that allows automatically requesting, retrieving and configuring TLS for hosts defined in ingress rules.

Cert manager uses a Custom Resource Definition (CRD) to perform X.509 certificate management to secure backend services. It works like [Certbot](https://certbot.eff.org/docs/intro.html) an easy-to-use ACME client that runs directly on a web server, fetches a certificate from Let’s Encrypt certificate authority (or any other CA that speaks the ACME protocol) and deploys it to the web server.

The ingress controller relies on the SNI extension of TLS to host multiple certificates for multiple domains and figure out which X.509 certificate to present to an external client.
The private key and the corresponding X.509 certificate (PEM) for the host is made available to the ingress controller as a Kubernetes secret.

### Certificate Acquisition

Automatically obtaining a certificate from a server that supports the ACME (Automated Certificate Management Environment) protocol, such as the let's encrypt certificate authority requires your request agent (cert manager in this case) to [prove that it controls the specified domain](https://letsencrypt.org/how-it-works/) name by either:
* Provisioning a DNS record under the domain
* Provisioning an HTTP resource under a well-known URI on http://example.com/

Certificates are scoped to a namespace, so when you're planning to use them in conjunction with ingress objects, be sure to define both the certificate and ingress objects in the same namespace.

## Kubernetes ecosystem

There are a huge number of [kubernetes supporting services](https://www.thoughtworks.com/insights/blog/macro-trends-tech-industry-nov-2018) for configuration scanning, security auditing, disaster recovery etc.

### Operators

Helm and Operators allow [managing complex application workloads in kubernetes](https://medium.com/@cloudark/kubernetes-operators-and-helm-it-takes-two-to-tango-3ff6dcf65619). Helm is geared towards performing templatization and deployment of Kubernetes YAMLs while [Operators](https://coreos.com/blog/introducing-operators.html) are geared towards ongoing management of applications that automatically scale, upgrade, backup and failover by watching events without editing Kubernetes config and protecting against data loss or unavailability. For example, if Kubernetes detects the loss of a node, an Operator could automatically replicate data from another cluster node running in Kubernetes while maintaining a quorum to bring the cluster back to the desired level of parity. Kubernetes started off as a great fit for managing stateless applications, therefore Operators in their early days were often focused on database applications and helping to extend Kubernetes capabilities to this critical category. Some of the examples were MongoDb, Cassandra and Redis avaialble on [operatorhub.io](https://operatorhub.io) registry. However, [Kubernetes operators aren't just for databases](https://enterprisersproject.com/article/2020/2/kubernetes-operators-4-things-know?page=1), examples include Prometheus Operator, [NATS Operator](https://github.com/nats-io/nats-operator)

### Helm

[Helm](https://github.com/helm/helm) is an open-source packaging tool that helps you install and manage the lifecycle of Kubernetes applications. Similar to Linux package managers such as APT and Yum, Helm is used to manage Kubernetes application using YAML artifacts and templates. Helm allows defining Kubernetes YAMLs with marked up properties. The actual values for these properties are defined in a separate file. Helm takes the templatized YAMLs and the values file and merges them before deploying the merged YAMLs into a cluster. The package consisting of templatized Kubernetes YAMLs and the values file is called a ‘Helm chart’.

```sh
helm search # Search for pre-created Helm charts

helm repo update # Update the list of charts

helm install stable/wordpress # Install charts with helm, e.g. a basic Wordpress deployment
```

### Managing kubernetes clusters

Kubernetes clusters come with their own management challenges that require metrics, observability, and a user-friendly interface to present their huge amount of complexity. Few options for managing kubernetes clusters and containers running within:

* https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard
* https://opensource.com/article/20/6/kubernetes-lens
* https://docs.openshift.com/container-platform/4.2/web_console/web-console.html
* https://rancher.com/

Things that could go wrong in a kubernetes cluster - https://www.youtube.com/watch?v=obB2IvCv-K0&feature=emb_logo

Configuration best practices - https://kubernetes.io/docs/concepts/configuration/overview/

### Service Mesh

A [servie mesh](https://www.hashicorp.com/resources/what-is-a-service-mesh) allows you to move cross cutting concerns in a microservices architecture like service discovery, service-to-service and origin-to-service security and monitoring capabilities outside your applications into the infrastructure layer that can be configured as code. The policy configurations can be consistently applied to the whole ecosystem of microservices; enforced on both north-south (via the mesh proxy as a gateway) as well east-west traffic (via the same mesh proxy as a sidecar container).

Rather than making your applications aware of the cross cutting concerns like implementing timeouts and retry, implementing tracing via OpenTracing Zipkin, instrument applications to produce Prometheus metrics or implement mutual TLS for encryption, a service mesh provides these capabilities as a service configurable via a unified [control plane](https://blog.envoyproxy.io/service-mesh-data-plane-vs-control-plane-2774e720f7fc). Ultimately, the goal of a control plane is to set policy that will eventually be enacted by the data plane.

* Service discovery and fine grained routing: Service load balancers often front a service tier and provide a static IP which must be updated as services scale up/down. Service Registry enables services to register and discover each other by listing all of the upstream/backend service instances that are available.
* Traffic routing to direct client requests to a particular service deployment for AB testing or direct a particular customer to a preferred highly stable service deployment or a bleeding edge one.
* Load balancing: Once an upstream service cluster has been selected during routing, to which upstream service instance should the request be sent? With what timeout? With what circuit breaking settings? If the request fails should it be retried? 
* Service to service security: A service mesh allows you to replace traditional host-based network security with service-based security to accommodate the highly dynamic nature of modern runtime environments. Rather than depend on security at the perimeter of the network to filter incoming traffic via firewalls, WAFs and SIEMs, a service mesh allows policy rules at the logical service level to solve security challenges with service identity and security control at the edge using mutual TLS.

* Observability including telemetry and distributed tracing without having to put instrumentation in your apps.

Service mesh isn't a silver bullet to all problems with microservices, [Istio](https://github.com/scotty-c/kubernetes-security-workshop/blob/master/introduction-into-istio/intro.md) is by far the most mature implementation there is right now, others including [Linkerd](https://linkerd.io/) and [Consul](https://learn.hashicorp.com/consul/). Its worth considering [do you really need a service mesh](https://www.nginx.com/blog/do-i-need-a-service-mesh/) for simple containerised applications running on a container orchestration platform like kubernetes. Kubernetes is a very capable platform with a rich networking layer that brings together service discovery, load balancing, health checks, and access control in order to support complex distributed applications. In a kubernetes cluster you may have all the apps i.e. frontend and the backend running within the same cluster without any static network segmentation, because [kubernetes security](https://github.com/scotty-c/kubernetes-security-workshop/) adopts a [dynamic approach](https://skillsmatter.com/skillscasts/13339-securing-and-integrating-legacy-applications-with-kubernetes-and-consul-connect) with **role based access control**.

### Serverless workloads

Serverless architectures allow the underlying platform to handle deploying, scaling and managing applications but most offerings are tied to proprietary implementations which means vendor lock-in. Google's [KNative](https://cloud.google.com/knative/) framework provides an alternative with the ability to build, deploy, and manage serverless workloads on Kubernetes. 

Google have however [declined to donate KNative and Istio to CNCF](https://www.theregister.co.uk/2019/10/02/google_knative_will_not_be_donated_to_any_foundation/) which has led to some concerns over lack of open governance that is applicable to Kubernetes itself. There are many possible factors. Open governance foundations may be less agile than those managed by a corporation, for example, since consensus on decisions could be harder to reach. Both Knative and Istio use the Apache License 2.0 and Google's announcement does confirm that Knative will remain open source and with multi-vendor participation.
