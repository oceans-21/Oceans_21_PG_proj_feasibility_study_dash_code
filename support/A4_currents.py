# -*- coding: utf-8 -*-
"""
.. module:: Currents
    :platform: Windows 7, Python 3.7.
    :synopsis: This module holds the functions developed by Chris Mahlathi.
.. moduleauthor:: Kirodh Boodhraj <kboodhraj@csir.co.za>
                  Chris Mahlathi <cdmahlathi@csir.co.za>


"""

# import system modules here:
import datetime as dt
import pathlib as pl
import xarray as xr
import sys

# import other modules here:
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import dash_table as tab
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import numpy as np


## functions go here:
###############################################
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

# get the uVelocity data:
def get_uvelocity_data(debug=False):
    # path to data:
    path = pl.Path("support/data/uVelNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path, False)
    if debug: print(data)
    # extract data: dimensions
    uvelocity = get_variable(data,"vozocrtx")
    if debug: print(uvelocity)
    return uvelocity

# get the vVelocity data:
def get_vvelocity_data(debug=False):
    # path to data:
    path = pl.Path("support/data/vVelNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path, False)
    if debug: print(data)
    # extract data: dimensions
    vvelocity = get_variable(data,"vomecrty")
    if debug: print(vvelocity)
    return vvelocity


get_vvelocity_data()

# get the time data:
def get_time_data(debug=False):
    # path to data:
    path = pl.Path("support/data/uVelNEMO.nc")
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
    path = pl.Path("support/data/vVelNEMO.nc")
    # open data as xarray:
    data = open_netcdf(path)
    if debug: print(data)
    # extract data:
    depth = get_variable(data, "depthv")
    if debug: print(len(depth))
    return depth

get_depth_data(True)
# get the depth data:
def get_lat_data(debug=False):
    # path to data:
    path = pl.Path("support/data/vVelNEMO.nc")
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
    path = pl.Path("support/data/vVelNEMO.nc")
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

# function to extract the depth and forecast profile given a lat/lon:
def get_depth_and_forecast_temperature_data(lonPoint,latPoint,lonData,latData,temperatureData,depthIndex,timeIndex,debug=False):
    # this function obtains the depth profile at a point and forecast at a point given a latitude and longitude point:
    # first get the indexes of lat and lon that need to be pulled out:
    latIndex = np.nanargmin(np.abs(latData-latPoint))
    closestLat = latData[latIndex]
    lonIndex = np.nanargmin(np.abs(lonData-lonPoint))
    closestLon = lonData[lonIndex]
    if debug: print(closestLat,closestLon)

    # now get the temperature data points:
    # for depth profile:
    depthProfile = temperatureData[timeIndex,:,latIndex,lonIndex]
    # for forecast profile:
    forecastProfile = temperatureData[:,depthIndex,latIndex,lonIndex]
    # return the values
    if debug: print(depthProfile,forecastProfile)
    return depthProfile,forecastProfile


# you can put your own functions here:
# all data:
uvel_data = get_uvelocity_data()[:,:,:-1,:]
vvel_data = get_vvelocity_data()[:,:,:,:-1]
umag_data = np.sqrt((uvel_data)**2 + (vvel_data)**2)
time_data = get_time_data()
depth_data = get_depth_data()
longitude = get_lon_data()[:,:-1]
latitude = get_lat_data()[:,:-1]
print (uvel_data.shape,vvel_data.shape,time_data.shape,depth_data.shape,longitude.shape,latitude.shape)
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

header_text = html.H1('Currents')



# these are yours :-)
# mapbox_access_token = "sk.eyJ1Ijoia2lyb2RoIiwiYSI6ImNrMDVjbHd2ejBzenczbnBuemUxZGxjM3gifQ.uEjF3QBfWY8xToNwU5NHKg" # my own one
mapbox_access_token = "pk.eyJ1Ijoia2lyb2RoIiwiYSI6ImNrMDVjaWY0ZzBqaXAzbXFvenp3OWVpd2MifQ.apsaN8lTiMfqgsOArDA5Xg" # public




###############################################
# put the dash layout here
# ...


# these are yours :-)
# intro text:
intro = html.Div(["This page displays currents forecasts ("+ "m/s). Use the sliders to change between the various "
                  "depths and time steps. The resulting currents profiles will be displayed for the point chosen "
                  "on the graph."])

# layout for main temperature graph:
# sort out colourbar:
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
        style="dark",  # streets, light dark satellite outdoors satellite-streets open-street-map
        center=dict(lon=25, lat=-30),
        zoom=3,
    ),
)


# print(longitude[0,:])
# print(latitude[:,0])
trace = [dict(
            type="scattermapbox",
            lon=flatten(longitude[0,:],latitude[:,0],uvel_data[0,0,:,:])["lon"],#[30,31,32],#longitude[0,:],
            lat=flatten(longitude[0,:],latitude[:,0],uvel_data[0,0,:,:])["lat"],#[-30,-31,-32],#latitude[:,0],
            text=[format(j,".2f")+" "+ u'\N{DEGREE SIGN}'+"C" for j in flatten(longitude[0,:],latitude[:,0],uvel_data[0,0,:,:])["data"]],
            # z=flatten(longitude[0,:],latitude[:,0],temp_data[0,-3,:,:])["data"],#[2,3,4],#temp_data[0,0,:,:],
            # name="the name",
            marker=dict(size=10, opacity=0.6, cmin=-2.5,cmax=2.5,
                color=flatten(longitude[0,:],latitude[:,0],uvel_data[0,0,:,:])["data"],
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


# main velocity graph:
Uvelocity_graph = dcc.Graph(
    id='Uvelocity_graph',
    className="temperatureGraph",
    figure={
        'data':trace,
        'layout': layout
    }
)


time_slider = dcc.Slider(
    id="VelocityTimeSlider",
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
    id="VelocityDepthSlider",
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

#Radio button


Velocity_option = dcc.RadioItems(
        id = 'Radio_Items',
        options =[
                {'label':'U currents', 'value':'uvel'},
                {'label':'V currents', 'value':'vvel'},
                {'label':'currents magnitude', 'value':'cmag'}
                ],
        value='uvel'
        )

DigiDate = daq.LEDDisplay(
        id = 'LedDisplay',
        value = '01:05:2019'
        )
## themometer to show temperature:
#themometer = daq.Thermometer(
#    id='thermometer',
#    className = "thermometer",
#    value=0,
#    min=0,
#    max=40,
#    # style={'height': '100vh'},
#    color = " #f83a3a",
#    showCurrentValue=True,
#    units=u'\N{DEGREE SIGN}'+"C",
#    # size= '25%'#300,
#    # labelPosition = "top",
#    # label="hello"
#)

# a block with all the required indicators:
indicators = html.Div(id="velIndicators",className="tempIndicators",children=[
    html.Div(id="SurfaceMaxV",children=["Surface Maximum Velocity = NaN "+"m/s"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="SurfaceMinV", children=["Surface Minimum Velocity = NaN "+"m/s"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="SurfaceAvgV", children=["Surface Average Velocity = NaN "+"m/s"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="depthAvgV", children=["Depth Average  Velocity = NaN "+"m/s"],style={'padding-left':"5vw",'padding-top':"5vh",'padding-bottom':"5vh"})
    # html.Div(id="SurfaceMaxV", children=["Surface Maximum Velocity = 0.0 deg C"]),
    # html.Div(id="SurfaceMaxV", children=["Surface Maximum Velocity = 0.0 deg C"])
])

# line graph for temperature forecast:
forecast_temperature_line_graph = dcc.Graph(
    id='velocity_forecast_line_graph',
    figure={
        'data': [
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Temperature forecast'},
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Average temperature'},
        ]
    }
)

# line graph for depth profile:
depth_temperature_line_graph = dcc.Graph(
    id='velocity_deptht_line_graph',
    figure={
        'data': [
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Depth profile'},
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Average temperature'},
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
        html.Div(children = [
                Velocity_option],style={'width': '25%', 'display': 'inline-block'}),
        html.Div(Uvelocity_graph,style={'width': '80%', 'display': 'inline-block'}),
        html.Div(style={'width': '5%', 'display': 'inline-block'}),
        html.Div([depth_slider],style={'width': '15%', 'height': '50vh', 'display': 'inline-block'}),
        # html.Div(["DEPTH"],className="depthSliderText",style={'width': '5%', 'height': '50vh', "transform": "rotate(90deg)", 'display': 'inline-block'}),
        html.Div(time_slider,style={'width': '80%', 'display': 'inline-block'}),
    ]),

    # themometer with various calculations and metrics
    html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
    html.Div(children=[
#        html.Div(themometer, style={'width': '50%', 'display': 'inline-block'}),
        html.Div(indicators, style={'width': '30%', 'display': 'inline-block'}),
        html.Div(style={'width': '20%', 'display': 'inline-block'}),
    ]),

    # line graph of forecast at the point selected,
    html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
    html.Div(children=[
        html.Div(forecast_temperature_line_graph, style={'width': '30%', 'display': 'inline-block'}),
        html.Div(depth_temperature_line_graph, style={'width': '70%', 'display': 'inline-block'}),
    ]),

    # line graph of depth profile at the point,
    html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
    html.Div(children=[

    ]),

])

#cmax
# all call backs go here:
# ...
# two call backs needed, one for the sliders and one for clicking the graph:

# for sliders:
@app.callback(
    [Output('SurfaceMaxV', 'children'),Output('SurfaceMinV', 'children'),Output('SurfaceAvgV', 'children'),Output('Uvelocity_graph','figure')],
    [Input('VelocityDepthSlider', 'value'),Input('VelocityTimeSlider', 'value'),Input('Radio_Items', 'value')])
def display_click_data(VelocityDepthSliderValue,VelocityTimeSliderValue,VelocityOptions):
    # print(VelocityDepthSliderValue,VelocityTimeSliderValue,depth_data)
    # print(VelocityDepthSliderValue)

    # invert the  depth index because I inverted it when I changed the labels around, i.e. max depth -1 - current slider value, -1 for a offset due to number of elements present and python counting from 0
    VelocityDepthSliderValue = len(depth_data) - 1 - VelocityDepthSliderValue
    # print(VelocityDepthSliderValue)
    # first get the data: data dimensions: time depth lat lon
    if VelocityOptions == 'vvel':
        data_layer = vvel_data[VelocityTimeSliderValue,VelocityDepthSliderValue,:,:]
    elif VelocityOptions == 'uvel':
        data_layer = uvel_data[VelocityTimeSliderValue,VelocityDepthSliderValue,:,:]
    else:
        data_layer = umag_data[VelocityTimeSliderValue,VelocityDepthSliderValue,:,:]
    # print(data_layer)

    # update components one by one
    # 1) Surface Maximum Velocity
    surface_maximum_temperature = np.nanmax(data_layer)
    surface_maximum_temperature = "Surface Maximum Velocity = "+format(surface_maximum_temperature,".3f") + " "+"m/s"
    # print("temp",surface_maximum_temperature)

    # 2) Surface Minimum Velocity
    surface_minimum_temperature = np.nanmin(data_layer[np.nonzero(data_layer)])
    surface_minimum_temperature = "Surface Minimum Velocity = "+format(surface_minimum_temperature,".3f") + " "+"m/s"


    # 3) Surface Average Velocity:
    surface_average_temperature = np.nanmean(data_layer)
    surface_average_temperature = "Surface Average Velocity = "+format(surface_average_temperature ,".2f") + " "+"m/s"

    # 4) the graph/figure:
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
            style="satellite",  # streets, light dark satellite outdoors satellite-streets open-street-map
            center=dict(lon=25, lat=-30),
            zoom=3,
        ),
    )
    # update data:
    trace = [dict(
        type="scattermapbox",
        lon=flatten(longitude[0, :], latitude[:, 0], data_layer)["lon"],
        lat=flatten(longitude[0, :], latitude[:, 0], data_layer)["lat"],
        text=[format(j,".2f")+" "+ "m/s" for j in flatten(longitude[0, :], latitude[:, 0], data_layer)["data"]],
        marker=dict(size=10, opacity=0.6, cmin=-2.5, cmax=2.5,
                    color=flatten(longitude[0, :], latitude[:, 0], data_layer)["data"],
                    colorscale="Jet",# Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,Hot,Blackbody,Earth,Electric,Viridis,Cividis
                    colorbar=dict(
                        thickness=10,
                        titleside='right',
                        outlinecolor='rgba(68,68,68,0)',
                        ticks='outside',
                        ticklen=3,
                        shoticksuffix='last'
                    ))
    )]

    # create the figure:
    figure = {
        'data': trace,
        'layout': layout
    }

    return [surface_maximum_temperature,surface_minimum_temperature,surface_average_temperature,figure]


# for profile graphs, thermometer and depth average:
@app.callback(
    # [Output('depthAvgV', 'children'),Output('thermometer', 'value'),Output('velocity_forecast_line_graph', 'figure'),Output('velocity_deptht_line_graph','figure')],
    [Output('depthAvgV', 'children'),Output('velocity_forecast_line_graph', 'figure'),Output('velocity_deptht_line_graph','figure')],
    # [Input('Uvelocity_graph', 'clickData'),Input('VelocityTimeSlider', 'value')])
    [Input('Uvelocity_graph', 'clickData'),Input('VelocityDepthSlider', 'value'),Input('VelocityTimeSlider', 'value'),Input('Radio_Items', 'value')],
    [State('depthAvgV', 'children'),State('velocity_forecast_line_graph', 'figure'),State('velocity_deptht_line_graph','figure')])
def display_click_data(click_data,VelocityDepthSliderValue,VelocityTimeSliderValue,VelocityOptions,depth_average_text_state,depth_graph_state,forcast_graph_state):
    # this callback generates the line graphs and thermometer and depth averaged temperature value
    if click_data is not None:
        # print(VelocityTimeSliderValue, VelocityDepthSliderValue)
        # invert the  depth index because I inverted it when I changed the labels around, i.e. max depth -1 - current slider value, -1 for a offset due to number of elements present and python counting from 0
        VelocityDepthSliderValue = len(depth_data) - 1 - VelocityDepthSliderValue

        # print(click_data)
        # print(VelocityTimeSliderValue,VelocityDepthSliderValue)

        # get the temperature from the clicked temperature value for thermometer:
        the_current_temperature = (click_data.get("points")[0]).get("marker.color")
        # get the lat/lon values
        the_current_latitude = (click_data.get("points")[0]).get("lat")
        the_current_longitude = (click_data.get("points")[0]).get("lon")
        # print(the_current_temperature)

        # get the velocity profiles:
        if VelocityOptions == 'vvel':
            depth_profile,forecast_profile = get_depth_and_forecast_temperature_data(the_current_longitude, the_current_latitude, longitude[0, :], latitude[:, 0], vvel_data,VelocityDepthSliderValue,VelocityTimeSliderValue)
        elif VelocityOptions == 'uvel':
            depth_profile,forecast_profile = get_depth_and_forecast_temperature_data(the_current_longitude, the_current_latitude, longitude[0, :], latitude[:, 0], uvel_data,VelocityDepthSliderValue,VelocityTimeSliderValue)
        else:
            depth_profile,forecast_profile = get_depth_and_forecast_temperature_data(the_current_longitude, the_current_latitude, longitude[0, :], latitude[:, 0], umag_data,VelocityDepthSliderValue,VelocityTimeSliderValue)

        # get the depth average value for display:
        depth_averaged_temperature = np.nanmean(depth_profile)
        depth_averaged_temperature_text = "Depth Average  Velocity = "+format(depth_averaged_temperature,".2f")+" "+"m/s"

        # processing for figures:
        # data
        depth_graph_data = [
                {'x': depth_profile, 'y': depth_data,
                 'type': 'line',
                 'name': 'Depth Velocity profile',
                 'marker':dict(size=10, opacity=0.6)
                 },
                {'x': [depth_averaged_temperature for i in range(len(depth_data))], 'y': depth_data,
                 'type': 'line',
                 'mode':"lines",
                 'name': 'Average velocity = '+format(depth_averaged_temperature,".2f")+" "+"m/s",
                 # 'marker':dict(size=10, opacity=1)
                 }
            ]
        forecast_graph_data = [
            {'x': get_time_data(), 'y': forecast_profile,
             'type': 'line',
             'name': 'Depth velocity profile',
             'marker': dict(size=10, opacity=0.6)
             },
            {'x': get_time_data(), 'y': [np.nanmean(forecast_profile) for i in range(len(get_time_data()))],
             'type': 'line',
             'mode': "lines",
             'name': 'Average velocity = ' + format(np.nanmean(forecast_profile),".2f") + " " + "m/s",
             # 'marker':dict(size=10, opacity=1)
             }
            ]

        # layouts:
        depth_graph_layout = {
            'title': dict(
            text="Velocity depth profile",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="#7f7f7f")
            ),
            'yaxis':dict(
            title="Depth (m)",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            ),
            autorange="reversed"),
            'xaxis': dict(
            title="Velocity (" + "m/s)",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )),
            # 'legend_orientation' : "h",
            'legend' : dict(x=-.1, y=-0.5)
        }
        forecast_graph_layout = {
            'title': dict(
            text="Velocity point forecast profile",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="#7f7f7f")
            ),
            'yaxis': dict(
                title="Velocity (" + "m/s)",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                ),
                autorange="reversed"),
            'xaxis': dict(
                title="Time",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                )),
            'legend': dict(x=-.1, y=-0.5)
        }

        # make the actual figures:
        figure_depth = {
            'data': depth_graph_data,
            'layout': depth_graph_layout}
        figure_forecast = {
            'data': forecast_graph_data,
            'layout': forecast_graph_layout}


        # return the final values:
        return [depth_averaged_temperature_text,figure_depth,figure_forecast]
    else:
        # return original state if no one has clicked:
        return depth_average_text_state,depth_graph_state,forcast_graph_state





