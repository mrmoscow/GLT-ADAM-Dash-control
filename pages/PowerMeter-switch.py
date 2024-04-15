import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

import time
from datetime import datetime
import socket

import ReceiverADAM as RAD #module for this project

dash.register_page(__name__)


channelOpt=RAD.channelOpt


#d_k = 'SAPar'
#d_v = 'NotAssigned'
#for remove the dic whit key,value=label,NotAssigned, also remove the key=SAPar for dropdown 
#channel_O2 = [{k : v for k, v in s.items() if k in ['label','value']} for s in channelOpt if s['label'] != 'NotAssigned']
def gotopt(gr):
    return [{k : v for k, v in s.items() if k in ['label','value']} for s in channelOpt if s['gr'] is gr]
#print(gotopt(channelOpt,'1A'))


layout = html.Div([
    html.H3('PowerMeter Selection Select'),
    #dcc.Dropdown(id='SA_sel', options=channel_O2,style={'max-width': '500px'}, placeholder='SA-chaannel-Select'),
    html.Br(),
    html.Table([
        html.Tr([html.Th(['Channel']),html.Th(['which IF you want!']),html.Th(),html.Th(['Setting Result'])]),
        html.Tr([html.Td([],style={'width':'200px'}),html.Td([],style={'width':'280px'}),
                 html.Td([],style={'width':'120px'}),html.Td([],style={'width':'200px'})],
                 style={'visibility':'hidden'}),
        html.Tr([html.Td(['PM 1, Channal A']),html.Td([dcc.Dropdown(id='1A',options=gotopt('P1A'))]),
                 html.Td([html.Button('Here to set.',id='PM_set')],rowSpan=0),html.Td(id='r_1A')]),
        html.Tr([html.Td(['PM 1, Channal B']),html.Td([dcc.Dropdown(id='1B',options=gotopt('P1B'))]),html.Td(id='r_1B')]),
        html.Tr([html.Td(['PM 2, Channal A']),html.Td([dcc.Dropdown(id='2A',options=gotopt('P2A'))]),html.Td(id='r_2A')]),
        html.Tr([html.Td(['PM 2, Channal B']),html.Td([dcc.Dropdown(id='2B',options=gotopt('P2B'))]),html.Td(id='r_2B')]),
        html.Tr([html.Td(['PM 3, Channal A']),html.Td([dcc.Dropdown(id='3A',options=gotopt('P3A'))]),html.Td(id='r_3A')]),
        html.Tr([html.Td(['PM 3, Channan B']),html.Td([dcc.Dropdown(id='3B',options=gotopt('P3B'))]),html.Td(id='r_3B')]),
        html.Tr([html.Td(['PM 4, Channal A']),html.Td([dcc.Dropdown(id='4A',options=gotopt('P4A'))]),html.Td(id='r_4A')]),
        html.Tr([html.Td(['PM 4, Channal B']),html.Td([dcc.Dropdown(id='4B',options=gotopt('P4B'))]),html.Td(id='r_4B')]),
        ],style={'max-width': '1000px','border-spacing':'30px 10px'}),
    html.Br(),
    html.Div(id='PM_res'),
    html.H6('Next is still under Development,'),
    html.Table([
        html.Tr([html.Th(['Power Meter  & Channel ']),html.Th(['IF now']),html.Th('Get Power Button'),html.Th('Power (dBm)')]),
        html.Tr([html.Td([],style={'width':'250px'}),html.Td([],style={'width':'350px'}),html.Td([],style={'width':'250px'})],
            style={'visibility':'hidden'}),
        html.Tr([html.Td(['PM 1, Channal A']),html.Td(id='S_1A'),
                 html.Td([html.Button('Got Power Value',id='GB')],rowSpan=0),html.Td(id='P_1A'),]),
        html.Tr([html.Td(['PM 1, Channal B']),html.Td(id='S_1B'),html.Td(id='P_1B'),]),
        html.Tr([html.Td(['PM 2, Channal A']),html.Td(id='S_2A'),html.Td(id='P_2A'),]),
        html.Tr([html.Td(['PM 2, Channal B']),html.Td(id='S_2B'),html.Td(id='P_2B')]),
        html.Tr([html.Td(['PM 3, Channal A']),html.Td(id='S_3A'),html.Td(id='P_3A')]),
        html.Tr([html.Td(['PM 3, Channal B']),html.Td(id='S_3B'),html.Td(id='P_3B')]),
        html.Tr([html.Td(['PM 4, Channal A']),html.Td(id='S_4A'),html.Td(id='P_4A')]),
        html.Tr([html.Td(['PM 4, Channal B']),html.Td(id='S_4B'),html.Td(id='P_4B')]),
        ],style={'max-width': '800px','border-spacing':'30px 10px'}),
    html.Br(),
    html.Button('Check IF at..',id='getIF'),
    html.Br(),
])

the_app = dash.get_app()        # Must specify due to @dash.callback limitations
@the_app.callback(Output('r_1A','children'),Output('r_1B','children'),Output('r_2A','children'),Output('r_2B','children'),
          Output('r_3A','children'),Output('r_3B','children'),Output('r_4A','children'),Output('r_4B','children'),
          Input('PM_set','n_clicks'),
          State('1A','value'),State('1B','value'),State('2A','value'),State('2B','value'),
          State('3A','value'),State('3B','value'),State('4A','value'),State('4B','value'),
          )
def PM_set(n_clicks,i_1A,i_1B,i_2A,i_2B,i_3A,i_3B,i_4A,i_4B):
    if n_clicks is None:
        raise PreventUpdate
    else:
        a=[i_1A,i_1B,i_2A,i_2B,i_3A,i_3B,i_4A,i_4B]
        #print(a)
        r=[]
        for i in a:
            if i is None:
                r.append(None)
            else:
                #r.append("Good")
                r.append(RAD.CAB1417switch(i,'PM'))
        return r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7]

@the_app.callback(
  Output('P_1A','children'),Output('P_1B','children'),
  Output('P_2A','children'),Output('P_2B','children'),
  Output('P_3A','children'),Output('P_3B','children'),
  Output('P_4A','children'),Output('P_4B','children'),
  Input('GB','n_clicks'),
         )
def PM_get(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        a,b=RAD.get_Power('PM1')
        c,d=RAD.get_Power('PM2')
        e,f=RAD.get_Power('PM3')
        g,h=RAD.get_Power('PM4')
        return a,b,c,d,e,f,g,h

@the_app.callback(
  Output('S_1A','children'),Output('S_1B','children'),
  Output('S_2A','children'),Output('S_2B','children'),
  Output('S_3A','children'),Output('S_3B','children'),
  Output('S_4A','children'),Output('S_4B','children'),
  Input('getIF','n_clicks'),
  )
def IF_get(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        a0,a1=RAD.getPowIF('P1A')
        b0,b1=RAD.getPowIF('P1B')
        c0,c1=RAD.getPowIF('P2A')
        d0,d1=RAD.getPowIF('P2B')
        e0,e1=RAD.getPowIF('P3A')
        f0,f1=RAD.getPowIF('P3B')
        g0,g1=RAD.getPowIF('P4A')
        h0,h1=['Still Testing','Still Testing']#RAD.getPowIF('P4B')
        return a0,b0,c0,d0,e0,f0,g0,h0
