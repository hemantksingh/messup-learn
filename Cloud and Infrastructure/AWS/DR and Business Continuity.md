# Disaster Recovery and Business Continuity

Disaster Recovery (DR) Plans should be tested on a regular basis, and there should be an auditable record that a test has taken place. This confirms the DR plan’s suitability and effectiveness should it need to be deployed in response to a live major incident. The runbooks/ Key Operating Procedures (KOPs) that need to be followed in execution of the tests should be well documented. Key questions to think about before opting for a DR strategy

* Are you planning for [high availability or disaster recovery](https://www.readysetcloud.io/blog/allen.helton/is-serverless-disaster-recovery-worth-it/)? People often think disaster recovery and high availability are the same thing.
  * **Disaster recovery** is the ability to get your system stable after a significant event. Significant events could be things like natural disasters (tornadoes or earthquakes), physical disasters (building fire or flooding in server room), or technology disasters (hacked or ransomware).
  * **High availability** is the ability of your system to stay up and running in an event with no downtime. This is what we tend to think of when we think of disasters. How robust is our solution and how quickly can we respond in the event that a disaster does happen?

* What is your expected RTO and RPO?
  * **Recovery Time Objective** (RTO) - Amount of time it takes to get your system operation after a disaster.
  * **Recovery Point Objective** (RPO) - Data recovery back to the point prior to the disaster or Point In Time Recovery (PITR)

## Serverless

Out of the box, serverless applications provide us with **HA in a single region** and depending upon your data storage, an RPO of a matter of seconds.

* Serverless services like Lambda, API Gateway, SQS, SNS and EventBridge all automatically span across all availability zones in a given region. This means you don’t have to worry about spinning up multiple instances in a multi-AZ architecture because AWS handles it for you.

* Using a database like DynamoDB, you get the high availability but you also have the option to turn on Point in Time Recovery (PITR). PITR allows you to restore your database with granularity down to the second for the past 35 days.

## Multi-Region Serverless

If your application has a zero tolerance for downtime, like an emergency computer-aided dispatch (CAD) system, you will need to explore a multi-region application. In the rare event that AWS has an entire region outage. Depending upon RTO/PTO times - hours, 10s of minutes, or few minutes you can opt for an [active/passive strategy](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)

### Active/Active

Since serverless has the pricing model of pay for what you use, having your serverless resources like Lambda functions and API Gateways deployed in a redundant region costs you no money. Where additional cost comes into play is getting your data into your failover region.

While implementing DynamoDB global tables to replicate data to your failover region, you pay for

* Write requests for the replication storage (per million units)
* Data transfer costs (per GB)

S3 two-way cross region replication

* cost for storage (GB-month)
* replication PUT requests (per 1000 requests)
* data transfer out (per GB)

### Active/Passive

Active/passive strategies use an active deployment (such as an AWS Region) to host the workload and serve traffic. The passive deployment (such as a different AWS Region) is used for recovery. The passive deployment does not actively serve traffic until a failover event is triggered.

Within AWS, services are divided into the data plane and the control plane. The **data plane** is responsible for delivering real-time service while **control planes** are used to configure the environment. For maximum resiliency, you should use only data plane operations as part of your failover operation. This is because the data planes typically have higher availability design goals than the control planes
