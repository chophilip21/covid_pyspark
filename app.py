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
os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_271.jdk/Contents/Home'


@app.route('/', methods=['POST', 'GET'])
def bar():

    spark = SparkSession.builder.appName('covid_19_analysis').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    static_data = data_to_df('cumulative', spark)

    df = static_data.toPandas()
    print(df.head(15))

    bar_labels = df.province # main labels

    active_cases = df.active_cases
    cumulative_cases = df.cumulative_cases # default


    # do we really need max values?
    # max_values = max(bar_values) + max(bar_values) * 0.1
    name = 'cumulative deaths' # For now TODO: update this dynamically. 

    return render_template('bar_test.html',
                           title=f'Canadian cumulative statistics up to {df.date[1]}', 
                           label_title=name, labels=bar_labels, values_default=cumulative_cases,
                           values_active = active_cases,
                           )


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080, debug=True)
