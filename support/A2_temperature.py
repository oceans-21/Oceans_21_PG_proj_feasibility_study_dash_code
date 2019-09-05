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


# flatten data array (for a certain depth only) for scatter plot
def flatten(lon,lat,data,debug=False):
    # this function assumes that a single depth and time layer comes into this function and is then flattened and inserted into a pandas array
    # data variable has dimension: time depth lat lon
    # empty array for holding data:

    the_array = []
    # loop through the lats, then the lons and extract the data point associated with it:
    for latIndex,lati in enumerate(lat):
        for lonIndex, loni in enumerate(lon):
            if data[latIndex,lonIndex] == 0:
                continue
            the_array.append([lati,loni,data[latIndex,lonIndex]])

    return pd.DataFrame(the_array,columns=["lat","lon","data"])



# all data:
temp_data = get_temperature_data()
time_data = get_time_data()
depth_data = get_depth_data()
longitude = get_lon_data()
latitude = get_lat_data()
# print(flatten(longitude[0,:],latitude[:,0],temp_data[0,0,:,:]))

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
    hoverinfo='all',
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Scroll to zoom. Double click to reset view",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",  # streets, light dark satellite outdoors satellite-streets open-street-map
        center=dict(lon=25, lat=-30),
        zoom=3,
    ),
)


# print(longitude[0,:])
# print(latitude[:,0])
trace = [dict(
            type="scattermapbox",
            lon=flatten(longitude[0,:],latitude[:,0],temp_data[0,-1,:,:])["lon"],#[30,31,32],#longitude[0,:],
            lat=flatten(longitude[0,:],latitude[:,0],temp_data[0,-1,:,:])["lat"],#[-30,-31,-32],#latitude[:,0],
            # text="hello",
            # z=flatten(longitude[0,:],latitude[:,0],temp_data[0,-3,:,:])["data"],#[2,3,4],#temp_data[0,0,:,:],
            # name="the name",
            marker=dict(size=4, opacity=0.6, cmin=0,cmax=37,
                color=flatten(longitude[0,:],latitude[:,0],temp_data[0,-1,:,:])["data"],
                colorscale="Jet", #Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis
                colorbar=dict(
                    thickness= 10,
                    titleside= 'right',
                    outlinecolor= 'rgba(68,68,68,0)',
                    ticks= 'outside',
                    ticklen= 3,
                    shoticksuffix= 'last'
                    # ticksuffix= 'inches',
                    # dtick= 0.1
                    ))
        )]


# main temperature graph:
temperature_graph = dcc.Graph(
    id='temperature_graph',
    className="temperatureGraph",
    figure={
        'data':trace,
        'layout': layout
    }
)


time_slider = dcc.Slider(
    min=0,
    max=len(get_time_data())-1,
    value=0,
    # a condition to show every third label:
    marks={(num): ({'label': str(i.strftime('%Y-%m-%d %H:%M')),
                    'style': {'color': 'black', "transform": "rotate(45deg)",
                              'margin-top': '5vh'}} if num % 3 == 0 else {'label': ''}) for num, i in
           enumerate(get_time_data())},
    included=False,
    className="timeSlider"
)

depth_slider = dcc.Slider(
    min=0,
    max=len(get_depth_data())-1,
    value=len(get_depth_data())-1,
    # this is iterating swapping the depth labels on the depth slider
    marks={(len(get_depth_data()) - 1 - index): {'label': str(int(depth_value)) + "m",
                                                 'style': {'color': 'black', 'margin-top': '50vh'}} for
           index, depth_value in enumerate(get_depth_data())},
    included=False,
    vertical= True,
    # tooltip={"placement": "topLeft"},
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
        html.Div(style={'width': '5%', 'display': 'inline-block'}),
        html.Div([depth_slider],style={'width': '15%', 'height': '50vh', 'display': 'inline-block'}),
        # html.Div(["DEPTH"],className="depthSliderText",style={'width': '5%', 'height': '50vh', "transform": "rotate(90deg)", 'display': 'inline-block'}),
        html.Div(time_slider,style={'width': '80%', 'display': 'inline-block'}),
    ]),

    # themometer with various calculations and metrics
    html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
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