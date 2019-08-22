# this is your scratch patch:
# it is a template for your testing of viewing of the graphs, testing other functions you write etc. ...



# basic template for testing your functions
# -*- coding: utf-8 -*-

# import your module:
from kobie import Kobie

# import other
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pathlib as pl




app = dash.Dash(__name__)
# app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(
            # tab properties:
            id="welcome",
            label='Welcome',
            value='tab-welcome',
            className='custom-tab',
            selected_className='custom-tab--selected',
            # tab content:
            children=[
                Kobie.kobie(),
                Kobie.kobie()
        ]),
        dcc.Tab(
            # tab properties:
            id="temperature",
            label='Temperature',
            value='tab-temperature',
            className='custom-tab',
            selected_className='custom-tab--selected',
            # tab content:
            children=[
                Kobie.kobie()
        ]),
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)



# test other functions here:


