# Interprocess communication

Windows and Unix-variant operating systems provide different approaches to inter process communication (IPC) that facilitate communications and data sharing between applications. [This](http://cs.brown.edu/people/slewando/files/IPCWinNTUNIX.pdf) paper discusses some of the IPC options that are available to programmers using UNIX and describe the corresponding techniques available to programmers writing for Windows.

* Pipes
* Sockets
* Shared memory
* Mailslots

Apart from the ones listed above [Windows provides a few additional IPC options](https://docs.microsoft.com/en-us/windows/win32/ipc/interprocess-communications#using-pipes-for-ipc)

* Clipboard
* COM
* Data Copy
* DDE
* File Mapping

## Sockets

A [UNIX socket](https://en.wikipedia.org/wiki/Unix_domain_socket), or Unix Domain Socket, is an inter-process communication mechanism that allows bidirectional data exchange between processes running on the same machine.

[IP sockets](https://en.wikipedia.org/wiki/Network_socket) (especially TCP/IP sockets) are a mechanism allowing communication between processes over the network. In some cases, you can use TCP/IP sockets to talk with processes running on the same computer (by using the loopback interface).

UNIX domain sockets know that they’re executing on the same system, so they can avoid some checks and operations (like routing); which makes them faster and lighter than IP sockets. So if you plan to communicate with processes on the same host, this is a better option than IP sockets.

UNIX domain sockets are subject to file system permissions, while TCP sockets can be controlled only on the packet filter level.

## Pipes

https://docs.microsoft.com/en-us/windows/win32/ipc/interprocess-communications#using-pipes-for-ipc

Anonymous pipes - one way, only for local communication, not over a network. Useful for communication between threads or parent and child processes.

Named pipes - support multiple clients talking to a server on the same machine or over a network. Can be one way or duplex

### Secure pipes

* Weakly ACL'd named pipes can be written to by low privilege processes
* Named pipes allow impersonation - ability of connected clients to use their oen permissions on remote servers. High privilege attacks can impersonate the caller and find information disclosed from the pipe.

You can define ACLs for a named pipe [using security descriptors](https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights). The ACLs in the default security descriptor for a named pipe grant full control to the LocalSystem account, administrators, and the creator owner. They also grant read access to members of the Everyone group and the anonymous account.

So in essence a pipe with a default security descriptor can only be accessed by the LocalSystem account.

## gRPC

gRPC calls between a client and service are usually sent over TCP sockets. TCP was designed for communicating across a network. Inter-process communication (IPC) is more efficient than TCP when the client and service are on the same machine. This document explains how to use gRPC with custom transports in IPC scenarios.

https://docs.microsoft.com/en-us/aspnet/core/grpc/interprocess?view=aspnetcore-5.0