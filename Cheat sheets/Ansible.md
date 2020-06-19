# Installation

Ansible control server (Debian based system like Ubuntu)

```sh
sudo apt-get install ansible
sudo apt-get install sshpass
```

## Organisation

* Best practice [directory layout](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#directory-layout)

## Ansible Variables

There are 3 kind of varibles that can be used

* Host varaibles - defined in the inventory file where you define the hosts. These are specific to a host.

* Facts - Use data gathered from the remote managed host like memory, IP addresses, CPU speed

* Dynamic variables - Created during the course of your playbook and then destroyed later. Create a variable during execution of a playbook and used for another playbook.

**Groups** are for organization or grouping of hosts. `group_vars` provide separation of the varibles for different groups e.g. `group_vars/webservers` will have configuration specific to webservers not dbservers. `group_vars/all` will have default values that are universally true.

[Magic variables](http://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#magic-variables-and-how-to-access-information-about-other-hosts) are some variables provided by ansible automatically. A host can belong to multiple groups. `group_names` is a list (array) of all the groups the current host is in. You could refer to a single element using `group_names[0]`

[Variable precedence](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) defines how variable values get overridden and where they should be defined.

## Ansible Roles

Allow modularising your tasks. Compartmentalised collections of tasks, templates, variables, using predefined dir structure and search paths for resue. Used to create a function like "web server", "app server" or "database server". The default place where ansible looks for roles is:

* `roles/{role_name}/tasks/main.yml`
* `roles/{role_name}/templates/{template_name}.j2`
* `roles/{role_name}/handlers/main.yml`

Invoking a role in a playbook:

```sh

roles:
    - role1
    - role2
```

### Handlers

[Handlers](https://codereviewvideos.com/course/ansible-tutorial/video/ansible-handlers) provide notify and subscribe mechanism while running tasks. e.g. in a playbook for installing Apache, as part of some of the tasks, we would have to re-start Apache. So instead of copy and paste a task over and over, we define a single Restart Apache handler and then notify that handler from the current task whenever a restart is required.

## Inventory

[Inventory](http://docs.ansible.com/ansible/devel/user_guide/intro_inventory.html) is the list of managed servers. It can be in INI-like format such as `/etc/ansible/hosts` or YAML

## Commands

Ping remote host using ansible

```sh
ansible 192.168.33.20 -i inventory -u vagrant -m ping -k -vvv
# -i identify inventory file
# -m is the module
# -k prompt for password
# -vvv for debug level 3
```

ping all the hosts in the inventory

```sh
ansible all or ansible *
```

run an adhoc command on all managed servers

```sh
ansible all -i inventory -u vagrant -m command -a "/usr/sbin/yum update -y"
# or
ansible all -i inventory -u vagrant -a "/usr/sbin/yum update -y"

# shell module is used for running commands if you want to use shell variables
```

### Manage Windows remote host

Ping remote windows server

```sh
ansible web -i inventory.yml -m win_ping # Ping remote host
```

Gather facts about windows remote host

```sh
ansible web -i inventory.yml -m setup # Gather facts about remote host
ansible all -i 52.236.183.27,  -m setup
```

## Best Practice

* https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html
* http://hakunin.com/six-ansible-practices