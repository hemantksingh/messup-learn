# Kubernetes cli

## kubectl

Kubernetes client to deploy and manage applications on Kubernetes cluster

```sh
kubectl cluster-info

# list all the kubernetes apis resources
kubectl api-resources

# nodes
kubectl get nodes
kubectl get nodes -o wide

kubectl describe nodes

# service
kubectl get svc <service-name>
kubectl get svc <service-name> -o wide
kubectl get svc <service-name> -o yaml

kubectl edit svc <service-name>

kubectl delete svc <service-name>

# deployment
kubectl get deployment <deployment-name>

kubectl describe deployment <deployment-name>

kubectl apply -f deployment.yaml # create based on the YAML file

kubectl delete deployment <deployment-name>

# replica sets
kubectl get replicasets
kubectl describe replicasets

# get fully qualified domain name for a service (performs a named lookup on the service)
kubectl run -it --rm nwutils --restart=Never --image nbrown/nwutils -- nslookup <service-name>

# get all resources with label query 'app.kubernetes.io/name=ingress-nginx'
kubectl -n <namespace> get -l app.kubernetes.io/name=ingress-nginx all
```

## Expose a service for external access

Using NodePort: https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/

## Configuration best practices

https://kubernetes.io/docs/concepts/configuration/overview/