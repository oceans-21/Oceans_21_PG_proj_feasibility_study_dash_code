# -*- coding: utf-8 -*-
"""
.. module:: Chris
    :platform: Windows 7, Python 3.7.
    :synopsis: This module holds the functions developed by Kirodh Boodhraj.
.. moduleauthor:: Kirodh Boodhraj <kboodhraj@csir.co.za>

TODO
say it is demo data
explain frequency of data
Mention CHPC
mention the approach

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

header_logo = html.A([html.Img(id="logo",src=app.get_asset_url('oceans21logo_small.png'),
                    style={
                    'height' : '15%',
                    'width' : '15%',
                    'float' : 'right',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-right' : 0
                })],href="https://www.csir.co.za",target="_blank")


header_heading = html.H1('Oceans 21 Home page',id="the_title")

# this is interesting, mark down needs to go against the wall here, if indented, it will not work!
ocean_forecast_measures = dcc.Markdown(
'''There are various ocean forecast measures namely
- Temperature
- Salinity
- Currents
- Energy
- Waves
- Ship Route Optimization
- Ocean Surface
- Particle Tracking
''')



## this is where all your elements come together:
layout = html.Div(id="welcomePages",children=[
    header_logo,
    header_heading,
    html.Br(),
    html.Br(),
    html.Div(id="text",children=["This is a platform for viewing a vision for an ocean forecast. "
                                 "This web application does not contain up to date data but displays historical data."]),
    ocean_forecast_measures,
    html.Div(id="text1",children=["Please use these buttons below to navigate to the appropriate pages:"]),

])


# all call backs go here:
# ...

# callback to display what value chosen in dropdown
# @app.callback(
#     Output('welcome-display-value', 'children'),
#     [Input('welcome-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)
