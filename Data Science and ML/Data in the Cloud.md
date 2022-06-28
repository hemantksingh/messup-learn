# Big data in the cloud

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
  * Cloud warehouses store and process data cost effectively, meaning more and more companies are [moving away from an ETL to an ELT approach](https://dataform.co/etl-vs-elt) for managing analytical data
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

## GPUs on demand

* Unlike CPUs which consists of a few cores optimized for sequential serial processing, GPUs have a massively parallel architecture consisting of thousands of smaller, more efficient cores optimized for taking huge batches of data and performing the same operation over and over very quickly
* GPUs have thousands of compute cores and when coupled with lightning fast memory access they accelerate machine learning, gaming, database queries, video rendering and transcoding, computational finance, molecular dynamics and many other applications
* With GPUs in the cloud, your calculation-heavy applications can be scaled on elastic GPU clusters without building this into your own data centre
