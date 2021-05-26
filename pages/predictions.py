# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import pandas as pd
from datetime import date
from tensorflow import keras
import numpy as np
import pickle
import sklearn

# Imports from this application
from app import app
from pred_lists import zip_code, neighborhood, amenities, property
from pred_lists import bathrooms_marks, amenities_marks
from airbnb_model import *
from model_tools_class import mt


# load model trained on airbnb data
model = keras.models.load_model('airbnb_model')
oe = mt.get_oe()
print('Model loaded successfully')


model_columns = [
    'property_type',
    'room_type',
    'bed_type',
    'cancellation_policy',
    'city',
    'host_identity_verified',
    'instant_bookable',
    'neighbourhood',
    'zipcode',
    'amenities',
    'accommodates',
    'bathrooms',
    'bedrooms',
    'beds',
    'host_since_days'
]


# create input form for User
row1 = html.Div(
    [
        # 1st Row. Introductory Marks
        dbc.Row(dbc.Col(html.Div('''Welcome to the Price Prediction Page! Fill out the form as
                                    accurately as possible, and we will compare similar
                                    properties (based on amenities and location) and
                                    provide you with the best estimate for your daily
                                    rental price on AirBnB.''', className='mb-4'))),
        # 2nd Row. Includes Property Type, Room Type
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Property Type", className='mb-1'),
                        dcc.Dropdown(
                            id='property',
                            options=property.property_type,
                            value='House',
                            className='mb-5',
                            style=dict(
                                width='60%',
                                verticalAlign="middle"
                            )
                        ),
                    ],

                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Room Type", className='mb-1'),
                        dcc.Dropdown(
                            id='room',
                            options=[
                                {'label': 'Entire Home/Apartment',
                                    'value': 'Entire home/apt'},
                                {'label': 'Private Room', 'value': 'Private room'},
                                {'label': 'Shared room', 'value': 'Shared room'}
                            ],
                            value='Entire home/apt',
                            className='mb-4',
                            style=dict(
                                width='70%',
                                verticalAlign="middle"
                            )
                        ),
                    ],
                ),
            ]
        ),
        # 3rd Row. Includes Accomadates, number of bathrooms
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Accomadates", className='mb-1'),
                        daq.NumericInput(
                            id='accomadates',
                            min=1,
                            max=16,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Number of Bathrooms",
                                     className='mb-1'),
                        dcc.Slider(
                            id='bathrooms',
                            min=0,
                            max=8,
                            step=0.5,
                            marks=bathrooms_marks.bathroom_marks,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 4th Row. Includes Bedrooms, Beds
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Number of Bedrooms",
                                     className='mb-1'),
                        daq.NumericInput(
                            id='bedrooms',
                            min=0,
                            max=10,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Number of Beds", className='mb-1'),
                        daq.NumericInput(
                            id='beds',
                            min=0,
                            max=18,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 5th Row. Includes bed_type, cancellation_policy
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Bed Type", className='mb-1'),
                        dcc.Dropdown(
                            id='bedtype',
                            options=[
                                {'label': 'Real Bed', 'value': 'Real Bed'},
                                {'label': 'Futon', 'value': 'Futon'},
                                {'label': 'Pull-out Sofa',
                                    'value': 'Pull-out Sofa'},
                                {'label': 'Airbed', 'value': 'Airbed'},
                                {'label': 'Couch', 'value': 'Couch'},
                            ],
                            value='Real Bed',
                            className='mb-4',
                            style=dict(
                                width='60%',
                                verticalAlign="middle"
                            )
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Cancellation Policy",
                                     className='mb-1'),
                        dcc.Dropdown(
                            id='cancellation',
                            options=[
                                {'label': 'Strict', 'value': 'strict'},
                                {'label': 'Flexible', 'value': 'flexible'},
                                {'label': 'Moderate', 'value': 'moderate'},
                                {'label': 'Super Strict 30',
                                    'value': 'super_strict_30'},
                                {'label': 'Super Strict 60',
                                    'value': 'super_strict_60'},
                            ],
                            value='flexible',
                            className='mb-4',
                            style=dict(
                                width='60%',
                                verticalAlign="middle"
                            )
                        ),
                    ],
                ),
            ]
        ),
        # 6th Row. Includes city
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### City", className='mb-1'),
                        dcc.Dropdown(
                            id='city',
                            options=[
                                {'label': 'New York City', 'value': 'NYC'},
                                {'label': 'Los Angeles', 'value': 'LA'},
                                {'label': 'San Francisco', 'value': 'SF'},
                                {'label': 'Washington DC', 'value': 'DC'},
                                {'label': 'Boston', 'value': 'Boston'},
                                {'label': 'Chicago', 'value': 'Chicago'},
                            ],
                            placeholder="Select a city",
                            className='mb-4',
                            style=dict(
                                width='55%',
                                verticalAlign="middle"
                            )
                        ),
                    ],
                ),
            ]
        ),
        # 7th Row. Includes host_identity_verified, instant_bookable, host_since_days
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown(
                            "##### You Are a Verified Host", className='mb-1'),
                        dcc.Dropdown(
                            id='bookable',
                            options=[
                                {'label': 'True', 'value': 'True'},
                                {'label': 'False', 'value': 'False'},
                            ],
                            value='True',
                            className='mb-4',
                            style=dict(
                                width='50%',
                                verticalAlign="middle"
                            )
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Is Instantly Bookable",
                                     className='mb-1'),
                        dcc.Dropdown(
                            id='verified_host',
                            options=[
                                {'label': 'True', 'value': 'True'},
                                {'label': 'False', 'value': 'False'},
                            ],
                            value='True',
                            className='mb-4',
                            style=dict(
                                width='60%',
                                verticalAlign="middle"
                            )
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Host Start Date",
                                     className='mb-1'),
                        dcc.DatePickerSingle(
                            id='days_host',
                            date=date(2019, 1, 1)
                        )
                    ],
                ),
            ]
        ),
        # 8th Row. Includes neighbourhood, zipcode
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Neighborhood", className='mb-1'),
                        dcc.Dropdown(
                            id='neighborhood',
                            options=neighborhood.neighborhoods,
                            placeholder="Select a Neighborhood",
                            className='mb-4',
                            style=dict(
                                width='70%',
                                verticalAlign="middle"
                            )
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Zipcode", className='mb-1'),
                        dcc.Dropdown(
                            id='zipcode',
                            options=zip_code.total_zip,
                            placeholder="Choose a ZipCode",
                            className='mb-4',
                            style=dict(
                                width='60%',
                                verticalAlign="middle"
                            )
                        ),
                    ],
                ),
            ]
        ),
        # 9th Row. Includes amenities
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Amenities", className='mb-1'),
                        dcc.Slider(
                            id='amenities',
                            min=0,
                            max=39,
                            step=1,
                            value=1,
                            marks=amenities_marks.amenity_marks,
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
    ]
)


# output section that returns estimated price based off inputs
row2 = html.Div(
    dbc.Col(
        [
            html.H2('Price Estimation', className='mb-5'),
        ]
    )
)


button = html.Div(
    [
        dbc.Button("Predict Price", id="example-button", color='primary',
                   className="mr-2"),
        html.Div(id='container-button-timestamp'),
        html.Span(id="example-output",
                  style={"vertical-align": "middle"}),
    ]
)


@app.callback(
    Output("container-button-timestamp",
           "children"), [Input("example-button", 'n_clicks')],
    [
        State('property', component_property='value'), State(
            'room', component_property='value'),
        State('accomadates', component_property='value'), State(
            'bathrooms', component_property='value'),
        State('bedrooms', component_property='value'), State(
            'beds', component_property='value'),
        State('bedtype', component_property='value'), State(
            'cancellation', component_property='value'),
        State('city', component_property='value'), State(
            'verified_host', component_property='value'),
        State('bookable', component_property='value'), State(
            'days_host', 'date'),
        State('neighborhood', component_property='value'), State(
            'zipcode', component_property='value'),
        State('amenities', component_property='value')
    ]
)
def on_button_click(n, property, room, accomadates, bathrooms, bedrooms, beds, bedtype, cancellation, city, verified_host, bookable, days_host, neighborhood, zipcode, amenities):
    '''
    on_button_click function passes information from the model on clicl
    '''
    if n is None:
        return "Not clicked."
    else:
        return predict(property, room, accomadates, bathrooms, bedrooms, beds, bedtype, cancellation, city, verified_host, bookable, days_host, neighborhood, zipcode, amenities)[0]


def predict(
    property, room, accomadates, bathrooms,
    bedrooms, beds, bedtype, cancellation,
    city, verified_host, bookable,
    days_host, neighborhood, zipcode, amenities
):
    '''
    predict function creates a dataframe and runs the dataframe in the
    get_prediction function
    '''
    df = pd.DataFrame(
        columns=[
            'property_type', 'room_type', 'accommodates', 'bathrooms',
            'bedrooms', 'beds', 'bed_type', 'cancellation_policy',
            'city', 'host_identity_verified', 'instant_bookable',
            'host_since_days', 'neighbourhood', 'zipcode', 'amenities'
        ],
        data=[
            [
                property, room, accomadates, bathrooms,
                bedrooms, beds, bedtype, cancellation,
                city, verified_host, bookable,
                days_host, neighborhood, zipcode, amenities
            ]
        ]
    )
    return get_prediction(df)


def get_confirm_df(input_list_objects, input_list_numbers, string_value_list):
    '''
    function to create confirmation df for viewing
    purposes for debugging
    '''
    df_rows = []
    for i in np.arange(9):
        df_rows.append(
            (model_columns[i], string_value_list[i], input_list_objects[0][i]))
    for i in np.arange(9, len(model_columns)):
        df_rows.append(
            (model_columns[i], input_list_numbers[i-9], input_list_numbers[i-9]))
    confirm_df = pd.DataFrame(
        df_rows, columns=['Variable', 'Value', 'Encoded'])
    return confirm_df


def get_prediction(df):
    '''
    function takes in a dataframe, transforms data, and runs 
    data into a sequential model to return a prediction 
    '''
    string_variable_list = ['property_type', 'room_type', 'bed_type',
                            'cancellation_policy', 'city', 'host_identity_verified',
                            'instant_bookable', 'neighbourhood', 'zipcode']
    number_variable_list = [
        'amenities', 'accommodates', 'bathrooms',
        'beds', 'bedrooms', 'host_since_days'
    ]

    number_value_list = []
    string_value_list = []

    for x in string_variable_list:
        string_value_list.append(df[x])
    for x in number_variable_list:
        if x != 'host_since_days':
            number_value_list.append(df[x].values[0])
        else:
            number_value_list.append(mt.get_days(df[x].values[0]))

    string_vectorized = oe.transform(
        np.array(string_value_list).reshape(1, -1))
    whole_input_vector = string_vectorized[0].tolist() + number_value_list
    confirm_df = get_confirm_df(
        string_vectorized, number_value_list, string_value_list)

    prediction = model.predict(np.array(whole_input_vector).reshape(1, -1))
    return prediction[0][0], confirm_df


def list_to_string(text):
    '''function to convert a list to a string'''
    str1 = ""
    for x in text:
        str1 += str(x)
    return str1


def get_confirm_df(input_list_objects, input_list_numbers, string_value_list):
    '''
    function to create confirmation df for viewing
    purposes for debugging
    '''
    df_rows = []
    for i in np.arange(9):
        df_rows.append(
            (model_columns[i], string_value_list[i], input_list_objects[0][i]))
    for i in np.arange(9, len(model_columns)):
        df_rows.append(
            (model_columns[i], input_list_numbers[i-9], input_list_numbers[i-9]))
    confirm_df = pd.DataFrame(
        df_rows, columns=['Variable', 'Value', 'Encoded'])
    return confirm_df


# layout of the page
layout = dbc.Row([row1, row2, button])
