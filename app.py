# -*- coding: utf-8 -*-
"""
.. module:: Main_App
    :platform: Windows 7, Python 3.7.
    :synopsis: This module combines individual contributions and holds the App.
.. moduleauthor:: Kirodh Boodhraj <kboodhraj@csir.co.za>


"""


import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import dash_table as tab
from dash.dependencies import Input, Output, State
import pathlib as pl
import pandas as pd
import numpy as np

# # import support functions:
# from support.nicolene import Nicolene
# from support.kobie import Kobie
# from support.gert import Gert
# from support.chris import Chris
# from support.melise import Melise
# from support.kirodh import Kirodh


external_stylesheets = ['assets\style.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)

server = app.server
app.config.suppress_callback_exceptions = True



# app.layout = html.Div([
#     dcc.Tabs(id="tabs", children=[
#         dcc.Tab(
#             # tab properties:
#             id="welcome",
#             label='Welcome',
#             value='tab-welcome',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="temperature",
#             label='Temperature',
#             value='tab-temperature',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="salinity",
#             label='Salinity',
#             value='tab-salinity',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="currents",
#             label='Currents',
#             value='tab-currents',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="energy",
#             label='Energy',
#             value='tab-energy',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="waves",
#             label='Waves',
#             value='tab-waves',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="ship_route_optimization",
#             label='Ship route optimization',
#             value='tab-ship_route_optimization',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="particle_tracking",
#             label='Particle tracking',
#             value='tab-particle_tracking',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi there :-)")
#         ]),
#         dcc.Tab(
#             # tab properties:
#             id="ocean_surface",
#             label='Ocean surface',
#             value='tab-ocean_surface',
#             className='custom-tab',
#             selected_className='custom-tab--selected',
#             # tab content:
#             children=[
#                 html.Div("stuff to introduce the proj"),
#                 html.Div("hi ther :-)")
#         ]),
#     ])
# ])
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)











# import dash
# import dash_html_components as html
# import dash_core_components as dcc
#
# from dash.dependencies import Input, Output
#
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#     dcc.Tabs(
#         id="tabs-with-classes",
#         value='tab-2',
#         parent_className='custom-tabs',
#         className='custom-tabs-container',
#         children=[
#             dcc.Tab(
#                 label='Tab one',
#                 value='tab-1',
#                 className='custom-tab',
#                 selected_className='custom-tab--selected'
#             ),
#             dcc.Tab(
#                 label='Tab two',
#                 value='tab-2',
#                 className='custom-tab',
#                 selected_className='custom-tab--selected'
#             ),
#             dcc.Tab(
#                 label='Tab three, multiline',
#                 value='tab-3', className='custom-tab',
#                 selected_className='custom-tab--selected'
#             ),
#             dcc.Tab(
#                 label='Tab four',
#                 value='tab-4',
#                 className='custom-tab',
#                 selected_className='custom-tab--selected'
#             ),
#         ]),
#     html.Div(id='tabs-content-classes')
# ])
#
#
# @app.callback(Output('tabs-content-classes', 'children'),
#               [Input('tabs-with-classes', 'value')])
# def render_content(tab):
#     if tab == 'tab-1':
#         return html.Div([
#             html.H3('Tab content 1')
#         ])
#     elif tab == 'tab-2':
#         return html.Div([
#             html.H3('Tab content 2')
#         ])
#     elif tab == 'tab-3':
#         return html.Div([
#             html.H3('Tab content 3x')
#         ])
#     elif tab == 'tab-4':
#         return html.Div([
#             html.H3('Tab content 4')
#         ])
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
#
#
#
#
#
#
#
# # # kirodh boodhraj
# # # 10/3/19
# # # purpose" to create a dummy graph of data given a ldb with fake water levels and then display it on a web app scatter plot
# # import dash
# # import dash_table
# # import dash_core_components as dcc
# # from dash.dependencies import Input, Output, State
# # import dash_html_components as html
# # from dash.exceptions import PreventUpdate
# # import plotly.plotly as py
# # import plotly.graph_objs as go
# # import random
# # import numpy as np
# # from datetime import datetime as dt
# # import pandas as pd
# # from readNames import readExcelFileDataSheet
# # import os
# #
# #
# #
# # # app.layout = html.Div([
# # #     dcc.DatePickerSingle(
# # #         id='my-date-picker-single',
# # #         min_date_allowed=dt(1995, 8, 5),
# # #         max_date_allowed=dt(2017, 9, 19),
# # #         initial_visible_month=dt(2017, 8, 5),
# # #         date=str(dt(2017, 8, 25, 23, 59, 59))
# # #     ),
# # #     html.Div(id='output-container-date-picker-single')
# # # ])
# # #
# # #
# # # @app.callback(
# # #     dash.dependencies.Output('output-container-date-picker-single', 'children'),
# # #     [dash.dependencies.Input('my-date-picker-single', 'date')])
# # # def update_output(date):
# # #     string_prefix = 'You have selected: '
# # #     if date is not None:
# # #         date = dt.strptime(date, '%Y-%m-%d')
# # #         date_string = date.strftime('%B %d, %Y')
# # #         return string_prefix + date_string
# #
# #
# #
# #
# #
# #
# #
# #
# # # # read in name data per division:
# # # MDSData = readExcelFileDataSheet(["names.xlsx", "MDS"])
# # # NREData = readExcelFileDataSheet(["names.xlsx", "NRE"])
# # # # put in the extra column to determine the presence:
# # # MDSData["not_present"] = "x" # x for not present
# # # NREData["not_present"] = "x"
# # # # print("mds:",MDSData)
# #
# # # # open marshals list:
# # # MARSHALData = readExcelFileDataSheet(["marshal_list.xlsx", "marshals"])
# # # MARSHALData = [{'label':' '.join(i),'value':num+1} for num,i in enumerate(zip(MARSHALData["name"].map(str),MARSHALData["surname"]))]
# # # # print(MARSHALData)
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # # style sheet: very clean and basic
# # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# #
# # app = dash.Dash(__name__, external_stylesheets=external_stylesheets,sharing=True)
# # server = app.server
# #
# # # tables and graphs
# #
# # app.layout = html.Div([
# #
# #     # Put some headers:
# #     html.H1(children="Welgevallen Gardens"), html.Div(children='''Garden bed map. When app loads, say the magic words:" I solemnly swear that I am up to no good " and the app will appear'''),
# #     # put in a dropdown here for marshal to select themselves:
# #     html.Div("", style={'padding': 50}),
# #     html.Div("Choose a date:",style={'textAlign': 'center'}),
# #     html.Div(children=dcc.DatePickerSingle(
# #         id='date',
# #         min_date_allowed=dt(2019, 1, 1),
# #         max_date_allowed=dt(2020, 1, 1),
# #         initial_visible_month=dt(2019, 5, 29),
# #         date=str(dt(2019, 5, 29))
# #     ),style={'textAlign': 'center'}),
# #     html.Div("", style={'padding': 50}),
# #     # put in doughnut graphs here:
# #     dcc.Graph(id='graph'),
# #     # html.Div("Key:", style={'padding': 50}),
# #     html.Div(children=dcc.Graph(id='graph2'), style={'marginLeft': '100px'}),
# #     html.Div("", style={'padding': 50}),
# #
# # ])
# #
# #
# #
# #
# #
# #
# # ## callbacks:
# #
# # @app.callback(
# #     dash.dependencies.Output('graph', 'figure'),
# #     [dash.dependencies.Input('date', 'date')])
# # def update_output(date):
# #     # print(date)
# #     if date is not None: # dont want empty date
# #         try: # seems as if the first value parsed has a time component added onto the date? try and except it out! Works.
# #             date = dt.strptime(date, '%Y-%m-%d')
# #         except:
# #             date = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
# #
# #         ## use this line below for the heading of graph later
# #         date_string = date.strftime('%B %d, %Y')
# #
# #         # find weeks from 1 Jan '19 to current time selected
# #         weeks = int((date-dt(2019,1,1)).days /7)
# #         if weeks == 0:
# #             weeks =1 # set weeks to 1 if it is 0, otherwise error
# #
# #         # open data for that week:
# #         data = readExcelFileDataSheet(["garden.xlsx",str(weeks)])
# #         # print(weeks,data)
# #
# #         # create colourscale
# #         # open file
# #         keys = readExcelFileDataSheet(["key.xlsx", "key"])
# #         # interval =1.0/ len(keys) # split the  interval between 0 and 1 with this
# #         intervals = np.linspace(0,1,len(keys))
# #         # print(intervals)
# #         # print(len(intervals))
# #
# #         my_colorsc = [[intervals[i], keys.iloc[i]["colour"]] for i in range(len(keys))]
# #
# #
# #         # def getColourAndPlant(rowData): # was for bar graph previously
# #         #     # function that gets colour from key table
# #         #     # open key file:
# #         #     keys = readExcelFileDataSheet(["key.xlsx","key"])
# #         #     # make lists to return:
# #         #     colours = []
# #         #     plantNames = []
# #         #
# #         #     # iterate through data:
# #         #     for entry in rowData:
# #         #         # find the colour and plant name
# #         #         tempdata = keys.loc[keys["key"] == entry] # get row with data
# #         #         colours.append(list(tempdata["colour"])[0])
# #         #         plantNames.append(list(tempdata["plant"])[0])
# #         #
# #         #     return [colours,plantNames]
# #         # # print(getColourAndPlant(data.iloc[0])) # testing
# #
# #
# #         def getColourAndPlant1(fullData):
# #             # function that gets colour from key table
# #             # open key file:
# #             keys = readExcelFileDataSheet(["key.xlsx","key"])
# #             # make lists to return:
# #             colours = []
# #             plantNames = []
# #             # print(fullData)
# #             # iterate through data:
# #             for ind,entry in fullData.iterrows():
# #                 # print(entry)
# #                 temarray = []
# #                 temarray2 = []
# #                 for ent1 in entry:
# #                     # find the colour and plant name
# #                     tempdata = keys.loc[keys["key"] == ent1] # get row with data
# #                     temarray.append(list(tempdata["colour"])[0])
# #                     temarray2.append(list(tempdata["plant"])[0])
# #                 colours.append(temarray)
# #                 plantNames.append(temarray2)
# #
# #             return [colours,plantNames]
# #         print(getColourAndPlant1(data)[0]) # testing
# #
# #
# #         # print(data)
# #         # for select in range(len(data)):
# #         traces =[]
# #         traces.append(go.Heatmap(
# #             y = [i+1 for i in range(len(data))],
# #             x=data.columns,
# #             z=data.values.tolist(),
# #             # opacity=0.6,
# #             text=getColourAndPlant1(data)[1],
# #             name="plant:",
# #             hoverinfo="text+x+y",
# #             hoverlabel={"namelength": 50},
# #             showscale=False,
# #             showlegend=False,
# #             colorscale = my_colorsc,
# #
# #         ))
# #
# #         layout = go.Layout(
# #         title=date_string+", week: "+str(weeks),
# #         xaxis={
# #             "title": "plot section",
# #             "tickfont": {"size": 20},
# #             'zeroline' : True,
# #             'showline' : True,
# #             'showgrid': True,
# #             'mirror' : 'ticks',
# #             'linecolor' : '#594021',
# #             'linewidth' : 6,
# #         },
# #         yaxis={
# #             "title": "Field",
# #             "tickangle": -90,
# #             "tickfont": {"size": 20},
# #             'autorange': 'reversed',
# #             'dtick':1,
# #             'showgrid': True,
# #             'zeroline': True,
# #             'showline': True,
# #             'mirror': 'ticks',
# #             'linecolor': '#594021',
# #             'linewidth': 6
# #         },
# #         hovermode='closest',
# #         height= 700,
# #         autosize=True,
# #
# #         )
# #
# #         # combine the graph and layout together into one object
# #         figure = {
# #             "data": traces,
# #             "layout": layout
# #         }
# #
# #         # return the figure
# #         return figure
# #
# # # put callback to draw static keys to other graph:
# # @app.callback(
# #     dash.dependencies.Output('graph2', 'figure'),
# #     [dash.dependencies.Input('date', 'date')])
# # def update_output(date):
# #     # just let this variable do nothing
# #     date
# #     # plot graph of keys:
# #     keys = readExcelFileDataSheet(["key.xlsx", "key"])
# #     # use traces to insert many bars and split the code into a graph part and layout part
# #     traces = []
# #     # print(keys["plant"].values.tolist())
# #     # for select in range(len(keys)):
# #     traces.append(go.Bar(
# #         x=[1 for i in range(len(keys))],
# #         y=keys["plant"].values.tolist(),
# #         orientation='h',
# #         marker=dict(
# #             color=keys["colour"].values.tolist(),
# #             line=dict(
# #             color=keys["colour"].values.tolist(),
# #             width=2)),
# #         # opacity=0.6,
# #         # mode='lines+markers',
# #         # labels=getColourAndPlant(data.iloc[select])[1],
# #         # text="gg",#[getColourAndPlant(data.iloc[select])[1]],
# #         hoverinfo="none",
# #         # hoverlabel={
# #         #     "namelength": 50},
# #         # # marker={"size": 6, },
# #         # showlegend=False,
# #     ))
# #
# #     layout = go.Layout(
# #         title="Key",
# #         xaxis={
# #             # "title": "plant",
# #             # "tickfont": {"size": 10},
# #             # "tickangle": -30,
# #             'ticks': '',
# #             'showticklabels': False,
# #             # 'zeroline': True,
# #             # 'showline': True,
# #             # 'showgrid': True,
# #             # 'mirror': 'ticks',
# #             # 'linecolor': '#594021',
# #             # 'linewidth': 6
# #         },
# #         yaxis={
# #             # "title": "Field",
# #             # "tickangle": -90,
# #             "tickfont": {"size": 14},
# #             'autorange': 'reversed',
# #             # 'dtick': 1,
# #             'showgrid': True,
# #             'automargin':True,
# #             # 'zeroline': True,
# #             # 'showline': True,
# #             # 'mirror': 'ticks',
# #             # 'linecolor': '#594021',
# #             # 'linewidth': 6,
# #         },
# #         hovermode='closest',
# #         height=700,
# #         autosize=True,
# #         width=400,
# #     )
# #
# #     # combine the graph and layout together into one object
# #     figure = {
# #         "data": traces,
# #         "layout": layout
# #     }
# #     return figure
# #
# #
# # """end"""
# #
# #
# #
# #
# # if __name__ == '__main__':
# #     app.run_server(debug=True)
