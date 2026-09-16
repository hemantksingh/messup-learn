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
| Images/mac.png |
| Images/patterns-effective-teams.jpg |
| Images/okta-pricing.png |
| Images/android-project-build.png |
| Images/android-tools-architecture.png |
| Images/data-analysis-experimentation.png |

## Moved (old → new)

| Old | New |
|---|---|
| Cheat sheets/Unix Basics.md | Fundamentals/Computing/The Unix Model.md |
| Computer Theory/NP Complete.md | Fundamentals/Computing/Algorithms and Complexity.md |
| Computer Theory/Software Complexity.md | Fundamentals/Computing/Code Quality.md |
| Distributed Systems/Concurrency Models.md | Fundamentals/Computing/Concurrency Models.md |
| Networking/Network Layers.md | Fundamentals/Networking/Network Layers.md |
| Networking/IPRouting.md | Fundamentals/Networking/IP Addressing.md |
| Networking/DNS.md | Fundamentals/Networking/DNS.md |
| Distributed Systems/Interprocess Communication.md | Fundamentals/Networking/Local IPC.md |
| Security/Web Security/Transport Layer Security.md | Fundamentals/Networking/TLS.md |
| Security/Web Security/TLS Certificates.md | Fundamentals/Networking/TLS Certificates.md |
| Distributed Systems/HTTP.md | Fundamentals/Web and APIs/HTTP.md |
| Distributed Systems/HTTP Caching.md | Fundamentals/Web and APIs/HTTP Caching.md |
| Distributed Systems/REST.md | Fundamentals/Web and APIs/REST.md |
| Distributed Systems/Synchronous Messaging.md | Fundamentals/Web and APIs/API Styles.md |
| SEO/Web Performance.md | Fundamentals/Web and APIs/Web Performance.md |
| Tools/Web Frameworks.md | Fundamentals/Web and APIs/Rendering Patterns.md |
| Distributed Systems/Consistency Models.md | Fundamentals/Data/Consistency Models.md |
| Distributed Systems/NoSql.md | Fundamentals/Data/Choosing a Database.md |
| Data and AI/Big Data.md | Fundamentals/Data/Data Platforms.md |
| Data and AI/Data Processing Pipeline.md | Fundamentals/Data/Data Pipelines.md |
| Data and AI/Machine Learning.md | Fundamentals/Data/Machine Learning.md |
| Distributed Systems/Asynchronous Messaging.md | Fundamentals/Messaging/Asynchronous Messaging.md |
| Distributed Systems/Event Sourcing.md | Fundamentals/Messaging/Event Sourcing and CQRS.md |
| Distributed Systems/Service Orientation.md | Fundamentals/Messaging/Service Orientation.md |
| Security/Data Security.md | Fundamentals/Security/Cryptography Basics.md |
| Security/Threat Modelling.md | Fundamentals/Security/Security Principles and Threat Modelling.md |
| Security/Web Security/Security Cookies.md | Fundamentals/Security/Browser Security Model.md |
| Security/Web Security/Cross Site Scripting.md | Fundamentals/Security/Cross Site Scripting.md |
| Security/Web Security/Cross Site Request Forgery.md | Fundamentals/Security/Cross Site Request Forgery.md |
| Security/Web Security/Security Headers.md | Fundamentals/Security/Security Headers.md |
| Security/Web Security/Web Application Security.md | Fundamentals/Security/Web Application Risks.md |
| Security/Storing secrets.md | Fundamentals/Security/Secrets Management.md |
| Security/Container Security.md | Fundamentals/Security/Supply Chain and Container Security.md |
| Security/Compliance.md | Fundamentals/Security/Standards and Compliance.md |
| Security/Cloud Security.md | Fundamentals/Security/Cloud Security.md |
| Security/Endpoint Security.md | Fundamentals/Security/Endpoint Security.md |
| Cloud and Infrastructure/Docker.md | Fundamentals/Platform/Containers.md |
| Cloud and Infrastructure/Kubernetes/Overview.md | Fundamentals/Platform/Kubernetes.md |
| Cloud and Infrastructure/Kubernetes/Kubernetes Security.md | Fundamentals/Platform/Kubernetes Security.md |
| Cloud and Infrastructure/Scalability.md | Fundamentals/Platform/Load Balancing and Proxies.md |
| Distributed Systems/Monitoring and Observability.md | Fundamentals/Platform/Observability.md |
| Cloud and Infrastructure/DevOps/Overview.md | Fundamentals/Platform/DevOps and Delivery.md |
| Cloud and Infrastructure/DevOps/Terraform.md | Fundamentals/Platform/Infrastructure as Code.md |
| Cloud and Infrastructure/DevOps/Ansible.md | Fundamentals/Platform/Configuration Management.md |
| Cloud and Infrastructure/AWS/Security.md | Cloud/AWS/README.md |
| Cloud and Infrastructure/AWS/Security - IAM.md | Cloud/AWS/Identity.md |
| Cloud and Infrastructure/AWS/Security - KMS.md | Cloud/AWS/Key Management.md |
| Cloud and Infrastructure/AWS/Security - Networking.md | Cloud/AWS/VPC Networking.md |
| Cloud and Infrastructure/AWS/EventBridge_SQS_SNS.md | Cloud/AWS/Messaging.md |
| Cloud and Infrastructure/AWS/DR and Business Continuity.md | Cloud/AWS/Disaster Recovery.md |
| Cloud and Infrastructure/AWS/EKS.md | Cloud/AWS/EKS.md |
| Cloud and Infrastructure/AWS/AWS.drawio | Cloud/AWS/AWS.drawio |
| Cloud and Infrastructure/Azure/Overview.md | Cloud/Azure/Tenants, Subscriptions and RBAC.md |
| Cloud and Infrastructure/Azure/AzureAd.drawio | Cloud/Azure/AzureAd.drawio |
| Tools/Testing.md | Practice/Testing Strategy.md |
| People/Leadership.md | Practice/Leadership.md |
| People/Influence.md | Practice/Influence and Negotiation.md |
| People/Capabilites.md | Practice/Roles and Hiring.md |
| People/Self Awareness.md | Practice/Self Awareness.md |

## Merged into another page, then removed

| Old | Folded into |
|---|---|
| Cheat sheets/Ansible.md | Fundamentals/Platform/Configuration Management.md |
| Cheat sheets/Kubernetes.md | Fundamentals/Platform/Kubernetes.md |
| Cloud and Infrastructure/Kubernetes/Production Readyness.md | Fundamentals/Platform/Kubernetes.md |
| Cheat sheets/Nginx.md | Fundamentals/Platform/Load Balancing and Proxies.md |
| Cloud and Infrastructure/Nginx.md | Fundamentals/Platform/Load Balancing and Proxies.md |
| Cloud and Infrastructure/Haproxy.md | Fundamentals/Platform/Load Balancing and Proxies.md |
| Cloud and Infrastructure/DevOps/SRE.md | Fundamentals/Platform/Observability.md |
| Data and AI/Regression Analysis.md | Fundamentals/Data/Machine Learning.md |
| Distributed Systems/AMQP.md | Fundamentals/Messaging/Asynchronous Messaging.md |
| Distributed Systems/Servicebus Frameworks.md | Fundamentals/Messaging/Asynchronous Messaging.md |
| Tools/Windows Background Tasks.md | Fundamentals/Messaging/Asynchronous Messaging.md |
| Distributed Systems/Continuous Deployment.md | Fundamentals/Platform/DevOps and Delivery.md |
| People/Negotiation.md | Practice/Influence and Negotiation.md |
| Security/Certification.md | Fundamentals/Security/Standards and Compliance.md |
| Cloud and Infrastructure/Azure/Security.md | Cloud/Azure/Tenants, Subscriptions and RBAC.md |
| Data and AI/Algorithm Design.md | Fundamentals/Computing/Algorithms and Complexity.md |
| Cheat sheets/Dotnet.md | Fundamentals/Web and APIs/Rendering Patterns.md |
| Security/Data Security.md (privacy half) | Fundamentals/Security/Data Privacy.md |
