# Securing REST APIs Summary

This content is based on the post https://hemantkumar.net/securing-rest-apis.html

| Security Goal         | Hash | MAC       | Digital Signature|
|:----------------------|:-----|:----------|:-----------------|
|Integrity              |  Yes |    Yes    |   Yes            |
|Authentication         |  No  |    Yes    |   Yes            |
|Confidentiality        |  ?   |    Yes    |   Yes            |
|Non-repudiation        |  No  |    No     |   Yes            |
|**Kind of keys**       | none | symmetric | asymmetric       |

Does encryption give you authenticity ?

## Integrity

A **hash** is a unique code, generally hexadecimal that represents a dataset e.g a file. It is designed to be:

* unique - the hash changes if the contents of the input data change
* reasonably quick to compute, but also not too quick. If it is too quick it is easy to break. 
* random, to avoid generating the same hash code for different inputs, thus minimising collisions when used in hash tables and such. 

A cryptographic hash is designed to be computationally infeasible to reverse, thus provide confidentiality via encryption whereas a checksum is designed to detect data integrity errors and often to be fast to compute. 

A **checksum** is necessarily a hash, however not all hashes are checksums (one's used in hash tables) but a cryptographically strong hash code is a good checksum if you can afford the computational cost.

**Encoding** is another way to maintain data integrity when data is sent over the wire. Base64 is a way to encode binary data into an ASCII character set known to pretty much every computer system, in order to transmit the data without loss or modification of the contents.