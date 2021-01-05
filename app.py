import socket
import requests_oauthlib
import numpy as np
import pandas as pd
import plotly.express as px
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fbprophet import Prophet
from data import *
import findspark
import os
from flask import Flask, jsonify, request
from flask import render_template
# from pyspark import SparkConf, SparkContext # these are for older Sparks.
# from pyspark.streaming import StreamingContext


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
findspark.init()
findspark.find()
# os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_271.jdk/Contents/Home'

@app.route('/', methods=['POST', 'GET'])
def bar():

    spark = SparkSession.builder.appName('covid_19_analysis').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    static_data = data_to_df('cumulative', spark)

    df = static_data.toPandas()
    print(df.head(15))

    # label
    bar_labels = df.province 

    # values
    active_cases = df.active_cases
    cumulative_cases = df.cumulative_cases # default
    cumulative_tested = df.cumulative_tested
    cumulative_deaths = df.cumulative_deaths
    vaccine_administration = df.vaccine_administration
    cumulative_recovered = df.cumulative_recovered


    return render_template('cumulative.html',
                           title=f'Canadian cumulative statistics up to {df.date[1]}', 
                           labels=bar_labels, values_default=cumulative_cases,
                           values_active_cases = active_cases, values_cumulative_cases = cumulative_cases,
                           values_cumulative_tested = cumulative_tested, values_cumulative_deaths= cumulative_deaths,
                           values_vaccine = vaccine_administration, values_cumulative_recovered = cumulative_recovered 
                           )


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080, debug=True)
