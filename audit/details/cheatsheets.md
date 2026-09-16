# Audit: `Cheat sheets/` (13 files)

Repo: `/Users/Hemant.Kumar@finova.tech/workspace/messup-learn`. Audit date 2026-09-16. Line numbers are from `cat -n`. Version/EOL statements are marked Unverified where I did not check a primary source; the only web check done was the `kubectl exec` syntax removal (High-severity claim).

## Cheat sheets/Ansible.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# Installation` | H1 does not match filename `Ansible.md`; the file covers variables, roles, inventory and commands, not just installation. | Rename H1 to `# Ansible cheat sheet` and demote `Installation` to `##`. | High |
| 16-22 | WRONG | "There are 3 kind of varibles ... Host varaibles / Facts / Dynamic variables" | Non-standard taxonomy. Ansible has many variable sources (inventory host/group vars, play vars, role defaults/vars, extra vars, registered vars, `set_fact`). "Dynamic variables" is not an Ansible term; registered/`set_fact` vars live for the run of the current `ansible-playbook` invocation (across plays for the same host), not for "another playbook" run. | Replace with the official precedence list or "inventory vars, facts, registered vars (`register`/`set_fact`), extra vars (`-e`)". | Medium |
| 40-45 | BROKEN | ```` ```sh ```` before `roles:` | YAML playbook fragment is in an `sh` code fence (and starts with an empty line). | Use ```` ```yaml ````. | High |
| 70 | WRONG | `ansible all or ansible *` | `ansible all` with no `-m` uses the default `command` module and fails with "No argument passed to command module"; it does not ping. An unquoted `*` is expanded by the shell. | `ansible all -i inventory -m ping` (and quote patterns: `ansible 'web*' -m ping`). | High |
| 76 | WRONG | `/usr/sbin/yum update -y` | `yum` normally lives at `/usr/bin/yum`, not `/usr/sbin`. Also the control node section is Debian while the managed hosts are yum-based; fine, but worth stating. | Use `yum update -y` (PATH) or the `yum`/`dnf` module (`-m yum -a "name=* state=latest"`). | Medium |
| 88, 94 | STALE | `-m win_ping`, `-m setup` on Windows | Windows hosts need `ansible_connection: winrm` (or `ssh`/`psrp`) inventory vars, not mentioned. Since Ansible 2.10 (2020-08) these modules live in the `ansible.windows` collection (`ansible.windows.win_ping`, `ansible.windows.setup`); short names only work via redirects in the community `ansible` package. | Add the WinRM connection vars example and use FQCNs. | Medium |
| 95 | OPINION | `ansible all -i 52.236.183.27,  -m setup` | Hard-coded public (Azure-range) IP from a personal experiment; the trailing-comma inline-inventory trick is valid but the literal IP should not be in a knowledge base. | Replace with `<host-ip>,` and note the trailing comma makes it an inline inventory. | High |
| 6 | STALE | `sudo apt-get install ansible` | Ubuntu's apt package lags several releases; Ansible docs now recommend `pipx install --include-deps ansible` or the PPA. Not wrong, but agents will get an old version. | Add `pipx`/PPA option; note that `sshpass` is only needed for `-k`. | Medium |
| whole file | DUPLICATE | — | `Cloud and Infrastructure/DevOps/Ansible.md` (7 lines, conceptual push-vs-pull model + image) shares the same basename. Overlap is small but two `Ansible.md` files confuse retrieval. | Merge the 7-line conceptual file as an intro `## What it is` section here, or rename this file `Ansible CLI.md` and cross-link. | High |

## Cheat sheets/Dotnet.md (last commit 2024-05-03)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 9 | WRONG | ".Net core replaced Katana" | Imprecise: .NET Core is a runtime. Katana/OWIN was superseded by ASP.NET Core's own hosting + middleware pipeline (Kestrel, `IApplicationBuilder`); OWIN interop remains via `Microsoft.AspNetCore.Owin`. | "ASP.NET Core's built-in hosting/middleware pipeline superseded Katana; OWIN is still supported via Microsoft.AspNetCore.Owin." | High |
| 11-18 | DUPLICATE | "Server side rendoring (SSR) technology ... Blazor / Razor Pages / MVC / SPA" | Verbatim (but thinner) copy of `Tools/Web Frameworks.md` L153-162, which has the expanded, better version of the same list. | Delete L11-18 here and link to `../Tools/Web Frameworks.md#aspnet`. (Known broken link on L18 not re-reported.) | High |
| 13 | WRONG | "Server side rendoring (SSR) technology" then lists Blazor | Blazor WebAssembly is client-side; describing ASP.NET Core as an SSR technology is only true for MVC/Razor Pages/Blazor Server. | Say "web framework; supports SSR (MVC, Razor Pages, Blazor Server) and client-side (Blazor WASM)". | Medium |
| 28-31 | WRONG | "contextual escaping - treat input as raw data" | Muddled definition. Contextual (output) escaping means encoding output according to where it is emitted (HTML body, attribute, JS, URL); "treat input as raw data" describes neither escaping nor encoding. The two bullets also overlap (encoding is how escaping is done). | Rewrite as one bullet: "auto-encode all interpolated data for the output context (HTML/attribute/JS/URL); Razor does this by default for `@expr`". | Medium |
| 28-31 | CLASSIFY | "Template engines should be configured to enforce strict syntax rules ..." | Generic web-security (XSS/SSTI) guidance in a .NET CLI cheat sheet. | Move to `Security/Web Security/Cross Site Scripting.md` and link. | High |
| 25 | STALE | `.vbhtml -> VB Razor` | VB Razor exists only in classic ASP.NET MVC (.NET Framework); ASP.NET Core has no VB view support. | Mark "(legacy, .NET Framework only)". | High |
| 48 | STALE | `dotnet new -i IdentityServer4.Templates` | `-i/--install` was deprecated in the .NET 7 SDK in favour of `dotnet new install` (still works with a warning). IdentityServer4 itself reached end of support (Nov 2022, replaced by Duende IdentityServer). | `dotnet new install <TemplatePackage>` with a neutral template package example. | High |
| 51-53 | STALE | `"net6.0", "net7.0", "net8.0"` / `-f net6.0` | As of 2026-09, net6.0 and net7.0 are out of support; net8.0 LTS ends Nov 2026; net9.0/net10.0 exist (exact dates Unverified). Example targets an EOL framework. | Use `net10.0`/`net8.0` and say "any installed SDK TFM". | Medium |
| 71, 80 | STALE | `-v 6.0.28` / `Microsoft.AspNetCore.TestHost 6.0.28` | Pins an out-of-support 6.x package line. | Drop the explicit version or use a current one. | Medium |
| 76-83 | BROKEN | `Project 'example.tests' has the following package references` | Command output pasted inside the `sh` fence with no comment marker; an agent may treat it as commands. | Split into a separate ```` ```text ```` fence or prefix with `#`. | High |
| 3-31 | CLASSIFY | OWIN / ASP.NET history sections | File mixes a conceptual essay (OWIN, Katana, view engines) with a `dotnet` CLI cheat sheet. | Keep CLI here; move OWIN/ASP.NET prose into `Tools/Web Frameworks.md#aspnet`. | High |
| 66-67 | BROKEN | `### packages` immediately followed by ```` ```sh ```` | No blank line between heading and fence (renders in most engines, but inconsistent with the rest of the file). | Add blank line. | Low |

## Cheat sheets/IIS.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# Troubleshooting` | H1 does not match filename `IIS.md`. | `# IIS troubleshooting (ASP.NET Core hosting)`. | High |
| 13 | WRONG | "`Windows Logs` -> `System` for IIS logs e.g." | Dangling "e.g." with no example. The System log holds WAS/W3SVC/HTTP.sys service events; IIS request logs are files under `%SystemDrive%\inetpub\logs\LogFiles\W3SVC<n>`. ANCM (ASP.NET Core Module) startup errors go to the Application log. | Rewrite: "System: WAS/W3SVC app-pool events; Application: .NET runtime + ANCM (IIS AspNetCore Module) errors; request logs: `C:\inetpub\logs\LogFiles`". | High |
| 21 | OPINION | "Most probably the windows account under which the app pool is running has been disabled or expired" | One cause among several (rapid-fail protection after repeated crashes, wrong .NET runtime, bad config) presented as the most likely. First-person troubleshooting anecdote. | Label "one common cause:" and list rapid-fail protection / missing runtime. | High |
| 27 | STALE | "HTTP Error 502.5 - Process Failure in ASP.NET Core 2.1 application" | ASP.NET Core 2.1 is long out of support (Aug 2021). In current ANCM, 502.5 is "ANCM Out-Of-Process Startup Failure"; in-process hosting (default since 3.0) surfaces as 500.30/500.31/500.32. | Generalise heading to "502.5 / 500.3x ANCM startup failure" and keep the `dotnet application.dll` tip. | High |
| 3-7 | DUPLICATE | `dotnet --info` / `dotnet --list-runtimes` | Same commands as `Dotnet.md` L38. | Keep in Dotnet.md, link from here. | High |
| 35 | WRONG | "Add `IIS_IUSRS` users to the installation dir" | Imprecise: the identity that needs read/execute is the app pool identity (`IIS AppPool\<PoolName>`) or the `IIS_IUSRS` group; "users" is not the right object. | "Grant Read & Execute to `IIS AppPool\<PoolName>` (or `IIS_IUSRS`)". | Medium |
| whole file | CLASSIFY | — | Content is ASP.NET Core-on-IIS troubleshooting, not general IIS. | Merge into `Dotnet.md` as `## Hosting on IIS - troubleshooting`, or rename `IIS - ASP.NET Core hosting.md`. | Medium |

## Cheat sheets/Kubernetes.md (last commit 2021-11-02)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# Kubernetes cli` | H1 differs from filename and from the repo's conceptual `Kubernetes/Overview.md` (`# Kubernetes`); ambiguous which is the "Kubernetes" doc. | Rename file `Kubectl.md`, H1 `# kubectl cheat sheet`. | Medium |
| 9 | WRONG | "Context is a cluster's location and credentials" | A context is a named triple: cluster + user (credentials) + namespace. | "Context = cluster + user + default namespace." | High |
| 30 | WRONG | `kubectl get all` "get all resources within default namespace" | `all` is a curated category (pods, services, deployments, replicasets, statefulsets, jobs...). It excludes ConfigMaps, Secrets, Ingress, PVCs, CRDs, etc. | Comment: "common workload resources only; use `kubectl api-resources --verbs=list -o name | xargs -n1 kubectl get` for everything". | High |
| 61, 74 | WRONG | `kubectl -n <namespace> exec -it <podname> ip addr` / `... route` | Command must be separated with `--`. The `kubectl exec [POD] [COMMAND]` form was deprecated in kubectl 1.18 and has since been removed (kubernetes/kubernetes#125437, ~v1.31/1.32); on current kubectl this errors. Also `route`/`ip` are absent in many minimal images. | `kubectl -n <ns> exec -it <pod> -- ip addr` and `-- ip route`. | High |
| 75 | WRONG | "the bridge crbr0 inside of that node" | The kubenet bridge is `cbr0` (also seen in kind clusters). `crbr0` is a typo. | `cbr0`. | Medium |
| 63-71, 75-78 | DUPLICATE | PodCIDR / bridge / default-route explanations | Conceptual pod-networking narrative duplicates `Cloud and Infrastructure/Kubernetes/Overview.md` L82-100 (inter-pod communication within node / bridge). | Keep only the commands and one-line comments here; link to Overview for the explanation. | High |
| 64-71, 76-78 | BROKEN | `1: lo: <LOOPBACK,UP,...` output | Command output pasted inside an `sh` fence without a comment prefix. | Prefix with `#` or move to a ```` ```text ```` fence. | Medium |
| 81, 84 | OPINION | `--image nbrown/nwutils` | Obscure personal-choice image for a netshoot pod. | Suggest `nicolaka/netshoot` or `busybox:1.36` with a note that it's a preference. | Medium |

## Cheat sheets/Mac.md (last commit 2021-10-21)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `## Shortcuts` (first line) | No H1 in the file. | Add `# macOS cheat sheet`. | High |
| 6 | BROKEN | `` `Ctlr+Power` `` | Typo in the shortcut itself (`Ctlr`). | `Ctrl+Power` (or `Ctrl+Eject` on older Macs). | High |
| 7 | WRONG | "Close Document without saving `Cmd+D`" | Per Apple's shortcut list, `Cmd+D` in an Open/Save dialog selects the Desktop folder; "Don't Save" in the close-confirmation dialog is `Cmd+Delete`. `Cmd+D` alone does not close a document. | `Cmd+W` then `Cmd+Delete` ("Don't Save"). | Medium |
| 10 | WRONG | "Delete text `Fn+Backspace`" | `Fn+Delete` is *forward* delete (deletes the character after the cursor); "Delete text" is misleading. | "Forward delete". | High |
| 16-21 | INCONSISTENT | "Edit the `/Users/<username>/.bash_profile`" | Contradicts L29 in the same file ("macOS includes Z shell (zsh) as default" since 10.15). On a default zsh, `.bash_profile` is never read; PATH edits belong in `~/.zshrc` or `~/.zprofile`. | Replace with `~/.zprofile` (login) / `~/.zshrc` (interactive) and mention `.bash_profile` only for bash users. | High |
| 21 | WRONG | "The `.bash_profile file` is loaded before Terminal loads your shell environment" | It is read by bash *login shells* at start-up; it is not something Terminal loads before the shell. | "Read by bash login shells (Terminal opens login shells by default)." | Medium |
| 25 | WRONG | "List all the path variables `env`" | `env` prints all environment variables, not "path variables". | "List all environment variables: `env`; show PATH entries: `echo $PATH | tr ':' '\n'`". | High |
| 56 | BROKEN | ```` ``` ```` before `$ xcode-select -p` | Code fence without language. | ```` ```sh ````. | High |
| 62-72 | STALE | "Download bootcamp support software ... BootCamp5.1.5621" | Boot Camp 5.1.5621 is a 2014 driver bundle; Boot Camp is unavailable on Apple silicon (all Macs sold since 2023). `magicutilities.net` is a third-party paid tool. | Mark as "Intel Mac only / historical" or archive. | High |
| 62-72 | CLASSIFY | "Use Magic keyboard and mouse on Windows" | Windows driver-install topic in a macOS cheat sheet. | Move to a Windows note (e.g. `Tools/Windows Background Tasks.md` sibling) or drop. | Medium |
| 68-70 | BROKEN | `AppleWirelessTrackpad64` ... three bare lines | Not a list or code block; renders as one run-on paragraph. | Make a bullet list. | High |
| 31-51 | DUPLICATE | "### Oh My ZSH" | Oh My Zsh install/config also in `Ubuntu.md` L19-20. | Keep one "zsh / Oh My Zsh" section (suggest `Unix Basics.md` -> `## Shell`) and link from both OS files. | High |
| 3-10 | BROKEN | Shortcut table header `Description` column | Table's third column is empty for 5 of 6 rows and row 5 has a stray trailing `| `. Cosmetic. | Drop the column or fill it. | Low |

## Cheat sheets/Nginx.md (last commit 2021-06-30)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# Architecture` | H1 does not match filename `Nginx.md`; also collides conceptually with `Cloud and Infrastructure/Nginx.md` (`# Nginx`). | `# Nginx cheat sheet`. | High |
| 3 | WRONG | "Apache that spawns a process per connection" | True only for the prefork MPM; worker/event MPMs use threads. Over-generalisation. | "Apache's prefork MPM spawns a process per connection; worker/event MPMs use threads." | Medium |
| 18 | WRONG | "just reload even if the binary gets updated" | `nginx -s reload` re-reads configuration and respawns workers; it does **not** load a new binary. A binary upgrade without downtime needs the `USR2` (start new master) then `WINCH`/`QUIT` (retire old master) procedure. | Split: config reload = `nginx -s reload`; binary upgrade = `kill -USR2 $(cat /run/nginx.pid)` then `kill -QUIT <oldpid>`. | High |
| 21 | WRONG | `nginx -v` | Prints the version; in a "reload config" snippet the intended command is almost certainly `nginx -t` (test config before reload). | `nginx -t && nginx -s reload`. | Medium |
| 29-31 | WRONG | "server: define multiple virtual servers for host based routing / default_server: used when can't match listen or server" | Host-based routing is done by the `server_name` directive (not listed); `default_server` is a parameter of `listen` selected when the Host header matches no `server_name` for that address:port. `listen` matching always succeeds for the chosen address:port first. The `location` block, the other core routing construct, is missing. | List `listen`, `server_name`, `default_server` (param of listen), `location`. | High |
| 1-8 | DUPLICATE | Event-driven architecture vs Apache | Overlaps `Cloud and Infrastructure/Nginx.md` L14-22 ("Nginx and Apache"). Two files with basename `Nginx.md`. | Move the architecture paragraph to the conceptual file; keep this file to commands, paths, logs. Rename this file `Nginx CLI.md` or merge both. | High |
| 12-16 | OPINION | "By default the nginx configuration file is ... placed in the directory" (three paths) | The location is build/package dependent (nginx.org docs list these three); not stated which distro gives which. | Note: `/etc/nginx` on Debian/Ubuntu/RHEL packages, `/usr/local/etc/nginx` Homebrew, `/usr/local/nginx/conf` source builds; `nginx -V` shows the compiled-in path. | Medium |

## Cheat sheets/Nuget.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 37, 43, 50 | WRONG | `nuget source add` / `nuget source update` / `nuget source remove` | The nuget.exe command is `nuget sources <add|update|remove|list|enable|disable>` (plural). `nuget source` is not a command. | `nuget sources add -Name ... -Source ... -UserName ... -Password ...`. | High |
| 16 vs 37 | INCONSISTENT | `nuget help sources` vs `nuget source add` | Same file uses the correct plural on L16-18 and the wrong singular on L37-50. | Use `sources` throughout. | High |
| 37, 43 | WRONG | `-password "<password>"` | On non-Windows nuget.exe (mono) and in `dotnet nuget`, a password can only be stored with `-StorePasswordInClearText`; otherwise the command fails. Not mentioned. | Add note / prefer environment-variable credentials. | Medium |
| 31 | STALE | `nuget update <sln-name>.sln -Id <package-name>` | `nuget update` works only for `packages.config` projects; SDK-style/PackageReference projects (default since 2017) are not supported. | For PackageReference: `dotnet add package <id>` (bumps version) or `dotnet outdated`. | High |
| whole file | STALE | nuget.exe-centric commands | `dotnet nuget add|list|update|remove source` (cross-platform, in SDK since 3.1.200) already existed when this was written and is the current recommendation; nuget.exe is Windows-only. | Show `dotnet nuget ... source` as primary with nuget.exe as alternative. | High |
| whole file | DUPLICATE | — | Overlaps `Dotnet.md` `### packages` (L66-83). | Merge into `Dotnet.md` as `## NuGet`. | High |
| 1 | BROKEN | `# Nuget` | Product name is spelled `NuGet` (heading/filename spelling). | `# NuGet`, file `NuGet.md`. | Medium |

## Cheat sheets/SqlServer.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 34 | STALE | `select name from master.dbo.sysdatabases` | `sysdatabases` is a SQL Server 2000 backward-compatibility view, deprecated since 2005. | `SELECT name FROM sys.databases;`. | High |
| 5, 12, 22, 31, 41 | INCONSISTENT | ```` ```sh ```` then ```` ```powershell ```` | Same kind of content (sqlcmd invocation + interactive T-SQL prompts `1>`/`2>`) fenced as `sh` once and `powershell` four times; the T-SQL lines are neither. | Use ```` ```sh ```` for the command line and ```` ```sql ```` for T-SQL, or ```` ```text ```` for interactive transcripts. | High |
| 14, 24 | STALE | `sqlcmd -S <server> -E` / `-U -P` | Modern sqlcmd (ODBC Driver 18-based v17.x+/18, and go-sqlcmd) enables encryption by default; connecting to servers with self-signed certs needs `-C` (trust server certificate) or `-N o`. (Exact versions Unverified.) | Add `-C` note. | Low |
| whole file | CLASSIFY | — | 47 lines, 5 commands; too thin to be a stand-alone knowledge-base page. | Merge into a `Databases.md` cheat sheet or expand (backup/restore, `sp_who2`, connection strings). | Medium |

## Cheat sheets/Typescript.md (last commit 2022-05-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 27-30 | STALE | `npm install tsd` / `tsd install angular --resolve --save` / `typings` directory | `tsd` was deprecated in 2016 (succeeded by `typings`, then by `@types/*` npm packages with TypeScript 2.0). Already six years stale at the 2022 commit; an agent following this will install an abandoned tool. | `npm install --save-dev @types/<lib>`; types resolve automatically from `node_modules/@types`. | High |
| 20, 26 | STALE | "types provided in external libraries e.g. Angular" / "Need a ts definition file per external library" | Angular 2+ (2016) is written in TypeScript and ships its own `.d.ts`; only AngularJS needed DefinitelyTyped. Many libraries now bundle types; DefinitelyTyped is the fallback. | "Use `@types/<lib>` only when the library does not ship its own types (check `types` in package.json)." | High |
| 8 | BROKEN | ```` ```js ```` before `{ "compilerOptions"` | JSON (`tsconfig.json`) fenced as `js`. | ```` ```json ````. | High |
| 11-13 | WRONG | `"target": "es5"` with `"outFile": "output.js"` and no `module` | `outFile` only works with `module: "amd"`, `"system"` (or `"none"`); with the default (`commonjs` for es5 target) `tsc` errors "Only 'amd' and 'system' modules are supported alongside --outFile". `es5` is also a legacy target. | Drop `outFile` (use `outDir`) and target `es2020`+; or add `"module": "amd"`. | High |
| 32-37 | STALE | "Typescript modules ... Define unique namespaces like other languages (C#, Java) System.IO / java.io" | Describes TS `namespace` (formerly "internal modules"), which is legacy; modern TS code uses ES modules (`import`/`export`) and file-based scoping. Conflating "modules" with C#/Java namespaces misleads. | "Modules = files with `import`/`export` (ES modules). `namespace` is legacy for global-script code." | High |
| 6 | STALE | `npm install typescript` | Missing `--save-dev`/`-g`; also `npx tsc` is the usual invocation. Minor. | `npm install --save-dev typescript` then `npx tsc --init`. | Medium |
| whole file | CLASSIFY | — | Conceptual intro to TypeScript (2015-era) rather than a cheat sheet; nothing on types, generics, unions, `strict`, or the `tsc` CLI. | Rewrite as `tsc`/`tsconfig` cheat sheet or archive; conceptual material could join `Tools/Web Frameworks.md`. | High |

## Cheat sheets/Ubuntu.md (last commit 2021-10-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 9 | WRONG | "`apt-get` is one of apt's backends so you could also just use `apt` alone" | Backwards: `apt` is a newer end-user front-end built on the same libapt library as `apt-get`/`apt-cache`; `apt-get` is the stable scriptable tool, not a backend of `apt`. | "`apt` is the interactive front-end; `apt-get` is the script-stable equivalent (both use libapt)." | High |
| 16-17 | STALE | `sudo apt-get install ... docker-compose -y` | Installs Compose v1 (Python `docker-compose`), end-of-life July 2023 and removed from Docker docs. Current is Compose v2 as the `docker compose` CLI plugin (`docker-compose-plugin` from Docker's apt repo). The comment on L16 says to follow Docker docs for the engine, then installs compose from Ubuntu's repo anyway (inconsistent). | Remove `docker-compose` from the apt line; install `docker-ce docker-ce-cli containerd.io docker-compose-plugin` from Docker's repo. | High |
| 28 | STALE | "# Install powershell for Ubuntu 18.04" | Ubuntu 18.04 standard support ended 2023; also a comment with no command. | Link generic "Install PowerShell on Ubuntu" and give the `snap install powershell --classic` or apt-repo command. | High |
| 37-38 | BROKEN | `### switch between windows within an application` (empty) | Empty heading with no body, duplicating the table row on L35. | Delete. | High |
| 31-35 | BROKEN | Table with one row | One-row shortcut table; `key above Tab` is a description, not a key name. | Write `` Alt+` `` (US) and note it is layout-dependent; or merge with Mac shortcuts into a cross-platform table. | Medium |
| 19-20 | DUPLICATE | "Instal Oh My Zsh" | Same as `Mac.md` L31-51. | Single zsh section, linked. | High |
| 7-29 | OPINION | "## Dev setup runbook" | Personal tool selection (zsh, vim, azcli, powershell) presented as "dev setup". Fine, but label. | "My preferred dev setup (opinionated)". | High |
| 26 | OPINION | `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash` | Piping remote script to `sudo bash` is Microsoft's documented one-liner but a security anti-pattern; worth a caveat in a knowledge base. | Add "or follow the manual apt-repo steps". | Medium |

## Cheat sheets/Unix Basics.md (last commit 2021-10-15)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# Unix model` | H1 does not match filename `Unix Basics.md`; only the first section is about the model. | `# Unix basics`, demote `Unix model` to `##`. | High |
| 9-10 | WRONG | "File handlers are files" / "Shared memory wan't files but it is now" | "File descriptors" is the term (they are integers referring to open files, arguably not files). The shared-memory sentence is garbled; POSIX shared memory is exposed as files under `/dev/shm` on Linux. | "File descriptors refer to files; POSIX shared memory appears as files under `/dev/shm`." | Medium |
| 16 | WRONG | "Most installations are also done in the user's home directory" | System package installs go to `/usr`, `/opt`, `/etc`; only per-user tools (pip --user, nvm, Homebrew on some setups) live in `$HOME`. | "Per-user tools may install under `$HOME`; system packages install under `/usr`, `/opt`." | High |
| 66, 74, 79, 101, 106, 112, 119 | BROKEN | ```` ``` ```` with no language (7 fences) | Code fences without language identifier. | ```` ```sh ````. | High |
| 80 | WRONG | `rm -r *.*` "Delete all the files in a directory" | `*.*` matches only names containing a dot; skips dotfiles and extension-less files; `-r` also recurses into subdirectories. | `rm -rf ./*` (visible) plus a warning; for dotfiles too: `find . -mindepth 1 -delete`. | High |
| 86 | OPINION | `chmod 777 <directoryName> # Make a directory writable` | World-writable is a security anti-pattern presented as the way to "make writable". | `chmod u+w dir` / `chmod 775 dir` and note 777 is discouraged. | High |
| 88-97 | BROKEN | "Available permissions / First number is for the owner..." inside ```` ```sh ```` | Prose and a table inside a shell code fence. | Close the fence after L86 and render the digit table as markdown. | High |
| 108 | WRONG | `... | sort -rn # ... sorted by name in reverse order` | `-n` requests numeric sort; on non-numeric paths GNU sort falls back to whole-line comparison so the output happens to be reverse name order, but the flag is misleading and does not do what the comment says. | `sort -r`. | Medium |
| 120 | CLASSIFY | `pwd|pbcopy` | `pbcopy` is macOS-only; this is in the generic "Unix commands" section. | Move to `Mac.md` (Linux: `xclip -sel clip` / `wl-copy`). | High |
| 139-145 | STALE | `netstat -plunt` etc. | `net-tools`/`netstat` is deprecated on Linux and not installed by default on modern distros; `ss` is the replacement. | `ss -plunt`, `ss -tan state established`. | High |
| 164 | BROKEN | `cat filename.txt # print file contents to the screentail # like cat...` | Two commands merged on one line (missing newline: "screentail"). | Split into `cat` and `tail` lines. | High |
| 165 | WRONG | "tail ... see the last 20 (by default) lines" | `tail` default is 10 lines. | "last 10 (by default)". | High |
| 167 | BROKEN | `tail -200 /var/log/messages # print ... to the screen$ more # like cat...` | Two commands merged ("screen$ more"); also `/var/log/messages` is RHEL-style, Debian/Ubuntu use `/var/log/syslog` or `journalctl`. | Split lines; mention `journalctl -f`. | High |
| 180 | WRONG | `xfs_growfs /dev/sda3` | `xfs_growfs` takes the *mount point* (newer versions accept a device but the documented argument is the mount point); also the LVM step (`pvresize`/`lvextend`) implied by the linked HOWTO is not shown. | `xfs_growfs /mount/point`; add `growpart` / `lvextend -r` steps. | Medium |
| 185, 187 | INCONSISTENT | "Quit without saving `q!`" / "Stop diff mode by quitting Vim `qa`" | Missing the leading `:` present in `:wq` on L184; `q!`/`qa` alone are not commands. | `:q!`, `:qa`. | High |
| 182-187 | CLASSIFY | "## Vim editor" | Editor cheat sheet tacked onto Unix basics; only 4 items. | Either its own `Vim.md` or fold into an "Editors" file with `VS.md`/`VSC.md`. | Medium |
| 45 | OPINION | "Basic unix commands can be found [here](cs.jhu.edu/~joanne/unix.html)" | Personal bookmark as primary reference. Fine but label. | Prefer `man` / tldr.sh. | Low |

## Cheat sheets/VS.md (last commit 2020-12-02)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1-2 | BROKEN | (blank line) then `## Resharper` | File starts with a blank line and has no H1; filename `VS` is an unexplained abbreviation. | `# Visual Studio cheat sheet` and `## ReSharper`. | High |
| 6 | STALE | "Toggle inlay hints `Ctrl+Alt+Shift+5`" | Single ReSharper shortcut; keymap-dependent (VS vs IntelliJ scheme) and version not stated. Value Unverified. | State keymap and version. | Low |
| whole file | CLASSIFY | — | 6-line file with one table row; not a viable stand-alone page. | Merge into an `IDE shortcuts.md` with `VSC.md`, or archive. | High |

## Cheat sheets/VSC.md (last commit 2020-06-19)

| Line | Type | Claim (quoted, short) | Problem | Suggested fix | Confidence |
|---|---|---|---|---|---|
| 1 | BROKEN | `# Common shortcuts` | H1 does not match filename; `VSC` is a non-standard abbreviation (product is "VS Code"). | `# VS Code shortcuts`, file `VS Code.md`. | High |
| 5-7 | INCONSISTENT | `Ctrl K + M`, `Alt+Shift+F`, `Alt+Z` | Windows/Linux bindings with no platform stated, while the repo also has `Mac.md` (Mac: `Cmd+K M`, `Shift+Option+F`, `Option+Z`). | Add a platform column or note. | High |
| 5 | BROKEN | `` `Ctrl K + M` `` | Chord notation inconsistent with VS Code's own (`Ctrl+K M`). | `Ctrl+K M`. | Medium |
| 8 | BROKEN | "Remove line with criteria `^.*"key": "value",.*$\n` in json file \| `Repace All`" | Typo "Repace"; the row is a find/replace recipe, not a shortcut, and omits that regex mode (`Alt+R`) must be on. | Move to a "Recipes" section: "Ctrl+H, enable regex (Alt+R), pattern `^.*"key": "value",.*$\n`, replace with empty, Replace All". | High |
| whole file | CLASSIFY | — | 8-line file; pairs naturally with `VS.md`. | Merge into `IDE shortcuts.md`. | High |

## File classification

| File | H1 title | Kind (reference / cheatsheet / conceptual-essay / opinion / index) | Status (current / partially-stale / stale / archive-candidate) | Audience | Suggested tags (3-6) | One-line summary (<=25 words) | Consolidation note |
|---|---|---|---|---|---|---|---|
| Cheat sheets/Ansible.md | Installation (mismatch) | cheatsheet | partially-stale | DevOps engineers | ansible, configuration-management, inventory, roles, cli | Ansible install, variable types, roles/handlers, inventory and ad-hoc command examples incl. Windows hosts. | Merge with `Cloud and Infrastructure/DevOps/Ansible.md` (concept intro) or rename `Ansible CLI.md`; fix `ansible all` ping and FQCN modules. |
| Cheat sheets/Dotnet.md | .NET | cheatsheet | partially-stale | .NET developers | dotnet-cli, aspnet-core, owin, nuget, templates | OWIN/Katana history, ASP.NET Core UI options, and `dotnet` CLI commands for templates, solutions and packages. | Move OWIN/ASP.NET prose to `Tools/Web Frameworks.md`; absorb `Nuget.md` and `IIS.md`; update TFMs and `dotnet new install`. Currently mixes cheatsheet and conceptual essay. |
| Cheat sheets/IIS.md | Troubleshooting (mismatch) | cheatsheet | stale | .NET/Windows ops | iis, aspnet-core, hosting, troubleshooting, windows | Event Viewer locations and fixes for 503 app-pool-stopped, 502.5 ANCM failure and permission errors on IIS. | Fold into `Dotnet.md` as "Hosting on IIS"; update ANCM error codes. |
| Cheat sheets/Kubernetes.md | Kubernetes cli | cheatsheet | partially-stale | Platform/K8s engineers | kubectl, kubernetes, networking, debugging, dns | `kubectl` config/inspect/apply commands plus pod-network debugging (ip addr, route, nslookup). | Rename `Kubectl.md`; fix `exec --`; move networking narrative to `Kubernetes/Overview.md`. |
| Cheat sheets/Mac.md | (none) | cheatsheet | partially-stale | Mac developers | macos, shortcuts, zsh, path, terminal | macOS shortcuts, PATH/env setup, zsh + Oh My Zsh, plus an obsolete Boot Camp driver note. | Add H1; fix `.bash_profile` vs zsh; dedupe Oh My Zsh with `Ubuntu.md`; archive Boot Camp section. |
| Cheat sheets/Nginx.md | Architecture (mismatch) | cheatsheet | partially-stale | Web/infra engineers | nginx, reverse-proxy, configuration, logging, reload | Nginx master/worker model, config file locations, reload command, request-routing constructs and log paths. | Merge architecture paragraph into `Cloud and Infrastructure/Nginx.md`; rename `Nginx CLI.md`; fix reload/upgrade and `default_server` claims. |
| Cheat sheets/Nuget.md | Nuget | cheatsheet | stale | .NET developers | nuget, dotnet, package-management, cli, sources | nuget.exe commands for help, config location, package update and source add/update/remove. | Merge into `Dotnet.md` as `## NuGet`; correct `sources` plural; add `dotnet nuget` equivalents. |
| Cheat sheets/SqlServer.md | SQL Server | cheatsheet | stale | Developers/DBAs | sqlcmd, sql-server, tsql, databases | `sqlcmd` connection tests (Windows/SQL auth) and two ways to list databases. | Too thin; merge into a `Databases.md` or expand; replace `sysdatabases`. |
| Cheat sheets/Typescript.md | Typescript | conceptual-essay | archive-candidate | Frontend developers | typescript, tsconfig, types, definitelytyped, modules | 2015-era TypeScript intro: tsconfig sample, `tsd` type-definition workflow, namespaces-as-modules. | Rewrite as `tsc`/`tsconfig` cheat sheet with `@types`; or archive. |
| Cheat sheets/Ubuntu.md | Ubuntu development setup | opinion | partially-stale | Linux developers | ubuntu, apt, dev-setup, docker, zsh | VirtualBox guest additions tip, apt-based dev tool install runbook (zsh, docker, vscode, az cli), one shortcut. | Fix Compose v1 install; dedupe Oh My Zsh; label as opinionated personal runbook; remove empty heading. |
| Cheat sheets/Unix Basics.md | Unix model (mismatch) | cheatsheet | partially-stale | Developers new to Unix | unix, shell, linux, permissions, monitoring, vim | Unix philosophy, shell redirection, common commands (scp, chmod, find, grep), monitoring, disk growth, Vim basics. | Fix `tail` default, `rm -r *.*`, merged lines, fences; move `pbcopy` to Mac; `netstat`->`ss`; consider separate Vim file. Opens with a conceptual 'Unix model' section. |
| Cheat sheets/VS.md | (none) | cheatsheet | archive-candidate | .NET developers | visual-studio, resharper, shortcuts | One ReSharper shortcut (toggle inlay hints). | Merge with `VSC.md` into `IDE shortcuts.md`. |
| Cheat sheets/VSC.md | Common shortcuts (mismatch) | cheatsheet | current | Developers | vscode, shortcuts, regex, editor | Four VS Code items: language mode, format, word wrap and a regex line-removal recipe. | Merge with `VS.md`; add platform column; fix "Repace". |

## Cross-file observations

1. **Headings/identity**: 7 of 13 files have a missing or mismatched H1 (`Ansible` -> "Installation", `IIS` -> "Troubleshooting", `Nginx` -> "Architecture", `Unix Basics` -> "Unix model", `VSC` -> "Common shortcuts", `Mac` and `VS` have no H1 at all). For an agent that keys on the first heading, these files look like they are about a different topic than the filename says. Suggest H1 = `<Product> cheat sheet` everywhere.
2. **Duplicate basenames across folders**: `Cheat sheets/Ansible.md` vs `Cloud and Infrastructure/DevOps/Ansible.md`, and `Cheat sheets/Nginx.md` vs `Cloud and Infrastructure/Nginx.md`. `Cheat sheets/Kubernetes.md` vs `Cloud and Infrastructure/Kubernetes/Overview.md` is the same problem with a different name. In each pair the cheat sheet also carries a paragraph of conceptual material that duplicates the conceptual file. Recommendation: cheat sheets hold only commands/paths/shortcuts and link to the conceptual page; rename to `<Product> CLI.md` (or `Kubectl.md`) so retrieval is unambiguous.
3. **.NET cluster**: `Dotnet.md`, `Nuget.md` and `IIS.md` are one topic split three ways, with `dotnet --info` in two of them and NuGet package commands in two. `Dotnet.md` L11-18 is additionally a verbatim subset of `Tools/Web Frameworks.md` L153-162. Suggest a single `Dotnet.md` (CLI, NuGet, IIS hosting troubleshooting) and leave ASP.NET/OWIN prose to `Tools/Web Frameworks.md`.
4. **Shell/OS cluster**: `Mac.md`, `Ubuntu.md` and `Unix Basics.md` overlap (Oh My Zsh appears twice; `pbcopy` is macOS-only but sits in Unix Basics; PATH/shell start-up files are covered in Mac only, with the wrong file for the default shell). Suggest: `Unix Basics.md` = portable shell + commands (incl. one zsh/Oh My Zsh section), `Mac.md`/`Ubuntu.md` = OS-specific only.
5. **Platform of keyboard shortcuts is never stated**: `VSC.md` and `VS.md` give Windows/Linux chords; `Mac.md` gives macOS ones; `Ubuntu.md` gives GNOME. An agent asked "how do I format a file in VS Code on Mac" would get the wrong answer. Add a platform column or per-table note.
6. **Tiny files**: `VS.md` (1 row), `VSC.md` (4 rows), `SqlServer.md` (5 commands) are below the threshold of a useful page. Merge `VS.md` + `VSC.md` (+ the Vim section of Unix Basics) into `Editors and IDEs.md`; merge or expand `SqlServer.md`.
7. **Cheat-sheet folder mixes kinds**: `Typescript.md` and the first half of `Dotnet.md` are conceptual intros, not cheat sheets; `Ubuntu.md` is a personal runbook. Label kind in front-matter or move.
8. **Currency**: 8 of 13 files were last touched in 2020-2021 and several carry 2015-2016 era advice (`tsd`, `docker-compose` v1, `netstat`, `nuget.exe`, Boot Camp 5.1, ASP.NET Core 2.1, `sysdatabases`). The highest-impact corrections for an agent executing commands are: `kubectl exec ... -- cmd` (now errors), `nuget sources` (plural), `ansible all -m ping`, `tail` default 10, `rm -r *.*`, nginx reload vs binary upgrade, `.bash_profile` vs zsh.
9. **Command output inside `sh` fences** (`Dotnet.md` L76-83, `Kubernetes.md` L64-78) and prose inside fences (`Unix Basics.md` L88-97) will be read as commands by an agent; separate output into `text` fences or comment it.
10. **Sensitive/personal literals**: `Ansible.md` L95 contains a real-looking public IP; `Mac.md` L18-19 uses `/Users/username`. Replace with placeholders.

Sources (used for the `kubectl exec` claim): [kubernetes/kubectl#1687 - Bring back `kubectl exec [POD] [COMMAND]`](https://github.com/kubernetes/kubectl/issues/1687), [kubernetes/kubernetes#89301 - kubectl exec deprecation message](https://github.com/kubernetes/kubernetes/issues/89301)
