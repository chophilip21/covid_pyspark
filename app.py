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
from flask import Flask,jsonify,request
from flask import render_template
# from pyspark import SparkConf, SparkContext # these are for older Sparks. 
# from pyspark.streaming import StreamingContext



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/', methods = ['POST', 'GET'])
def bar():

    bar_labels=df.province
    bar_values= df.cumulative_cases

    if request.method == 'POST':
        try:
            formulier = request.json
            action = formulier["action"];

            print('requested action:', action)

            bar_values = df[action]

        except TypeError:
            print('INVALID Type')
        
        
    print('what is the bar value now..?', bar_values)
    max_values = max(bar_values) + max(bar_values) * 0.1

    return render_template('bar_test.html')

    # return render_template('bar_test.html', title= f'Canadian cumulative deaths from COVID-19 up to {df.date[1]}', max=max_values, labels=bar_labels, values=bar_values)

@app.route('/active_cases')
def data():
    return df.active_cases.to_jso



if __name__ == "__main__":

    findspark.init()
    findspark.find()

    #use below if you must
    # os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_271.jdk/Contents/Home'
    spark = SparkSession.builder.appName('covid_19_analysis').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    static_data = data_to_df('cumulative', spark)

    df = static_data.toPandas()

    print(df.head(15))

 
    app.run(host='0.0.0.0', port=8080, debug=True)