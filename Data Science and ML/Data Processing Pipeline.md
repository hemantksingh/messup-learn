# Data Pipeline

* Capture - ingest and aggregate data from different data sources
* Curate -  analyse, filter, transform, correlate and enhance data with processing tools e.g. R, Python
* Consume - interpret via visualization and reporting

## Data ingestion

[Data warehousing and BI system pipelines](https://www.thoughtworks.com/insights/blog/agile-data-warehousing-and-business-intelligence-action) typically employ batch processing to data that has been stored over a period of time. This may involve polling to periodically look for data changes and process data in batches. The processing results may be consumed for visualization and reporting after day(s) or maybe week(s).

However if you are working in low latency scenarios where processing results in real time can affect business and security outcomes, [stream processing](https://medium.com/@gowthamy/big-data-battle-batch-processing-vs-stream-processing-5d94600d8103) will be your preferred choice. Examples of such cases are

* fraud detection systems to detect credit card usage patterns in streams of events
* trading systems to examine price changes in financial markets
* infrastructure monitoring to identify faults & security risks in machines
* military & intelligence systems to track potential signs of attack

As opposed to working with stored data, stream processing allows you to process the data as it arrives in real time e.g. while streaming audio/video content - the binary content is transmitted over the wire and processed in real time to be rendered for consumption.

## Data processing

Logstash started out as a log aggregator for parsing text based files but has evolved into a [powerful data processing tool]( https://opensource.com/article/17/10/logstash-fundamentals) for data ingestion and transformation. At the core it is an ETL tool that can be configured to stream and transform multiple data sources into Elastic Search and [send data to over 70 O/Ps](https://www.elastic.co/blog/archiving-your-event-stream-with-logstash) including S3 buckets. 

The ELK stack due to its impressive set of tooling has been a success in data analytics pipelines but what about [elastic search for data science](https://towardsdatascience.com/elasticsearch-for-data-science-just-got-way-easier-95912d724636)?

Data scientists are generally not used to NoSQL database engines for common tasks or even relying on REST APIs for analysis. Dealing with large amounts of data using Elasticsearch’s low-level python clients, for example, is also not that intuitive and has somewhat of a steep learning curve for someone coming from a field different from Software engineering. Although Elastic made significant efforts in enhancing the ELK stack for Analytics and Data Science use cases, it still lacked an easy interface with the existing Data Science ecosystem (pandas, numpy, scikit-learn, PyTorch,and other popular libraries).

Elasticsearch is trying to achieve widespread adoption in the data science industry, with the release of [Eland](https://eland.readthedocs.io/en/latest/), a brand new Python Elasticsearch client and toolkit with a powerful (and familiar) pandas-like API for analysis, ETL and Machine Learning. however the ELK stack Regression and Classification Machine learning jobs are still experimental.


## Analytics and modelling

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
