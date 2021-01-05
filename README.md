# covid_pyspark

This repository uses Python API of Apache Spark for processing COVID-19 related data. It uses Python Flask for backend, and Javascript for the front. 

## Live Demo

Link for the live demo and screen shot will goo here. 

## How do run
This repository assumes that you have already configured Apache Spark, JAVA, Scala environment properly. 
If not, you can refer to some of the guides available online like the following: https://phoenixnap.com/kb/install-spark-on-ubuntu

Now if you want to test out my code, do the following:

Create Python 3.8 virtual env first by running

```
python3.8 -m venv env
```
Install requirements by running

```
pip install -r requirements.txt
```
and then run:
```
python app.py
```

<!-- 
## Data Streaming using Apache Spark

Traditionally, when people think about data streaming, terms such as “real-time,” “24/7,” or “always on” come to mind. But you may have cases where data only arrives at fixed intervals. That is, data appears every hour or once a day, and COVID-19 data is only updated once a day as well. Nevertheless, we cannot say that the nature of our data is static, and therefore it is still beneficial to perform incremental processing on this data. However, it would be wasteful to keep a cluster up and running 24/7 just to perform a short amount of processing once a day. We can minimze the waste using trigger feature in Pyspark structured streaming. 

Structured streaming has benefit over traditional batch based streaming in that you do not have to deal with figuring out what data is new, what you should process, and what you should not.

## Kafka 

Kafka is an event streaming platform, which acts as a database in this case. Here, we pulish and subscribe to streams of events, similar to a message queue or enterprise messaging system. You can also store streams of events in a fault-tolerant storage as long as you want (hours, days, months, forever). -->