import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
from datetime import datetime
import socket

import ReceiverADAM as RAD #module for this project

dash.register_page(__name__)



#The SAPar:[Center Frequency(Hz),SPAN(Hz),Reference Lavel (dBm),Scale(dB/div),RBW(Hz),VBW(Hz)]
channelOpt =[
 {'label':'EHT1_POL0 IF 4-9 GHz',    'value':1,  'gr':'1A',   'SAPar':[8E9,1E10,-40,5,3E6,300]},
 {'label':'EHT1_POL0 BB 6-8 GHz',    'value':2,  'gr':'1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL0 BB 4-6 GHz',    'value':3,  'gr':'1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL1 BB 4-6 GHz',    'value':4,  'gr':'1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL1 IF 4-9 GHz',    'value':5,  'gr':'1B',   'SAPar':[8E9,1E10,-40,5, 3E6,300]},
 {'label':'EHT1_POL1 BB 6-8 GHz',    'value':6,  'gr':'1B',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'10Mhz-Left rack',         'value':7,  'gr':'1B',   'SAPar':[1E7,200,10,10, 1,1]},
 {'label':'100MHz',                  'value':8,  'gr':'1B',   'SAPar':[1E8,200,10,10, 1,1]},
 {'label':'ContDet Input LHC 4-8GHz','value':9,  'gr':'2A',   'SAPar':[6E9,8E9,-60,2, 3E6,300]},
 {'label':'ContDet Input RHC 4-8GHz','value':10, 'gr':'2A',   'SAPar':[6E9,8E9,-60,2, 3E6,300]},
 {'label':'VVM Input (Rx) 50 MHz',   'value':11, 'gr':'2A',   'SAPar':[5E7,200,-40,10, 1,1]},
 {'label':'VVM Input (Ref) 50 MHz',  'value':12, 'gr':'2A',   'SAPar':[5E7,200,0,10, 1,1]},
 {'label':'5.95 GHz',                'value':13, 'gr':'2B',   'SAPar':[5.9E9,200,0,10, 1,1]},
 {'label':'0.5 or 1.5 GHz',          'value':14, 'gr':'2B',   'SAPar':[1E9,1.6E9,0,10, 3E6,300]},
 {'label':'31.5 MHz',                'value':15, 'gr':'2B',   'SAPar':[3.15E7,200,-50,10, 1, 1]},
 {'label':'44.5 or 18.5MHz',         'value':16, 'gr':'2B',   'SAPar':[31.5E6,50E6,-40,10, 1,1]},
 {'label':'NotAssigned',             'value':17, 'gr':'SA',   'SAPar':[4.0E9,1.0E9,0,10, 10E4,1E5]},
 {'label':'NotAssigned',             'value':18, 'gr':'SA',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'EHT1_LO_6GHz',            'value':19, 'gr':'SA',   'SAPar':[6E9,200,10,10, 1,1]},
 {'label':'EHT1_LO_7GHz',            'value':20, 'gr':'SA',   'SAPar':[7E9,200,10,10, 1,1]},
 {'label':'NotAssigned',             'value':21, 'gr':'SA',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Ref1+Ref3 (Test)',        'value':22, 'gr':'SA',   'SAPar':[27E9,20E9,20,10, 3E6,300]},
 {'label':'EHT2_POL0 IF 4-9',        'value':23, 'gr':'3A',   'SAPar':[8E9,1E10,-40,5,3E6,300]},
 {'label':'EHT2_POL0 BB 6-8 GHz',    'value':24, 'gr':'3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL0 BB 4-6 GHz',    'value':25, 'gr':'3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL1 BB 4-6 GHz',    'value':26, 'gr':'3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL1 IF 4-9 GHz',    'value':27, 'gr':'3B',   'SAPar':[8E9,1E10,-40,5, 3E6,300]},
 {'label':'EHT2_POL1 BB 6-8 GHz',    'value':28, 'gr':'3B',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'3.85 GHz',                'value':29, 'gr':'3B',   'SAPar':[3.85E9,200,10,10, 1,1]},
 {'label':'8.15 GHz',                'value':30, 'gr':'3B',   'SAPar':[8.15E9,200,10,10, 1,1]},
 {'label':'2.048 GHz',               'value':31, 'gr':'4A',   'SAPar':[2.048E9,200,10,10, 1,1]},
 {'label':'NotAsssigned',            'value':32, 'gr':'4A',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'EHT2 LO (6GHz)',          'value':33, 'gr':'4A',   'SAPar':[6E9,200,10,10, 1,1]},
 {'label':'EHT2 LO (7GHz)',          'value':34, 'gr':'4A',   'SAPar':[7E9,200,10,10, 1,1]},
 {'label':'NotAssigned',             'value':35, 'gr':'4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':36, 'gr':'4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':37, 'gr':'4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':38, 'gr':'4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':39, 'gr':'SA',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':40, 'gr':'SA',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':41, 'gr':'SA',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':42, 'gr':'SA',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Spectrum path (RF Swwitch #1)',   'value':43, 'gr':'SA',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Ref1(18-32GHz)',                  'value':44, 'gr':'SA',   'SAPar':[25E9,20E9,-15,5, 3E6,300]},
  ]

#d_k = 'SAPar'
#d_v = 'NotAssigned'
#for remove the dic whit key,value=label,NotAssigned, also remove the key=SAPar for dropdown 
#channel_O2 = [{k : v for k, v in s.items() if k in ['label','value']} for s in channelOpt if s['label'] != 'NotAssigned']
def gotopt(channelO,gr):
    return [{k : v for k, v in s.items() if k in ['label','value']} for s in channelOpt if s['gr'] is gr]
print(gotopt(channelOpt,'1A'))


layout = html.Div([
    html.H3('PowerMeter Selection Select'),
    #dcc.Dropdown(id='SA_sel', options=channel_O2,style={'max-width': '500px'}, placeholder='SA-chaannel-Select'),
    html.Br(),
    html.Table([
        html.Tr([html.Th(['Power Meter  & Channel ']),html.Th(['which IF you want!'])]),
        html.Tr([html.Td([]),html.Td([],style={'width':'350px'})],style={'visibility':'hidden'}),
        html.Tr([html.Td(['PM 1, Channal A']),html.Td([dcc.Dropdown(id='1A',options=gotopt(channelOpt,'1A'))]),]),
        html.Tr([html.Td(['PM 1, Channal B']),dcc.Dropdown(id='1B',options=gotopt(channelOpt,'1B')) ]),
        html.Tr([html.Td(['PM 2, Channal A']),dcc.Dropdown(id='2A',options=gotopt(channelOpt,'2A')) ]),
        html.Tr([html.Td(['PM 2, Channal B']),dcc.Dropdown(id='2B',options=gotopt(channelOpt,'2B')) ]),
        html.Tr([html.Td(['PM 3, Channal A']),dcc.Dropdown(id='3A',options=gotopt(channelOpt,'3A')) ]),
        html.Tr([html.Td(['PM 3, Channan B']),dcc.Dropdown(id='3B',options=gotopt(channelOpt,'3B')) ]),
        html.Tr([html.Td(['PM 4, Channal A']),dcc.Dropdown(id='4A',options=gotopt(channelOpt,'4A')) ]),
        html.Tr([html.Td(['PM 4, Channal B']),dcc.Dropdown(id='4B',options=gotopt(channelOpt,'4B')) ]),
        ],style={'max-width': '800px','border-spacing':'30px 10px'}),
    html.H6(''),
    html.Br(),
    html.Button('Here to set.',id='PM_set'),
    html.Div(id='PM_res'),
    html.Table([
        html.Tr([html.Th(['Power Meter  & Channel ']),html.Th(['which IF you want!']),html.Th('Get Power Button')]),
        html.Tr([html.Td([],style={'width':'250px'}),html.Td([],style={'width':'350px'}),html.Td([],style={'width':'250px'})],
            style={'visibility':'hidden'}),
        html.Tr([html.Td(['Test, Channal A']),html.Td([dcc.Dropdown(id='TA',options=gotopt(channelOpt,'1A'))]),]),
        html.Tr([html.Td(['Test, Channal B']),html.Td([dcc.Dropdown(id='TB',options=gotopt(channelOpt,'1B'))]),
                 html.Td([html.Button('Got Power from PM1-Ch B',id='TB2')]),])
        ],style={'max-width': '800px','border-spacing':'30px 10px'}),
    html.Br(),
])
