# Phase 3 report: fundamentals/platform/Containers.md

File: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/platform/Containers.md (not committed). About 1,850 words including code fences, about 1,550 words of prose; the target was 1,100 to 1,400 and the ceiling 1,870. H1 "Containers", twelve H2s, two fences (`dockerfile`, `sh`), no dashes, no frontmatter, no images.

## (a) The question the page now answers

What is a container, really, and why is it not a small virtual machine? Answered in the first paragraph: a container is an ordinary process on the host kernel with a restricted view (namespaces), a metered share (cgroups) and a layered root filesystem; no second kernel, so fast start-up and weaker isolation follow from the same fact.

## (b) Kept from the original

- The italic VM tagline ("Take a physical machine and carve it up...") and the host/guest vocabulary.
- The "OS is a necessary evil" thought, now a `> Own view:` blockquote.
- The four-bullet namespace list (process tree, root filesystem, network stack, user accounts), expanded to the six named namespaces.
- The `-p 8080:5000 -v $(pwd)/<app-name>:/app -w /app` example, direction corrected, reused as the bind-mount example and in the commands block.
- The detached ping example, now `docker run -d busybox ping -c 30 8.8.8.8` (the official `ubuntu` image does not ship `iputils-ping`, so the owner's Ubuntu version would exit at once with "command not found"), and "the container exits" instead of "docker exits".
- The fridge sequence: `run`, `commit`, `history`, `save -o /tmp/fridge.tar fridge` (image argument added), `load`. The base image is `ubuntu:24.04` instead of untagged `fedora`, so the example follows the page's own advice to pin tags.
- Both `COPY --from=build-env` lines with the owner's comments (directory contents; trailing slash for a file), now inside a `dockerfile` fence within a full multi-stage example on `mcr.microsoft.com/dotnet/sdk:8.0` and `aspnet:8.0`. The runtime stage has `WORKDIR /app` and copies the publish output to `./` so the ENTRYPOINT resolves; the `junit` logger carries a comment that it needs the `JunitXml.TestLogger` package.
- The ENTRYPOINT sentence (default executable; trailing `docker run` arguments are passed to it).
- `docker logs -f` as stdout/stderr of PID 1; `docker stop` as SIGTERM to PID 1.
- The docker0 bridge, veth pair and NAT description, rewritten; the NAT link to IP Addressing kept (stray `**` in the link text removed).
- "Container isolation is not as good as a full VM's" kept as its own section, with the reason.

## (c) Dropped and why

- "bare minimum linux machine" (WRONG per audit L13): replaced by the process-with-a-restricted-view statement; the page now says explicitly why the old phrasing is wrong.
- "aufs" as the example driver (STALE L15): overlay2, aufs named only as history.
- "Docker always runs the latest version... downloads if outdated" (WRONG L28): replaced by the tag/`latest`/pull-policy paragraph.
- `microsoft/aspnet:1.0.0-rc1 ... dnu restore && dnx test` (WRONG L40): dead toolchain; the .NET example survives only as the multi-stage Dockerfile.
- `--entrypoint 'make push'` (WRONG L46): dropped rather than fixed; it did not demonstrate anything about the model.
- `rmi -f $(docker images -q -a -f dangling=true)` "all unused images" (WRONG L56) and the `grep none | awk | xargs rmi` one-liner: replaced by `docker image prune -a` with a correct comment.
- `docker-compose up` / `docker-compose.yml` (STALE L60): `docker compose up`, `compose.yaml`, v1 noted as end of life.
- `nsenter -m -u -n -p -i -t` (STALE L70): `docker exec -it` is primary; the namespace idea is shown instead via `docker inspect -f '{{.State.Pid}}'` and `ls -l /proc/<pid>/ns`.
- "daemon spins up a new container per instruction, commits, bins it" (STALE L76): replaced by layers-per-filesystem-instruction plus BuildKit.
- `docker run fedora ...` described as detached without `-d` (WRONG L92): kept in the fridge sequence without the "detached" claim.
- Cheat-sheet commands with no model to show (audit CLASSIFY L26-107): `docker images`, `rm -f $(docker ps -a -q)`, `rmi $(docker images -q)`, `-P`, `docker top`, `docker attach`, `Ctrl+P+Q`, `docker ps -l`, the `/var/lib/docker/<driver>` path.
- The paragraph on OS licensing and opex costs of VMs: compressed into one sentence plus the Own view quote.

## (d) Added, with sources

- Six namespaces (pid, net, mnt, uts, ipc, user) and what each hides: Linux `namespaces(7)`; Julia Evans, "What even is a container".
- cgroups meter CPU, memory, I/O, pids; memory limit ends in the OOM killer: Linux `cgroups(7)`; Liz Rice, Container Security ch. 3.
- overlay2 semantics (read falls through, write to upper layer, whiteout marker on delete): Docker docs, "OverlayFS storage driver".
- Image = layers + config; container = image + writable layer + namespaces/cgroup; layers shared between containers: Docker docs, "Storage drivers"; OCI Image Format Specification.
- `docker run` pull policy `missing`, `--pull always`, digest pinning `image@sha256:...`: Docker CLI reference for `docker run --pull`.
- CLI, dockerd, containerd, runc chain; OCI image and runtime specs; Kubernetes uses containerd or CRI-O via CRI; dockershim removed in Kubernetes 1.24 (version fact that changes the concept, so stated): OCI specs; Kubernetes blog "Dockershim removed from Kubernetes 1.24" (May 2022). Consistent with the parallel Kubernetes rewrite, which says the same and links back to this page.
- Embedded DNS at 127.0.0.11 on user-defined networks only; default bridge has no name resolution; Compose creates a per-project network: Docker docs, "Bridge network driver" and "Networking in Compose".
- Bind mount vs volume: Docker docs, "Volumes" and "Bind mounts".
- Only filesystem-changing instructions produce layers; metadata instructions show as zero size in `docker history`: Docker docs, "Dockerfile reference" and "Build cache".
- BuildKit default since Docker 23.0 (February 2023), graph execution, parallel stages, per-step caching: Docker 23.0 release notes; Docker docs "BuildKit".
- Isolation: shared kernel, root-is-root unless user namespace remaps, rootless mode, capabilities and seccomp, gVisor (user-space kernel), Kata Containers (VM per container), Firecracker (microVMs behind Lambda and Fargate): Liz Rice, Container Security ch. 8 and 9; gVisor, Kata and Firecracker project documentation.
- `docker stop` sends SIGTERM to PID 1, SIGKILL after the grace period: Docker CLI reference for `docker stop`. Cross-links The Unix Model, which now says the same.
- `/proc/<pid>/ns` shows a container's namespaces from the host, qualified "on a Linux host; under Docker Desktop they live inside its VM" (same qualifier on `docker0`), since the owner works on macOS: `namespaces(7)`; Julia Evans; Docker Desktop architecture docs.
- `busybox` image ships `ping`; the official `ubuntu` image does not: Docker Hub official image pages for busybox and ubuntu.
- Docker Desktop paid subscription for larger organisations (threshold deliberately left out, link to Docker's terms); Podman daemonless, rootless by default, CLI-compatible: Docker subscription service agreement (effective 31 Aug 2021); podman.io.
- Cross-links added: Kubernetes.md, ../computing/The%20Unix%20Model.md, ../networking/IP%20Addressing.md (Network Address Translation section exists), ../security/Supply%20Chain%20and%20Container%20Security.md. All four targets exist.

## (e) Diagrams for Phase 5

The old page had no images. Three diagrams would earn their place, in this order:

1. `vm-vs-container.drawio.svg`: side by side. Left: hardware, host OS/hypervisor, then per-VM guest kernel plus app. Right: hardware, one host kernel, then containers as processes each wrapped in namespaces + cgroup, with a shared kernel bar under all of them. Label the kernel as the trust boundary difference.
2. `image-layers-overlay2.drawio.svg`: read-only image layers stacked (base, dependencies, app), one thin writable container layer on top, arrows showing a read falling through and a write landing on top; two containers sharing the same lower layers.
3. `container-runtime-stack.drawio.svg`: docker CLI to dockerd to containerd to runc to process, with the OCI image spec and runtime spec marked at the boundaries; a second path kubelet to CRI to containerd/CRI-O joining at containerd, to show why Kubernetes needs no Docker.

Optional fourth: docker0 bridge with two veth pairs, NAT to the host interface and one published port as a port forward. The IP Addressing page's NAT diagram may cover this.

## (f) Open questions for the owner

1. The page is about 1,550 words of prose plus 300 words of code, roughly 10 percent over the top of the target range for prose alone. The commands block and the multi-stage Dockerfile are the flexible parts; say if either should be cut further.
2. The `fridge` commit/history/save/load sequence was kept because the brief asked for `save` with the image argument and it makes layers tangible. `docker commit` is otherwise discouraged in practice (images should come from a Dockerfile). Keep, or add one sentence saying so?
3. The .NET multi-stage example was rebuilt around `mcr.microsoft.com/dotnet/sdk:8.0` and `aspnet:8.0` to keep the owner's `COPY --from` lines. If the owner no longer works in .NET, a Go or Node example would date less obviously.
4. The Docker Desktop line names no threshold (brief rule 4). If the owner wants the actual criteria on the page, they belong in a `Source:` link rather than the text.
5. Windows containers are not mentioned (they use Windows kernel isolation primitives, or Hyper-V isolation). One sentence could be added if the owner cares about that platform; left out as not fundamental to the model.
