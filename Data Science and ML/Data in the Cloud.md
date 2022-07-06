# Big data in the cloud

Data services broadly fall into the following categories

## Data integrations - moving data

targeted at Data Engineers

* AWS Glue
  * serverless data integration service that provides both visual and code-based interfaces to discover, prepare, and combine data for analytics, machine learning and application development
  * allows you to visually create, run and monitor ETL workflows in AWS Glue Studio
  * with AWS Glue DataBrew, data analysts and data scientists can visually enrich, clean, and normalize data without writing code
  * with AWS Glue Elastic Views, application developers can use SQL to combine and replicate data across different data stores

* Azure Data Factory
  * serverless data integration and transformation service
  * code free and code based ETL and ELT processes
  * orchestrate and monitor data pipelines

* Google Cloud Dataprep
  * serverless service for visually exploring, cleaning, and preparing structured and unstructured data for analysis, reporting, and machine learning.

### Stream processing

Stream processing is the infrastructure for continuous data processing. The computational model can be as general as MapReduce or other distributed processing frameworks, but with the ability to produce low-latency results. The real driver for the processing model is the method of data collection. Data which is collected in batch is naturally processed in batch. When data is collected continuously, it is naturally processed continuously.

* Kafka - messaging system with durability guarantees and strong ordering semantics
* Kinesis Data Stream - collection and storage mechanism
  * ingest and store data from multiple data sources - log & event data collection, IOT, mobile and game devices
  * after data stream is saved, a data receiver e.g. firehose, lambda is required for further data processing or delivery
* Kinesis Data Firehose - delivery mechanism
  * easiest way to load streaming data into data lakes - S3, RedShift, Open Search or Splunk
  * writes data in micro batches, buffer of 60 seconds for **near real-time processing**
  * for real-time processing you can remove firehose and replace it with a lambda
* Kinesis Data Analytics
  * analyze streaming data for **real-time insights** e.g. used to uncover real-time monitoring metrics such as response time and error-rate spikes in a centralized logging system
  * provides real-time streaming ETL and analytics using Apache Flink - open-source framework and distributed processing engine for stateful computations
  * build streaming application using Apache Flink in Java, Scala, and Python
  
## Analytics and modelling

targeted at Data Analysts, Data Scientists

The tools you use for data analysis and processing may defer depending upon whether you are going to employ [machine learning in real time](https://dzone.com/articles/build-and-deploy-scalable-machine-learning-in-prod)

* you want to deploy a new model in production in real time (as soon as it is built) ? Overtraining the models can lead to information loss. Generic ML models that are based on a wider data set e.g. a model per geographical region will provide better results than a model per gas site.
* is latency of the model build process an issue ?
* is the ordering of messages important ?
* analytics of fuel prices and sales volume streams ? - adopt stream analytics (aggregations and statistical metrics over a large number of events) Many open source distributed stream processing frameworks are designed with analytics in mind - Apache Storm, Spark Streaming, Samza and Kafka streams
* monitoring in place for analysing the outcomes of the applied model ?
* single model per tenant or a single model for the entire system ?

and the type of analysis you are looking to perform:

* descriptive
* diagnostic
* predictive
* prescriptive - prescribe options to consumers

### Services

* Amazon Athena
  * serverless interactive fast query service that makes it easy to perform **ad-hoc analysis** data in Amazon S3 using standard SQL
  * point to your data in Amazon S3, define the schema, and start querying using standard SQL, pay per query and the data scanned
  * integrated with AWS Glue Data Catalog

* Google Cloud ML Engine
  * allows you to [train machine learning models](https://towardsdatascience.com/how-to-train-machine-learning-models-in-the-cloud-using-cloud-ml-engine-3f0d935294b3) in TensorFlow and other Python ML libraries (such as scikit-learn) without having to manage any infrastructure

* Kaggle
  * the *Github of Data Science*
  * allows users to find and publish data sets, explore and build models in a web-based data-science environment, work with other data scientists and machine learning engineers, and enter competitions to solve data science challenges  
  * offers a no-setup, customizable, Jupyter Notebooks environment for data analysis

* GPUs on demand for ML workloads
  * Unlike CPUs which consists of a few cores optimized for sequential serial processing, GPUs have a massively parallel architecture consisting of thousands of smaller, more efficient cores optimized for taking huge batches of data and performing the same operation over and over very quickly
  * GPUs have thousands of compute cores and when coupled with lightning fast memory access they accelerate machine learning, gaming, database queries, video rendering and transcoding, computational finance, molecular dynamics and many other applications
  * With GPUs in the cloud, your calculation-heavy applications can be scaled on elastic GPU clusters without building this into your own data centre

### Data warehousing

A data warehouse typically stores highly structured, frequently accessed data in a relational, PostGres like database with direct ODBC/JDBC connections to data sources. A data warehouse is a piece of batch query infrastructure which is well suited to many kinds of reporting and ad hoc analysis, particularly when the queries involve simple counting, aggregation, and filtering. They provide seamless integration with visualization tools like PowerBI, Tableau

* Amazon Redshift

* Dataform (part of Google Cloud)
  * Cloud warehouses store and process data cost effectively, meaning more and more companies are [moving away from an ETL to an ELT approach](https://dataform.co/etl-vs-elt) for managing analytical data
  * [Dataform](https://dataform.co) helps in converting captured data to curated data in BigQuery data warehouse
* Google BigQuery
  * fully managed, serverless data warehouse that scales with your storage and computing power needs

## Big data workloads

* Amazon EMR
  * cloud big data platform for running large-scale distributed data processing jobs, SQL queries, and ML applications using open-source analytics frameworks such as Apache Spark, Apache Hive, and Presto.
* Azure Databricks
  * Apache Spark-based big data analytics platform with the ability to run ML workloads (R, Python, Scala, Java) in Apache Spark workers
  * fully managed Apache Spark clusters with global scale and availability

* Azure HDInsight
  * on demand Hadoop type big data clusters
  * requires cluster management

## Data visualization

* Amazon QuickSight
* PowerBI
* Tableau