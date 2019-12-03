# -*- coding: utf-8 -*-
"""
.. module:: Energy
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
from dash.dependencies import Input, Output, State
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
    # if debug: print("Extracted data from NetCDF: ", variableData)
    if debug: print("Dimension of data: ", variableData.shape)

    return variableData


# get the salinity data:
def get_salinity_data(debug=False):
    # path to data:
    path = pl.Path("support/data/uVelNEMO.nc")
    path2 = pl.Path("support/data/vVelNEMO.nc")
    # open data as xarray:
    dataU = open_netcdf(path)
    dataV = open_netcdf(path2)
    if debug: print(dataU)
    if debug: print(dataV)
    # extract data: dimensions
    vvel = get_variable(dataV,"vomecrty")[:,:,:,:-1]
    uvel = get_variable(dataU,"vozocrtx")[:,:,:-1,:]

    # print(vvel.shape, uvel.shape)
    # get means:
    uvelbar = np.nanmean(uvel)
    vvelbar = np.nanmean(vvel)

    # get the fluctuating velocities:
    uveldash = uvel - uvelbar
    vveldash = vvel - vvelbar
    energy = 0.5 *(uveldash*uveldash + vveldash*vveldash)

    if debug: print(uvel)
    return energy


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
    return lat[:-1,:-1]

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
    return lon[:-1,:-1]


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
def get_depth_and_forecast_salinity_data(lonPoint,latPoint,lonData,latData,salinityData,depthIndex,timeIndex,debug=False):
    # this function obtains the depth profile at a point and forecast at a point given a latitude and longitude point:
    # first get the indexes of lat and lon that need to be pulled out:
    latIndex = np.nanargmin(np.abs(latData-latPoint))
    closestLat = latData[latIndex]
    lonIndex = np.nanargmin(np.abs(lonData-lonPoint))
    closestLon = lonData[lonIndex]
    if debug: print(closestLat,closestLon)

    # now get the salinity data points:
    # for depth profile:
    depthProfile = salinityData[timeIndex,:,latIndex,lonIndex]
    # for forecast profile:
    forecastProfile = salinityData[:,depthIndex,latIndex,lonIndex]
    # return the values
    if debug: print(depthProfile,forecastProfile)
    return depthProfile,forecastProfile




# all data:
sal_data = get_salinity_data()
time_data = get_time_data()
depth_data = get_depth_data()
longitude = get_lon_data()
latitude = get_lat_data()
# print(time_data.shape,longitude.shape,latitude.shape,depth_data.shape)
# print(flatten(longitude[0,:],latitude[:,0],sal_data[0,0,:,:]))


# mapbox token:
# mapbox_access_token = "sk.eyJ1Ijoia2lyb2RoIiwiYSI6ImNrMDVjbHd2ejBzenczbnBuemUxZGxjM3gifQ.uEjF3QBfWY8xToNwU5NHKg" # my own one
mapbox_access_token = "pk.eyJ1Ijoia2lyb2RoIiwiYSI6ImNrMDVjaWY0ZzBqaXAzbXFvenp3OWVpd2MifQ.apsaN8lTiMfqgsOArDA5Xg" # public



# todo: have to check out the id's of components
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

header_text = html.H1('Energy')



# these are yours :-)
# intro text:
intro = html.Div(["This page displays forecasted hourly eddy kinetic energy spread in normalized units. Use the sliders to change between the various "
                  "depths and time steps. The resulting energy profiles will be displayed for the point chosen "
                  "on the graph."])

# layout for main salinity graph:
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
        style="light",  # streets, light dark satellite outdoors satellite-streets open-street-map
        center=dict(lon=25, lat=-30),
        zoom=3,
    ),
)


# print(longitude[0,:])
# print(latitude[:,0])
trace = [dict(
            type="scattermapbox",
            lon=flatten(longitude[0,:],latitude[:,0],sal_data[0,0,:,:])["lon"],#[30,31,32],#longitude[0,:],
            lat=flatten(longitude[0,:],latitude[:,0],sal_data[0,0,:,:])["lat"],#[-30,-31,-32],#latitude[:,0],
            text=[format(j,".2f")+" "+ "Normalized units" for j in flatten(longitude[0,:],latitude[:,0],sal_data[0,0,:,:])["data"]],
            # z=flatten(longitude[0,:],latitude[:,0],sal_data[0,-3,:,:])["data"],#[2,3,4],#sal_data[0,0,:,:],
            # name="the name",
            marker=dict(size=10, opacity=0.6, cmin=0,cmax=4,
                color=flatten(longitude[0,:],latitude[:,0],sal_data[0,0,:,:])["data"],
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


# main salinity graph:
salinity_graph = dcc.Graph(
    id='energy_graph',
    className="salinityGraph",
    figure={
        'data':trace,
        'layout': layout
    }
)


time_slider = dcc.Slider(
    id="energyTimeSlider",
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
    id="energyDepthSlider",
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

# themometer to show salinity:
themometer = daq.Thermometer(
    id='thermometerE',
    className = "thermometer",
    value=0,
    min=0,
    max=4,
    # style={'height': '100vh'},
    color = " #f83a3a",
    showCurrentValue=True,
    units="Normalized EKE",
    # size= '25%'#300,
    # labelPosition = "top",
    # label="hello"
)

# a block with all the required indicators:
indicators = html.Div(id="salIndicators",className="salIndicators",children=[
    html.Div(id="surfaceMaxE",children=["Surface Maximum EKE = NaN "+"Normalized units"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="surfaceMinE", children=["Surface Minimum EKE = NaN "+"Normalized units"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="surfaceAvgE", children=["Surface Average EKE = NaN "+"Normalized units"],style={'padding-left':"5vw",'padding-top':"5vh"}),
    html.Div(id="depthAvgE", children=["Depth Average EKE = NaN "+"Normalized units"],style={'padding-left':"5vw",'padding-top':"5vh",'padding-bottom':"5vh"})
    # html.Div(id="surfaceMaxE", children=["Surface Maximum Salinity = 0.0 deg C"]),
    # html.Div(id="surfaceMaxE", children=["Surface Maximum Salinity = 0.0 deg C"])
])

# line graph for salinity forecast:
forecast_salinity_line_graph = dcc.Graph(
    id='energy_forecast_line_graph',
    figure={
        'data': [
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Energy forecast'},
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Average energy'},
        ]
    }
)

# line graph for depth profile:
depth_salinity_line_graph = dcc.Graph(
    id='energy_depth_line_graph',
    figure={
        'data': [
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Depth profile'},
            {'x': [0, 1, 2], 'y': [0, 0, 0],
             'type': 'line', 'name': 'Average energy'},
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
    # salinity graph with sliders bordering it:
    html.Div(children = [
        html.Div(salinity_graph,style={'width': '80%', 'display': 'inline-block'}),
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
        html.Div(forecast_salinity_line_graph, style={'width': '30%', 'display': 'inline-block'}),
        html.Div(depth_salinity_line_graph, style={'width': '70%', 'display': 'inline-block'}),
    ]),

    # line graph of depth profile at the point,
    html.Br(),html.Br(),html.Br(),html.Br(), # for spacing
    html.Div(children=[

    ]),

])


# all call backs go here:
# ...
# two call backs needed, one for the sliders and one for clicking the graph:

# for sliders:
@app.callback(
    [Output('surfaceMaxE', 'children'),Output('surfaceMinE', 'children'),Output('surfaceAvgE', 'children'),Output('energy_graph','figure')],
    [Input('energyDepthSlider', 'value'),Input('energyTimeSlider', 'value')])
def display_click_data(salDepthSliderValue,salTimeSliderValue):
    # print(salDepthSliderValue,salTimeSliderValue,depth_data)
    # print(salDepthSliderValue)

    # invert the  depth index because I inverted it when I changed the labels around, i.e. max depth -1 - current slider value, -1 for a offset due to number of elements present and python counting from 0
    salDepthSliderValue = len(depth_data) - 1 - salDepthSliderValue
    # print(salDepthSliderValue)
    # first get the data: data dimensions: time depth lat lon
    data_layer = sal_data[salTimeSliderValue,salDepthSliderValue,:,:]
    # print(data_layer)

    # update components one by one
    # 1) surface maximum salinity
    surface_maximum_salinity = np.nanmax(data_layer)
    surface_maximum_salinity = "Surface Maximum Energy = "+format(surface_maximum_salinity,".3f") + " Normalized units"
    # print("sal",surface_maximum_salinity)

    # 2) surface minimum salinity
    surface_minimum_salinity = np.nanmin(data_layer[np.nonzero(data_layer)])
    surface_minimum_salinity = "Surface Minimum Energy = "+format(surface_minimum_salinity,".3f") + " Normalized units"


    # 3) surface average salinity:
    surface_average_salinity = np.nanmean(data_layer)
    surface_average_salinity = "Surface Average Energy = "+format(surface_average_salinity ,".2f") + " Normalized units"

    # 4) the graph/figure:
    # layout for main salinity graph:
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
    # update data:
    trace = [dict(
        type="scattermapbox",
        lon=flatten(longitude[0, :], latitude[:, 0], data_layer)["lon"],
        lat=flatten(longitude[0, :], latitude[:, 0], data_layer)["lat"],
        text=[format(j,".2f")+" "+ "Normalized units" for j in flatten(longitude[0, :], latitude[:, 0], data_layer)["data"]],
        marker=dict(size=10, opacity=0.6, cmin=0,cmax=4,
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

    return [surface_maximum_salinity,surface_minimum_salinity,surface_average_salinity,figure]


# for profile graphs, thermometerE and depth average:
@app.callback(
    # [Output('depthAvgE', 'children'),Output('thermometerE', 'value'),Output('energy_forecast_line_graph', 'figure'),Output('energy_depth_line_graph','figure')],
    [Output('depthAvgE', 'children'),Output('thermometerE', 'value'),Output('energy_forecast_line_graph', 'figure'),Output('energy_depth_line_graph','figure')],
    # [Input('energy_graph', 'clickData'),Input('energyTimeSlider', 'value')])
    [Input('energy_graph', 'clickData'),Input('energyDepthSlider', 'value'),Input('energyTimeSlider', 'value')],
    [State('depthAvgE', 'children'),State('thermometerE', 'value'),State('energy_forecast_line_graph', 'figure'),State('energy_depth_line_graph','figure')])
def display_click_data(click_data,salDepthSliderValue,salTimeSliderValue,depth_average_text_state,thermometerS_state,depth_graph_state,forcast_graph_state):
    # this callback generates the line graphs and thermometerE and depth averaged salinity value
    if click_data is not None:
        # print(salTimeSliderValue, salDepthSliderValue)
        # invert the  depth index because I inverted it when I changed the labels around, i.e. max depth -1 - current slider value, -1 for a offset due to number of elements present and python counting from 0
        salDepthSliderValue = len(depth_data) - 1 - salDepthSliderValue

        # print(click_data)
        # print(salTimeSliderValue,salDepthSliderValue)

        # get the salinity from the clicked salinity value for thermometerE:
        the_current_salinity = (click_data.get("points")[0]).get("marker.color")
        # get the lat/lon values
        the_current_latitude = (click_data.get("points")[0]).get("lat")
        the_current_longitude = (click_data.get("points")[0]).get("lon")
        # print(the_current_salinity)

        # get the salinity profiles:
        depth_profile,forecast_profile = get_depth_and_forecast_salinity_data(the_current_longitude, the_current_latitude, longitude[0, :], latitude[:, 0], sal_data,salDepthSliderValue,salTimeSliderValue)

        # get the depth average value for display:
        depth_averaged_salinity = np.nanmean(depth_profile)
        depth_averaged_salinity_text = "Depth Average Energy = "+format(depth_averaged_salinity,".2f")+" Normalized units"


        # processing for figures:
        # data
        depth_graph_data = [
                {'x': depth_profile, 'y': depth_data,
                 'type': 'line',
                 'name': 'Depth energy profile',
                 'marker':dict(size=10, opacity=0.6)
                 },
                {'x': [depth_averaged_salinity for i in range(len(depth_data))], 'y': depth_data,
                 'type': 'line',
                 'mode':"lines",
                 'name': 'Average energy = '+format(depth_averaged_salinity,".2f")+" "+"Normalized units",
                 # 'marker':dict(size=10, opacity=1)
                 }
            ]
        forecast_graph_data = [
            {'x': get_time_data(), 'y': forecast_profile,
             'type': 'line',
             'name': 'Depth energy profile',
             'marker': dict(size=10, opacity=0.6)
             },
            {'x': get_time_data(), 'y': [np.nanmean(forecast_profile) for i in range(len(get_time_data()))],
             'type': 'line',
             'mode': "lines",
             'name': 'Average energy = ' + format(np.nanmean(forecast_profile),".2f") + " Normalized units",
             # 'marker':dict(size=10, opacity=1)
             }
            ]

        # layouts:
        depth_graph_layout = {
            'title': dict(
            text="Energy depth profile",
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
            title="Energy (Normalized units)",
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
            text="Energy point forecast profile",
            # font=dict(
            #     family="Courier New, monospace",
            #     size=18,
            #     color="#7f7f7f")
            ),
            'yaxis': dict(
                title="Energy (Normalized units)",
                font=dict(
                    family="Courier New, monospace",
                    size=18,
                    color="#7f7f7f"
                ),
                # autorange="reversed"
            ),
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
        return [depth_averaged_salinity_text,the_current_salinity,figure_depth,figure_forecast]
    else:
        # return original state if no one has clicked:
        return depth_average_text_state,thermometerS_state,depth_graph_state,forcast_graph_state
