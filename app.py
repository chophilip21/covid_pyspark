import socket
import requests_oauthlib
import numpy as np
import pandas as pd
import plotly.express as px
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark import SparkConf, SparkContext # these are for older Sparks. 
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fbprophet import Prophet
from data import * 
import findspark
import os


if __name__ == "__main__":

    findspark.init()
    findspark.find()

    #use below if you must
    os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_271.jdk/Contents/Home'
    spark = SparkSession.builder.appName('covid_19_analysis').getOrCreate()

    data = data_to_df('cumulative', spark)
    data.show(5)



