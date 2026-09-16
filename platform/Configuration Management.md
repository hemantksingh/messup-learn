---
title: "Configuration Management"
summary: "How a configuration management tool converges machines to a declared state, using Ansible's push over SSH model as the example."
kind: concept
status: current
last_reviewed: 2026-09-16
sources: []
tags: [configuration-management, ansible, ssh, playbooks, inventory]
---
# Configuration Management

Configuration management means declaring the desired state of your machines (packages, files, services, users) and having a tool converge them to it; Ansible is the tool this page uses as the example.

Ansible can be used for provisioning infrastructure, orchestrating and automating deployements. Unlike Puppet and Chef that use a **pull model** where agents deployed on the remote nodes (also called managed nodes) request relevant info (using HTTP APIs) from the masters that control configuration information, ansible uses a **push model** where the ansible control node pushes configuration to managed nodes over SSH (WinRM for Windows hosts; `ansible-pull` inverts this and has each node fetch and apply a playbook from a git repository).

In contrast to other configuration management frameworks, Ansible does not require the installation of any agents within managed environments. Instead commands are pushed over SSH and interpreted by a Python runtime. The Ansible **control node**, packages up the configuration in a python package and delivers it to the remote nodes over SSH, which upon execution return the execution result as json. The python package that was delivered is stored in a temp dir on the remote node and deleted after execution, therefore leaving no residual software on the remote node.

![Ansible push model: the Inventory (hosts, groups, variables), a Playbook of tasks and Modules feed the control server, which pushes to three managed nodes over SSH, or WinRM for a Windows node. Notes: the control server opens every connection and managed nodes never call back to a master; no agent runs on the managed nodes, the Python package is delivered over SSH, runs from a temp dir, returns its result as JSON and is deleted](../images/ansible-push-model.drawio.svg "Ansible push model")

## Ansible in practice: things that bit me

* `ping` is a module, not a default. `ansible all -i inventory -m ping` works; `ansible all` on its own runs the `command` module and fails asking for an argument. Quote host patterns (`'web*'`) or the shell expands them first.
* Where a variable is defined decides what wins. Inventory host and group variables, `group_vars/all` defaults, role defaults, play variables, `register` and `set_fact` results, and `-e` extra variables each sit at a different level of [variable precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence). `group_vars/<group>` separates settings per group; a host can be in several groups and `group_names` lists them.
* Facts are variables gathered from the managed host (memory, addresses, CPU) by the `setup` module at the start of a play. `gather_facts: false` skips that when speed matters.
* Roles are the unit of reuse: `roles/<name>/{tasks,templates,handlers}/main.yml`, invoked from a playbook with `roles:`. A handler is a task that runs once at the end of the play only if something notified it, which is how "restart the service only when the config changed" works.
* Windows hosts need `ansible_connection: winrm` (or `ssh`) in the inventory and the `ansible.windows` collection; `win_ping` replaces `ping`.
* A trailing comma turns a bare host into an inline inventory: `ansible all -i <host>, -m setup`.
* Ubuntu's apt package lags several releases. `pipx install --include-deps ansible` gives you a current one.
