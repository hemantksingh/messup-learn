# Tighten report: fundamentals/computing/The Unix Model.md

File: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/computing/The Unix Model.md (not committed)

## Word count (code fences excluded)

* Before: 1,506
* After: 1,094 (target 1,000 to 1,100; ceiling 1,300)

Fixed material that could not shrink: three tables 194 words, Sources 74, headings 37. Body prose went from about 1,200 to about 790.

## Checks

* Code fences: byte-identical to the pre-tighten version (all corrected commands and the owner's pipelines intact: `du ... | sort -rh`, `find ... | sort -r`, `ps aux | grep '[n]ginx'`, `ss -tlnp`, `tail -f`, `pwd | pbcopy`, redirection block including the ordering trap).
* Tables: FHS, permission digits, start-up files all byte-identical.
* Headings: same nine, same order, unchanged.
* Links: Local IPC and Containers both kept.
* No em/en dashes. British spelling. No "> Own view:" block exists (none in before either).
* Backtick spans dropped: `kill <pid>` (now "the `kill` default", same fact), `rm` (the aside "so you can `ls` and `rm` them" about /dev/shm), `read`/`write` in the descriptor bullet (now "the small integers `open` returns"), and `pip install --user` from the per-user tools list (nvm, rustup kept as the examples).
* Product lists trimmed under rule 3: "Terminal and iTerm2" -> "macOS terminals"; three per-user tool examples -> two.

## What was cut, by category

Restatement of the previous sentence
* "Hold those five sentences and the command line stops being a list of incantations. This page derives the rules, then shows the shell as the glue between them." (intro throat-clearing)
* "The kernel hides what sits behind that interface, so the same calls work on very different things."
* "Because output is text on descriptor 1 and input is text on descriptor 0, any tool can feed any other, so each tool only has to do one thing" cut to "Text out on 1 feeds text in on 0, so any tool feeds any other" (the section's thesis, kept in short form).
* "The exit code drives control flow" lead-in; the `&&` / `||` sentence stands alone.
* "By default all three point at your terminal" folded into the descriptor sentence.

Explanatory asides a reader can infer
* fork/exec mechanics cut to two sentences (clone with new PID; replace program keeping PID and descriptors; shell forks, child rearranges, execs).
* Signals cut to one line each; dropped "so a server can close its files first", "the kernel simply removes the process", "Ctrl-C is not a key the program sees" (kept as "the program never sees the key").
* "They index the process's own table of open files" (file descriptors).
* "so you can `ls` and `rm` them" (/dev/shm).
* "Read the string in threes: `rwx` for the owner, `r-x` for the group, `r--` for others" and the 4+2+1 arithmetic; the digit table already shows it.
* "the block of strings a child inherits across fork and exec" -> "which children inherit".
* "so it runs once per window" (zprofile).
* "(still skips dotfiles)" kept as "(also skips dotfiles)"; "has no confirmation and no undo" -> "has no undo".
* "put them in a group" before `chown :group`.

Connective filler and lecture voice
* "When you type `ls`" -> "For `ls`"; "which is why ... and why" -> "so"; "Everything running is a process with a PID" -> "Every process has a PID"; "A process ends with an exit code" -> "Exit code 0 is success".
* "Signals are how the kernel interrupts a process" -> "Signals interrupt a process".
* "Pipes, sockets and shared memory as ways for processes to talk are in" -> "Pipes, sockets, shared memory:".

Hedges and padding adjectives
* "crucially" (exec keeps descriptors); "really" kept only in the owner's own opening sentence.
* "it is the usual reflex ... and it is the wrong one" -> "is the reflex ... and it is wrong".
* "A group of people or services" -> "A group".

Second examples / long lists
* Directory bits sentence shortened to "`r` lists names, `x` enters, `w` creates, renames or deletes entries".
* "How to rederive this" cut from 110 words to 61, five one-line bullets.

## Tempted to cut but kept (facts, corrections or owner sentences)

* The owner's opening six sentences, verbatim ("Unix is based on a really simple model. Everything is a file. ...").
* "Files are files" (owner's bullet wording) and the `/etc/passwd` field list; `/etc/shadow` unreadable by ordinary users (correction).
* "File descriptors are handles, not files" (corrects the owner's "File handlers are files").
* Shared memory System V vs POSIX, `/dev/shm` (corrects "Shared memory wasn't files but it is now").
* PID 1 has parent 0; `docker stop` sends SIGTERM to PID 1; daemon has no terminal.
* Sticky bit on `/tmp` (`1777`); setuid `passwd` example; `sudo` logs.
* macOS zsh since 10.15 (2019), macOS terminals open login shells so PATH goes in ~/.zprofile, Linux desktops non-login (the gotcha).
* "The home directory is ... not where software is installed" (reverses the owner's original claim that most installs go in $HOME).
* macOS adds `/Users`, `/Applications`, `/Library`.
* `netstat` deprecated, `tail` default 10, `sort -r` not `-rn`, `xfs_growfs` takes the mount point, `rm -r *.*` skips dotfiles: all in fences or the "Two habits" paragraph, untouched or trimmed only of connectives.
* Every Sources line, verbatim.
