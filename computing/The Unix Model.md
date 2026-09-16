---
title: "The Unix Model"
summary: "Everything is a file, everything running is a process, and the shell glues them together with pipes and redirection."
kind: concept
status: current
last_reviewed: 2026-09-16
sources:
  - "Kernighan and Pike, The UNIX Programming Environment (1984), ch. 1 to 3"
  - "Raymond, The Art of Unix Programming (2003), ch. 1"
  - "Filesystem Hierarchy Standard 3.0, Linux Foundation"
  - "bash manual, Bash Startup Files; zsh manual, Startup/Shutdown Files"
  - "Apple support, Use zsh as the default shell on your Mac"
tags: [unix, shell, processes, file-permissions, pipes]
---
# The Unix Model

Unix is based on a really simple model. Everything is a file. Everything running is a process. Every file is text or data. Each command does one thing well. Pipelines allow composition.

## Everything is a file

A file is anything you can `open`, `read`, `write` and `close`.

* Files are files. `/etc/passwd` holds the account list (name, user id, home directory, shell); `/etc/shadow` holds the hashed passwords, unreadable by ordinary users.
* Devices are files: `/dev/tty` a terminal, `/dev/sda` a disk, `/dev/null` discards writes.
* Processes are files: Linux exposes each under `/proc/<pid>/` (`cmdline`, `environ`, `fd/`). macOS has no `/proc`; use `ps` and `lsof`.
* Shared memory was the exception. System V (`shmget`) had no filesystem name; POSIX (`shm_open`) does, under `/dev/shm` on Linux.
* File descriptors are handles, not files: the small integers `open` returns.

Pipes, sockets, shared memory: [Local IPC](../networking/Local%20IPC.md).

## Processes

Every process has a PID and a parent PID; all descend from PID 1 (`init` or `systemd`), whose parent is 0. `fork` clones the process into a child with a new PID; `exec` replaces the program, keeping the PID and open descriptors. The shell forks, the child rearranges its descriptors, then execs: that is redirection.

Exit code 0 is success, anything else failure; the shell keeps the last in `$?`.

Signals interrupt a process.

* `SIGTERM` (the `kill` default) asks a process to stop; it can be caught.
* `SIGKILL` (`kill -9`) cannot be caught, blocked or ignored.
* `SIGINT`: the terminal driver sends it to the foreground process group on Ctrl-C; the program never sees the key.

A daemon has no terminal, so closing yours does not signal it. `docker stop` sends `SIGTERM` to PID 1 in the container ([Containers](../platform/Containers.md)).

## Users and permissions

Every file has an owner, a group and three permission sets (owner, group, others) of three bits: read, write, execute.

```text
-rwxr-xr--  1 alice staff  512 Sep 16 09:00 deploy.sh
```

Weight the bits 4, 2, 1: `rwx` = 7, `r-x` = 5, `r--` = 4, so this file is `754`.

| Digit | Bits | Meaning |
|---|---|---|
| 7 | rwx | read, write, execute |
| 6 | rw- | read, write |
| 5 | r-x | read, execute |
| 4 | r-- | read |
| 3 | -wx | write, execute |
| 2 | -w- | write |
| 1 | --x | execute |
| 0 | --- | none |

On a directory `r` lists names, `x` enters, `w` creates, renames or deletes entries.

`chmod 777` is the reflex for "make it writable" and it is wrong: every account can now write. Ask "writable by whom?" You: `chmod u+w file`. A group: `chown :group file` then `chmod g+w file` (or `775`). `/tmp` is world-writable by design but has the sticky bit (`1777`), so you only delete your own files.

A setuid binary runs as its owner, not the caller, so `passwd` can write `/etc/shadow`. `sudo` runs one command as another user (root by default) and logs it.

## The shell as glue

Every process starts with descriptors 0 (stdin), 1 (stdout), 2 (stderr) on your terminal. Redirection and pipes repoint them before the program runs, so it never knows.

```sh
cmd > out.txt        # descriptor 1 to a file, truncated
cmd >> out.txt       # same, appending
cmd 2> err.txt       # descriptor 2 to a file
cmd > all.txt 2>&1   # 2 becomes a copy of 1, so both go to the file
cmd 2>&1 > all.txt   # wrong order: 2 copies the terminal, then 1 moves
cmd 2> /dev/null     # discard errors
cmd1 | cmd2          # descriptor 1 of cmd1 joined to descriptor 0 of cmd2
```

`a && b` runs `b` only if `a` returned 0; `a || b` only if `a` failed.

For `ls` the shell checks aliases, functions and builtins, then walks `$PATH` left to right; first match wins. The current directory is not on `$PATH`, so a local script is `./script.sh`.

`export NAME=value` copies a shell variable into the environment, which children inherit. A child cannot change its parent's variables, so `cd` must be a builtin and a script cannot set yours unless you `source` it. `echo $PATH | tr ':' '\n'` prints it one entry per line.

Start-up files depend on the shell and whether it is a login shell.

| Shell | Login shell reads | Interactive non-login shell reads |
|---|---|---|
| bash | `~/.bash_profile` (else `~/.profile`) | `~/.bashrc` |
| zsh | `~/.zprofile` | `~/.zshrc` |

macOS has defaulted to zsh since 10.15 (2019), so `~/.bash_profile` is never read unless you switched back. `PATH` edits go in `~/.zprofile` (macOS terminals open login shells) or `~/.zshrc` (every interactive shell). Most Linux desktops open a non-login shell, so `~/.bashrc` runs.

## Where things live

The Filesystem Hierarchy Standard fixes the Linux layout.

| Path | What goes there |
|---|---|
| `/bin`, `/sbin` | Essential commands; often symlinks into `/usr` now |
| `/usr` | Programs and libraries owned by the package manager |
| `/usr/local`, `/opt` | Software installed outside the package manager |
| `/etc` | System-wide configuration, plain text |
| `/var` | Data that changes while running: logs, spool, databases, caches |
| `/home/<user>` | One user's files and dotfiles (`~`) |
| `/tmp` | Scratch, may be wiped at boot |
| `/dev`, `/proc`, `/sys` | Kernel-provided views of devices and processes |

The home directory is the user's private area, not where software is installed. Packages go under `/usr` and `/opt`; only per-user tools (nvm, rustup) live under `$HOME`. macOS keeps this tree plus `/Users`, `/Applications` and `/Library`.

## Text as the universal interface

Text out on 1 feeds text in on 0, so any tool feeds any other. McIlroy, quoted by Raymond: write programs that do one thing and do it well, and write programs to work together.

```sh
# disk use under /var/lib, largest first (GNU du; macOS: du -h -d 1)
du -h --max-depth=1 /var/lib | sort -rh | head

# all png files under a directory, reverse name order
find ~/Desktop -type f -name '*.png' | sort -r

# is nginx running? the brackets stop grep matching itself
ps aux | grep '[n]ginx'

# who is listening on which port (Linux; netstat is deprecated)
ss -tlnp

# follow a log; tail shows the last 10 lines by default
tail -f /var/log/syslog
journalctl -fu nginx             # systemd journal for one unit

# copy the current path to the clipboard
pwd | pbcopy                     # macOS
pwd | xclip -selection clipboard # Linux with X11
```

Two habits to unlearn. `rm -r *.*` does not delete everything: `*.*` only matches names with a dot, so dotfiles survive. Use `rm -rf ./*` (also skips dotfiles) or `find . -mindepth 1 -delete`, and check `pwd` first; `-rf` has no undo. Growing an XFS filesystem is `xfs_growfs /mount/point`, not the device.

## How to rederive this

* "Everything is a file" means one interface: open, read, write, close.
* Redirecting without the program knowing forces fork, rearrange descriptors, exec.
* Every redirection is "point descriptor N at X", left to right.
* Weight the bits 4, 2, 1, ask "writable by whom?", and 777 is never the answer.
* A child inherits environment and descriptors, not variables; hence `export` and `source`.

## Sources

* Kernighan and Pike, The UNIX Programming Environment (1984), ch. 1 to 3 on files, the shell and filters.
* Raymond, The Art of Unix Programming (2003), ch. 1, for the McIlroy quotation and the design rules.
* Filesystem Hierarchy Standard 3.0, Linux Foundation.
* bash manual, "Bash Startup Files"; zsh manual, "Startup/Shutdown Files".
* Apple support, "Use zsh as the default shell on your Mac": zsh is the default since macOS Catalina 10.15.
