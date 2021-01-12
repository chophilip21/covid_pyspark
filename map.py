# from dash import Dash
# import plotly.graph_objects as go
# import plotly.express as px
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px
import os
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from data import *
import findspark

findspark.init()
findspark.find()
os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_271.jdk/Contents/Home'

def init_dashboard(server=None, field='cumulative_cases', file_location='data/gpr_000b11a_e.shp'):

    # get data from the Spark session
    spark = SparkSession.builder.appName('covid_19_map').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    static_data = data_to_df('cumulative', spark)
    data_df = static_data.toPandas()
    data_df.insert(1, "ID", [48, 24, 46, 13, 10, 12, 62, 61, 35, 11, 24, 47, 60], True) 

    #get map data
    print('reading shp file to make map data...')
    can = gpd.read_file(file_location)
    can_df = can.astype({'PRUID': 'int64'})
 
    #merge
    df_merged = pd.merge(data_df[['ID', field, 'province']], can_df[['PRUID', 'geometry']], left_on='ID', right_on='PRUID', how='left')
    df_merged = df_merged.dropna(subset=[field, 'geometry']).set_index('ID')
    print(df_merged.head(14))




if __name__ == "__main__":

    init_dashboard()
 

 

  




 