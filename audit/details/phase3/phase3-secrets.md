# Phase 3 report: fundamentals/security/Secrets Management.md

File rewritten: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn/fundamentals/security/Secrets Management.md`. Not committed. After the owner's tighten instruction: 1,117 words by `wc -w`, 1,034 prose (fences and link URLs excluded), against a target of 900 to 1,200. Earlier draft was 1,487. No `> Own view:` block (the owner did not write one; the two points it carried are stated neutrally: "No long-lived secret is the goal" and "Tags are what others build from, so sign those at least"). "How to rederive this" is 4 bullets. One H1 "Secrets Management", two `sh` fences, no dashes, British spelling, no personal data, no filler words from the owner's list. Checks run: word count, dash grep, H1 count, fence languages, all five link targets exist, the `#encoding-is-not-encryption` anchor exists in Cryptography Basics.

## (a) The question the page answers

Where should a secret live, how does it reach the code that needs it, and how do I sign what I publish? The opening paragraph answers it as a chain: plaintext in the repo is in history forever, so encrypt; encryption needs a key, so the key becomes the secret and moves to a store; reaching the store needs a credential (secret zero); workload identity removes that last long-lived credential. No long-lived secret is the goal; the earlier options are legitimate once their cost is known.

## (b) Kept from the original

- The owner's argument that a signed tag is part of the repository, travels with every clone, and can be verified by anyone with the public key and a reason to trust it (old L5), rewritten in place but same reasoning.
- The distinction between SSH for authentication and GPG for signing (old L3 and L5), corrected per the audit: SSH proves possession to any host holding your public key and leaves no artefact; a signature does.
- The GPG recipe, reduced to the essential commands: generate (now `--full-generate-key`), list, export, `git config user.signingkey`. Placeholders kept as placeholders (`<key-id>`; the old `<your-email>` form is gone because the key id is what `user.signingkey` wants).
- Blackbox, reduced to two sentences as history: the earlier form of encrypted-in-repo (GPG-encrypt chosen files for admins listed by GPG UID), still works, low-activity now, SOPS is the mainstream equivalent. No last-release date asserted (audit marked that unverified). The page does not comment on its own past; that lives in the audit folder.

## (c) Dropped and why

- All `blackbox_*` commands (initialize, addadmin, register_new_file, edit, update_all_files): tool recipe for a low-activity tool, one link away at the source.
- `gpg --delete-secret-key` / `--delete-key`, `gpg --import`: key housekeeping, not part of the question the page answers.
- Old L3 "does not prove anything to anyone who is not Github": WRONG per audit; replaced.
- Old L5 "Using SSH for signing would be theoretically possible, it's just not convenient": STALE per audit (Git 2.34); replaced with the SSH signing section.
- `gpg --gen-key`: STALE per audit; replaced with `--full-generate-key`.

## (d) Added, with source for each non-obvious claim

- Git history, forks and CI logs as copies; "a secret that has been in source is leaked, rotate it": OWASP Secrets Management Cheat Sheet; GitHub docs on removing sensitive data.
- Reconciliation with the DevOps page's rule (paraphrased, not in quotation marks: no secrets in source, store them in a vault rather than in CI-generated files): stated as a plaintext rule, with the honest trade-off that encrypted-in-repo makes every historical ciphertext depend on one key that cannot rotate the past. Own derivation from how Git history works.
- SOPS encrypts values not keys; key sources age, PGP, cloud KMS: SOPS README (github.com/getsops/sops).
- git-crypt via Git filters; sealed-secrets with an in-cluster controller and `kubeseal`: the projects' READMEs.
- External stores (Vault, AWS Secrets Manager, Parameter Store, Azure Key Vault, GCP Secret Manager); envelope encryption linked to `../../cloud/aws/Key%20Management.md` rather than repeated; Vault dynamic secrets and leases, "secret zero", Vault Agent: HashiCorp Vault docs.
- Workload identity (IAM roles, managed identities, Kubernetes service accounts bound to cloud roles, OIDC federation for CI runners): AWS and GitHub Actions OIDC documentation. Stated as the goal, with CI as the first place to apply it.
- Env var pitfalls: inherited by child processes, readable in `/proc/<pid>/environ` by the same user, present in core dumps, printed by `docker inspect` and framework debug pages. Files: permissions, tmpfs, re-readable on rotation. Sidecar (Vault Agent) and Secrets Store CSI driver. OWASP cheat sheet plus Linux and Docker behaviour.
- Kubernetes Secrets are base64-encoded: anyone with `get` on Secrets reads the value (RBAC is the API-side control), and etcd holds them unencrypted unless encryption at rest is configured (a separate protection that does not affect API reads, since the API server decrypts before returning). Kubernetes docs; linked to Cryptography Basics "Encoding is not encryption". Two clauses only; Kubernetes Security owns the detail. An earlier draft conflated the two protections; the advisor review caught it.
- Rotation as revocation practised in advance; least privilege bounds blast radius; audit trail decides rotate vs breach response; push-time secret scanning (GitHub push protection, gitleaks).
- Signature semantics: proves the key holder signed that object, not that the code is good; commit author field is free text; key-to-person binding is a separate trust decision. Git documentation; consistent with Cryptography Basics.
- SSH signing since Git 2.34 (November 2021) via `gpg.format ssh`; GitHub verification since August 2022; `gpg.ssh.allowedSignersFile` needed for local verification because SSH has no keyring. Git `git-config` docs and GitHub Docs "About commit signature verification". Both dates rated High in the audit.
- `commit.gpgsign` and `tag.gpgsign` config keys: Git `git-config` docs.
- Keyless signing with gitsign / Sigstore (OIDC identity, short-lived certificate, transparency log), one sentence, cross-linked to Supply Chain and Container Security, whose parallel rewrite describes cosign keyless the same way and links back to this page for key custody.
- No `> Own view:` block. The original page had no explicit opinions and the owner asked that none be invented. Two stance-like sentences remain as neutral statements: "No long-lived secret is the goal" (OWASP and every cloud provider's guidance) and "Tags are what others build from, so sign those at least" (Git documentation on signed tags). See (f) if the owner wants them marked as own view.

## (e) Diagrams Phase 5 should draw

- `secrets-spectrum.drawio.svg`: four boxes left to right, plaintext in repo, encrypted in repo, external store, workload identity; under each, "what is still secret" (the file, the decryption key, the store credential, nothing long-lived) and "how a leak is handled" (cannot fix history, re-encrypt everything, rotate one value, token expires). This is the chain the page is built on. Embed after the first paragraph or at the top of "The spectrum".
- No old image existed on this page; nothing to remove.

## (f) Open questions for the owner

1. The page has no `> Own view:` block. If you want one, candidates are: preferring workload identity and moving back toward the repo only when forced; keeping the decryption key for encrypted-in-repo out of personal keyrings; SSH signing over GPG for a personal setup; signing tags at minimum. Write it in your words or leave the page as derived-only.
2. Did you use Blackbox in earnest or only evaluate it? The page now describes it neutrally as the earlier form of encrypted-in-repo. If you ran it in production, a first-person line ("I used this for X") would fit the notebook style better and is worth adding.
3. The page mentions the Secrets Store CSI driver and Vault Agent as the file-delivery pattern. If you have run the External Secrets Operator instead, that is the other common answer and would be worth a clause.
4. Should the wiki carry a page on Git signing separately (the overlaps audit suggested `Git and GPG Signing.md`)? I folded signing into this page per the assignment; it is about a third of the text.
