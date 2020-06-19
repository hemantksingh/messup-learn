# Hashing and salting

![password-hashing.png](../Images/password-hashing.png Password Hashing)

http://blog.conviso.com.br/worst-and-best-practices-for-secure-password-storage/


## Salt and Nonce

Hashing the same data (message) multiple times results in the same hash. Nonce is a one time value used to generate a unique hash per request, to prevent replay attacks.

Salt on the other hand is a random number generated and stored with the password hash to verify the password.
