# CI tools

| Feature                                                      | VS Team Services  | Appveyor              |
| ------------------------------------------------------------ | ----------------- | --------------------- |
| Commonly used tools availability (docker, nuget, nodejs etc) | Yes               | Yes                   |
| Deployment support, Webdeploy & Azure cloud service!         | Yes               | Yes + AWS deployments |
| CI build agent control (RDP), installation of custom s/w     | No                | Yes                   |
| Build agents in private cloud on Azure Vms                   | No ?              | Yes in Premium plan  https://www.appveyor.com/docs/build-environment/ |
| Pipeline as configuration                                    | Yes ? very verbose| Yes intuitive (.yml)   |
| UI Test - Selenium Webdriver support                         | No                | Yes (Firefox)         |
| Managed Nuget server                                         | No ?              | Yes https://www.appveyor.com/docs/nuget/ |
| Cost                                                         | **$110/month** https://www.visualstudio.com/team-services/pricing/ | **$99/month** (Additional concurrent job for $50/month) https://www.appveyor.com/pricing/ |

## CI hosted on-premise

Self hosted on-premise options provide better control and varied language support but incur a management cost, including:

* Security and software updates. Patching the CI server with security updates is paramount, if we are going to hold application secrets (like API keys, cloud provider creds) for deployments.
* Agent configuration drift
* Managing long running builds (Memory leaks)
* Maintaining Docker engine for Windows, needs freeing up hard disk space

| Feature                                                      | Jenkins            | Bamboo                |
| ------------------------------------------------------------ | ------------------ | --------------------- |
| Build tools integration                                      | Yes                | Yes                   |
| Branch management                                            | Possible with plugins but configuraion required    | Can auto-merge when a build succeeds and can clean up unused feature branches|
| Pipeline as configuraiton                                       | Groovy - Intuitive ? Possibly higher learning curve| No, Bitbucket Pipelines is the cloud offering, with pipeline as configuration but only supports dotnet core https://confluence.atlassian.com/bitbucket/language-guides-856821477.html |
| Integration with Altassian tools                             | Limited, with JIRA | Yes, fully integrated |

## Build propagation using Fan in Fan out

* Fan in - Multiple (upstream) pipelines lead into a single (downstream) pipeline.
* Fan out - After build & before acceptance, running functional tests on multiple OS.
* Further info https://www.gocd.org/2017/04/17/build-propagation-using-fan-in-fan-out.html