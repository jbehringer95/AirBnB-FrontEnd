# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app


# 2 column layout. 1st column width = 4/12
column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## What could you earn as an Airbnb host?
            Have a property that you want to list on Airbnb?
            The Airbnb Price Calculator can help you determine
            how much to list your property for. We analyze listings
            in your area and compare ammenities to calculate the
            best price for your listing. Click the button below
            and start making money today!

            """
        ),
        dcc.Link(
            dbc.Button('Predict Your Price', color='primary'),
            href='/predictions'
        )
    ],
    md=4,
)


column2 = dbc.Col(
    [
        html.Img(src='assets/houses.jpeg', width='700px', height='470px'),
    ]
)

layout = dbc.Row([column1, column2])
