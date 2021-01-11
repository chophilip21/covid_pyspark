# Covid_pyspark

This repository uses Python API of Apache Spark for processing real-time COVID-19 related data. It uses Python Flask for back-end API, and Javascript (Chart.js) for the front-end visualization. This Flask App contains two pages, one for <b>cumulative real time stats</b> taken from following open source provider: https://opencovid.ca/api/, and another for <b>time-series forecasting</b> based on Facebook Prophet.  

## Live Demo (A. Cumulative, B. Time series forecasting)

![Cumulative](sample/cumulative.gif)

![Time_series](sample/time_series.gif)


## How to run the code
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

## Future Improvements

The original plan was to use Spark Structured Streaming for processing the data, supported with Apache Kafka. Nevertheless, unlike dynamic data like stock price that changes every minute, Covid-19 data is only updated once a day and I thought using structured streaming for local server project is a bit of overkill. Future plans include uploading the project on live server and use structured streaming.

Next, COVID-19 data is extremely volatile as forecasting this accurately will require immense amount of data, including multi-variate information like population density, provincial government covid-19 related policy changes, and such. Even the ground-truth value itself is quite irregular, as despite it being updated every single day, the counts are tallied in temporarily irregular basis. Nonetheless, regurlarily updated data are extremely scarce, and thus the forecasting logic solely based on univariate time series (12 months data of cases) that is readily available. When this project gets updated in the future, forecasting logic will also be revised, and other models like ARIMA, VAR, or even RNN based Neural Networks may be examined.   
