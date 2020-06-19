# Virtualization

*Take a physical machine and carve it up into multiple virtual machines where each virtual machine looks, feels and tastes just like the physical machine.*

Virtualization allows an unmodified operating system with all its installed software to run in an isolated environment on top of your existing operating system. This environment called a **virtual machine** is created by the virtualization software by intercepting access to certain hardware components and certain features. The physical computer (with an existing operating system) is usually called the **host**, while the isolated environment on top (virtual machine) is often called a **guest**. The isolation between the VM (guest) and the host allows software written for one operating system to run on another (say, Windows software on Linux) without having to reboot.

## Containers

VMs allow multiple applications to run on the same physical machine by having a VM per application but each VM requires a full blown OS. Just running the OS requires CPU, memory and disk space and can incur licensing costs too (RedHat Enterprise Linux isn't free and Windows is definitely not). An OS also needs feeding and caring for like updating, security patching, driver support and antivirus management which incurs an operational cost. Add to this the capex cost of the resources (CPU, memory & disk space) an OS needs while running. An OS therefore attaches a significant overhead to running a VM.

OS's are a necessary evil to run applications. What is important to us is to be able to run applications not an OS to support them. OS's as cool and important as they are, are a necessary evil. If we could run applications directly on the server hardware, we surely would.

In come *Containers* that are more like application runtime environments i.e. applications run inside a container. A container is quite like a VM but light-weight, it is a bare minimum linux machine with minimum packages installed, it uses less CPU, less memory and less disk space. It sits on the already existing OS (Docker host) and only creates an **isolated environment** called *container* in which to run your apps.

Docker uses the resource isolation features of the Linux kernel such as cgroups and kernel namespaces, and a union-capable file system such as aufs and others to allow independent "containers" to run within a single Linux instance, avoiding the overhead of starting and maintaining virtual machines.

**Kernel Namespaces**  isolate the application's view of the operating system and allow each container to have its own:

* Independent process tree
* View of the root file system
* Network stack (own IP address, port range and routing table).
* User accounts

Unlike a traditional VM, containers place only a little extra load on the system, so there is very little overhead. Because of the shared kernel (OS), container isolation is not as good as a full VM’s, but depending upon the nature of your apps it suits many people just fine.

## Docker Commands

Docker always runs based on the latest version of the image if no image version is specified. It downloads the latest image version if the local one is outdated. Therefore it is recommended to specify the image version while running docker.

`docker ps` - List currently running containers.

### Docker run

`docker run -it ubuntu /bin/bash` - Runs an *interactive* container based on 'ubuntu' image. This image is downloaded from *docker hub* - the public docker registry, if it is not present locally. Once the images are downloaded they are stored under `/var/lib/docker/<storage driver>` on the host.

`docker run -it -p 8080:5000 -v $(pwd)/<app-name>:/app -w "/app" <image-name>` - Runs an interactive container, maps port 5000 on host to port 8080 on the container and volume mounts the <app-name> directory to `app` in the container.

`docker run -d ubuntu:10.04 /bin/bash -c "ping 8.8.8.8 -c 30"` - Runs a *detached* container based on the specified (10.04) 'ubuntu' image. In detached mode, the specified command (ping Google's DNS server for 30 sec) is run, the process ends and docker exits. It is a short lived command as compared to interactive mode. Docker container exits as soon as the process running inside it exits, therefore in the above case the container will only exist for 30 sec (duration of the ping).

`docker run --rm -v $(pwd)/StockportWebapp/test:/app/test/ -w "/app/test/StockportWebapp.Tests" microsoft/aspnet:1.0.0-rc1-update1-coreclr sh -c 'dnu restore && dnx test'` - Runs a container that automatically gets removed after it exits. The `sh` process allows you to run multiple commands in the running container.

`docker run -d -p 80:80 <image-name>` - Runs a detached container and maps port 80 on host to port 80 on the container.

`docker run -d -P <image-name>` - Runs a detached container and maps all the ports specified in the Dockerfile to  random high numbered ports on the host.

`docker run --rm --env APP_VERSION=${APP_VERSION} --entrypoint 'make push' ${IMAGE}` - Override the default entry point

### Docker images

`docker images` - Get local images

`docker rm -f $(docker ps -a -q)` - Delete all containers

`docker rmi $(docker images -q)` - Delete all images

`docker rmi -f $(docker images -q -a -f dangling=true)` - Delete all unused images  
or  
`docker images | grep none | awk '{print$3}' | xargs -n 1 docker rmi`

`docker-compose up` - Docker compose is a way to spin up more than one containers, subsequently more than one apps in a single command by configuring a `docker-compose.yml` file.

## Docker debugging

`docker logs -f <container-name>` - Tail logs of PID1 inside a running container

`docker top <container-id>` - Lists the processes running inside the  specified container

`docker attach <container-id>` - Attaches to PID 1 inside the container. This is fine as long as the running process inside the container is a shell, but usually this is not the case.

`nsenter -m -u -n -p -i -t <container-Pid>` - Allows us to enter Namespaces. <container-Pid> can be found by `docker inspect <container-id> | grep Pid`

`docker stop <container-id>` - Stop a given container (Stop sends a SIGTERM signal to the process with PID 1 running inside the container which stops the process, that in turn stops the container. Similarly a `kill` can be sent to the process with PID 1.

## Dockerfile

For each instruction in the Dockerfile, the daemon  spins up a new container, executes the instruction, commits the change to a  new image layer and bins the container.

ENTRYPOINT is a way to specify the default runtime behavior of a container. Anything specified at the end of the docker run command is interpreted as arguments.

## Copying contents

```sh
# For copying dir contents
COPY --from=build-env /app/output /app/testresults # testresults is created if it does not exist

# For copying files
COPY --from=build-env /app/junit.xml /app/testresults/
```

### Create and export a docker image

`docker run fedora /bin/bash -c "echo 'some content' > /tmp/some-content"` - Run container in detached mode

`docker ps -a` - List all the containers that have run in the past on this host

`docker ps -l` Last container that ran on this host

`docker commit <container-id> fridge` - Creates a new image named *fridge*

`docker history fridge` - Shows the history of the the image

`docker save -o /tmp/fridge.tar` - Saves the image as a tar, that can be moved.

`docker load -i /tmp/fridge.tar` - Imports the image from tarball

`Ctrl + P +Q` - Return to the host CLI without stopping the container or detach from a container

## Docker Networking

**docker0 virtual bridge** - Its a virtual ethernet bridge that acts as an interface for all external network traffic and for connecting containers. The bridge is connected into the namespace of Docker host meaning all containers attached to it can communicate with the host and the outside world. Virtual Ethernet interfaces with one end in Docker namespace and the other in Docker host namespace allow external communication. Docker configures container networking so that all container IPs are [NAT**ted](../Networking/IPRouting.md) This means containers can get to the outside world, but the outside world cant necessarily get in. Familiar scenario is [AWS VPC](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Scenario2.html) (Virtual Private Cloud) that uses a NAT gateway and [Routing Tables](http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Route_Tables.html).