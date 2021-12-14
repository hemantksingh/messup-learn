# Storing secrets

SSH keys are used to authenticate to Github, which allows you access to Github repositories but does not prove anything to anyone who is not Github.

GPG keys are used for signing your commits/tags to establish integrity of the code by ensuring it wasn't tampered with after being tagged by the signer and the commit in question really does correspond to the release in question. Using SSH for signing would be theoretically possible, it's just not convenient. When you GPG-sign a git tag, that tag is part of the repository, and can be pushed to other copies of the repository. Thus, other people who clone your repository can verify the signed tag, assuming that they have access to your public key and reason to trust it.

## GPG

* Generate a key `gpg --gen-key`

* Delete a key
    * `gpg --delete-secret-key hk@hemantkumar.net`
    * `gpg --delete-key hk@hemantkumar.net`

* List keys
    * `gpg --list-secret-keys --keyid-format LONG`
    * `gpg --list-keys`

* Export a key `gpg --armor --export hk@hemantkumar.net > hk_pub.gpg`

* Import a key `gpg --import hk_pub.gpg`

## Blackbox

Store secrets safely with [blackbox](https://github.com/StackExchange/blackbox)

* Enable blackbox for a git repository `blackbox_initialize`
* To see a list of GPG keys on your machine, and to get the UID you need to provide blackbox with, run `gpg --list-keys`
* Add a blackbox admin `blackbox_addadmin <hk@hemantkumar.net>`
* Start encrypting file(s) for the first time `blackbox_register_new_file <file>`

### Editing encrypted files

* `blackbox_edit <file.gpg>`

### Giving others access

* Add them as admin `blackbox_addadmin <hk@hemantkumar.net>`
* Import their public key `gpg --import hk_pub.gpg`
* Decrypt and encrypt all the files using the new keyring `blackbox_update_all_files`
