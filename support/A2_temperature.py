# -*- coding: utf-8 -*-
"""
.. module:: Chris
    :platform: Windows 7, Python 3.7.
    :synopsis: This module holds the functions developed by Kirodh Boodhraj.
.. moduleauthor:: Kirodh Boodhraj <kboodhraj@csir.co.za>


"""

# import system modules here:
import datetime as dt
import pathlib as pl
import sys

# import other modules here:
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import dash_table as tab
from dash.dependencies import Input, Output
from app import app
import pandas as pd
import numpy as np
import xarray as xr

## functions go here:
###############################################
# open netcdf file:
def open_netcdf(fileName, debug=False):
    """
        Purpose: Open a file using xarray.

        :param fileName: The numpy array containg the latitude data.
        :type fileName: str
        :keyword debug: Boolean to print debug information.
        :type debug: bool

        Returns:
        (tuple): tuple containing:

            data (str): The data from file as xarray object

        How to use this function

        >>> openNetcdf("theFile.nc")
        """

    data = xr.open_dataset(fileName)
    if debug: print("Opened netcdf data as xarray: ", data)
    data.close()
    return data

# get data from a variable from xarray datatype
def get_variable(data, variableName, debug=False):
    """
        Purpose: get data using xarray.

        :param data: The xarray data.
        :type data: float
        :param variableName: The variable name wanted.
        :type variableName: str
        :keyword debug: Boolean to print debug information.
        :type debug: bool

        Returns:
        (tuple): tuple containing:
            data (str): The data from file as numpy object

        How to use this function

        >>> getVariable(data,"theVariable")
        """

    variableData = data[variableName].values
    if debug: print("Extracted data from NetCDF: ", variableData)
    if debug: print("Dimension of data: ", variableData.shape)

    return variableData


# get the temperature data:
def get_temperature_data(debug=False):
    # path to data:
    path = pl.Path("support/data/tempSalineNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path)
    if debug: print(data)
    # extract data: dimensions
    temperature = get_variable(data,"votemper")
    if debug: print(temperature)
    return temperature


# get the time data:
def get_time_data(debug=False):
    # path to data:
    path = pl.Path("support/data/tempSalineNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path)
    if debug: print(data)
    # extract data:
    time = get_variable(data, "time_counter")
    if debug: print(time)
    # get todays date and make a forecast out of it
    today = dt.datetime.today()
    # generate a pandas series of dates and times
    dates = pd.date_range(today, periods=len(time),freq="60min")
    return dates


# get the depth data:
def get_depth_data(debug=False):
    # path to data:
    path = pl.Path("support/data/tempSalineNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path)
    if debug: print(data)
    # extract data:
    depth = get_variable(data, "deptht")
    if debug: print(depth)
    return depth

# get the depth data:
def get_lat_data(debug=False):
    # path to data:
    path = pl.Path("support/data/tempSalineNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path)
    if debug: print(data)
    # extract data:
    lat = get_variable(data, "nav_lat")
    if debug: print(lat)
    return lat

# get the depth data:
def get_lon_data(debug=False):
    # path to data:
    path = pl.Path("support/data/tempSalineNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path)
    if debug: print(data)
    # extract data:
    lon = get_variable(data, "nav_lon")
    if debug: print(lon)
    return lon

# all data:
temp_data = get_temperature_data()
time_data = get_time_data()
depth_data = get_depth_data()
longitude = get_lon_data()
latitude = get_lat_data()
# mapbox token:
# mapbox_access_token = "sk.eyJ1Ijoia2lyb2RoIiwiYSI6ImNrMDVjbHd2ejBzenczbnBuemUxZGxjM3gifQ.uEjF3QBfWY8xToNwU5NHKg" # my own one
mapbox_access_token = "pk.eyJ1Ijoia2lyb2RoIiwiYSI6ImNrMDVjaWY0ZzBqaXAzbXFvenp3OWVpd2MifQ.apsaN8lTiMfqgsOArDA5Xg" # public




###############################################
# put the dash layout here
# ...

# defaults (leave these alone):
header_logo = html.A([html.Img(id="logo",src=app.get_asset_url('oceans21logo_small.png'),
                    style={
                    'height' : '15%',
                    'width' : '15%',
                    'float' : 'right',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-right' : 0
                })],href="https://www.csir.co.za",target="_blank")

header_text = html.H1('Temperature')



# these are yours :-)
# intro text:
intro = html.Div(["This page displays forecasted hourly temperature data. Use the sliders to change between the various "
                  "depths and time steps. The resulting temperature profiles will be displayed for the point chosen "
                  "on the graph."])

# layout for main temperature graph:
# for mapbox layout
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        # accesstoken=mapbox_access_token,
        style="open-street-map",  # streets, light dark satellite outdoors satellite-streets
        center=dict(lon=25, lat=-30),
        zoom=1,
    ),
)

# print(longitude[0,:])
# print(latitude[:,0])
trace = [dict(
            type="densitymapbox",
            lon=longitude[0,:],
            lat=latitude[:,0],
            # text="hello",
            z=temp_data[0,0,:,:],
            # name="the name",
            marker=dict(size=4, opacity=0.6)
        )]


# main temperature graph:
temperature_graph = dcc.Graph(
    id='temperature_graph',
    className="temperatureGraph",

    figure={
        # 'data':{'type':"scattermapbox"},


        'data':trace,
        # 'data': [
        #     {'x': [0, 2, 3], 'y': [40, 1, 2],
        #      'type': 'bar', 'name': 'SF'},
        #     {'x': [0, 2, 3], 'y': [2, 4, 5],
        #      'type': 'bar', 'name': u'Montréal'},
        # ],
        'layout': layout
    }
)


time_slider = dcc.Slider(
    min=0,
    max=len(get_time_data())-1,
    value=0,
    marks={ i:{'label': str(i), 'style': {'color': 'black'}} for i in range(len(get_time_data()))},
    included=False,
    className="timeSlider"
)

depth_slider = dcc.Slider(
    min=0,
    max=len(get_depth_data())-1,
    value=0,
    marks={i:{'label': str(i), 'style': {'color': 'black'}} for i in range(len(get_depth_data()))},
    included=False,
    vertical= True,
    tooltip={"placement": "topLeft"},
    className="depthSlider"

)

# themometer to show temperature:
themometer = daq.Thermometer(
    id='thermometer',
    className = "thermometer",
    value=0,
    min=0,
    max=40,
    # style={'height': '100vh'},
    color = " #f83a3a",
    showCurrentValue=True,
    units="C",
    # size= '25%'#300,
    # labelPosition = "top",
    # label="hello"
)

# a block with all the required indicators:
indicators = html.Div(id="tempIndicators",className="tempIndicators",children=[
    html.Div(id="surfaceMaxT",children=["Surface Maximum Temperature = 0.0 deg C"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="surfaceMinT", children=["Surface Minimum Temperature = 0.0 deg C"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="surfaceAvgT", children=["Surface Average Temperature = 0.0 deg C"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="depthAvgT", children=["Depth Average Temperature = 0.0 deg C"],style={'padding-left':"5vw",'padding-top':"5vh",'padding-bottom':"5vh"})
    # html.Div(id="surfaceMaxT", children=["Surface Maximum Temperature = 0.0 deg C"]),
    # html.Div(id="surfaceMaxT", children=["Surface Maximum Temperature = 0.0 deg C"])
])

# line graph for temperature forecast:
forecast_temperature_line_graph = dcc.Graph(
    id='temperature_forecast_line_graph',
    figure={
        'data': [
            {'x': [0, 2, 3], 'y': [40, 1, 2],
             'type': 'bar', 'name': 'SF'},
            {'x': [0, 2, 3], 'y': [2, 4, 5],
             'type': 'bar', 'name': u'Montréal'},
        ]
    }
)

# line graph for depth profile:
depth_temperature_line_graph = dcc.Graph(
    id='temperature_depth_line_graph',
    figure={
        'data': [
            {'x': [0, 2, 3], 'y': [40, 1, 2],
             'type': 'bar', 'name': 'SF'},
            {'x': [0, 2, 3], 'y': [2, 4, 5],
             'type': 'bar', 'name': u'Montréal'},
        ]
    }
)

## this is where all your elements come together:
layout = html.Div([
    # header (leave alone):
    header_logo,
    header_text, html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),

    # Your components:
    # introduction
    intro, html.Br(), html.Br(), html.Br(),
    # temperature graph with sliders bordering it:
    html.Div(children = [
        html.Div(temperature_graph,style={'width': '80%', 'display': 'inline-block'}),
        html.Div([depth_slider],style={'width': '20%', 'height': '50vh', 'display': 'inline-block'}),
        # html.Div(["DEPTH"],className="depthSliderText",style={'width': '10%', 'height': '50vh', 'display': 'inline-block'}),
        html.Div(time_slider,style={'width': '80%', 'display': 'inline-block'}),
    ]),

    # themometer with various calculations and metrics
    html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
    html.Div(children=[
        html.Div(themometer, style={'width': '50%', 'display': 'inline-block'}),
        html.Div(indicators, style={'width': '30%', 'display': 'inline-block'}),
        html.Div(style={'width': '20%', 'display': 'inline-block'}),
    ]),

    # line graph of forecast at the point selected,
    html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
    html.Div(children=[
        html.Div(forecast_temperature_line_graph, style={'width': '50%', 'display': 'inline-block'}),
        html.Div(depth_temperature_line_graph, style={'width': '50%', 'display': 'inline-block'}),
    ]),

    # line graph of depth profile at the point,
    html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
    html.Div(children=[

    ]),

])


# all call backs go here:
# ...

# # callback to display what value chosen in dropdown
# @app.callback(
#     Output('temperature-display-value', 'children'),
#     [Input('temperature-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)

# @app.callback(
#     Output('themometer', 'label'),
#     [Input('themometer', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)