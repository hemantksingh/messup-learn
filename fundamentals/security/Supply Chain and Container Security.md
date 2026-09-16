# Supply Chain and Container Security

How do I know that what I run is what I meant to run, and how do I limit the damage if it is not? Before the container starts, every artefact on the path from source to registry carries proof of who built it and what is inside, and anything without proof is refused. After it starts, the process gets so little that a compromise cannot reach far.

## The threat

Most of the code you ship is code you did not write: the base image, the runtime, hundreds of packages, the compiler and the CI system. Each step from commit to running container is a place to swap or add something. Your tests run against whatever the pipeline produced, so they will not notice.

SolarWinds was a tampered build: the build system inserted a backdoor and customers installed a correctly signed update. Log4Shell was a vulnerable dependency teams did not know they were running. The first needs provenance and build integrity. The second needs an inventory. Both are described under [Web Application Risks](../security/Web%20Application%20Risks.md).

## Provenance and signing

A signature lets a consumer check who produced an artefact and that nobody changed it since. The current tools are Sigstore cosign and CNCF Notation. Both store the signature in the registry next to the image. Cosign is usually keyless: the build gets a short lived certificate bound to its OIDC identity (one CI workflow in one repository), signs with it, and records the signature in a public transparency log. There is no long lived key to steal. Notation uses X.509 certificates, for organisations that already run a PKI.

Docker Content Trust and Notary v1 are legacy. Notary v1 is unmaintained and Docker announced the retirement of Content Trust in 2025.

Content Trust was built on The Update Framework (TUF), whose ideas still apply. TUF assumes the repository or one signing key may be compromised, so it splits trust across roles. Root says which keys are valid for the other roles. Targets signs the artefacts. Snapshot signs the set of current metadata, so old and new files cannot be mixed. Timestamp re-signs a short lived statement often, so a client can tell it is being fed stale data. The root key is used rarely and kept offline; the online keys are the ones that can be rotated. One signature covers a whole image because the image digest is the hash of the manifest, and the manifest lists the digests of the config and every layer. That is why an image manifest is called a Merkle tree.

Every signing scheme needs a root of trust distributed out of band. Content Trust's default was trust on first use: record whatever root key you see first. Pinning the publisher identity in admission policy is stronger.

## Knowing what is inside

A software bill of materials (SBOM) lists every package and version in an image, in SPDX or CycloneDX format. Syft generates one; Trivy and Grype match it against vulnerability databases. Scan in CI so a bad image is never pushed, and in the registry so a clean image is flagged when a new CVE lands. An air gapped registry needs its vulnerability database fed offline.

Less inside means less to scan. Start from a minimal or distroless base (no shell, no package manager). Pin base images by digest; a tag can be moved. Rebuild when the base is updated, because a fix in the base does nothing until your image is rebuilt on it.

## Build integrity

SLSA grades how much you can trust the build. Level 1: the build produces provenance, a statement of what source and steps made the artefact. Level 2: a hosted build platform signed that provenance, so a laptop cannot forge it. Level 3: the platform is hardened; builds are isolated from each other, the build's own steps cannot forge the provenance, and secrets are out of reach of user defined steps. Hermetic builds (no network, all inputs declared) and reproducible builds (same inputs, identical output, so anyone can rebuild and compare) are separate practices. Older SLSA drafts graded them; the current specification does not.

Whoever controls the build platform can produce a valid signature. With long lived keys the CI system holds them; with keyless signing it holds the identity. Protect the pipeline like production: least privilege, audit logs, reviewed changes. Key custody is covered in [Secrets Management](../security/Secrets%20Management.md).

## Runtime least privilege

The old Unix advice was to start privileged, bind the port, then drop privileges. In a container you rarely need root at the start. Set a non-root `USER` in the Dockerfile. Bind a port above 1024, or grant only `NET_BIND_SERVICE`. Then:

* Forbid privilege escalation, so a setuid binary cannot regain what you dropped.
* Make the root filesystem read-only; mount a writable volume only where needed.
* Drop all capabilities and add back the one or two you can justify.
* Apply a seccomp profile (the runtime default is a good start) and an AppArmor or SELinux profile.
* Never run privileged containers. Privileged is the host with a different prompt.
* Set CPU and memory limits so one bad container cannot starve its neighbours.

In Kubernetes the `restricted` Pod Security Standard, enforced by Pod Security Admission, covers all but the read-only root and resource limits, which are policy you add. See [Kubernetes Security](../platform/Kubernetes%20Security.md).

## The isolation spectrum

Containers share the host kernel, so a kernel bug is a way out of any container on the host ([Containers](../platform/Containers.md) covers what namespaces and cgroups isolate). Liz Rice orders the options by how much overhead buys how much boundary. gVisor puts a user space kernel between the container and the real one, so most system calls never reach the host. Kata runs each pod in its own lightweight VM. Firecracker microVMs, which AWS Fargate and Lambda run on, are VMs stripped down to boot in milliseconds. A full VM is the strongest and heaviest. Trusted code suits a shared kernel; other people's code does not.

## Registries and admission

Run a private registry as the only allowed source. Enforce it with an admission controller (Kyverno, Gatekeeper or Sigstore policy-controller) that rejects any image not from that registry or not signed by a pinned identity. Signing without verification at admission is paperwork.

The traditional model was a hard shell and a soft interior: once inside, everything was trusted. The controls above assume the interior is hostile too.

## How to rederive this

* List every hop from commit to running process: source, dependencies, build, registry, scheduler, kernel. Each needs a control.
* At each hop ask what a consumer can check: a signature proves who, provenance proves how, an SBOM proves what.
* A signature is only as good as its root of trust and who controls the signer.
* Once running, ask what the process could reach if malicious, and remove it. What is left is the kernel boundary; if that is not enough, move along the spectrum.

## Sources

* Liz Rice, *Container Security* (O'Reilly): capabilities, seccomp, rootless containers, isolation options
* [SLSA specification](https://slsa.dev/), Build track
* [Sigstore documentation](https://docs.sigstore.dev/): keyless signing, transparency log
* [The Update Framework specification](https://theupdateframework.github.io/): roles and key management
* NIST SP 800-190, *Application Container Security Guide*
* Docker, [Retiring Docker Content Trust](https://www.docker.com/blog/retiring-docker-content-trust/) (2025)
* [Think Docker, think security](https://hemantkumar.net/think-docker-think-security.html), the 2017 post these notes began from
