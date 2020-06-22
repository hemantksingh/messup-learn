Each user account on a unix machine is associated with a directory called its "home directory" into which the user is automatically placed upon logging in. This acts as a private application data area for the user. Most installations are also done in the user's home directory.

## Arguments
```sh
$* # prints all the arguments passed to a shell script
$# # prints the number of arguments 
```
## Standard in, out, and error
There are three standard sources of input and output for a program. These three file descriptors (you can think of them as “data pipes”) are often called STDIN, STDOUT, and STDERR.

Sometimes they’re not named, they’re numbered! The built-in numberings for them are 0, 1, and 2, in that order.

```sh
2>&1 # Redirects stderr to stdout
1>&2 # Redirects stdout to stderr
```

## Users

[/etc/passwd](https://www.digitalocean.com/community/tutorials/how-to-use-passwd-and-adduser-to-manage-passwords-on-a-linux-vps) File

## Shell

* [Basic Shell Scripting](https://linuxconfig.org/bash-scripting-tutorial)
* [Dev Null](http://askubuntu.com/questions/514748/what-does-dev-null-mean-in-a-shell-script)
* [Positional parameters](http://stackoverflow.com/questions/5163144/what-are-the-special-dollar-sign-shell-variables)
* [I/O Redirection](http://www.tldp.org/LDP/abs/html/io-redirection.html)

## Unix commands
Basic unix commands can be found [here](http://www.cs.jhu.edu/~joanne/unix.html)

Find the linux distribution

```
$ lsb_release

# Not all Debian builds have lsb_release. e.g. even the official Ubuntu Docker image 
# does not have lsb_release. The alternative is to use 

$ cat /etc/os-release
```

Copy individual files to a remote system
```
$ scp local_file(s) user@host:destination_dir

# copy directory
$ scp -r /source_dir deploy@host:/tmp/destination_dir
```

Copy files from remote system
```
$ scp deploy@host:/tmp/filename.file /destination_dir
```

Delete all the files in a directory
```
$ rm -r *.*
```

Change file permissions
```sh

$ chmod 777 <directoryName> # Make a directory writable

Available permissions
First number is for the owner, second for the group, and third for everyone.
7 = Read + Write + Execute
6 = Read + Write
5 = Read + Execute
4 = Read
3 = Write + Execute
2 = Write
1 = Execute
0 = All access denied
```

View all files and folders in a directory (hidden files that begin with a '.' too)  
```
$ ls -al
```

Find
```
$ find . -name banner.jpg # specified file 'banner.jpg' in current dir
$ find ~/Desktop/ -type f -name "*.png" | sort -rn # all 'png' files of regular type (-type f) in specified dir '~/Desktop', sorted by name in reverse order
```

Search
```
$ grep sidebar index.php #  all occurrences of the word 'sidebar' in a specified file 'index.php'.

$ grep '^\.Pp' myfile # all occurrences of the pattern `.Pp' at the beginning of a line
```

Copy current path to clipboard
```
$ pwd|pbcopy
```

## System monitoring

Identify a running process

```sh
ps aux | grep '<process_name>'

top # top resource-consuming processes

htop # processes ordered by the amount of CPU usage
```

Identify currently open ports

```sh
# list all the tcp ports being listened on and the name of each listener’s daemon and its PID
netstat -plunt

# list listening ports
netstat -an | grep LISTEN

# list active tcp connections
netstat -an | grep EST
```

File system

```sh
df
```

Disk usage

```sh
du -H --max-depth=2 # current directory, following symbolic links on the command line not in file hierarchies.
du -h --max-depth=1 /var/lib | sort -rh # disk usage for dir '/var/lib' sorted by size in reverse order in human readable format
```

Logs

```sh
cat filename.txt # print file contents to the screentail # like cat, but only reads the end of the file
tail /var/log/messages # see the last 20 (by default) lines of /var/log/messages
tail -f /var/log/messages # watch the file continuously, while it's being updated
tail -200 /var/log/messages # print the last 200 lines of the file to the screen$ more # like cat, but opens the file one screen at a time rather than all at once
# hit Space to go to the next page, q to quit
```

## Increase storage

1. Add physical storage (usually through a VM manager console)
2. [Resize a Partition using fdisk](https://access.redhat.com/articles/1190213)
3. Reboot
    * `/sbin/shutdown -r now` or
    * `reboot`
    * `shutdown -r +5` Inform all logged in users, system is going down, login prevented for 5 minutes
4. [Grow file system](http://www.tldp.org/HOWTO/LVM-HOWTO/extendlv.html)
    * For XFS file systems `xfs_growfs <partition>` e.g. `xfs_growfs /dev/sda3`

## Vim editor

Write and Quit `:wq`  
Quit without saving `q!`  
Insert (Edit mode) `i`  
Stop diff mode by quitting Vim `qa`

## Windows Subsystem for Linux

There is no linux kernel, sys calls are routed to the windows kernel, but allows linux processes to be run on Windows. e.g. Rails for Unix can be setup in the Windows subsystem

DO NOT modify linux files using Windows apps
