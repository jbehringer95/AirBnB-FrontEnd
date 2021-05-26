import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
from pred_lists import zip_code
from os import getenv

token = "pk.eyJ1Ijoicm93aXR0IiwiYSI6ImNrcDR4NHpzeDA1eDgybnA5bm42enhuYW0ifQ.W4P1yyHS0GIiEi6IGNkobg" # you will need your own token

df = px.data.election()
df2 = pd.read_csv('assets/train.csv',
                    dtype={'zipcode':str})
geojson = px.data.election_geojson()
geojson2 = 'assets/GeoCells.json'
with open(geojson2) as f:
    data = json.load(f)
candidates = df.winner.unique()


from app import app



@app.callback(
    Output("choropleth", "figure"), 
    [Input("zipcode", "value")])
def display_choropleth(value):
    lati, longi = check(value)
    if len(lati) != 0:
        lti = lati.iloc[1]
        lgi = longi.iloc[1]
    else:
        lti = 40.78919
        lgi = -73.96236
    fig = px.choropleth_mapbox(
        df2, geojson=data,
        locations="zipcode", featureidkey="properties.ZCTA5CE10",
        color='review_scores_rating',
        center={"lat": lti, "lon": lgi}, zoom=11,
        range_color=[0, 100])
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken=token)

    return fig



layout = html.Div([
    html.P("Rental Zip Code:"),
    dcc.Dropdown(
        id='zipcode', 
        options=zip_code.total_zip,
        value=zip_code.total_zip[1]['value']
        #labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
])


def check(inp):

    one = df2.loc[df2.zipcode == str(inp)]
    olat = one['latitude']
    olong = one['longitude']
    return olat, olong


# # 




    #     dcc.Markdown("##### Zipcode", className='mb-1'),
    # dcc.Dropdown(
    #     id='zipcode',
    #     options=zip_code.total_zip,
    #     className='mb-4'
    # ),