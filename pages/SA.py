import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
from datetime import datetime
import socket

import ReceiverADAM as RAD #module for this project

dash.register_page(__name__)


#for SA
'''
   strcpy(anycf,argv[1]);
   strcpy(anysp,argv[2]);
   strcpy(anylg,argv[3]);
   strcpy(anyrl,argv[4]);
   strcpy(anyrb,argv[5]);
   strcpy(anyvb,argv[6]);
      sprintf(message,"FREQ:CENT %s Hz\n",anycf);
      sprintf(message,"FREQ:SPAN %s Hz\n",anysp);
      sprintf(message,"BAND %s Hz\n",anyrb);
      sprintf(message,"BAND:VID %s Hz\n",anyvb);
      sprintf(message,"DISP:WIND:TRAC:Y:RLEV %s dBm\n",anyrl);
      sprintf(message,"DISP:SEM:VIEW:WIND:TRAC:Y:PDIV %s dB\n",anylg);
'''

#The SAPar:[Center Frequency(Hz),SPAN(Hz),Reference Lavel (dBm),Scale(dB/div),RBW(Hz),VBW(Hz)]
channelOpt =[
    {'label':'EHT1_POL0 IF 4-9 GHz',    'value':1,  'SAPar':[8E9,1E10,-40,5,3E6,300]},
    {'label':'EHT1_POL0 BB 6-8 GHz',    'value':2,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT1_POL0 BB 4-6 GHz',    'value':3,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT1_POL1 BB 4-6 GHz',    'value':4,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT1_POL1 IF 4-9 GHz',    'value':5,  'SAPar':[8E9,1E10,-40,5, 3E6,300]},
    {'label':'EHT1_POL1 BB 6-8 GHz',    'value':6,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'10Mhz-Left rack',         'value':7,  'SAPar':[1E7,200,10,10, 1,1]},
    {'label':'100MHz',                  'value':8,  'SAPar':[1E8,200,10,10, 1,1]},
    {'label':'ContDet Input LHC 4-8GHz',        'value':9,  'SAPar':[6E9,8E9,-60,2, 3E6,300]},
    {'label':'ContDet Input RHC 4-8GHz',        'value':10, 'SAPar':[6E9,8E9,-60,2, 3E6,300]},
    {'label':'VVM Input (Rx) 50 MHz',           'value':11, 'SAPar':[5E7,200,-40,10, 1,1]},
    {'label':'VVM Input (Ref) 50 MHz',          'value':12, 'SAPar':[5E7,200,0,10, 1,1]},
    {'label':'5.95 GHz',                        'value':13, 'SAPar':[5.9E9,200,0,10, 1,1]},
    {'label':'0.5 or 1.5 GHz',                  'value':14, 'SAPar':[1E9,1.6E9,0,10, 3E6,300]},
    {'label':'31.5 MHz',                        'value':15, 'SAPar':[3.15E7,200,-50,10, 1, 1]},
    {'label':'Ref1 (SG) couple out',            'value':16, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':17, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':18, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':19, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':20, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':21, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Ref1+Ref3 (18.5-33.5G)',          'value':22, 'SAPar':[1500,29000,-30,5, 30000,300]},
    {'label':'EHT2_POL0 IF 4-9',                'value':23, 'SAPar':[8E9,1E10,-40,5,3E6,300]},
    {'label':'EHT2_POL0 BB 6-8 GHz',            'value':24, 'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT2_POL0 BB 4-6 GHz',            'value':25, 'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT2_POL1 BB 4-6 GHz',            'value':26, 'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT2_POL1 IF 4-9 GHz',            'value':27, 'SAPar':[8E9,1E10,-40,5, 3E6,300]},
    {'label':'EHT2_POL1 BB 6-8 GHz',            'value':28, 'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'3.85 GHz',                        'value':29, 'SAPar':[3.85E9,200,10,5, 1,1]},
    {'label':'8.15 GHz',                        'value':30, 'SAPar':[8.15E9,200,10,5, 1,1]},
    {'label':'2.048 GHz',                       'value':31, 'SAPar':[2.048E9,200,10,5, 1,1]},
    {'label':'10 MHz at Right Rack',            'value':32, 'SAPar':[1E7,200,10,5, 1,1]},
    {'label':'EHT LO (7GHz)',                   'value':33, 'SAPar':[7E9,200,10,10, 1,1]},
    {'label':'EHT LO (6GHz)',                   'value':34, 'SAPar':[6E9,200,10,10, 1,1]},
    {'label':'NotAssigned',                     'value':35, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':36, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':37, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Ref1 (SG) couple out',            'value':38, 'SAPar':[1.1E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':39, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':40, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':41, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':42, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Spectrum path (RF Swwitch #1)',   'value':43, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Ref1(18-32GHz)',                  'value':44, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    ]

d_k = 'SAPar'
d_v = 'NotAssigned'
#for remove the dic whit key,value=label,NotAssigned, also remove the key=SAPar for dropdown 
#channel_O2 = [{k : v for k, v in s.items() if k != d_k} for s in channelOpt]
channel_O2 = [{k : v for k, v in s.items() if k != d_k} for s in channelOpt if not(s['label'] == 'NotAssigned')]

#print(channel_O2)

layout = html.Div([
    html.H3('SA setting Select'),
    dcc.Dropdown(id='SA_sel', options=channel_O2,style={'max-width': '460px'}, placeholder='SA-chaannel-Select'),
    html.H6(''),
    html.Button('Submit',id='SA_set'),
    html.Div(id='SA_setting_res'),
    html.Br()
])


@callback(Output('SA_setting_res','children'),
          Input('SA_set','n_clicks'),
          State('SA_sel','value'),
          )
def SA_set(n_clicks,channel):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print(channel,channelOpt[channel-1]['label'],channelOpt[channel-1]['SAPar'])
        Sp=channelOpt[channel-1]['SAPar']
        re=RAD.set_SA('SA1',Sp[0],Sp[1],Sp[2],Sp[3],Sp[4],Sp[5])
        time.sleep(1)
        return channelOpt[channel-1]['label']+str(Sp)+re

