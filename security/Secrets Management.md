# Secrets Management

A secret is anything that gives access when disclosed: a password, an API key, a private key, a token. Where it lives is a chain. Plaintext in the repo is in history forever, so encrypt it. Encryption needs a key, so the key is now the secret and moves to a store. Reaching the store needs a credential, so one secret is left (Vault calls it secret zero). Workload identity removes that one: the platform vouches for the process and gives it a token that expires in minutes. No long-lived secret is the goal. Signing is the other half: proving that what you published came from you.

## Why "in the repo" fails

Git never forgets. A secret committed once is in every clone, fork and backup. Deleting it in the next commit only hides it from `HEAD`; rewriting history does not reach copies you do not control. CI logs are another copy: a build step that echoes its environment publishes the secret to anyone who reads the log. A secret that has ever been in source is leaked. Rotate it.

The [DevOps page](../platform/DevOps%20and%20Delivery.md) says no secrets in source code, keep them in a vault. That rule is about plaintext. An encrypted file in the repo does not break it, but the secret is now only as safe as the decryption key. If that key leaks, every historical ciphertext is open, because you cannot rotate the past. You get versioning and convenience; you take a wider blast radius.

## The spectrum

**Encrypted in the repo.** [SOPS](https://github.com/getsops/sops) encrypts the values in a YAML or JSON file and leaves the keys readable, so diffs still make sense. Its data key comes from age, PGP or a cloud KMS. git-crypt encrypts whole files through Git filters. sealed-secrets does it for Kubernetes: `kubeseal` encrypts with a public key whose private half only the in-cluster controller holds. Fits GitOps, where the repo is the whole truth, and small teams with no store to run.

**An external store.** HashiCorp Vault, AWS Secrets Manager and Parameter Store, Azure Key Vault, GCP Secret Manager. The secret sits outside the code, behind the platform's identity system, and every read is logged. Values are encrypted under a KMS key with envelope encryption, see [Key Management](../cloud/aws/Key%20Management.md). Vault adds dynamic secrets: a database credential created per lease and revoked when the lease ends. Fits when more than one system needs the same secret, when you need to know who read it, or when rotation must not need a deploy. The AWS pair is in the [AWS hub](../cloud/aws/README.md).

**No long-lived secret.** An IAM role on an instance, a managed identity on a VM, a Kubernetes service account bound to a cloud role, an OIDC token from a CI runner exchanged for cloud credentials. The platform knows which workload is running and issues a short-lived token. Nothing to store, rotate or leak. CI is the place to start: a runner's static cloud key is the classic long-lived secret.

## How a secret reaches the process

Environment variables are easy, which is why they leak. Every child process inherits them. `/proc/<pid>/environ` shows them to anything running as the same user. Crash dumps and `docker inspect` show them. Files are better: permissions apply, a tmpfs mount keeps them off disk, and a process can re-read a file when the secret rotates; an environment variable is fixed at start. A sidecar (Vault Agent) or the Secrets Store CSI driver fetches from the store and writes the file, so the application never holds a store credential.

A Kubernetes Secret is base64-encoded, and [encoding is not encryption](Cryptography%20Basics.md#encoding-is-not-encryption). Anyone with `get` on Secrets reads the value, so RBAC is the control at the API. In etcd it is unencrypted unless encryption at rest is turned on; that is a separate protection.

## Rotation, least privilege, audit trail

A leak is survivable only if you can revoke. Rotation makes revocation routine: if every secret changes on a schedule, changing one now is normal. Least privilege bounds what a leaked secret can do; a read-only key to one bucket is a smaller incident than an admin key. The audit trail shows whether a leaked secret was used: that decides between rotation and breach response. Secret scanning on push (GitHub push protection, gitleaks) catches plaintext before it reaches history.

## Signing your work

SSH keys authenticate you to a host that holds your public key. That proves possession at the moment you connect and leaves nothing behind. A signature is an artefact. It is stored with the commit or tag and travels with every clone. Anyone with your public key can check that the object was not changed after signing and that a holder of your private key made it. It does not prove the code is good. The author field is free text; the signature is the only thing binding the commit to a key, and trusting that key is a separate decision. Tags are what others build from, so sign those at least.

GPG:

```sh
gpg --full-generate-key                        # choose ECC (ed25519) and an expiry
gpg --list-secret-keys --keyid-format LONG     # find the key id
gpg --armor --export <key-id>                  # public key, paste into GitHub
git config --global user.signingkey <key-id>
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

Since Git 2.34 (November 2021) an SSH key can sign, and GitHub has verified SSH signatures since August 2022:

```sh
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

Verifying locally needs an allowed-signers file (`gpg.ssh.allowedSignersFile`), because SSH has no keyring. Keyless signing (gitsign, on Sigstore) removes the long-lived signing key: authenticate with an OIDC identity, get a certificate valid for minutes, sign, and the signature goes into a public log. The same mechanism signs container images, see [Supply Chain and Container Security](Supply%20Chain%20and%20Container%20Security.md).

## How to rederive this

* Repo history, forks, CI logs and crash dumps are all copies. A secret in any of them is leaked; rotate it.
* Encrypting moves the problem to the key; storing the key moves it to the store credential; only platform identity ends the chain.
* Environment variables are inherited and dumped; files have permissions and can be re-read.
* Authentication is a moment; a signature is an artefact others can check later.

## Sources

* OWASP Secrets Management Cheat Sheet
* HashiCorp Vault documentation (secret zero, dynamic secrets, Vault Agent)
* Git documentation, `git-config`, on `gpg.format` and `gpg.ssh.allowedSignersFile`; GitHub Docs, "About commit signature verification"
* SOPS README
* Sigstore and gitsign documentation
