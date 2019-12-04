# -*- coding: utf-8 -*-
"""
.. module:: Welcome_page
    :platform: Windows 7, Python 3.7.
    :synopsis: This module holds the functions developed by Kirodh Boodhraj.
.. moduleauthor:: Kirodh Boodhraj <kboodhraj@csir.co.za>

TODO
*say it is demo data
explain frequency of data/forecast
Mention CHPC
mention the approach/method

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


header_heading = html.H1(id="the_title",children=['Oceans 21 Home page'])

introduction = html.Div(id="introduction", className="introductionWelcomeText",
                        children=[
    "A feasibility study is currently underway for the Oceans 21 project. Oceans 21 aims to create an ocean forecast "
    "using machine learning techniques not applied to this field previously. The methodology "
    "is explained below. This web application demo displays the concept of having a ocean forecast and its various uses. "
    "The data displayed is historical data so please do not use it for realtime decision making."])

methodology_heading = html.H4(id="methodology_heading",children=["Methodology:"])
methodology_body = dcc.Markdown(id="methodology", children=[
'''
1. The methodology employed will be to apply machine learning to the ocean model input data, i.e. the surface forcing data from climate reanalyses.
2. This will provide a forecast of the ocean input data, which can further be used in other applications.
3. The forecasted ocean input data will be used in the ocean model to produce an ocean forecast.
'''])


hazards_heading = html.H4(id="hazards_heading",children=["Challenges:"])
hazards = dcc.Markdown(id="hazards", children=[
'''The following challenges are recognised:
- Various errors associated with the ocean input data, forcasted ocean input data and ocean forecast data.
- Computational running time needed is costly. The Centre for Higher Performance Computing (CHPC) will be used for this undertaking.
- Funding and administration. 
'''])


# this is interesting, mark down needs to go against the wall here, if indented, it will not work!
ocean_forecast_measures_heading = html.H4(id="forecastfun_heading",children=["Ocean forecast measures and possible uses:"])
ocean_forecast_measures = dcc.Markdown(
'''This list is not exhaustive:
- Temperature
- Salinity
- Currents
- Energy
- Waves
- Ship Route Optimization
- Ocean Surface
- Particle Tracking
''')

# stopped here!

## this is where all your elements come together:
layout = html.Div(id="welcomePages",children=[
    header_logo,
    header_heading,
    html.Br(),
    html.Br(),
    introduction,
    html.Br(),
    methodology_heading,
    methodology_body,
    html.Br(),
    hazards_heading,
    hazards,
    html.Br(),
    ocean_forecast_measures_heading,
    ocean_forecast_measures,
    html.Br(),
    html.Div(id="text1",children=["Please use these buttons below to navigate to the different web tools:"]),

])


