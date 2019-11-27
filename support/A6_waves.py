# -*- coding: utf-8 -*-
"""
.. module:: Waves
    :platform: Windows 7, Python 3.7.
    :synopsis: This module holds the functions developed by Gert Wessels and Dr. Kobie Smit.
.. moduleauthor:: Kirodh Boodhraj <kboodhraj@csir.co.za>
                  Gert Wessels <gwessels@csir.co.za>
                  Dr. Kobie Smit <ksmit@csir.co.za>


"""

# import system modules here:
import datetime as dt
import pathlib as pl
import sys
#import base64
import os
#import io

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
from .data_import import Data_Import
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from scipy.special import gamma, gammainc
from scipy.stats import invgauss

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)
app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}


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


def load_data(filename):
    
    di = Data_Import()
    di.set_default_ncep_wave_columns()
    di.read_data(filename)

# columns: y m d t HMO hlf TP tz tcf tbf DIR spr hs hmax instr
#          0 1 2 3  4   5   6  7  8   9  10  11  12  13    14
    data = di.data
    date = pd.DataFrame(di.date_time)
    
    df = pd.DataFrame(data, columns = ['year', 'month', 'day', 'time', 'hmo', 
                                       'hlf', 'tp', 'tz', 'tcf', 'tbf', 'dir', 
                                       'spr', 'hs', 'hmax', 'instr' ], 
                      dtype = float)
    df = df.drop(columns=['hlf', 'tz', 'tcf', 'tbf', 'spr', 'hs', 'hmax', 'instr' ])
    
    df[df['hmo']==0] = np.nan
    
    df['Date'] = date
    
    return df

def wind_rose_update(in_df):
    
    max_hm0 = max(in_df['hmo'])
    
    lvl = {'l1':(max_hm0*0.75, max_hm0), 'l2':(max_hm0*0.50, max_hm0*0.75), 
           'l3':(max_hm0*0.25, max_hm0*0.50), 'l4':(0, max_hm0*0.25)}
    
    direction = [("North", 337.5, 22.5), ("N-E", 22.5, 67.5), ("East", 67.5, 112.5), 
                 ("S-E", 112.5, 157.5), ("South", 157.5, 202.5), ("S-W", 202.5, 247.5), 
                 ("West", 247.5, 292.5), ("N-W", 292.5, 337.5)]

    cnt = len(in_df)
    
    df = pd.DataFrame({'direction':direction})
    for l in lvl.keys():
        df[l] = 0
    
    for l in lvl.keys():
        
        tmp_df = in_df[(in_df['hmo']>=lvl[l][0]) & (in_df['hmo']<lvl[l][1])]
        
        for index, row in df.iterrows():
            if row['direction'][0] == "North":
                df.at[index,l] = 100.0*len(tmp_df[(tmp_df['dir']>= row['direction'][1]) | (tmp_df['dir']< row['direction'][2])])/cnt
            else:
                df.at[index,l] = 100.0*len(tmp_df[(tmp_df['dir']>= row['direction'][1]) & (tmp_df['dir']< row['direction'][2])])/cnt
    
    return [lvl, df]
    

def extract_peaks_rolling(df,stormDuration, autoThres, method):
    df = df.reset_index(drop=True)
    
    duration_s = stormDuration*60*60
    df[df['hmo']>900] = -0.1
    df[df['tp']>900] = -0.1
    dt_0 = df['Date'][0]
    pp = []
    
    for i in range(1,len(df)-2):
        if((df['hmo'][i]-df['hmo'][i-1]>=0) and (df['hmo'][i]-df['hmo'][i+1]>=0) ):
            calc = df['Date'][i] - dt_0
            ds = calc.days*24*60*60+calc.seconds
            pp.append([df.index[i],  df['Date'][i].year,  df['Date'][i].month,  df['Date'][i].day,  df['Date'][i].time(), df['Date'][i], ds, df['hmo'][i], df['tp'][i], df['dir'][i]])

    peaks = pd.DataFrame(pp, columns=['index','year','month','day','time','date_time','seconds','hmo','tp','dir'])
    
    storms = peaks.copy()
    
    storms_max = storms.groupby(storms['date_time'].dt.date)['hmo'].max()
    
    storms_dur = storms_max.rolling(int(stormDuration/24),center=True).max()
    data = []
    for index, row in storms_dur.iteritems():
        tmp = storms[ (storms['year']==index.year) & (storms['month']==index.month) & (storms['day']==index.day) & (storms['hmo']==row)]
        
        if len(tmp)>0:
            data.append([tmp['date_time'].iloc[0],tmp['hmo'].iloc[0],tmp['tp'].iloc[0],tmp['dir'].iloc[0]])
    
    data = pd.DataFrame(data, columns=['date_time','hmo','tp','dir'])
    
    if autoThres:
        POT = autoThresholdSelect(data['hmo'],method)
    
    res = data[data['hmo']>=POT] 
    
    return [res, POT]
    

def autoThresholdSelect(x, method):
    Nuc     = 100             #number of candidate thresholds
    u1      = np.median(x)
    xs      = np.sort(x)
    Nx      = len(x)
    xsi98   = np.ceil(0.98*Nx)

    if Nx-xsi98 < 100:
        xsi98 = Nx-99
        
    if xsi98 < 1:
        u = 0
        return u
    
    un = xs[xsi98]
    uc = np.linspace(u1, un, Nuc)
    
    alpha = np.zeros(Nuc)
    beta  = np.zeros(Nuc)
    tao   = np.zeros(Nuc)
    
    for i in np.arange(0,Nuc):
        if method == 'weibull':
            xuc = x[x>uc[i]]
            xuc = xuc - uc[i]
            [alpha[i], beta[i], chipassed] = weibull(xuc)
        elif method == 'weibull3':
            xuc = x[x>i]
            xuc = xuc - uc[i]
            print(xuc)
            [alpha[i], beta[i], xi, chipassed] = weibull3(xuc)

        if method == 'weibull3':
            tao[i] = alpha[i] - beta[i]*xi
        else:
            tao[i] = alpha[i] - beta[i]*uc[i]

    dtao = np.diff(tao)

    Nt = len(tao)
    for i in range(Nt):
        ChisPassed = ChisTest_gauss(dtao, 2, 0, np.std(dtao))
        if ChisPassed == 1:
            u = uc[i]
            return u
        dtao = dtao[1:]
    return un

def ChisTest_gauss(x, r, mu, sigma):
    n = len(x)
    k = int(round(1 + 3.3*np.log10(n))) #change this estimate laters
    prob  = 1.0/k
    probs = [xi/float(k) for xi in range(k)]
    x = np.array(x)
    
    quantiles = invgauss.cdf(probs, mu)
    e = np.ones(k)*n*(prob)
    o = np.zeros(len(e))
    
    for i in range(len(o)):
        if i == len(o)-1:
            o[i] = len(x[x >= quantiles[i]])
        else:
            o[i] = len(x[(x < quantiles[i+1]) & (x >= quantiles[i]) ])
    Chis = sum(((o - e)**2)/e)
    alpha = gammainc((k-r-1)/2, Chis/2)
    if (alpha > 0.05):
        return True
    else:
        return False

def ChisTest_weibull(x, r, alpha, beta):
    n = len(x)
    k = int(round(1 + 3.3*np.log10(n))) #change this estimate laters
    prob  = 1.0/k
    probs = [i/float(k) for i in range(k)]
    
    quantiles = quantile_weibull(probs, alpha, beta)
    e = np.ones(k)*n*(prob)
    o = np.zeros(len(e))
    
    for i in range(len(o)):
        if i == len(o)-1:
            o[i] = len(x[x >= quantiles[i]])
        else:
            o[i] = len(x[(x < quantiles[i+1]) & (x >= quantiles[i]) ])
    Chis = sum(((o - e)**2)/e)
    alpha = gammainc((k-r-1)/2, Chis/2)
    if (alpha > 0.05):
        return True
    else:
        return False

    
def ChisTest_weibull3(x, r, alpha, beta, xi):
    n = len(x)
    k = int(round(1 + 3.3*np.log10(n))) #change this estimate laters
    prob  = 1.0/k
    probs = [i/float(k) for i in range(k)]
    x = np.array(x)
    
    quantiles = quantile_weibull3(probs, alpha, beta, xi)
    e = np.ones(k)*n*(prob)
    o = np.zeros(len(e))
    
    for i in range(len(o)):
        if i == len(o)-1:
            o[i] = len(x[x >= quantiles[i]])
        else:
            o[i] = len(x[(x < quantiles[i+1]) & (x >= quantiles[i]) ])
    Chis = sum(((o - e)**2)/e)
    alpha = gammainc((k-r-1)/2, Chis/2)
    if (alpha > 0.05):
        return True
    else:
        return False


def weibull(x):
    x[x==0] = x[x==0] + 0.01
    
    alpha_   = 0.5
    beta__   = 0.48
    beta_    = 0.5
    epsilon  = 0.05
    max_iter = 1e2
    n        = len(x)
    
    sigma2  = np.var(x)
    mu      = np.mean(x)
    converged = False
    i = 0
    
    while not converged and i < max_iter:
        beta = beta_ - (beta_ - beta__)/(mom_beta(beta_,sigma2,mu) - mom_beta(beta__,sigma2,mu))*mom_beta(beta_,sigma2,mu)
        
        if (abs(beta-beta_)/beta_)<epsilon:
            converged = True
            
        i = i+1
        beta__ = beta_
        beta_  = beta
        
    alpha = mu/gamma(1+1.0/beta)

    # Maximum Likelihood estimation
    converged = False
    i = 0
    beta_ = 0.9*beta_
    while not converged and i < max_iter:
        try:
            beta = 1.0/(sum(np.log(x)*x**beta_)/sum(x**beta_) - 1.0/n*sum(np.log(x)))
        except:
            beta = np.nan
        
        if (abs((beta-beta_)/beta_)*100 < epsilon):
            converged = True
        
        i = i+1
        beta_ = beta

    alpha = (1.0/n*sum(x**beta))**(1/beta)
    
    Chispassed = ChisTest_gauss(x,2,alpha,beta)
    
    return [alpha, beta, Chispassed]

def weibull3(x):
    x[x==0] = x[x==0] + 0.01
    
    alpha_   = 0.5
    beta__   = 0.48
    beta_    = 0.5
    epsilon  = 0.05
    max_iter = 1e2
    n        = len(x)
    
    sigma2  = np.var(x)
    mu      = np.mean(x)
    converged = False
    i = 0
    gamma3 = np.mean( (x-mu)**3 /(np.mean(x-mu)**2) )**(3.0/2)
    if (gamma3 >= 0.25) & (gamma3 <= 5) & (n>=20) & (n<=90):
        B = (0.01 + 5.05/n + 20.13/(n**2)) + (0.69/n + 27.15/(n**2))*gamma3**3
        gamma3 = (1+B)*gamma3
    else:
        gamma3 = np.sqrt(n*(n-1))*gamma3/(n-2)
    
    while not converged & (i < max_iter):
        beta = beta_ - (beta_ - beta__)/(mom_beta_3(beta_,gamma3) - mom_beta_3(beta__,gamma3))*mom_beta_3(beta_,gamma3)
        if (abs(beta-beta_)/beta_)*100<epsilon:
            converged = True
            
        i = i+1
        beta__ = beta_
        beta_  = beta
        
    alpha = np.sqrt(sigma2)/np.sqrt(gamma(1+2.0/beta)-(gamma(1+1.0/beta)**2))
    xi = mu - alpha*gamma(1+1.0/beta)
        
    Chispassed = ChisTest_weibull3(x,2,alpha,beta,xi)
    
    return [alpha, beta, xi, Chispassed]

def mom_beta(beta, sigma2, mu):
    return gamma(1+2.0/beta)/gamma(1+1.0/beta)**2 - (sigma2/mu**2 + 1)

def mom_beta_3(beta, gamma3):
    return (gamma(1+3.0/beta) - 3*gamma(1+1.0/beta)*gamma(1+2.0/beta) +  2*(gamma(1+1.0/beta))**3)/(gamma(1+2.0/beta) - (gamma(1+1.0/beta))**2)**(3/2) - gamma3

def quantile_weibull(p,alpha, beta):
    return alpha*(-np.log(1-p))**(1.0/beta)

def quantile_weibull3(p,alpha, beta,xi):
    return xi + alpha*(-np.log(1-p))**(1.0/beta)

def pdf_weibull(x,alpha,beta):
    return beta/alpha*(x/alpha)**(beta-1)*np.exp(-(x/alpha)**beta)

## --------- Kobie's functions ----------- ##
def month_names(df):
    ## Create dataframe with Datetime index. Add month names

    df_info = df.copy()
    df_info.set_index('Date', inplace=True)
    df_info['Month_Name'] = df_info.index.month_name()

    ## Fill in all NaN values with a linear interpolation method
#    df_info.interpolate(method='linear', axis=0, inplace=True)    
    
    ## Cast year, month and day to integers (previously floats)
#    df_info.year = df_info.year.astype(int)
#    df_info.month = df_info.month.astype(int)
#    df_info.day = df_info.day.astype(int)
#    df_info.time = df_info.time.astype(int)
    
    return list(df_info['Month_Name'].unique())

## Boxplot formatting
def col_range(N):
   # generate an array of rainbow colors by fixing the saturation and lightness of the HSL
    # representation of colour and marching around the hue.
    # Plotly accepts any CSS color format, see e.g. http://www.w3schools.com/cssref/css_colors_legal.asp.
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)] 
    
    return c

## --------- End of Kobie's functions ----------- ##

###############################################
# put the dash layout here
# ...


address = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(address, 'data')


df = load_data(os.path.join(path, '31118_all.wav'))
mxy = int(df['year'].max())
mny = int(df['year'].min())
yr_dict = {}
for y in np.arange(mny,mxy+1):
    yr_dict[str(y)] = str(y)
print(mxy,mny)
print(yr_dict)

# Get a list of the month names for the boxplot
months = month_names(df)

# Boxplot colour formatting
num_m = df['month'].nunique() ## 12 months in year
box_colours = col_range(num_m) 


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

header_text = html.H1('Waves')


   
    
layout = html.Div([
#    # header (leave alone):
    header_logo,
    header_text, html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),

    dcc.Loading(id="loading", children=[
            html.Div([dcc.Graph(id="hmo-graph")]),
            html.Div([dcc.Graph(id="tp-graph")]),
            html.Div([dcc.Graph(id="dir-graph")]),
            html.Div([html.H2("Wave characteristics grouped by Month")], 
                      style={"textAlign": "center"}),
            html.Div([dcc.Graph(id="box-graph")]),
    ], type="default"),

    html.Div([dcc.RangeSlider(id="year-range", min=mny, max=mxy, step=1, value=[mny, mxy],
                                                 marks=yr_dict)]),
    
    
#    html.Div([dcc.RangeSlider(id="year-range", min=1997, max=2013, step=1, value=[1997, 2013],
#                                                 marks={"1997": str(1997), "1998": str(1998), "1999": str(1999),
#                                                        "2000": str(2000), "2001": str(2001), "2002": str(2002),
#                                                        "2003": str(2003), "2004": str(2004), "2005": str(2005),
#                                                        "2006": str(2006), "2007": str(2007), "2008": str(2008),
#                                                        "2009": str(2009), "2010": str(2010), "2011": str(2011),
#                                                        "2012": str(2012), "2013": str(2013)
#                                                        })]),
    html.Br(), html.Br(),
], className="container")


@app.callback(
    [Output('hmo-graph', 'figure'), Output('tp-graph', 'figure'), Output('dir-graph', 'figure'), Output('box-graph', 'figure')],
    [Input('year-range', 'value')])
def update_figure(year):
    
    dff = df[(df["year"] >= year[0]) & (df["year"] <= year[1])]
    
    [res, POT] = extract_peaks_rolling(dff, 48, True, 'weibull' )
    trace1 = []
    trace1.append(go.Scatter(x=dff["Date"], y=dff['hmo'], name='Significant Wave Height', mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    trace1.append(go.Scatter(x=res["date_time"], y=res['hmo'], name='Storms/ Extreme events', mode='markers', marker_color='rgba(255, 0, 0, 0.9)'))
    
    trace2 = []
    trace2.append(go.Scatter(x=dff["Date"], y=dff['tp'], name='Peak Wave Period', mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    trace2.append(go.Scatter(x=res["date_time"], y=res['tp'], name='Storms/ Extreme events', mode='markers', marker_color='rgba(255, 0, 0, 0.9)'))
    
    [lvl, rose_df] = wind_rose_update(dff)
    
    fig = go.Figure()
    
    fig.add_trace(go.Barpolar(
                    r=[i for i in rose_df['l4']],
                    text=[i[0] for i in rose_df['direction']],
                    name='<%0.2f m'%(lvl['l4'][1]),
                    marker=dict(color='rgb(242,240,247)')
                    ))
    fig.add_trace(go.Barpolar(
                    r=[i for i in rose_df['l3']],
                    text=[i[0] for i in rose_df['direction']],
                    name='%0.2f-%0.2f m'%(lvl['l3'][0],lvl['l3'][1]),
                    marker=dict(color='rgb(203,201,226)')
                    ))    
    fig.add_trace(go.Barpolar(
                    r=[i for i in rose_df['l2']],
                    text=[i[0] for i in rose_df['direction']],
                    name='%0.2f-%0.2f m'%(lvl['l2'][0],lvl['l2'][1]),
                    marker=dict(color='rgb(158,154,200)')
                    ))    
    fig.add_trace(go.Barpolar(
                    r=[i for i in rose_df['l1']],
                    text=[i[0] for i in rose_df['direction']],
                    name='%0.2f-%0.2f m'%(lvl['l1'][0],lvl['l1'][1]),
                    marker=dict(color='rgb(106,81,163)')
                    ))
    
    fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
    fig.update_layout(
        title='Significant Wave Height Directional Distribution',
        font_size=16,
        legend_font_size=16,
        polar_radialaxis_ticksuffix='%',
        polar_angularaxis_rotation=90,
        polar = dict(angularaxis = dict(direction = "clockwise",period = 6)                    )
        )
    
    ## Boxplot updates:
    # Initialise figure with subplots
    fig_bp = make_subplots(rows=3, cols=1, 
                           subplot_titles=(f"Significant wave heights for {'-'.join(str(i) for i in year)}",
                           f"Peak wave periods for {'-'.join(str(i) for i in year)}",
                           f"Significant wave height directional distributions for {'-'.join(str(i) for i in year)}"))
    
    # Add traces
    for month, month_name, cls in zip(dff.month.unique(), months, box_colours):
        fig_bp.add_trace(go.Box(y=dff[dff['month'] == month]['hmo'], name=month_name, marker={'size': 4, 'color': cls}, showlegend=False), row=1, col=1)
        fig_bp.add_trace(go.Box(y=dff[dff['month'] == month]['tp'], name=month_name, marker={'size': 4, 'color': cls}, showlegend=False), row=2, col=1)
        fig_bp.add_trace(go.Box(y=dff[dff['month'] == month]['dir'], name=month_name, marker={'size': 4, 'color': cls}, showlegend=False), row=3, col=1)
    
    # Update xaxis properties
    for i in [1,2,3]:
        fig_bp.update_xaxes(title_text='Month', row=i, col=1)
    
    # Update yaxis properties
    axes_labels = ['Sig wave height (m)', 'Peak wave period (s)', 'Sig wave dir (degrees)']
    for ylabel in axes_labels:
        fig_bp.update_yaxes(title_text=ylabel, row=(axes_labels.index(ylabel)+1), col=1)
        
    # Update figure layout
    fig_bp.update_layout(autosize=True,
                         margin={"l": 70, "b": 80, "r": 70},
                         xaxis={"showticklabels": True,},
                         yaxis={"zerolinecolor": "rgb(243, 243, 243)", "zerolinewidth": 3,},
                         width=960,
                         height=1100 #px
                         )
           
    return [{"data": trace1,
            "layout": go.Layout(title="Significant Wave Height", colorway=['#2c7bb6','#81e36d'],
                                yaxis={"title": "Hm0 ( meter )"}, yaxis2={"title": "Tp ( second )", "side":"right", "overlaying":'y'}, 
                                xaxis={"title": "Date"})},
            {"data": trace2,
            "layout": go.Layout(title="Peak Wave Period", colorway=['#81e36d'],
                                yaxis={"title": "Tp ( second )"}, xaxis={"title": "Date"})},
            fig,
            fig_bp
            ]

