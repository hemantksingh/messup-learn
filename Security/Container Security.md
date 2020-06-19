# Container Security

Building and running docker containers pose a [number of security challenges](https://hemantkumar.net/think-docker-think-security.html). Docker ecosystem itself provides the following options in terms of addressing some of the security concerns while running your applications in containers.

## Docker content trust

Can be turned on across an organisation and groups using universal control planes

Trust on first use - By default yes, unless you are using universal control planes configured otherwise.

Adversarial environment 

Store root keys offline

## The Update Framework (TUF)

[The Update Framework](https://theupdateframework.github.io/) (TUF) helps developers maintain the security of software update systems, providing protection even against attackers that compromise the repository or signing keys. TUF provides a flexible framework and specification that developers can adopt into any software update system. 

Docker manifest follows a merkel tree

## Docker Trusted Registry

Security scanning for the enterprise, trusted registry may not have access to the internet, therefore the vulnerabilities database needs to be kept up to data offline.

Traditionally - Hard shell soft interior

## Docker Swarm

Join tokens are used to join a swarm (cluster) as a manager or worker

Managers communicate with each other using mutual TLS

## Container networking

Service discovery is network scoped

## Security aware apps

Applications may need elevated privileges on startup, but it is recommended to drop additional privileges post application startup.
