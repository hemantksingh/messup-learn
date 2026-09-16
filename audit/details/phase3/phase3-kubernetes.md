# Phase 3 report: fundamentals/platform/Kubernetes.md

File: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Kubernetes.md (not committed; only this file edited).

Size: 12.7 KB (was 27 KB). Word count: 1,998 by raw `wc -w` (code, table cells and URLs included); 1,737 words of prose. About 330 of those prose words are the two verbatim Phase 1 sections. Checks passed: one H1 "Kubernetes", no em or en dashes, no connective filler or American spellings, every fence has a language, all five relative links resolve, no `> Own view:` blocks, both Phase 1 sections byte-identical to HEAD apart from heading level (see open question 1). The Helm snippet uses placeholders so it cannot fail on a fresh machine.

## (a) Question the page answers

What problem does Kubernetes solve, and how do its parts fit together? The first paragraph answers it (run many containers across many machines without hand-placing, restarting or rewiring), then everything is derived from one idea: desired state and a reconciliation loop, which the page returns to for controllers, operators, Ingress controllers and the "How to rederive this" bullets.

## (b) Kept from the original (owner's sentences and examples)

- "Applications needn't care about the infrastructure they run on."
- The VM / container / pod "unit of deployment" analogy and "a pod works like a small VM".
- The pause-container explanation, shortened, content unchanged.
- The three pod-networking rules, near verbatim, and "Kubernetes doesn't itself provide an inter node networking implementation" (as "Kubernetes ships no network implementation").
- etcd as the only stateful component; back it up.
- The Service hop chain (cloud LB, node, Service, pod), the lost client IP and `externalTrafficPolicy: Local`, and the conclusion that Ingress controllers send traffic straight to pod endpoints.
- ClusterIP as the default that the other types build on; LoadBalancer cost per Service.
- "Kubernetes has no built-in controller that acts on Ingress objects, and this is by design."
- Ingress limitations: "lowest common denominator" and the "annotations stopgap".
- cert-manager operational detail: SNI, Secret holding key and certificate, namespace scoping.
- Helm: templates plus values merged into a release; Helm versus Operators ("Helm installs; an operator keeps managing").
- The owner's position that choosing managed versus self-hosted "should be a considered one", with the patching, upgrading, node and HA list, stated as a plain sentence.
- Both Phase 1 sections verbatim: "Seeing pod networking from inside a pod" (at the end of the networking model, after Services) and "Production readiness checklist" (after "Running it").

## (c) Dropped and why

- The feature bullet list with the ThoughtWorks link; "Google, Red Hat, CoreOS"; "Docker or rkt" (twice); the "Docker uses containers as a runtime" typo sentence.
- "master" terminology; kubelet 10255 listed as a feature; the incomplete `kubeadm join`.
- "replication controller controls replicas in a pod", "endpoints controller", "replication set": replaced by ReplicaSet. The EndpointSlice controller mention the audit asked for was cut in the final length pass (open question 4).
- "same cgroup limits": corrected to one cgroup per container.
- The AKS subsection with its Microsoft Learn paste. AKS now appears once, under Managed, with the Azure CNI Overlay default. The kubenet contradiction is resolved generically in the Routed bullet.
- The Ingress-controller catalogue: ingress-nginx and haproxy annotation links, Contour/Ambassador/Traefik under old names, the "future v2 Ingress API" prediction, the websocket-reload workaround, the considerations list (rate limiting, IP whitelisting, WAF/ModSecurity). Replaced by Gateway API and the retirement fact.
- The ACME "Certificate Acquisition" section: now one link to TLS Certificates, where Phase 1 moved it.
- "Kubernetes ecosystem" intro, the Operators paragraph's database history and product list, Helm 2 commands, the cluster-management link list (dashboard, Lens, OpenShift 4.2, Rancher), the "things that could go wrong" video and config best-practices links.
- The service-mesh bullet list (HashiCorp and Envoy-blog derived), "Istio is by far the most mature", OpenTracing/Zipkin, the Consul Connect and skillsmatter links, and the owner's "do you really need a mesh" aside (cut for length; open question 3).
- The "Google declined to donate Knative and Istio" paragraph, entirely, per the brief.
- The `> Own view:` blocks I had drafted were removed after the owner's feedback; nothing is marked as the owner's stance that the owner did not write.

## (d) Added, with sources for non-obvious claims

- Desired state and reconciliation as the organising idea; status via `kubectl describe`. Kubernetes docs, Concepts (Cluster Architecture, Controllers).
- API server as the only door; etcd odd-numbered quorum; scheduler inputs (requests, affinity, taints). Kubernetes docs; Kubernetes: Up and Running.
- Kubelet authenticated port 10250; read-only 10255 disabled by default. Audit finding (infra-k8s.md lines 61-62); kubelet reference.
- CRI with containerd and CRI-O; dockershim removal in 1.24; Docker uses containerd. Kubernetes blog on dockershim removal; Container Runtimes docs.
- Workload table (Pod, ReplicaSet, Deployment, StatefulSet, DaemonSet, Job/CronJob). Kubernetes docs, Workloads.
- Containers share network and IPC namespaces and volumes, each with its own cgroup. Kubernetes docs, Pods; audit finding line 76.
- Routed versus overlay as the two ways to satisfy the rules; kubenet as routed with UDR in Azure. Kubernetes docs, Cluster Networking; Microsoft Learn "Configure kubenet networking in AKS" (via audit).
- kube-proxy modes iptables, IPVS, nftables; eBPF CNIs (Cilium) replacing kube-proxy. Kubernetes docs, Virtual IPs and Service Proxies; Cilium docs.
- CoreDNS naming scheme. Kubernetes docs, DNS for Services and Pods.
- Gateway API GA October 2023; GatewayClass, Gateway, HTTPRoute and the role split. gateway-api.sigs.k8s.io.
- ingress-nginx retired March 2026, "about half" of clusters, no releases or security patches; surviving implementations. Kubernetes blog 2025-11-11 (https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/) and 2026-01-29 (https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/), both URLs confirmed by web search during this task.
- cert-manager Certificate and Issuer resources, ACME or internal CA. cert-manager docs.
- ConfigMap, Secret (base64, not encryption), PersistentVolumeClaim and StorageClass. Kubernetes docs, Configuration and Storage.
- Helm 3 commands (`helm repo add`, `helm search repo`, `helm install <release> <chart>`, `oci://`), stable repository archived. Helm docs; audit findings lines 196-200.
- kind, k3d, minikube docker driver, Docker Desktop bundled cluster. Project docs; audit finding line 20.
- Complete `kubeadm join` with control-plane endpoint and `--discovery-token-ca-cert-hash`. kubeadm reference; audit finding line 26.
- AKS defaults to Azure CNI Overlay, kubenet legacy. Audit (verified against Microsoft Learn 2026-09-16).
- Service mesh sidecar or ambient data plane; Istio and Linkerd CNCF graduated; OpenTelemetry. CNCF announcements (Istio July 2023, Linkerd 2021); Istio ambient docs.
- Knative as a CNCF project. CNCF blog, Knative accepted March 2022 (link in audit/details/overlaps.md).
- Book: Burns, Beda, Hightower and Evenson, Kubernetes: Up and Running, 3rd ed., O'Reilly, 2022.

## (e) Diagrams for Phase 5

The page has no images and none were added. Two would earn their place:

1. `kubernetes-architecture.drawio.svg`: control plane (API server as the single entry, etcd behind it, scheduler and controller manager as API-server clients) and two nodes (kubelet, kube-proxy, runtime via CRI, pods). Every arrow points at the API server to show "only door".
2. `pod-networking-paths.drawio.svg`: one node with two pods on veth pairs into a bridge; a second node; the cross-node path drawn twice, once routed (route table entry "10.244.1.0/24 via node B") and once as an overlay tunnel. Label the three rules on the picture. This is the diagram the kubenet contradiction needed.

## (f) Open questions for the owner

1. The two Phase 1 sections are verbatim in text, but their headings were demoted from H2 to H3 so they sit inside "Networking model" and "Running it". If "verbatim" includes heading level, change `### ` back to `## ` on those two lines.
2. Length is at the cap (1,998 raw). Nothing more can come out without cutting the owner's own material (the Service hop chain, the cert-manager namespace sentence) or the verbatim sections.
3. Two stances from the original were kept as plain sentences or cut: managed versus self-hosted "should be a considered one" (kept, neutral wording) and "do you really need a service mesh for simple containerised applications" (cut for length). Say if either should return as `> Own view:`.
4. The EndpointSlice controller mention was cut for length; the audit asked for it. One clause in the controller-manager sentence would restore it.
5. `Kubernetes Security.md` still carries the `default-cluster-roles.png` screenshot that Phase 5 turns into a table; nothing on this page depends on it.
