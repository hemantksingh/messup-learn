# Disaster Recovery and Business Continuity

Key questions to think about before before planning your DR strategy

* Are you planning for [high availability or disaster recovery](https://www.readysetcloud.io/blog/allen.helton/is-serverless-disaster-recovery-worth-it/)? People often think disaster recovery and high availability are the same thing.
  * **Disaster recovery** is the ability to get your system stable after a significant event. Significant events could be things like natural disasters (tornadoes or earthquakes), physical disasters (building fire or flooding in server room), or technology disasters (hacked or ransomware).
  * **High availability** is the ability of your system to stay up and running in an event with no downtime. This is what we tend to think of when we think of disasters. How robust is our solution and how quickly can we respond in the event that a disaster does happen?

* What is your expected RTO and RPO?
  * **Recovery Time Objective** (RTO) - Amount of time it takes to get your system operation after a disaster.
  * **Recovery Point Objective** (RPO) - Data recovery back to the point prior to the disaster or Point In Time Recovery (PITR)

## What scenarios are you looking to recover from?

* Accidental writes or data loss e.g. delete of a production table or malicious data loss e.g. data locking via encryption by someone with access to the AWS account
  * Restore from a backup in the same account and point your services to the new data store
  * Restore from a backup in a separate account - ensures unauthorized access to an AWS account does not effect backups.
* Loss of an AWS region
  * Implement a multi region data replication strategy
* Are you looking at long term data retention?

## Is your DR plan effective?

For confirming the DR plan’s suitability and effectiveness should it need to be deployed in response to a live major incident, it is crucial to test your Disaster Recovery (DR) Plans on a regular basis. Following best practice

* Document the runbooks/ Key Operating Procedures (KOPs) that need to be followed in execution of the tests.
* Check the status of your backups. Have you got monitoring and alarms in place to track backup failures?
* Validate whether your backup and restore process works against large volumes of data. What is the difference in volume of data between production and backup environments?
  * If you were to do the test in staging env for example, The PRD/STG factor = Row Count in PRD/ Row Count in STG. The PRD/STG factor should ideally be >= 1 but you should aim for a PRD/STG factor of at least 0.60
  * Can your back jobs work with millions of records or are they going to time out if the data volume increases significantly?
  * Rather than using custom built scripts you may consider using a native service - Amazon DynamoDB is natively integrated with AWS Backup. You can use AWS Backup to schedule, copy, tag and life cycle your DynamoDB on-demand backups automatically.
* Audit the restore process. Do you use a pipeline to start the restore process that can tell you who ran the test along with RTO and RPO? When planning for disaster recovery it is best practice to regularly document average restore completion times and establish how these times affect your overall Recovery Time Objective.

## Serverless

Out of the box, serverless applications provide us with **HA in a single region** and depending upon your data storage, an RPO of a matter of seconds.

* Serverless services like Lambda, API Gateway, SQS, SNS and EventBridge all automatically span across all availability zones in a given region. This means you don’t have to worry about spinning up multiple instances in a multi-AZ architecture because AWS handles it for you.

* Using a database like DynamoDB, you get the high availability but you also have the option to turn on:
  * **On Demand Backups**
    * create full backups of your tables for long-term retention, and archiving required for compliance needs in regulated industries
    * automated scheduled backup and retention enforcement using the AWS backup service
    * copy backups between AWS regions and accounts (cross region and cross account)
    * secure with copying the backups to AWS Backup Vaults with dedicated encryption key
    * automatically move old backups to cold storage tier and save on backup costs
    * enforce service control policies and permissions based on tags inherited from dynamodb tables
  * Continuous incremental backups with **Point in Time Recovery** (PITR)
    * allows you to restore your database with granularity down to the second in the last 35 days
    * don't have to worry about creating, maintaining, or scheduling on-demand backups, thus do not effect provisioned throughput on the table or API latencies
    * helps to recover from accidental writes and deletes. When you delete a table that has PITR enabled, DynamoDB automatically creates a backup snapshot called a *system backup* and retains it for 35 days which can be used to restore the deleted table to the state it was in just before deletion
    * exporting to S3 and other AWS services for analytics
    * you should have a really good reason for not to enable PITR on your production tables

## Multi-Region Serverless

If your application has a zero tolerance for downtime, like an emergency computer-aided dispatch (CAD) system, you will need to explore a multi-region application. In the rare event that AWS has an entire region outage. Depending upon RTO/PTO times - hours, 10s of minutes, or few minutes you can opt for an [active/passive strategy](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)

### Active/Active

Since serverless has the pricing model of pay for what you use, having your serverless resources like Lambda functions and API Gateways deployed in a redundant region costs you no money. Where additional cost comes into play is getting your data into your failover region.

DynamoDB automatically distributes data and traffic to tables across a sufficient number of servers to handle throughput and storage requirements. All data is automatically replicated across multiple Availability Zones in an AWS Region. You can implement DynamoDB **global tables** to replicate data across regions in to a failover region. This means you pay for

* Write requests for the replication storage (per million units)
* Data transfer costs (per GB)

S3 two-way cross region replication

* cost for storage (GB-month)
* replication PUT requests (per 1000 requests)
* data transfer out (per GB)

### Active/Passive

Active/passive strategies use an active deployment (such as an AWS Region) to host the workload and serve traffic. The passive deployment (such as a different AWS Region) is used for recovery. The passive deployment does not actively serve traffic until a failover event is triggered.

Within AWS, services are divided into the data plane and the control plane. The **data plane** is responsible for delivering real-time service while **control planes** are used to configure the environment. For maximum resiliency, you should use only data plane operations as part of your failover operation. This is because the data planes typically have higher availability design goals than the control planes
