---
title: "Kubernetes Security"
summary: "How the API server authenticates callers, how roles and bindings scope what they may do, and what hardens pods and the cluster."
kind: concept
status: current
last_reviewed: 2026-09-16
sources: []
tags: [kubernetes, rbac, authentication, service-accounts, pod-security, cis-benchmarks]
---
# Kubernetes Security

## Securing the API Server

Communication with a kubernetes cluster is handled by the API server through REST requests. Authentication to the API server is configurable, and you could define one or more authentication methods. This is made possible using an authentication plugin that  is defined by the cluster administrator with configuration parameters on the API server itself. There are no usernames stored in the API server for authentication purposes, it's up to the selected authentication plugin to define and implement how a user is defined and authenticated. Some of the common authentication plugins available are:

* Client Certificates - a request is authenticated when a valid, trusted certificate is presented as part of the HTTP request. The certificate carries the username (used for authorization - i.e. what the user can do) in the Common Name (CN) field and groups in the Organization (O) fields. Cluster components use certificates, and they are the bootstrap and break-glass path for admins. Humans on managed clusters (AKS, EKS, GKE) normally authenticate with OIDC or cloud IAM tokens instead.
* Bearer tokens in the HTTP Authorization header. Sources include a static token file, bootstrap tokens (for joining nodes), service account tokens, OIDC ID tokens and webhook token authentication.

Basic HTTP authentication (`--basic-auth-file`) was removed in Kubernetes 1.19 and is no longer an option.

Open ID Connect enables external identity providers for authentication and remote authentication services. This requires additional set up integration with that external provider, but enables you to have a centralized user database which can facilitate for single sign on. This can be useful in scenarios where you have multiple clusters or multiple applications that require centralized authentication services for your organization.

The main idea here is that authentication is plugable and you have the ability to use one or more than one method for authentication.

## Certificate based authentication

Kubernetes uses certificates to provide TLS encryption. The API server is exposed on an https endpoint using a certificate. In addition to providing encryption, certificates are also used for authenticating both users and system components.

Every Kubernetes cluster has a cluster root Certificate Authority (CA). The CA is generally used by cluster components to validate the API server’s certificate, by the API server to validate `kubelet` or `kubectl` client certificates, etc. There can be [more than one CAs in a kubernetes cluster](https://jvns.ca/blog/2017/08/05/how-kubernetes-certificates-work/) e.g API server CA and kubelete CA.

The API server provides a certificate API enabling you to submit a Certificate Signing Request (CSR) to be used to [request X.509 certificates](https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/#requesting-a-certificate). Once generated and signed you can download a certificate for use in your cluster by users and system components. This could be done at the command line using certificate tools like `OpenSSL` or `CFSSSL`, but the API provides a programmatic interface for Certificate management for the internal cluster self signed CA on the control plane node. The CSR API is `certificates.k8s.io/v1` (since 1.19) and every request must name a `signerName`, e.g. `kubernetes.io/kube-apiserver-client` for client certificates.

```sh
# Get the client certificate from kubeconfig
kubectl config view --raw -o jsonpath='{ .users[*].user.client-certificate-data }' | base64 --decode > admin.crt

# Inspect the client certificate
openssl x509 -in admin.crt -text -noout | more

```

## Authorization with service accounts

Running a pod in kubernetes without a specified service account runs it with the default service account. Since 1.24 service account tokens are bound, time-limited projected tokens; long-lived token Secrets are no longer created automatically. Set `automountServiceAccountToken: false` on pods (or the service account) that do not call the API; it is the hardening default.

```sh
# List all service accounts
kubectl get serviceaccounts

# Check if a service account <serviceaccountname> is authorized to list pods by impersonating as the <serviceaccountname>
kubectl auth can-i list pods --as=system:serviceaccount:default:<serviceaccountname>
```

## Roles based access

Role/ClusterRole - only define what can be done. It maps nouns to verbs `get pods`. Role is confined to a namespace whereas a ClusterRole is applicable to the entire cluster.

RoleBinding - defines who can do what. It defines the Subjects and refers to a Role/ClusterRole. The Subject can be User/Group or ServiceAccount. *Users and Groups are not namespaced objects and are considered cluster-wide resources*. The Role and RoleBinding must be defined in the same namespace.

When a ClusterRole is used with their RoleBinding, your specifying who can do which actions potentially across multiple name spaces, or even the whole cluster. These objects do not have to be in the same namespace, because the scope of their security is potentially across multiple namespaces or even the whole cluster. This allows you to have the same cluster role in several namespaces and potentially all namespaces. If you find yourself configuring this for all namespaces use a ClusterRoleBinding instead.

ClusterRoleBinding -  ClusterRoleBinding is used to grant access to all namespaces across a cluster. When you combine a ClusterRole with a ClusterRoleBinding, this will scope security for the subjects defined in the ClusterRoleBinding to all namespaces or all non-namespace cluster scoped resources. Use a ClusterRole with a ClusterRoleBinding if you need to give access to

* all namespaces or
* cluster scoped resource like nodes and persistent volumes

### What to use when

* Use a Role and RoleBinding to scope security to a single namespace. e.g. giving one development group access to a whole name space for their applications or projects.

* Use a ClusterRole and RoleBinding to scope security to several or potentially all of the namespaces in a cluster. Perhaps this is a development architect or manager overseeing several projects deployed across several namespaces, but usually not the whole cluster.
  
* Use a ClusterRole and a ClusterRoleBinding to scope security to all namespaces OR cluster-scoped resources. The resource is this most often will be someone that's in charge of managing a cluster or those cluster-scoped resources like nodes and persistent volumes

### Default cluster roles

Kubernetes ships four ClusterRoles meant for people. `cluster-admin` is bound cluster-wide with a ClusterRoleBinding; the other three are meant to be bound within a namespace with a RoleBinding.

| Role | Scope | Can | Cannot |
|---|---|---|---|
| `cluster-admin` | Cluster-wide superuser. With a RoleBinding, full admin within that namespace, including the namespace object itself | Any action on any resource | Nothing is off limits |
| `admin` | One namespace | Read and write most resources; create and edit Roles and RoleBindings | Write resource quotas or the namespace itself |
| `edit` | One namespace | Read and write most resources, including Secrets; run pods as any service account in the namespace | View or edit Roles and RoleBindings; write resource quotas |
| `view` | One namespace | Read most resources | View Roles, RoleBindings or Secrets; write anything |

`edit` can read Secrets and run pods as any service account, so it can reach the API with any service account's permissions in that namespace. `view` cannot read Secrets for the same reason. Source: [Kubernetes RBAC, user-facing roles](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles).

### Multi tenancy

RBAC can be employed to run multi-tenant application in kubernetes. The namespace logical isolation along with RBAC provides the fundamentals of [multi-tenancy in kubernetes](https://www.infoq.com/presentations/multi-tenancy-kubernetes/). All tenants share the control plane where secrets and ConfigMaps are stored, therefore the API server can be overloaded by a user from a particular tenant. This can result in tenants crowding each other accidentally or on purpose. [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/) (GA in 1.29) limits this: `FlowSchema` objects classify requests and `PriorityLevelConfiguration` objects share the capacity between them. The `--max-requests-inflight` and `--max-mutating-requests-inflight` flags only set the total budget.

## Pod security

* PodSecurityPolicy was removed in 1.25. Its replacement is Pod Security Admission, which enforces the Pod Security Standards (`privileged`, `baseline`, `restricted`) per namespace via labels.
* Default-deny `NetworkPolicy` per namespace, then allow only the traffic each workload needs.
* Encrypt Secrets at rest in etcd (`EncryptionConfiguration`) or use a KMS provider.
* Enable API server audit logging and ship the logs off the cluster.

## Compliance

How do you embed security and validate compliance against standards like PCI, NIST, and SOC2 across the lifecycle of containers and Kubernetes? Start from the CIS Kubernetes Benchmark for the cluster, the Pod Security Standards for workloads, and an admission policy engine (Kyverno, Gatekeeper or the built-in `ValidatingAdmissionPolicy`) to enforce your own rules.

Check cluster against CIS kubernetes benchmarks

* [kube-bench](https://github.com/aquasecurity/kube-bench) is a Go application that checks whether Kubernetes is deployed securely by running the checks documented in the CIS Benchmarks.

Check for security weaknesses/vulnerabilities in Kubernetes clusters

* [kube-hunter](https://github.com/aquasecurity/kube-hunter) is no longer under active development; its README points to [Trivy](https://github.com/aquasecurity/trivy), also from Aqua, which scans clusters and runs the CIS checks that kube-bench covers.
