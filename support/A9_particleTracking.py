# -*- coding: utf-8 -*-
"""
.. module:: Particle_Tracking
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


## functions go here:
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

header_text = html.H1('Particle Tracking')



# these are yours :-)
# element 1
the_graph = dcc.Graph(
        # id='example-graph',
        figure={
            'data': [
                {'x': [0, 2, 3], 'y': [40, 1, 2],
                 'type': 'bar', 'name': 'SF'},
                {'x': [0, 2, 3], 'y': [2, 4, 5],
                 'type': 'bar', 'name': u'Montréal'},
            ]
        }
    )

# element 2
dropdown = dcc.Dropdown(
        id='particle-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in ['NYC', 'MTL', 'LA']
        ],value="hello"
    )




## this is where all your elements come together:
layout = html.Div([
    # header (leave alone):
    header_logo,
    header_text, html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),

    # Your components:
    dropdown,
    the_graph,
    html.Div(id='particle-display-value'),
])


# all call backs go here:
# ...

# callback to display what value chosen in dropdown
@app.callback(
    Output('particle-display-value', 'children'),
    [Input('particle-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
