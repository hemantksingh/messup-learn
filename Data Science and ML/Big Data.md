# Aspects of big data

* Data that is too big (100s of TB - x PB) or moves too fast to be processed by conventional means (too big of OLTP).
* Three Vs

    * Volume -  Data too big to fit on a single machine
    * Velocity - The rate at which the data comes into the system and the velocity of the output of the system matters. The tighter the feedback loop, the greater is the competitive advantage. The results might go directly into a product e.g. – Facebook recommendations. The need of speed has also driven the development of NoSQL databases where RDBMS' aren’t the right fit.
    * Variety - The data being generated can be unstructured with a format that is outside your control. A common use of big data processing is to take unstructured data and extract meaning out of it for either human consumption or as a structured input to another application.  Relational databases with their fixed schemas aren’t always a natural fit for storing such data. Semi-structured NoSQL databases provide the flexibility to store unstructured data that has less formal schema.

* Partition a big dataset into multiple smaller datasets and send each chunk of the data to a separate node in a cluster to be processed individually and in parallel.

## Big Data Architectures

A [big data architecture](https://docs.microsoft.com/en-us/azure/architecture/data-guide/big-data/) is designed to handle the ingestion, processing, and analysis of data (usually done via a [data pipeline](./Data%20Processing%20Pipeline.md)) that is too large or complex for traditional database systems.

A Lambda architecture separates batch processing from stream processing whereas the Kappa architecture enables you to build your streaming and batch processing system on a single technology. With a sufficiently fast stream processing engine (like Hazelcast Jet), you may not need a separate technology that is optimized for batch processing. While the Lambda Architecture does not specify the technologies that must be used, the batch processing component is often done on a large-scale data platform like Apache Hadoop. The Hadoop Distributed File System (HDFS) can economically store the raw data that can then be transformed via Hadoop tools into an analyzable format. While Hadoop is used for the batch processing component of the system, a separate engine designed for stream processing is used for the real-time analytics component. One advantage of the Lambda Architecture, however, is that much larger data sets (in the petabyte range) can be stored and processed more efficiently in Hadoop for large-scale historical analysis.

### Hadoop

Hadoop is a platform for distributing computing across a number of servers in a cluster. It is an open source implementation of MapReduce. It combines a **MapReduce** engine with a **Hadoop distributed file system (HDFS)**. HDFS allows the disks local to individual nodes in a Hadoop cluster to operate as a single pool of storage. Files are replicated across various nodes so that loss of one node will not cause loss of data. Facebook uses A MySQL database to store the core user data which is then derived on to Hadoop servers. After computations the data is then transferred to MySQL database for pages served to the users.

When working with very large data sets, it can take a long time to run the sort of queries that clients need. These queries can't be performed in real time, and often require algorithms such as **MapReduce** that operate in parallel across the entire data set. The results are then stored separately from the raw data and used for querying.

* Map: split the data and distribute the computation over multiple servers in parallel. For that computation to take place each server must have access to the data. HDFS makes this possible.
* Reduce: take the O/P from the map phase (in a key value format) and aggregate the results

![hadoop-stack.png](../Images/hadoop-stack.png "Hadoop Stack")

Databases require you to structure data according to a particular model (e.g. relational or document) whereas files in a distributed filesystem are just byte sequences which can be written using any data model and encoding. They might be collections of database records but they can equally well be text, images, videos, sensor readings, genome sequences or any other kind of data.

Hadoop opened up the possibility of indiscriminately dumping data into HDFS, and only later figuring out how to process it further. By contrast, MPP (Massively Parallel Processing) databases typically require careful **up-front modelling** of the data and query patterns before importing the data into the database's proprietary storage format.

From a purist's point of view, it may seem that careful modelling and import is desirable, because it means the users of the database have better-quality data to work with. However, in practice, it appears that simply making data available quickly - even if it is in a quirky, difficult-to-use, raw format is often valuable than trying to decide on the ideal data model up front.

The idea is similar to a **data warehouse**: simply bringing data from various parts of a large organisation together in one place is valuable, because it enables joins across datasets that were previously disparate.

SQL is completely relational, while your **data lakes** are completely unstructured — they can be any kind of data.

### Apache Spark

Large scale data processing engine that can run on Hadoop, Mesos, standalone, or in the cloud.

* Whereas Hadoop was a child of the cheap storage era, Spark is a child of the memory and network era.
* Spark can perform more efficient computations in less time using fewer machines than Hadoop.
* Its generalized abstractions result in less code.

**Cluster manager** manages resource distribution between different apps. **Yarn** and **Mesos** are two most widely used cluster managers in big data systems at the moment, Spark can run on either.

## Big data in the cloud

### GPUs on demand

* Unlike CPUs which consists of a few cores optimized for sequential serial processing, GPUs have a massively parallel architecture consisting of thousands of smaller, more efficient cores optimized for taking huge batches of data and performing the same operation over and over very quickly
* GPUs have thousands of compute cores and when coupled with lightning fast memory access they accelerate machine learning, gaming, database queries, video rendering and transcoding, computational finance, molecular dynamics and many other applications
* With GPUs in the cloud, your calculation-heavy applications can be scaled on elastic GPU clusters without building this into your own data centre

## Managed data services

* Azure Databricks 
  * Apache Spark-based big data analytics platform with the ability to run ML workloads (R, Python, Scala, Java) in Apache Spark workers
  * fully managed Apache Spark clusters with global scale and availability

* Azure HDInsight
  * on demand Hadoop type big data clusters 
  * requires cluster management

* Azure Data Factory
  * serverless data integration and transformation service
  * code free and code based ETL and ELT processes
  * orchestrate and monitor data pipelines

* AWS Glue 
  * serverless data integration service that provides both visual and code-based interfaces to discover, prepare, and combine data for analytics, machine learning and application development - targeted at Data Engineers
  * allows you to visually create, run and monitor ETL workflows in AWS Glue Studio
  * with AWS Glue DataBrew, data analysts and data scientists can visually enrich, clean, and normalize data without writing code
  * with AWS Glue Elastic Views, application developers can use SQL to combine and replicate data across different data stores

* Amazon Athena
  * serverless interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL - targeted at Data Athena
  * point to your data in Amazon S3, define the schema, and start querying using standard SQL, pay per query and the data scanned
  * integrated with AWS Glue Data Catalog

* Dataform (part of Google Cloud) 
  * Cloud warehouses store and process data cost effectively, meaning more and more companies are [moving away from an ETL to an ELT approach](https://dataform.co/etl-vs-elt) for managing analytical data. 
  * [Dataform](https://dataform.co) helps in converting captured data to curated data in BigQuery data warehouse
* Goolge BigQuery 
  * fully managed, serverless data warehouse that scales with your storage and computing power needs
* Google Cloud ML Engine
  * allows you to [train machine learning models](https://towardsdatascience.com/how-to-train-machine-learning-models-in-the-cloud-using-cloud-ml-engine-3f0d935294b3) in TensorFlow and other Python ML libraries (such as scikit-learn) without having to manage any infrastructure.
* Google Cloud Dataprep 
  * serverless service for visually exploring, cleaning, and preparing structured and unstructured data for analysis, reporting, and machine learning.

* Kaggle 
  * the *Github of Data Science*
  * allows users to find and publish data sets, explore and build models in a web-based data-science environment, work with other data scientists and machine learning engineers, and enter competitions to solve data science challenges  
  * offers a no-setup, customizable, Jupyter Notebooks environment for data analysis 
