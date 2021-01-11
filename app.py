import numpy as np
import pandas as pd
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from fbprophet import Prophet
from data import *
import findspark
import os
from flask import Flask, jsonify, request
from flask import render_template
from flask_caching import Cache
from forecast import prophet_forecast
# from pyspark import SparkConf, SparkContext # these are for older Sparks.
# from pyspark.streaming import StreamingContext

cache = Cache(config={'CACHE_TYPE': 'simple'})
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
findspark.init()
findspark.find()
cache.init_app(app)
os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_271.jdk/Contents/Home'

@app.route('/', methods=['POST', 'GET'])
@cache.cached(timeout=300)
def cumulative():

    spark = SparkSession.builder.appName('covid_19_cumulative').getOrCreate()
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

@app.route('/forecast', methods=['POST', 'GET'])
@cache.cached(timeout=300)
def timeseries():

    spark = SparkSession.builder.appName('covid_19_time_series').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    alberta_df, bc_df, quebec_df, ontario_df  = data_to_df('time_series', spark)

    alberta_df = alberta_df.toPandas()
    bc_df =  bc_df.toPandas()
    quebec_df = quebec_df.toPandas()
    ontario_df = ontario_df.toPandas()

    # label are the dates here 
    bar_labels = alberta_df.date_report 

    # values (daily)
    alberta_cases = alberta_df.cases
    bc_cases = bc_df.cases
    quebec_cases = quebec_df.cases
    ontario_cases = ontario_df.cases

    #! I may use these values in the future
    # alberta_cumulatve = alberta_df.cumulative_cases
    # bc_cumulative = bc_df.cumulative_cases
    # quebec_cumulative = quebec_df.cumulative_cases
    # ontario_cumulative = ontario_df.cumulative_cases

    #prediction value
    alberta_prediction, new_dates = prophet_forecast(alberta_df)
    bc_prediction, _ = prophet_forecast(bc_df)
    ontario_prediction, _ = prophet_forecast(quebec_df)
    quebec_prediction, _ = prophet_forecast(ontario_df)

    return render_template('timeseries.html',
                           title=f'Daily COVID-19 cases from {bar_labels.iloc[1]} up to {bar_labels.iloc[-1]}', 
                           labels=bar_labels, forecast_labels= new_dates, values_alberta=alberta_cases, 
                           forecast_alberta = alberta_prediction, values_bc = bc_cases, forecast_bc = bc_prediction, 
                           values_quebec = quebec_cases, forecast_quebec = ontario_prediction, values_ontario = ontario_cases, 
                           forecast_ontario = quebec_prediction,
                           )

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080, debug=True)
