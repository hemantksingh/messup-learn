
# Securing the API Server

Authentication in Kubernetes is configurable, and you could define one or more authentication methods for your API server. An authentication plugin is defined by the cluster administrator with configuration parameters on the API server itself. There are no usernames stored in the API server for authentication purposes, it's up to the selected authentication plugin to define and implement how a user is defined and authenticated. Some of the common authentication plugins available are:

* Client Certificates - most commonly used - e.g. in managed cloud service like AKS. A request is authenticated when a valid, trusted certificate is presented as part of the HTTP request. Certificate contains the username (used for authorization - i.e. what the user can do) in the Common Name (CN) field of the certificate.
* Authentication Tokens - HTTP Authorization header in the client request
* Basic Http - uses static password files read during API server startup, simple to setup and use (Dev)

Open ID Connect enables external identity providers for authentication and remote authentication services. This requires additional set up integration with that external provider, but enables you to have a centralized user database which can facilitate for single sign on this, convey useful in scenarios where you have multiple clusters or multiple applications that require centralized authentication services for your organization.

The main idea here is that authentication is plugable and you have the ability to use one or more than one method for authentication.

## Certificate based authentication

```sh
# Get the client certificate from kubeconfig
kubectl config view --raw -o jsonpath='{ .users[*].user.client-certificate-data }' | base64 --decode > admin.crt

# Inspect the client certificate
openssl x509 -in admin.crt -text -noout | more

```

## Authorization with service accounts

Running a pod without a specified service account runs it with the default service account.

```sh
# List all service accounts
kubectl get serviceaccounts

# Check if a service account <serviceaccountname> is authorized to list pods (impersonation)
kubectl auth can-i list pods --as=system:serviceaccount:default:<serviceaccountname>

```
