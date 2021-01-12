from dash import Dash
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from urllib.request import urlopen
import json
import numpy as np


# with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/canada.geojson') as response:
#     provinces = json.load(response)

data = {'provinces': ['Alberta','British Columbia', 'Manitoba', 'New Brunswick',
'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon'], 'deaths':
[200, 150, 30, 15, 10, 2, 5, 4, 450, 3, 600, 30, 15], 'catodb_id': np.arange(1,14)}

df = pd.DataFrame.from_dict(data)


fig = go.Figure(data=go.Choropleth(
    locations=df['catodb_id'], # Spatial coordinates
    z = df['deaths'].astype(float), # Data to be color-coded
    locationmode = 'geojson-id', # set of locations match entries in `locations`
    colorscale = 'Reds',
    autocolorscale=False,
    text= df['deaths'],
    marker_line_color='white',
    colorbar_title = "Cumulative deaths",
))

fig.update_layout(
    title_text = 'Cumulative deaths by provinces',
    geo_scope='north america', # limite map scope to USA
)

fig.show()


if __name__ == "__main__":
    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    app.run_server(debug=True, use_reloader=True)


    data = {'provinces': ['Alberta','British Columbia', 'Manitoba', 'New Brunswick',
    'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia', 'Nunavut',
    'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon'], 'deaths':
    [200, 150, 30, 15, 10, 2, 5, 4, 450, 3, 600, 30, 15], 'catodb_id': np.arange(1,14)}

    df = pd.DataFrame.from_dict(data)

    print(df)