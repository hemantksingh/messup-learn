# Phase 3 report: Supply Chain and Container Security

File: /Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Supply Chain and Container Security.md. Not committed.

Final word count after the owner's tighten pass: 1,166 words of page text (target 900 to 1,200), 1,228 including the Sources list. One H1, sections at H2, no code fences, no dashes, no `> Own view:` blocks, all four relative links resolve.

## (a) Question the page now answers

How do I know that what I run is what I meant to run, and how do I limit the damage if it is not? First paragraph: before start, every artefact on the source-to-registry path carries proof of who built it and what is inside, and anything without proof is refused; after start, the process gets so little that a compromise cannot reach far.

## (b) Kept from the original

* The hemantkumar.net link "Think Docker, think security": owner's own blog, verified live (HTTP 200) and OK in audit/details/linkcheck.tsv. Now a Sources entry.
* TUF fragments ("store root keys offline", "adversarial environment") expanded into one paragraph: roles (root, targets, snapshot, timestamp), root offline, timestamp for freshness.
* "Docker manifest follows a merkel tree" corrected to Merkle and explained: image digest is the hash of the manifest, manifest lists digests of config and layers, so one signature binds every byte.
* "Trust on first use" generalised: every signing scheme needs an out-of-band root of trust; TOFU is the weak option, pinning the publisher identity in admission policy the strong one.
* DTR offline scanning note kept, vendor-neutral: an air gapped registry needs its vulnerability database fed offline.
* "Drop privileges post startup" kept as the opening of the runtime section, then corrected (see d).
* "Traditionally - Hard shell soft interior" kept as one neutral sentence at the end of the admission section ("once inside, everything was trusted; the controls above assume the interior is hostile too"). Not marked as Own view because the owner only wrote the fragment, not the stance.

## (c) Dropped and why

* Docker Universal Control Plane and Docker Trusted Registry: sold to Mirantis in 2019 and renamed (audit STALE L7, L21-23).
* Docker Swarm section (join tokens, manager mutual TLS): niche orchestrator; the wiki's orchestration content is Kubernetes (audit L27-31).
* "Service discovery is network scoped": a Swarm overlay-network concept; goes with Swarm.
* The opening "Docker ecosystem itself provides the following options": framed the page around Docker products.
* Docker Content Trust as a current control: reduced to one sentence marking it and Notary v1 legacy.
* Two `> Own view:` blocks drafted in an earlier pass (the "hard shell" stance and a "trusted code suits a shared kernel" heuristic) were removed per the owner's instruction not to write Own view text the owner did not write. Both points now appear as neutral single sentences.

## (d) Added, with sources

* SolarWinds as tampered build vs Log4Shell as unknown vulnerable dependency, splitting the page into provenance/build integrity vs inventory; pointer to Web Application Risks as instructed.
* Sigstore cosign keyless flow (short-lived certificate bound to an OIDC identity, signature in a transparency log); Notation uses X.509. Source: Sigstore docs, Notary Project docs.
* Docker Content Trust retirement announced 2025. Verified by WebSearch (docker.com/blog/retiring-docker-content-trust; InfoQ, Aug 2025; Notary v1 service scheduled to shut down December 2026). Only the year is in the page, per the no-dates rule.
* TUF roles and purposes (snapshot prevents mix-and-match, timestamp prevents stale-data attacks). Source: TUF specification.
* SBOM formats SPDX and CycloneDX; Syft to generate, Trivy and Grype to scan; scan in CI and in the registry; minimal/distroless bases; pin by digest because tags are mutable; rebuild on base updates. Sources: Liz Rice, Container Security; NIST SP 800-190.
* SLSA Build track levels as in the 1.x spec: L1 provenance exists, L2 hosted platform signs it, L3 hardened platform (isolated builds, unforgeable provenance, secrets unreachable from user-defined steps). Hermetic and reproducible builds stated as separate practices that older SLSA drafts graded and the current spec does not. Source: slsa.dev.
* "Whoever controls the build platform can produce a valid signature" as the principle covering both long-lived keys and keyless identity; link to Secrets Management for key custody.
* Runtime list: non-root USER, no privilege escalation, read-only root FS, drop all capabilities, seccomp plus AppArmor/SELinux, no privileged containers, resource limits. The page says the `restricted` Pod Security Standard covers all but read-only root and resource limits, which are policy added on top (PSA does not mandate those). Link to Kubernetes Security. Sources: Liz Rice; Kubernetes Pod Security Standards.
* Isolation spectrum attributed inline to Liz Rice: shared kernel, gVisor (user-space kernel), Kata (lightweight VM per pod), Firecracker microVMs (what Fargate and Lambda run on), full VM. Sources: Liz Rice; AWS Firecracker announcement.
* Registry and admission: private registry as the only allowed source; Kyverno, Gatekeeper or Sigstore policy-controller verifying signer and origin at admission.
* How to rederive this: four bullets.

## (e) Diagrams Phase 5 should draw

One diagram, `images/supply-chain-path.drawio.svg`: the hops source, dependencies, build, registry, admission, running container; under each hop the tamper point, above it the control that closes it (review and pinned dependencies; SLSA provenance and protected CI; signature and SBOM in the registry; admission policy verifying signer and origin; least-privilege runtime and isolation boundary). The old page had no image, so nothing to remove.

## (f) Open questions for the owner

1. "Hard shell soft interior" is now a neutral sentence. If you hold the stance ("assume the interior is hostile too"), it can be promoted to `> Own view:` in your words.
2. "Trusted code suits a shared kernel; other people's code does not" (end of the isolation section) is a judgement call written by the rewrite. Keep, reword or delete.
3. overlaps.md recommends a `## Security` stub in fundamentals/platform/Containers.md linking here. Containers.md was read-only for this task and is being rewritten by another agent (it shows as modified in the working tree); whoever finishes it should add the cross-link.
4. Secrets Management is linked for key custody but is still the old GPG/Blackbox text until its own rewrite lands. The filename is stable so the link holds.
