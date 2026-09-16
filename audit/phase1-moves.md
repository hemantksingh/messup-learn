# Phase 1 move map (2026-09-16)

Every path in `details/`, `file-triage.md` and `README.md` is pre-migration. Use these tables to find where content went.

## Dropped

| File |
|---|
| Cheat sheets/IIS.md |
| Cheat sheets/Mac.md |
| Cheat sheets/Nuget.md |
| Cheat sheets/SqlServer.md |
| Cheat sheets/Typescript.md |
| Cheat sheets/Ubuntu.md |
| Cheat sheets/VS.md |
| Cheat sheets/VSC.md |
| Cloud and Infrastructure/AWS/AWS Cli.md |
| Cloud and Infrastructure/AWS/Overview.md |
| Cloud and Infrastructure/Azure/Azure Cli.md |
| Cloud and Infrastructure/Azure/Azure Functions.md |
| Cloud and Infrastructure/DevOps/Azure DevOps.md |
| Cloud and Infrastructure/DevOps/Chef.md |
| Data and AI/Data in the Cloud.md |
| Distributed Systems/IOT Device Landscape.md |
| Mobile/Android.md |
| Tools/CICD.md |
| Tools/Okta.md |
| Tools/Tesseract.md |
| Photography/Photography Basics.md |
| images/mac.png |
| images/patterns-effective-teams.jpg |
| images/okta-pricing.png |
| images/android-project-build.png |
| images/android-tools-architecture.png |
| images/data-analysis-experimentation.png |

## Moved (old → new)

| Old | New |
|---|---|
| Cheat sheets/Unix Basics.md | computing/The Unix Model.md |
| Computer Theory/NP Complete.md | computing/Algorithms and Complexity.md |
| Computer Theory/Software Complexity.md | computing/Code Quality.md |
| Distributed Systems/Concurrency Models.md | computing/Concurrency Models.md |
| Networking/Network Layers.md | networking/Network Layers.md |
| Networking/IPRouting.md | networking/IP Addressing.md |
| Networking/DNS.md | networking/DNS.md |
| Distributed Systems/Interprocess Communication.md | networking/Local IPC.md |
| Security/Web Security/Transport Layer Security.md | networking/TLS.md |
| Security/Web Security/TLS Certificates.md | networking/TLS Certificates.md |
| Distributed Systems/HTTP.md | web and apis/HTTP.md |
| Distributed Systems/HTTP Caching.md | web and apis/HTTP Caching.md |
| Distributed Systems/REST.md | web and apis/REST.md |
| Distributed Systems/Synchronous Messaging.md | web and apis/API Styles.md |
| SEO/Web Performance.md | web and apis/Web Performance.md |
| Tools/Web Frameworks.md | web and apis/Rendering Patterns.md |
| Distributed Systems/Consistency Models.md | data/Consistency Models.md |
| Distributed Systems/NoSql.md | data/Choosing a Database.md |
| Data and AI/Big Data.md | data/Data Platforms.md |
| Data and AI/Data Processing Pipeline.md | data/Data Pipelines.md |
| Data and AI/Machine Learning.md | data/Machine Learning.md |
| Distributed Systems/Asynchronous Messaging.md | messaging/Asynchronous Messaging.md |
| Distributed Systems/Event Sourcing.md | messaging/Event Sourcing and CQRS.md |
| Distributed Systems/Service Orientation.md | messaging/Service Orientation.md |
| Security/Data Security.md | security/Cryptography Basics.md |
| Security/Threat Modelling.md | security/Security Principles and Threat Modelling.md |
| Security/Web Security/Security Cookies.md | security/Browser Security Model.md |
| Security/Web Security/Cross Site Scripting.md | security/Cross Site Scripting.md |
| Security/Web Security/Cross Site Request Forgery.md | security/Cross Site Request Forgery.md |
| Security/Web Security/Security Headers.md | security/Security Headers.md |
| Security/Web Security/Web Application Security.md | security/Web Application Risks.md |
| Security/Storing secrets.md | security/Secrets Management.md |
| Security/Container Security.md | security/Supply Chain and Container Security.md |
| Security/Compliance.md | security/Standards and Compliance.md |
| Security/Cloud Security.md | security/Cloud Security.md |
| Security/Endpoint Security.md | security/Endpoint Security.md |
| Cloud and Infrastructure/Docker.md | platform/Containers.md |
| Cloud and Infrastructure/Kubernetes/Overview.md | platform/Kubernetes.md |
| Cloud and Infrastructure/Kubernetes/Kubernetes Security.md | platform/Kubernetes Security.md |
| Cloud and Infrastructure/Scalability.md | platform/Load Balancing and Proxies.md |
| Distributed Systems/Monitoring and Observability.md | platform/Observability.md |
| Cloud and Infrastructure/DevOps/Overview.md | platform/DevOps and Delivery.md |
| Cloud and Infrastructure/DevOps/Terraform.md | platform/Infrastructure as Code.md |
| Cloud and Infrastructure/DevOps/Ansible.md | platform/Configuration Management.md |
| Cloud and Infrastructure/AWS/Security.md | cloud/aws/README.md |
| Cloud and Infrastructure/AWS/Security - IAM.md | cloud/aws/Identity.md |
| Cloud and Infrastructure/AWS/Security - KMS.md | cloud/aws/Key Management.md |
| Cloud and Infrastructure/AWS/Security - Networking.md | cloud/aws/VPC Networking.md |
| Cloud and Infrastructure/AWS/EventBridge_SQS_SNS.md | cloud/aws/Messaging.md |
| Cloud and Infrastructure/AWS/DR and Business Continuity.md | cloud/aws/Disaster Recovery.md |
| Cloud and Infrastructure/AWS/EKS.md | cloud/aws/EKS.md |
| Cloud and Infrastructure/AWS/AWS.drawio | cloud/aws/AWS.drawio |
| Cloud and Infrastructure/Azure/Overview.md | cloud/azure/Tenants, Subscriptions and RBAC.md |
| Cloud and Infrastructure/Azure/AzureAd.drawio | cloud/azure/AzureAd.drawio |
| Tools/Testing.md | practice/Testing Strategy.md |
| People/Leadership.md | practice/Leadership.md |
| People/Influence.md | practice/Influence and Negotiation.md |
| People/Capabilites.md | practice/Roles and Hiring.md |
| People/Self Awareness.md | practice/Self Awareness.md |

## Merged into another page, then removed

| Old | Folded into |
|---|---|
| Cheat sheets/Ansible.md | platform/Configuration Management.md |
| Cheat sheets/Kubernetes.md | platform/Kubernetes.md |
| Cloud and Infrastructure/Kubernetes/Production Readyness.md | platform/Kubernetes.md |
| Cheat sheets/Nginx.md | platform/Load Balancing and Proxies.md |
| Cloud and Infrastructure/Nginx.md | platform/Load Balancing and Proxies.md |
| Cloud and Infrastructure/Haproxy.md | platform/Load Balancing and Proxies.md |
| Cloud and Infrastructure/DevOps/SRE.md | platform/Observability.md |
| Data and AI/Regression Analysis.md | data/Machine Learning.md |
| Distributed Systems/AMQP.md | messaging/Asynchronous Messaging.md |
| Distributed Systems/Servicebus Frameworks.md | messaging/Asynchronous Messaging.md |
| Tools/Windows Background Tasks.md | messaging/Asynchronous Messaging.md |
| Distributed Systems/Continuous Deployment.md | platform/DevOps and Delivery.md |
| People/Negotiation.md | practice/Influence and Negotiation.md |
| Security/Certification.md | security/Standards and Compliance.md |
| Cloud and Infrastructure/Azure/Security.md | cloud/azure/Tenants, Subscriptions and RBAC.md |
| Data and AI/Algorithm Design.md | computing/Algorithms and Complexity.md |
| Cheat sheets/Dotnet.md | web and apis/Rendering Patterns.md |
| Security/Data Security.md (privacy half) | security/Data Privacy.md |
