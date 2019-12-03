# -*- coding: utf-8 -*-
"""
.. module:: Ocean_surface
    :platform: Windows 7, Python 3.7.
    :synopsis: This module holds the functions developed by Dr. Nicolene Botha and Melise Steyn.
.. moduleauthor:: Kirodh Boodhraj <kboodhraj@csir.co.za>
                  Nicolene Botha <nbotha@csir.co.za>
                  Melise Steyn <msteyn2@csir.co.za>


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

from mpl_toolkits.basemap import Basemap
import base64
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
import plotly.graph_objs as go
import matplotlib
## functions go here:


address = os.path.dirname(os.path.abspath(__file__))
print(address)
path = os.path.join(address, 'data')

Longitude = os.path.join(path, 'Longetude.npy')
Latitude = os.path.join(path, 'Latitude.npy')

print(Longitude)

## This coordinate jumble will be fixed when the 'real' area is decided and
## incorporated
x_lon = np.load(Longitude)
#x_lon = np.load('Longetude.npy') # want ~10 tot ~35 #x
lont = x_lon[48:258]
lont = lont[::-1]
x = lont[110:212]
#x = lon[20:120]
xmin = np.min(x)
xmax = np.max(x)

y_lat = np.load(Latitude) #want -40 to -30  #x
#y_lat = np.load('Lattitude.npy') #want -40 to -30  #x
y_lat = y_lat[::-1]
latt = y_lat[200-14:350-14]
y = latt[20:90]
#y = lat[20:120]
ymin = np.min(y)
ymax = np.max(y)
# For mapbox
Xg = list(x.flatten())
Yg = list(y.flatten())
Xg, Yg = np.meshgrid(Xg, Yg)
Lon = Xg.ravel('A')
Lat = Yg.ravel('A')
df = pd.DataFrame(np.zeros((len(Lon), 2)),columns=['lat', 'lon'])
df['lat'] = Lat
df['lon'] = Lon

mapbox_access_token = "pk.eyJ1Ijoia2lyb2RoIiwiYSI6ImNrMDVjaWY0ZzBqaXAzbXFvenp3OWVpd2MifQ.apsaN8lTiMfqgsOArDA5Xg" # public

''' markdown texts '''
markdown_text = '''
This page displays forecasted hourly air temperature (2 m). Use the sliders to change between 
the various time steps. The resulting air temperature data will be displayed in the map.
'''


###############################################
# you can put your own functions here:
# ...
def i_do_something(whatever_parameters,another_param):
    """
        Purpose: Fill this in.

        :param whatever_parameters: Fill this in.
        :type whatever_parameters: str
        :param another_param: make copies of the param/type for more arguments to the functions.
        :type another_param: bool

        :returns:  None -- Fill here if something is returned.

        How to use this function

        >>> i_do_something("hello",11)


        .. note::

            You can put a not here if you want.

        """


    # please comment your codes as you code :-)
    print(whatever_parameters,another_param)

    return None





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

header_text = html.H1('Ocean Surface')

V = html.H1(children='Forecasting the ocean state',
    style={'textAlign': 'center', 'color': '#7FDBFF'})


text = html.Div([dcc.Markdown(children=markdown_text)])


spacer = html.Div('', style={'padding': 10})



dropdown = html.Div([html.Label('Ocean parameter',style={'marginLeft': 1}),
                     html.Div('',style={'padding':15}),
                     dcc.Dropdown(id = 'variable',
                                  style={'height': '30px', 'width': '200px','marginBottom': '3em'},
                                  options=[
                                          {'label': 'Temperature', 'value': 'Temperature', 'disabled': False},
                                          {'label': u'Wave height', 'value': 'wave_height', 'disabled': True},
                                          {'label': 'Salinity', 'value': 'salinity', 'disabled': True},
                                          {'label': 'Variable 4', 'value': 'var4', 'disabled': True},
                                          {'label': 'Variable 5', 'value': 'var5', 'disabled': True}

                                          ],
                                  value='Temperature',
                                  )], style={'width': '49%', 'display': 'inline-block','vertical-align': 'top'})


slider = html.Div([html.Label('Forecasting timestep of ocean parameter'),
                   html.Div('',style={'padding':20}),
                   html.Div([
                           daq.Slider(
                                   id='my-daq-slider-ex',
                                   size=400,
                                   min=1,
                                   max=72,
                                   value=4,
                                   handleLabel={"showCurrentValue": True,"label": "HOUR"}),
                           html.Div(id='slider-output')
                            ])
                           ],style={'width': '49%', 'display': 'inline-block','vertical-align': 'top'})


#    html.Label(id='message1',style={'marginLeft':80,'marginBottom':-2}),#, children='Please select ocean state variable and forecasted hour to view.'),
image = html.Div([
                html.Img(id='image'),
                ], style={'marginLeft':250})
    
    
graph = html.Div([dcc.Graph(id='map')], style={'marginLeft':200})


## this is where all your elements come together:
layout = html.Div([
    # header (leave alone):
    header_logo,
    header_text, html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),

    # Your components:
    # V,
    text,
    spacer,
    dropdown,
    slider,
    image,
    spacer,
    graph,
    spacer,
    html.Div(id='surface-display-value'),
])


# all call backs go here:
# ...

@app.callback(
    dash.dependencies.Output('slider-output', 'children'),
    [dash.dependencies.Input('my-daq-slider-ex', 'value')])
def update_output(value):
    return '{} hour.'.format(value)



@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('my-daq-slider-ex', 'value'),
    dash.dependencies.Input('variable', 'value')])
def plot_output(hour,var):
    var_array = str(var)+'.npy'
    selected_var = os.path.join(path, var_array)
    data = np.load(selected_var)
    f = data[int(hour)-1]
    matplotlib.use('Agg')
    m = Basemap(projection='cyl', llcrnrlon=xmin,llcrnrlat=ymin,urcrnrlon=xmax,urcrnrlat=ymax,resolution='l')
    m.drawcoastlines()
    # add intensities (currently normalised but will be fixed - eventually)
    parallels = np.arange(-80.,10,5.)
    m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(10.,50.,5.)
    m.drawmeridians(meridians,labels=[True,False,False,True])
    plt.xlabel('\nLongitude')
    plt.ylabel('Latitude')
    # add all the bells and whistles
    im = m.imshow(f[::-1],extent=[np.min(x),np.max(x),np.min(y),np.max(y)])
    plt.title('Graphical representation of ' + str(var) + ' for a ' + str(hour) + ' hour forecast\n\n' )
    # plt.colorbar(im, orientation="vertical", pad=0.1)
    ax = plt.gca()
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.5)
    plt.colorbar(im, cax=cax)#, orientation="vertical", pad=0.1)
    temp_image = os.path.join(path, 'temp.png')
    print("temp: image",temp_image)
    plt.savefig(temp_image)
    plt.cla()
    plt.clf()
    plt.close()
    # image_filename = 'temp.png' # replace with your own image
    encoded_image = base64.b64encode(open(temp_image, 'rb').read())
    src='data:image/png;base64,{}'.format(encoded_image.decode())
    return src


@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('my-daq-slider-ex', 'value'),
    dash.dependencies.Input('variable', 'value')])
def plot_output_test_mapbox(hour,var):
    var_array = str(var)+'.npy'
    selected_var = os.path.join(path, var_array)
    data = np.load(selected_var)
    #data = np.load(var_array)
    #d=data[::-1]
    h = data[int(hour)-1].ravel('A')
    lt = df['lat'][::-1]
    ln = df['lon'][::-1]
    return {
            'data': [
                go.Scattermapbox(
                    lat = lt,
                    lon = ln,
                    mode = 'markers',
                    marker = dict(size=9, 
                                  opacity=0.7, 
                                  cmin=np.min(h), 
                                  cmax=np.max(h),
                                  color=h,
                                  colorbar=dict(title='colourbar'),
                                  colorscale='Viridis'
                                  ),
                    text=np.round(h,2))
                    ],
            'layout': go.Layout(
                    margin = dict(l=30, r=20, t=0, b=0),
                    width = 750,
                    height = 550,
                    hovermode = 'closest',
                    mapbox = dict(
                            accesstoken = mapbox_access_token,
                            center=dict(lon=25, lat=-30),
                            pitch=0,
                            zoom=4
                            )
                        )}
                    
                    