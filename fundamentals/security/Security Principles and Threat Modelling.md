# Threat Modelling


[Threat Modelling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) is a structured approach of identifying and prioritizing potential threats to a system, and determining the value that potential mitigations would have in reducing or neutralizing those threats. Essentially it is trying to find answers to the following [questions](https://www.youtube.com/watch?v=VbW-X0j35gw&ab_channel=OWASPFoundation):

* What are we working on?
* What could go wrong?
* What are we going to do about it?

It is worth noting that rather than doing exhaustive upfront analysis to create the perfect threat model, in modern engineering teams it can be more valuable to [start small and iterate](https://martinfowler.com/articles/agile-threat-modelling.html) on your threat model.

## Threat model development

* Define a security objective - what data to protect and how to protect it?
* Document system decomposition and map data flows through the organization, network and your system. As it is data that we are trying to protect, data flow diagrams are the most effective way of documenting threats.
  * identify trust boundaries - users, files, process boundaries, network boundaries, machine boundaries that share privileges, rights, access and identifiers  
* Threat identification
* Mitigation analysis - how to deal with the threats based on priority low to high. The most desirable to least desirable mitigation techniques are:
  * redesign the system to eliminate the threat all together
  * apply a standard form of mitigation e.g. ACL
  * invent a new mitigation
  * accept the vulnerability and its associated threat
* Validate the threat model

### Attack surface evaluation

* Unnecessary functionality
* Understand history of application vulnerabilities

Microsoft has published its list of attack surface elements associated with Windows. This list can serve as a guide wrt attack surface elements associated with Windows, even if all the elements are not applicable to every application running on the Windows OS

* Open sockets
* Services
* Active web handlers
* Enabled accounts including guest accounts
* Weak ACLs related to the file system, registry, shares

### Attack surface minimization

* Reduce exposure by turning off unnecessary services, removing unused features or restricting access to limited IP range
* Reduce the attack surface by limiting the number of components and document the work done

## Security principles

* Good enough security - Good security design decisions are based on level of risk and need to consider
  * the cost associated with adding security
  * resources available - technology and people capabilities
  * level of security should not hamper the time taken by users of your application to get stuff done
* Least privilege
* Defense in depth
* Separation of duties
* Fail safe
* Complete mediation - reverify user authentication when they are trying to complete a sensitive task by putting in the appropriate security controls at each stage of the customer journey
* Open design - Given enough eyeballs all bugs are shallow
