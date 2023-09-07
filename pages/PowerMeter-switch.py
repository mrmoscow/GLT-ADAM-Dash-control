import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

import time
from datetime import datetime
import socket

import ReceiverADAM as RAD #module for this project

dash.register_page(__name__)



#The SAPar:[Center Frequency(Hz),SPAN(Hz),Reference Lavel (dBm),Scale(dB/div),RBW(Hz),VBW(Hz)]
channelOpt =[
 {'label':'EHT1_POL0 IF 4-9 GHz',    'value':1,  'gr':'P1A',   'SAPar':[8E9,1E10,-40,5,3E6,300]},
 {'label':'EHT1_POL0 BB 6-8 GHz',    'value':2,  'gr':'P1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL0 BB 4-6 GHz',    'value':3,  'gr':'P1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL1 BB 4-6 GHz',    'value':4,  'gr':'P1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL1 IF 4-9 GHz',    'value':5,  'gr':'P1B',   'SAPar':[8E9,1E10,-40,5, 3E6,300]},
 {'label':'EHT1_POL1 BB 6-8 GHz',    'value':6,  'gr':'P1B',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'10Mhz-Left rack',         'value':7,  'gr':'P1B',   'SAPar':[1E7,200,10,10, 1,1]},
 {'label':'100MHz',                  'value':8,  'gr':'P1B',   'SAPar':[1E8,200,10,10, 1,1]},
 {'label':'ContDet Input LHC 4-8GHz','value':9,  'gr':'P2A',   'SAPar':[6E9,8E9,-60,2, 3E6,300]},
 {'label':'ContDet Input RHC 4-8GHz','value':10, 'gr':'P2A',   'SAPar':[6E9,8E9,-60,2, 3E6,300]},
 {'label':'VVM Input (Rx) 50 MHz',   'value':11, 'gr':'P2A',   'SAPar':[5E7,200,-40,10, 1,1]},
 {'label':'VVM Input (Ref) 50 MHz',  'value':12, 'gr':'P2A',   'SAPar':[5E7,200,0,10, 1,1]},
 {'label':'5.95 GHz',                'value':13, 'gr':'P2B',   'SAPar':[5.9E9,200,0,10, 1,1]},
 {'label':'0.5 or 1.5 GHz',          'value':14, 'gr':'P2B',   'SAPar':[1E9,1.6E9,0,10, 3E6,300]},
 {'label':'31.5 MHz',                'value':15, 'gr':'P2B',   'SAPar':[3.15E7,200,-50,10, 1, 1]},
 {'label':'44.5 or 18.5MHz',         'value':16, 'gr':'P2B',   'SAPar':[31.5E6,50E6,-40,10, 1,1]},
 {'label':'NotAssigned',             'value':17, 'gr':'S17',   'SAPar':[4.0E9,1.0E9,0,10, 10E4,1E5]},
 {'label':'NotAssigned',             'value':18, 'gr':'S18',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'EHT1_LO_6GHz',            'value':19, 'gr':'S19',   'SAPar':[6E9,200,10,10, 1,1]},
 {'label':'EHT1_LO_7GHz',            'value':20, 'gr':'S20',   'SAPar':[7E9,200,10,10, 1,1]},
 {'label':'NotAssigned',             'value':21, 'gr':'S21',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Ref1+Ref3 (Test)',        'value':22, 'gr':'S22',   'SAPar':[27E9,20E9,20,10, 3E6,300]},
 {'label':'EHT2_POL0 IF 4-9',        'value':23, 'gr':'P3A',   'SAPar':[8E9,1E10,-40,5,3E6,300]},
 {'label':'EHT2_POL0 BB 6-8 GHz',    'value':24, 'gr':'P3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL0 BB 4-6 GHz',    'value':25, 'gr':'P3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL1 BB 4-6 GHz',    'value':26, 'gr':'P3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL1 IF 4-9 GHz',    'value':27, 'gr':'P3B',   'SAPar':[8E9,1E10,-40,5, 3E6,300]},
 {'label':'EHT2_POL1 BB 6-8 GHz',    'value':28, 'gr':'P3B',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'3.85 GHz',                'value':29, 'gr':'P3B',   'SAPar':[3.85E9,200,10,10, 1,1]},
 {'label':'8.15 GHz',                'value':30, 'gr':'P3B',   'SAPar':[8.15E9,200,10,10, 1,1]},
 {'label':'2.048 GHz',               'value':31, 'gr':'P4A',   'SAPar':[2.048E9,200,10,10, 1,1]},
 {'label':'NotAsssigned',            'value':32, 'gr':'P4A',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'EHT2 LO (6GHz)',          'value':33, 'gr':'P4A',   'SAPar':[6E9,200,10,10, 1,1]},
 {'label':'EHT2 LO (7GHz)',          'value':34, 'gr':'P4A',   'SAPar':[7E9,200,10,10, 1,1]},
 {'label':'NotAssigned',             'value':35, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':36, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':37, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':38, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':39, 'gr':'S39',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':40, 'gr':'S40',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':41, 'gr':'S41',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':42, 'gr':'S42',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Spectrum path (RF Swwitch #1)',   'value':43, 'gr':'S43',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Ref1(18-32GHz)',                  'value':44, 'gr':'S44',   'SAPar':[25E9,20E9,-15,5, 3E6,300]},
  ]

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
        html.Tr([html.Td(['PM 2, Channal B']),html.Td(['None']),html.Td(id='P_2B')]),
        html.Tr([html.Td(['PM 3, Channal A']),html.Td(id='S_3A'),html.Td(id='P_3A')]),
        html.Tr([html.Td(['PM 3, Channal B']),html.Td(id='S_3B'),html.Td(id='P_3B')]),
        html.Tr([html.Td(['PM 4, Channal A']),html.Td(id='S_4A'),html.Td(id='P_4A')]),
        html.Tr([html.Td(['PM 4, Channal B']),html.Td(id='S_4B'),html.Td(id='P_4B')]),
        ],style={'max-width': '800px','border-spacing':'30px 10px'}),
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
