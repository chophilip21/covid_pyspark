# from dash import Dash
# import plotly.graph_objects as go
import plotly.express as px
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
import os
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
from data import *
import findspark
from mpl_toolkits.axes_grid1 import make_axes_locatable

findspark.init()
findspark.find()
os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_271.jdk/Contents/Home'


def init_dashboard(server=None, field='cumulative_cases', file_location='data/gpr_000b11a_e.shp'):

    # get data from the Spark session TODO: replace this with dataframe
    spark = SparkSession.builder.appName('covid_19_map').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    static_data = data_to_df('cumulative', spark)
    data_df = static_data.toPandas()
    data_df.insert(1, "ID", [48, 24, 46, 13, 10, 12,
                             62, 61, 35, 11, 24, 47, 60], True)

    # get map data using geopandas
    print('reading shp file to make map data...')
    can = gpd.read_file(file_location)
    can_df = can.astype({'PRUID': 'int64'})

    # merge
    df_merged = pd.merge(can_df[['PRUID', 'geometry']], data_df[[
                         'ID', field, 'province']], left_on='PRUID', right_on='ID', how='left')
    df_merged = df_merged.dropna(subset=[field, 'geometry']).set_index('PRUID')
    df_merged = df_merged.drop(['ID'], axis=1)
    print(df_merged.head(14))

    # Convert geopandas to GeoJSON for plotly
    df_merged = df_merged.to_crs(epsg=4326)
    df_geo_json = df_merged.__geo_interface__

    fig = px.choropleth(df_merged, geojson=df_geo_json,
                        locations=df_merged.index, color=field, projection='mercator', 
                        hover_name='province', hover_data=['province', field])

    # fig.update_geos
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
    fig.show()

if __name__ == "__main__":

    init_dashboard()
