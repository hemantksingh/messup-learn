Store secrets safely with [blackbox](https://github.com/StackExchange/blackbox)

# GPG

* Generate a key `gpg --gen-key`

* Delete a key
    * `gpg --delete-secret-key hk@hemantkumar.net`
    * `gpg --delete-key hk@hemantkumar.net`

* List keys
    * `gpg --list-secret-keys --keyid-format LONG`
    * `gpg --list-keys`

* Export a key `gpg --armor --export hk@hemantkumar.net > hk_pub.gpg`

* Import a key `gpg --import hk_pub.gpg`

# Blackbox

* Enable blackbox for a git repository `blackbox_initialize`
* To see a list of GPG keys on your machine, and to get the UID you need to provide blackbox with, run `gpg --list-keys`
* Add a blackbox admin `blackbox_addadmin <hk@hemantkumar.net>`
* Start encrypting file(s) for the first time `blackbox_register_new_file <file>`

## Editing encrypted files
*  `blackbox_edit <file.gpg>`

## Giving others access
* Add them as admin `blackbox_addadmin <hk@hemantkumar.net>`
* Import their public key `gpg --import hk_pub.gpg`
* Decrypt and encrypt all the files using the new keyring `blackbox_update_all_files`
