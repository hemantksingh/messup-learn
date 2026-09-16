# Containers

A container is not a small virtual machine. It is an ordinary [process](../computing/The%20Unix%20Model.md) (or process tree) on the host's kernel with a restricted view. No second kernel, no virtual hardware, no boot sequence: hence millisecond start-up and weaker isolation than a VM.

## VM versus container

*Take a physical machine and carve it up into multiple virtual machines where each virtual machine looks, feels and tastes just like the physical machine.* A hypervisor intercepts CPU, memory and device access so each **guest**, an unmodified OS with its own kernel, believes it owns the **host** hardware. Bringing its own kernel lets a guest run a different OS, and costs CPU, memory, disk, patching and sometimes a licence.

A container skips that: the kernel is the host's and the container is a process it fences in, whether the image is a whole distribution's userland or one static binary (`scratch`). "Bare minimum Linux machine" is wrong: there is no machine.

> Own view: OS's are a necessary evil to run applications. What is important to us is to be able to run applications not an OS to support them. If we could run applications directly on the server hardware, we surely would.

## The three mechanisms

**Namespaces decide what the process can see.** Each type gives it a private copy of one global resource:

* pid: its own process tree, starting at PID 1, whose exit ends the container
* net: its own interfaces, IP address, ports and routing table
* mnt: its own root filesystem and mounts
* uts: its own hostname
* ipc: its own shared memory and message queues
* user: its own user IDs, so root inside can be unprivileged outside

**cgroups decide what the process can use.** They meter and cap CPU, memory, I/O and process count. A memory limit is a cgroup limit; exceed it and the OOM killer takes the process.

**A union filesystem decides what the process sees on disk.** The storage driver (overlay2; aufs is history) stacks the image's read-only layers under one thin writable layer. Reads fall through to the first layer with the file; writes go to the top. A delete writes a marker on top that hides the lower file; the bytes stay.

## Images and containers

An **image** is read-only layers plus metadata (command, environment, ports). A **container** is a running instance: the same layers, a fresh writable layer, the namespaces and cgroup. Ten containers from one image share its layers on disk; only their top layers differ.

A **tag** is a name pointing at an image. `latest` is just the default tag, not "the newest version"; publishers need not keep it current. `docker run` uses the local image under that tag without checking the registry (pull policy `missing`); `docker pull` or `--pull always` refreshes it, so two machines on "the same" tag can differ. Pin a tag, or better a digest (`image@sha256:...`), which names exact content.

## The runtime stack

The `docker` CLI talks to the daemon (`dockerd`) over a socket. The daemon manages images, networks and volumes and hands running a container to **containerd**, which calls **runc** to create the namespaces and cgroup and exec the process.

The boundaries are the open OCI image and runtime specs, so [Kubernetes](Kubernetes.md) dropped Docker (the dockershim went in 1.24): the kubelet talks to containerd or CRI-O through its Container Runtime Interface, and Docker-built images still run because they are OCI images.

## Networking

By default a container joins the `docker0` bridge, a virtual switch in the host's network namespace (on Docker Desktop, its Linux VM). Each container gets a virtual Ethernet pair, one end in its net namespace, one in the bridge, plus a private address from its subnet. Outbound traffic is [NATted](../networking/IP%20Addressing.md) to the host's address, so containers reach out but nothing reaches in until a port is published: `-p <host port>:<container port>`, so `-p 8080:5000` forwards host port 8080 to container port 5000.

On a **user-defined** network (`docker network create`) containers resolve each other by name through Docker's embedded DNS at `127.0.0.11`; the default bridge does not. Compose creates one per project, so services in `compose.yaml` reach each other by name.

## Volumes and bind mounts

The writable layer dies with the container; anything that must outlive it goes on a mount. A **bind mount** maps a host path into the mnt namespace: `-v $(pwd)/<app-name>:/app -w /app` puts the current directory at `/app` and starts there. A **volume** is a directory Docker manages under its own storage root, mounted the same way; use it for data nothing on the host needs by path.

## Building images

A Dockerfile adds one layer per instruction that changes the filesystem (`RUN`, `COPY`, `ADD`); `ENV`, `EXPOSE`, `CMD` and the like only change metadata (zero size in `docker history`). Since Docker 23 the default builder is BuildKit, which runs independent stages in parallel and skips steps whose inputs are unchanged. Cache is per layer, so put what changes least (base image, dependencies) first and source last.

A **multi-stage build** keeps the toolchain out of the shipped image: one stage compiles, the last copies only the output into a small runtime image:

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build-env
WORKDIR /app
COPY . .
# The junit logger is the JunitXml.TestLogger package, not built in
RUN dotnet test --logger "junit;LogFilePath=/app/junit.xml"
RUN dotnet publish -c Release -o /app/output

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
# Copying a directory copies its contents
COPY --from=build-env /app/output ./
# File into a directory: keep the trailing slash
COPY --from=build-env /app/junit.xml /app/testresults/
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

`ENTRYPOINT` is the default executable; arguments after the image name on `docker run` go to it.

## Weaker isolation

Every container shares one kernel, so a kernel bug reachable from one is reachable from all, and a process that escapes its namespaces is a process on the host, with no hypervisor in between. Root inside is real root unless the user namespace remaps it.

What closes the gap: run as non-root, or run the daemon rootless so container root is an ordinary host user; drop capabilities and add a seccomp profile to block unneeded syscalls; for untrusted workloads restore a boundary with gVisor (a user-space kernel), Kata Containers (a light VM per container) or Firecracker (microVMs, how AWS Lambda and Fargate isolate tenants). Provenance, scanning and runtime hardening: [Supply Chain and Container Security](../security/Supply%20Chain%20and%20Container%20Security.md).

## Commands

```sh
# host:container; the bind mount is the mnt namespace
docker run -it -p 8080:5000 -v $(pwd)/<app-name>:/app -w /app <image>

# exec joins the container's namespaces; it replaced nsenter for this job
docker exec -it <container> sh

# The namespaces are files on a Linux host
docker inspect -f '{{.State.Pid}}' <container>
sudo ls -l /proc/<pid>/ns

# Without -a: dangling (untagged) images only; with -a: every image no container uses
docker image prune -a

# Export and import an image; the image argument to save is required
docker save -o /tmp/fridge.tar fridge
docker load -i /tmp/fridge.tar

# Compose v2 is a CLI plugin; docker-compose v1 is end of life
docker compose up
```

`docker commit` freezes a changed container as an image; outside experiments it is discouraged, as nothing records how it was made.

## Docker Desktop and Podman

Docker Desktop needs a paid subscription for larger organisations (the engine stays open source); Podman runs the same OCI images with a compatible CLI, no daemon, rootless by default.

## How to rederive this

* A container is a process: what it sees (namespaces), uses (cgroups) and sees on disk (layers).
* One shared kernel: weaker isolation than a VM, faster start-up.
* An image is layers plus metadata, a container adds a writable layer; a tag is a pointer, a digest is content.
* Open specs between CLI, daemon, containerd and runc, so Kubernetes can drop Docker and keep its images.
* Networking is a home router: private bridge, NAT, and a published port is a port forward.

## Sources

* Julia Evans, "What even is a container" (jvns.ca) and the *How Containers Work* zine
* Docker documentation: storage drivers, bridge networking and embedded DNS, pull policy, BuildKit and multi-stage builds
* Open Container Initiative, Image Format Specification and Runtime Specification
* Liz Rice, *Container Security* (O'Reilly, 2020)
* Kubernetes blog, "Dockershim removed from Kubernetes 1.24"
