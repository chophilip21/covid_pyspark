# from dash import Dash
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
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
from config import MAPBOX_ACCESSTOKEN

findspark.init()
findspark.find()

def init_map(server, data, case='cumulative_cases'):

    print('Initializing map instance....')

    #get figure
    fig = draw_fig(df=data, field=case)
    
    app = dash.Dash(server, routes_pathname_prefix='map')
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

    return app.server



def draw_fig(df=None, field='cumulative_cases', file_location='data/gpr_000b11a_e.shp'):

    data_df = df.copy()
    data_df.insert(1, "ID", [48, 59, 46, 13, 10, 12,
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

    print('preparing figure...')
    zmin = df_merged[field].min()
    zmax = df_merged[field].max()

    data = go.Choroplethmapbox(
        geojson=df_geo_json,
        locations=df_merged.index,
        z=df_merged[field],
        text=df_merged.province,
        colorbar=dict(thickness=20, ticklen=3),
        marker_line_width=1, marker_opacity=0.7, colorscale="Bluered",
        zmin=zmin, zmax=zmax,
        hovertemplate="<b>%{text}</b><br>" +
        "%{z}<br>" +
        "<extra></extra>")

    layout = go.Layout(
        mapbox1=dict(
            # domain={'x': [0, 1], 'y': [0, 1]},
            center=dict(lat=56.13, lon=-106.34),
            accesstoken=MAPBOX_ACCESSTOKEN,
            zoom=2),
        autosize=True,
        height=650,
        margin=dict(l=0, r=0, t=0, b=0))

    fig=go.Figure(data=data, layout=layout)

    # fig.write_image("data/fig1.svg")


    return fig

  
if __name__ == "__main__":
    spark = SparkSession.builder.appName('covid_19_cumulative').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    static_data = data_to_df('cumulative', spark)
    df = static_data.toPandas()

    draw_fig(df=df)
