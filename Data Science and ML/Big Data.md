# Aspects of big data

* Data that is too big (100s of TB - x PB) or moves too fast to be processed by conventional means (too big of OLTP).
* Three Vs

    * Volume -  Data too big to fit on a single machine
    * Velocity - The rate at which the data comes into the system and the velocity of the output of the system matters. The tighter the feedback loop, the greater is the competitive advantage. The results might go directly into a product e.g. – Facebook recommendations. The need of speed has also driven the development of NoSQL databases where RDBMS' aren’t the right fit.
    * Variety - The data being generated can be unstructured with a format that is outside your control. A common use of big data processing is to take unstructured data and extract meaning out of it for either human consumption or as a structured input to another application.  Relational databases with their fixed schemas aren’t always a natural fit for storing such data. Semi-structured NoSQL databases provide the flexibility to store unstructured data that has less formal schema.

* Partition a big dataset into multiple smaller datasets and send each chunk of the data to a separate node in a cluster to be processed individually and in parallel.

## Data Warehousing and BI

Capture (Ingest Data Sources) -> Curate (Prepare & Analyze) -> Consume (Publish & Visualize)

https://www.thoughtworks.com/insights/blog/agile-data-warehousing-and-business-intelligence-action

## Background processing

[Stream processing or Batch processing](https://medium.com/@gowthamy/big-data-battle-batch-processing-vs-stream-processing-5d94600d8103)?

Stream processing processes the data as it comes in real time e.g. stream audio/video content online the binary content is transmitted over the wire and processed in real time to be rendered for consumption. Stream processing is applicable in low latency scenarios where processing results in real time can affect business and security outcomes e.g.

* fraud detection systems to detect credit card usage patterns in streams of events
* trading systems to examine price changes in financial markets
* monitoring systems to identify faults in machines
* military & intelligence systems to track potential signs of attack

Batch processing processes the data (that has been stored over a period of time) once. It may employ polling to periodically look for data changes and process data in batches. The processing results may be utilized after day(s) or maybe week(s).

what is the use case - [scalable machine learning](https://dzone.com/articles/build-and-deploy-scalable-machine-learning-in-prod)?

* do you want to deploy the new model in production in real time (as soon as it is built)?
* is latency of the model build process an issue?
* is the ordering of messages important?
* analytics of fuel prices and sales volume streams ? - adopt stream analytics (aggregations and statistical metrics over a large number of events) Many open source distributed stream processing frameworks are designed with analytics in mind - Apache Storm, Spark Streaming, Samza and Kafka streams
* monitoring in place for analysing the outcomes of the applied model?
* single model per tenant or a single model for the entire system?

## Technologies

Databases require you to structure data according to a particular model (e.g. relational or documents) whereas files in a distributed filesystem are just byte sequences which can be written using any data model and encoding. They might be collections of database records but they can equally well be text, images, videos, sensor readings, genome sequences or any other kind of data.

Hadoop opened up the possibility of indiscriminately dumping data into HDFS, and only later figuring out how to process it further. By contrast, MPP (Massively Parallel Processing) databases typically require careful **up-front modelling** of the data and query patterns before importing the data into the database's proprietary storage format.

From a purist's point of view, it may seem that careful modelling and import is desirable, because it means the users of the database have better-quality data to work with. However, in practice, it appears that simply making data available quickly - even if it is in a quirky, difficult-to-use, raw format - is often valuable than trying to decide on the ideal data model up front.

The idea is similar to a **data warehouse**: simply bringing data from various parts of a large organisation together in one place is valuable, because it enables joins across datasets that were previously disparate.

SQL is completely relational, while your **data lakes** are completely unstructured — they can be any kind of data.

### MapReduce

Map: split the data and distribute the computation over multiple servers in parallel. For that computation to take place each server must have access to the data. The Hadoop distributed file system (HDFS) makes this possible.

Reduce: take the O/P from the map phase (in a key value format) and aggregate the results

### Hadoop

Hadoop is a platform for distributing computing across a number of servers in a cluster. It is an open source implementation of MapReduce. It combines a **MapReduce** engine with a **Hadoop distributed file system (HDFS)**. HDFS allows the disks local to individual nodes in a Hadoop cluster to operate as a single pool of storage. Files are replicated across various nodes so that loss of one node will not cause loss of data. Facebook uses Hadoop. A MySQL database stores the core data which is derived on to Hadoop servers. After computations the data is then transferred to MySQL database for pages served to the users.

![hadoop-stack.png](../Images/hadoop-stack.png "Hadoop Stack")

### Apache Spark

Large scale data processing engine that can run on Hadoop, Mesos, standalone, or in the cloud.

* Whereas Hadoop was a child of the cheap storage era, Spark is a child of the memory and network era.
* Spark can perform more efficient computations in less time using fewer machines than Hadoop.
* Its generalized abstractions result in less code.

**Cluster manager** manages resource distribution between different apps. **Yarn** and **Mesos** are two most widely used cluster managers in big data systems at the moment, Spark can run on either.

## Big data in the cloud

GPUs have a massively parallel architecture consisting of thousands of smaller, more efficient cores optimized for taking huge batches of data and performing the same operation over and over very quickly, unlike CPUs which consists of a few cores optimized for sequential serial processing.

GPUs have thousands of compute cores and when coupled with lightning fast memory access they accelerate machine learning, gaming, database queries, video rendering and transcoding, computational finance, molecular dynamics and many other applications. With GPUs in the cloud, you can scale your calculation-heavy applications without constructing your own data centre.

Supercomputer power with GPUs on demand

Shazam - music recognition app that uses Google cloud.
Audio recognition algorithm runs on GPUs. Google provides elastic GPU clusters.

### Azure Data Bricks

Big data analytics and AI with the ability to run ML workloads (R, Python, Scala, Java) in Apache Spark workers. [Azure databricks](https://azure.microsoft.com/en-gb/services/databricks/) allows you to spin up clusters in a fully managed Apache Spark environment with global scale and availability.

### Azure HDInsight

Hadoop type big data clusters on demand, require cluster management.

### Goolge BigQuery

Google's fully managed, serverless data warehouse that scales with your storage and computing power needs.

### Google Cloud ML Engine

Cloud ML Engine allows you to [train machine learning models](https://towardsdatascience.com/how-to-train-machine-learning-models-in-the-cloud-using-cloud-ml-engine-3f0d935294b3) in TensorFlow and other Python ML libraries (such as scikit-learn) without having to manage any infrastructure.

### Google Cloud Dataprep

Data service for visually exploring, cleaning, and preparing structured and unstructured data for analysis, reporting, and machine learning.

### Kaggle

Kaggle is the *Github of Data Science*

It offers a no-setup, customizable, Jupyter Notebooks environment. It allows users to find and publish data sets, explore and build models in a web-based data-science environment, work with other data scientists and machine learning engineers, and enter competitions to solve data science challenges

## Data Analysis Pipeline

* Capture - aggregate
* Curate - analyse via processing tools like R, Python
* Consume - interpret via visualization and reporting

### Stages of Analytics

* Descriptive
* Diagnostic
* Predictive
* Prescriptive - Prescribe options to consumers

### Modelling

Overtraining the models can lead to information loss. Generic ML models that are based on a wider data set e.g. a model per geographical region than a gas site provide better results.
  