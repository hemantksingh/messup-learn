# Tighten report: fundamentals/platform/Containers.md

File: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Containers.md (edited in place, not committed).

## Word counts (code fences excluded)

* Before: 1,552 (`wc -w` on prose lines)
* After: 1,197 by the same count; about 1,168 once `##` and `*` markup tokens are dropped
* Target 1,100 to 1,200, ceiling 1,400. Landed at the top of the target band; every remaining sentence carries a fact, an owner sentence, a link, a Sources line or a rederive bullet, so going lower would mean dropping facts.

Checks: no em- or en-dashes; no page links to a `Containers.md#` section anchor, so the shortened headings break nothing; four cross-links present (The Unix Model, IP Addressing, Kubernetes, Supply Chain and Container Security); British spelling; Sources unchanged; section order unchanged; five one-line rederive bullets.

## What was cut, by category

* Restatements: intro's "its own process list, network stack and root filesystem" (repeated by the namespace bullets); "A Docker container is these three kernel features combined and given a name" (rederive bullet 1 says it); "Docker is a platform; the runtime underneath is a small program that starts one process"; "Remove the container and the writable layer goes with it" in Images (Volumes opens with the same fact); "A VM has a hypervisor between guest and host; a container has only the kernel's own checks" (folded into "with no hypervisor in between"); "only a process with a restricted view" repeated after the bare-minimum correction; "That is why a container starts in milliseconds... both facts follow from the same design" compressed to one clause.
* Explanatory asides a reader can infer: the OCI spec glosses "(how layers and metadata are packaged)" and "(how a bundle on disk becomes a running process)"; "treats the Dockerfile as a dependency graph"; "so source edited outside is seen inside"; "Two machines running the same tag can be running different images" folded into a clause; "not a crashed VM" after the OOM killer; "which is how" before Lambda and Fargate.
* Connective filler and hedges: "Because both are open, Kubernetes does not need Docker" to "the open OCI ... specs, so Kubernetes dropped Docker"; "That is why you pin" to "Pin"; "today" after overlay2; "which is how" before Lambda and Fargate; "It is worth"-style joins did not exist on this page, so nothing else in this category.
* Second examples and long lists: "working directory" dropped from the image metadata list; the gVisor, Kata and Firecracker glosses cut from clauses to two or three words each; "and cannot move" dropped after "names exact content" to pay for the PID 1 fact below.
* Headings shortened: "A VM virtualises hardware, a container restricts a process" to "VM versus container"; "Isolation is weaker than a VM's" to "Weaker isolation" (the first sentence carries the claim); "Commands that show the model" to "Commands"; "Docker Desktop and alternatives" to "Docker Desktop and Podman".
* Rederive bullets: five kept, each cut to one line, second sentences dropped.
* Dockerfile fence: three comments shortened; the junit-logger correction kept.
* Commands fence: kept run with -p and -v, exec, inspect for the PID (with the `ls /proc/<pid>/ns` line it exists to feed), image prune, save with the image argument, load, compose v2. Dropped `run -it ubuntu bash`, the busybox ping, `ps -a`, `logs`, `stop`, the echo/commit/history fridge steps. Their comments carried command semantics rather than the model (stop is SIGTERM then SIGKILL after the grace period; logs are PID 1's stdout and stderr; ps -a includes exited containers) and go with them. The one model fact in those comments, that the container lives as long as PID 1, moved into the pid namespace bullet ("whose exit ends the container"). The "Docker Desktop lives in a VM" fence comment moved to the Networking parenthetical. One sentence after the fence says `docker commit` is discouraged outside experiments because nothing records how the image was made.
* Docker Desktop and Podman: one sentence.

## Own view block (rule 7)

The pre-tighten block was a paraphrase plus one sentence not in HEAD ("Containers are the closest thing: one kernel, many fenced processes"). Replaced with the owner's three sentences verbatim from `git show HEAD:fundamentals/platform/Containers.md` (OS's are a necessary evil...; What is important to us...; If we could run applications directly on the server hardware...). The non-owner sentence was dropped, since the paragraph above already says one kernel, fenced process. Verified each sentence with grep -F against HEAD.

Owner examples kept as-is: the italic "Take a physical machine and carve it up..." sentence; `-p 8080:5000 -v $(pwd)/<app-name>:/app -w /app`; the junit `COPY --from=build-env /app/junit.xml /app/testresults/`; `fridge.tar` save/load. The corrected port direction (host 8080 to container 5000) is kept; HEAD had it backwards.

## Tempted to cut but kept

* overlay2 whiteout detail ("A delete writes a marker on top that hides the lower file; the bytes stay"): fact.
* "aufs is history": fact and a correction of the old page.
* `docker history` showing metadata instructions at zero size: fact.
* Kubernetes 1.24 dockershim removal and the CRI, containerd, CRI-O names: facts and a correction.
* "publishers need not keep `latest` current": supports the tag correction.
* Docker Desktop runs the engine in a Linux VM: fact, kept as a short parenthetical in Networking.
* The `scratch` image and the `(or process tree)` aside: facts.
* Embedded DNS at `127.0.0.11` and the default bridge not resolving names: facts.
* "for larger organisations" on the Desktop subscription: the threshold is the fact.
* The Lambda and Fargate example for Firecracker: the only concrete anchor for microVMs.
* "Bare minimum Linux machine is wrong": correction of the owner's old wording, kept in quotes.
