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

# get_temperature_data(True)
# print(len(get_time_data()))
# print(get_time_data()[2])



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
# element 1
temperature_graph = dcc.Graph(
        id='temperature_graph',
        figure={
            'data': [
                {'x': [0, 2, 3], 'y': [40, 1, 2],
                 'type': 'bar', 'name': 'SF'},
                {'x': [0, 2, 3], 'y': [2, 4, 5],
                 'type': 'bar', 'name': u'Montréal'},
            ]
        }
    )


time_slider = dcc.Slider(
    min=0,
    max=len(get_time_data())-1,
    value=0,
    marks={ i:{'label': str(i), 'style': {'color': '#77b0b1'}} for i in range(len(get_time_data()))},
    included=False
)

depth_slider = dcc.Slider(
    min=0,
    max=len(get_depth_data())-1,
    value=0,
    marks={i:{'label': str(i), 'style': {'color': '#77b0b1'}} for i in range(len(get_depth_data()))},
    included=False,
    vertical= True,
    tooltip = {  "placement":"topLeft" }

)

# stopped here



## this is where all your elements come together:
layout = html.Div([
    # header (leave alone):
    header_logo,
    header_text, html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),

    # Your components:
    html.Div(temperature_graph,style={'width': '80%', 'display': 'inline-block'}),
    html.Div([depth_slider],style={'width': '20%', 'height': '50vh', 'display': 'inline-block'}),
    html.Div(time_slider,style={'width': '80%', 'display': 'inline-block'}),
    # temperature_graph,
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    # time_slider,
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    # depth_slider,

])


# all call backs go here:
# ...

# # callback to display what value chosen in dropdown
# @app.callback(
#     Output('temperature-display-value', 'children'),
#     [Input('temperature-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)
