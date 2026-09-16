# Phase 3 report: fundamentals/computing/The Unix Model.md

File edited: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/computing/The Unix Model.md (not committed). 1,713 words total, 1,312 of prose outside tables and code fences. One H1 matching the filename, sections at H2, three code fences all tagged (`text`, `sh`, `sh`), no em or en dashes, British spelling, no frontmatter. Cross-links to `../networking/Local%20IPC.md` and `../platform/Containers.md` both resolve.

## (a) Question the page answers

What is the mental model behind Unix that makes the command line make sense? Answered in the first paragraph with the owner's five sentences (everything is a file, everything running is a process, every file is text or data, each command does one thing well, pipelines allow composition), then derived section by section: files, processes, permissions, the shell as glue, filesystem layout, text as interface, how to rederive.

## (b) Kept from the original

- Opening sentence "Unix is based on a really simple model" and the five-bullet model, now as sentences.
- `/etc/passwd` and `/etc/shadow` as the first "everything is a file" example.
- "Files are files, devices are files, processes are files" preserved as the bullet structure; the two garbled lines corrected (see d).
- The home directory as the user's private area (corrected: not where installations go).
- stdin/stdout/stderr as 0, 1, 2; `2>&1` and `1>&2` idea, now with the full redirection block.
- The permission digit table (7 down to 0), moved out of the shell fence into a markdown table.
- The owner's pipelines: `du -h --max-depth=1 /var/lib | sort -rh`, `find ~/Desktop -type f -name "*.png" | sort`, `ps aux | grep`, `tail -f`, `pwd | pbcopy`, all with corrected flags or platform labels.
- `rm` "delete all files" and `xfs_growfs`, as corrected one-liners in "habits worth unlearning".
- `ls -al` idea is implicit in the `ls -l` sample output used to derive the octal digits.

## (c) Dropped and why

- The link list (linuxconfig, askubuntu, tldp, JHU command list, stackoverflow positional parameters): bookmarks, not knowledge; the concepts they pointed at (dev null, redirection, arguments) are now explained inline or out of scope.
- `$*` and `$#` positional parameters: scripting detail, not model.
- Distro identification (`lsb_release`, `/etc/os-release`, `hostnamectl`, `uname -r`): a procedure, not part of the model. Candidate for a Linux runbook page if the owner wants one.
- `scp` examples: tool usage, not model.
- `top`, `htop`, `df`, `more` and the `netstat` block: catalogue. `ss` replaces `netstat` in the pipelines section.
- The "Increase storage" runbook (fdisk, reboot, shutdown variants, LVM link): a procedure with a wrong command; only the corrected `xfs_growfs /mount/point` survives as a one-liner.
- Vim section: dropped as the brief permitted; noted in this report only, not in the page. The audit already proposes an Editors page.
- From the Mac sheet: keyboard shortcuts, Oh My Zsh, xcode-select, Boot Camp drivers. Only the shell start-up file concept was folded in, as the brief asked.

## (d) Added, with sources for non-obvious claims

- File descriptors as small integers indexing the process's open-file table (corrects "file handlers are files"). Kernighan and Pike ch. 7; any open(2) man page.
- System V `shmget` had no filesystem name; POSIX `shm_open` objects appear under `/dev/shm` on Linux (corrects the garbled shared memory line). shm_overview(7) man page.
- `/proc/<pid>/` on Linux; macOS has no `/proc`. proc(5) man page; macOS has never shipped procfs.
- fork and exec, and that the shell forks, rearranges descriptors, then execs, which is what makes redirection possible. Kernighan and Pike ch. 7; Raymond ch. 7.
- Exit code 0 is success, `$?`. Kernighan and Pike ch. 3.
- SIGTERM can be caught, SIGKILL cannot be caught, blocked or ignored; Ctrl-C becomes SIGINT for the foreground process group via the terminal driver. signal(7) and termios(3) man pages.
- `docker stop` sends SIGTERM to PID 1 in the container: taken from the existing Containers page.
- Octal digits derived from 4+2+1 with a worked `rwxr-xr--` = 754 example; directory semantics of r, w, x; `/tmp` is 1777 with the sticky bit. chmod(1) and sticky(8)/FHS.
- Why `chmod 777` is wrong and the `u+w` / group plus `g+w` or `775` alternative. Standard security practice; marked as derived reasoning, not opinion.
- setuid explained through `passwd` writing `/etc/shadow`. Kernighan and Pike ch. 2; passwd(1).
- Redirection block including the `> file 2>&1` versus `2>&1 > file` ordering trap. bash manual, "Redirections" (processed left to right).
- `&&` and `||` on exit status. bash manual, "Lists".
- `$PATH` search order after aliases, functions and builtins; `.` not on PATH hence `./script`. bash manual, "Command Search and Execution".
- Shell variables versus environment; `export`; why `cd` is a builtin and why `source` is needed. bash manual, "Environment" and "Shell Builtin Commands".
- Start-up file table for bash and zsh. bash manual "Bash Startup Files"; zsh manual "Startup/Shutdown Files".
- macOS default zsh since 10.15 (2019) so `.bash_profile` is never read; PATH edits in `~/.zprofile` (login) or `~/.zshrc` (interactive); Terminal and iTerm2 open login shells. Apple support article "Use zsh as the default shell on your Mac"; the audit finding for Mac.md L16-29.
- FHS table for /bin /usr /usr/local /opt /etc /var /home /tmp /dev /proc /sys; note that /bin and /sbin are often symlinks into /usr (usrmerge on Debian, Fedora, Ubuntu, Arch). FHS 3.0.
- Corrects "most installations are in the home directory": system packages under /usr and /opt, per-user tools (pip --user, nvm, rustup) under $HOME. FHS 3.0.
- macOS adds /Users, /Applications, /Library. Apple File System Programming Guide.
- McIlroy's "do one thing well, work together" via Raymond ch. 1.
- Pipeline corrections: `tail` default 10 lines (tail(1)); `sort -r` not `-rn` for names; `ss -tlnp` since net-tools is deprecated on Linux; `journalctl -fu <unit>`; `grep '[n]ginx'` bracket trick; `du -h -d 1` as the portable form; `pbcopy` labelled macOS, `xclip -selection clipboard` for Linux X11.
- `rm -r *.*` does not delete dotfiles or extension-less names; `rm -rf ./*` or `find . -mindepth 1 -delete`, with a warning. Shell globbing rules.
- `xfs_growfs` takes a mount point. xfs_growfs(8).

No `> Own view:` blocks were needed; every stance in the page is derived or sourced.

## (e) Diagrams for Phase 5

1. Three descriptors 0, 1, 2 of two processes, with a pipe joining descriptor 1 of the first to descriptor 0 of the second, and stderr of both still pointing at the terminal. Would sit in "The shell as glue".
2. Fork then exec: the shell as parent, the forked child rearranging its descriptors (opening a file onto descriptor 1), then exec replacing the program image while the descriptor table survives. Would sit in "Processes".
3. Optional: the permission string `rwxr-xr--` split into three triples with weights 4, 2, 1 under each bit summing to 7 5 4. Could replace the `text` fence if a picture reads better.

No existing images were embedded in the old page, so nothing was removed.

## (f) Open questions for the owner

1. Oh My Zsh: the audit's cross-file note suggested folding the zsh / Oh My Zsh section from Mac.md and Ubuntu.md into this page. The brief's outline did not include it, so it is out. Does the owner want a short "Shell setup" page or a section here?
2. Vim: dropped from this page. Does the owner want an Editors page (Vim, VS, VS Code shortcuts with the platform stated), as the audit proposed, or is Vim survival not worth a page?
3. The distro identification and storage-growth runbooks were procedures with value to the owner in 2021. If still used, they belong in a Linux operations runbook page, not here. Wanted?
4. The page treats `/proc`, `/dev/shm` and the FHS table as Linux and labels them so, with one sentence on macOS layout. Is that the right depth for the owner, who works on macOS but deploys to Linux?
5. `/var/log/syslog` versus `/var/log/messages`: the page uses the Debian/Ubuntu path plus `journalctl`. If the owner's servers are RHEL-family, swap the example.
