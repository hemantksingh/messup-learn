# Data Pipeline

A [data pipeline](https://www.youtube.com/watch?v=VtzvF17ysbc) facilitates [data flow management](https://docs.cloudera.com/HDPDocuments/HDF3/HDF-3.4.0/hdf-overview/content/overview.html) and fits into the "Curate" stage of your data analytics solution.

* Capture - ingest and aggregate data from different data sources
* Curate -  analyse, filter, transform, correlate and enhance data with processing tools e.g. R, Python
* Consume - interpret via visualization and reporting

## Data ingestion

[Data warehousing and BI system pipelines](https://www.thoughtworks.com/insights/blog/agile-data-warehousing-and-business-intelligence-action) typically employ batch processing to data that has been stored over a period of time. This may involve polling to periodically look for data changes and process data in batches. The processing results may be consumed for visualization and reporting after day(s) or maybe week(s). Batch processing follows sequential processing steps in a directed acyclic graph that is difficult to scale.

However if you are working in low latency scenarios where processing results in real time can affect business and security outcomes, [stream processing](https://medium.com/@gowthamy/big-data-battle-batch-processing-vs-stream-processing-5d94600d8103) will be your preferred choice. Examples of such cases are

* fraud detection systems to detect credit card usage patterns in streams of events
* trading systems to examine price changes in financial markets
* infrastructure monitoring to identify faults & security risks in machines
* military & intelligence systems to track potential signs of attack

As opposed to working with stored data, stream processing allows you to process the data as it arrives in real time e.g. while streaming audio/video content - the binary content is transmitted over the wire and processed in real time to be rendered for consumption.

### Data ingestion and transformation

Data transformation enables raw data to be converted into a format that can be used in data analytics and AI applications.

Logstash started out as a log aggregator for parsing text based files but has evolved into a [powerful data processing tool]( https://opensource.com/article/17/10/logstash-fundamentals) for data ingestion and transformation (aggregation, filtering and enrichment). At the core it is an ETL tool that can be configured to stream and transform multiple data sources into Elastic Search and [send data to over 70 O/Ps](https://www.elastic.co/blog/archiving-your-event-stream-with-logstash) including S3 buckets.

Logstash acts as an aggregator — pulling data from various sources before pushing it down the pipeline, usually into Elasticsearch but also into a buffering component in larger production environments. It’s worth mentioning that the latest version of Logstash also includes support for persistent queues when storing message queues on disk.

Filebeat, and the other members of the Beats family, acts as a lightweight agent deployed on the edge host, pumping data into Logstash for aggregation, filtering and enrichment. Filebeat is one of the best log file shippers out there today — it’s lightweight, supports SSL and TLS encryption, supports back pressure with a good built-in recovery mechanism, and is extremely reliable. It cannot, however, in most cases, turn your logs into easy-to-analyze structured log messages using filters for log enhancements. That’s the role played by Logstash.

Beats are used as lightweight agents installed on the different servers in your infrastructure for shipping logs or metrics. These can be

* log files (Filebeat)
* network metrics (Packetbeat)
* server metrics (Metricbeat)
* any other type of data - write your own (Libbeat)

![elastic-stack](../Images/elastic-log-shippers.jpg)

The ELK stack due to its impressive set of tooling has been a success in data analytics pipelines but [is elastic search a good fit for data science](https://towardsdatascience.com/elasticsearch-for-data-science-just-got-way-easier-95912d724636)?

Data scientists are generally not used to NoSQL database engines for common tasks or even relying on REST APIs for analysis. Dealing with large amounts of data using Elasticsearch’s low-level python clients, for example, is also not that intuitive and has somewhat of a steep learning curve for someone coming from a field different from Software Engineering. Although Elastic made significant efforts in enhancing the ELK stack for Analytics and Data Science use cases, it still lacked an easy interface with the existing Data Science ecosystem (pandas, numpy, scikit-learn, PyTorch,and other popular libraries).

Elasticsearch is trying to achieve widespread adoption in the data science industry, with the release of [Eland](https://eland.readthedocs.io/en/latest/), a brand new Python Elasticsearch client and toolkit with a powerful (and familiar) pandas-like API for analysis, ETL and Machine Learning. however the ELK stack Regression and Classification Machine learning jobs are still experimental.

#### Logstash and Fluentd

[Logz.io](https://logz.io/blog/fluentd-logstash/) provides a good comparison of the two log collectors. Logstash is most known for being part of the ELK Stack while Fluentd (part of CNCF) has become increasingly used by communities of users of software such as Docker, GCP and Elasticsearch.

![logstash-fluentd-comparison](../Images/logstash-fluentd-comparison.png)

Fluentd has built in reliability for persistence across restarts and has a configurable in-memory or on-disk buffering system while [Logstash is limited to an in-memory queue](https://platform9.com/blog/kubernetes-logging-comparing-fluentd-vs-logstash) that holds 20 events and, therefore, relies on an external persistence, like Redis.

[Logstash can have performance issues](https://logz.io/blog/filebeat-vs-logstash/), it requires JVM to run, and this dependency coupled with the implementation in Ruby became the root cause of significant memory consumption, especially when multiple pipelines and advanced filtering are involved.
