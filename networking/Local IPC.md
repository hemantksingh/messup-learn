# Local IPC

Windows and Unix-variant operating systems provide different approaches to inter process communication (IPC) that facilitate communications and data sharing between applications. [This](http://cs.brown.edu/people/slewando/files/IPCWinNTUNIX.pdf) paper discusses some of the IPC options that are available to programmers using UNIX and describe the corresponding techniques available to programmers writing for Windows.

* Pipes
* Sockets
* Shared memory -e.g. [memory mapped files](https://docs.microsoft.com/en-us/dotnet/standard/io/memory-mapped-files) contain the contents of a file in virtual memory that enables a process to treat the contents of a file as if they were a block of memory in the process's address space.
* Mailslots

Apart from the ones listed above [Windows provides a few additional IPC options](https://docs.microsoft.com/en-us/windows/win32/ipc/interprocess-communications#using-pipes-for-ipc)

* Clipboard
* COM
* Data Copy
* DDE

## Sockets

Taken from [difference between Unix socket and TCP/IP socket](https://stackoverflow.com/questions/46151707/is-there-a-difference-between-tcp-and-unix-socket)

A [UNIX socket](https://en.wikipedia.org/wiki/Unix_domain_socket), or Unix Domain Socket, is an inter-process communication mechanism that allows bidirectional data exchange between processes running on the same machine.

[IP sockets](https://en.wikipedia.org/wiki/Network_socket) (especially TCP/IP sockets) are a mechanism allowing communication between processes over the network. In some cases, you can use TCP/IP sockets to talk with processes running on the same computer (by using TCP loopback address: 127.0.0.1).

UNIX domain sockets know that they’re executing on the same system, so they can avoid some checks and operations (like routing); which, as the StackOverflow answer above puts it, usually makes them **faster and lighter than IP sockets**. So if you plan to communicate with processes on the same host, this is usually the better option, though loopback TCP is portable and fine for many applications.

UNIX domain sockets are subject to file system permissions, while TCP sockets can be controlled only on the packet filter level.

## Pipes

https://docs.microsoft.com/en-us/windows/win32/ipc/interprocess-communications#using-pipes-for-ipc

Anonymous pipes - one way, only for local communication, not over a network. Useful for communication between threads or parent and child processes.

Named pipes - support multiple clients talking to a server on the same machine or over a network. Can be one way or duplex

### Secure pipes

* Weakly ACL'd named pipes can be written to by low privilege processes
* Named pipes allow impersonation - the pipe server thread can adopt the security context of the connected client (`ImpersonateNamedPipeClient`). The classic attack is a low privilege process creating a pipe with a predictable name so that a high privilege client connects to it and is impersonated. Clients can limit this by connecting with the `SECURITY_IDENTIFICATION` or `SECURITY_ANONYMOUS` impersonation level. Servers should create pipes with `FILE_FLAG_FIRST_PIPE_INSTANCE` so that creation fails if a pipe with that name already exists.

You can define ACLs for a named pipe [using security descriptors](https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights). The ACLs in the default security descriptor for a named pipe grant full control to the LocalSystem account, administrators, and the creator owner. They also grant read access to members of the Everyone group and the anonymous account.

So with the default security descriptor any local user can read from the pipe, and only LocalSystem, Administrators and the creating owner have full control. Supply an explicit security descriptor when creating the pipe if that is too permissive.

## gRPC

gRPC calls between a client and service are usually sent over TCP sockets. TCP was designed for communicating across a network. Inter-process communication (IPC) is more efficient than TCP when the client and service are on the same machine. Consider using a transport like Unix domain sockets (UDS) or named pipes for gRPC calls between processes on the same machine. 

UDS are supported on Linux, macOS and modern versions of Windows. Support for the unix socket has existed both in BSD and Linux for the longest time, but, not on Windows. On Windows, there were some alternatives for local IPC, such as named pipes. But, calling conventions are different between the named pipes and sockets, making writing low-maintenance cross-platform applications difficult. [Windows 10 build 17063 provides support for unix socket](https://devblogs.microsoft.com/commandline/af_unix-comes-to-windows/) (AF_UNIX) address family on Windows to communicate between Win32 processes.

* How to do [IPC with gRPC on UDS](https://learn.microsoft.com/aspnet/core/grpc/interprocess)
* .NET 8 and later support gRPC over Windows named pipes as well as Unix domain sockets.

For gRPC as an API style rather than as a transport, see the [gRPC section of API Styles](../web%20and%20apis/API%20Styles.md#grpc).
