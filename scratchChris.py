import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from support import A1_welcome,A2_temperature,A3_salinity,A4_currents,A5_energy,A6_waves,A7_shipRouteOptimization,A8_oceanSurface,A9_particleTracking
import os

app.layout = html.Div([
    dcc.Location(id='url', refresh=True, pathname="/support/A1_welcome"),
    html.Div(id='page-content'),
    dcc.Link(html.Button("Welcome page"), href='/support/A1_welcome', className="welcomePage"),
    html.Spacer("  "),
    dcc.Link(html.Button("Temperature"), href='/support/A2_temperature', className="temperature"),
    html.Spacer("  "),
    # dcc.Link(html.Button("Salinity"), href='/support/A3_salinity', className="salinity"),
    # html.Spacer("  "),
    dcc.Link(html.Button("Currents"), href='/support/A4_currents', className="currents"),
    html.Spacer("  "),
    # dcc.Link(html.Button("Energy"), href='/support/A5_energy', className="energy"),
    # html.Spacer("  "),
    # dcc.Link(html.Button("Waves"), href='/support/A6_waves', className="waves"),
    # html.Spacer("  "),
    dcc.Link(html.Button("Ship Route Optimization"), href='/support/A7_shipRouteOptimization',
             className="shipRouteOptimization"),
    html.Spacer("  "),
    # dcc.Link(html.Button("Ocean Surface"), href='/support/A8_oceanSurface', className="oceanSurface"),
    # html.Spacer("  "),
    # dcc.Link(html.Button("Particle Tracking"), href='/support/A9_particleTracking', className="particleTrackingButton"),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # print(pathname)
    if pathname == '/support/A1_welcome':
        return A1_welcome.layout
    elif pathname == '/support/A2_temperature':
        return A2_temperature.layout
    # elif pathname == '/support/A3_salinity':
    #     return A3_salinity.layout
    elif pathname == '/support/A4_currents':
        return A4_currents.layout
    # elif pathname == '/support/A5_energy':
    #     return A5_energy.layout
    # elif pathname == '/support/A6_waves':
    #     return A6_waves.layout
    elif pathname == '/support/A7_shipRouteOptimization':
        return A7_shipRouteOptimization.layout
    # elif pathname == '/support/A8_oceanSurface':
    #     return A8_oceanSurface.layout
    # elif pathname == '/support/A9_particleTracking':
    #     return A9_particleTracking.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader = False)