# Threat Model Development

* Define a security objective - what data to protect and how to protect it?
* Document system decomposition an d how data flows through the organization, network using data flow diagram - most effective way of documenting threats as it is the data that we are trying to protect
  * identify trust boundaries - users, files, process boundaries, network boundaries, machine boundaries that share privileges, rights, access and identifiers  
* Threat identification
* Mitigation analysis - how to deal with the threats based on priority low to high. The most desirable to least desirable mitigation techniques are:
  * redesign the system to eliminate the threat all together
  * apply a standard form of mitigation way e.g. ACL
  * invent a new mitigation
  * accept the vulnerability and its associated threat
* Validate the threat model

## Attack surface evaluation

* Unnecessary functionality
* Understand history of application vulnerabilities

Microsoft has published its list of attack surface elements associated with Windows. This list can serve as a guide wrt attack surface elements associated with Windows, even if all the elements are not applicable to every application running on the Windows OS

* Open sockets
* Services
* Active web handlers
* Enabled accounts including guest accounts
* Weak ACLs related to the file system, registry, shares

## Attack surface minimization

* Reduce exposure by turning off unnecessary services, removing unused features or restricting access to limited IP range
* Reduce the attack surface by limiting the number of components and document the work done

## Security principles

* Good enough security - Good security design decisions are based on level of risk and need to consider
  * the cost associated with adding security
  * resources available - technology and people capabilities
  * level of security does not hamper the time taken by users of your application to get stuff done
* Least privilege
* Defense in depth
* Separation of duties
* Fail safe
* Complete mediation - reverify user authentication when they are trying to complete a sensitive task by putting in the appropriate security controls at each stage of the customer journey
* Open design - Given enough eyeballs all bugs are shallow
