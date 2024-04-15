import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

import time
from datetime import datetime
import socket
import sys

#import ReceiverTest as RAD #module for this project
import ReceiverADAM as RAD #module for this project
import SpecAnalyzer as SA  #module for SA relative in this project

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

channelOpt=RAD.channelOpt

d_k = 'SAPar'
d_v = 'NotAssigned'
#for remove the dic whit key,value=label,NotAssigned, also remove the key=SAPar for dropdown 
channel_O2 = [{k : v for k, v in s.items() if k in ['label','value']} for s in channelOpt if s['label'] != 'NotAssigned']
#print(channel_O2)

layout = html.Div([
    html.H3('SA setting Select'),
    dcc.Dropdown(id='SA_sel', options=channel_O2,style={'max-width': '500px'}, placeholder='SA-chaannel-Select'),
    html.Br(),
    html.Table([
        html.Tr([html.Th(['The parameter on the SA    ']),html.Th(['     The value of parameters'])]),
        html.Tr([html.Td(['Center Frequency (Hz)']),  dcc.Input(id='S_V1')]),
        html.Tr([html.Td(['Span (Hz)']), dcc.Input(id="S_V2")]),
        html.Tr([html.Td(['Reference level dBm']),dcc.Input(id="S_V3")]),
        html.Tr([html.Td(['Scale dBm/DIV']), dcc.Input(id="S_V4")]),
        html.Tr([html.Td(['Resolution Bandwidth (Hz)']), dcc.Input(id="S_V5", type="number")]),
        html.Tr([html.Td(['Video Bandwidth (Hz)']), dcc.Input(id="S_V6", type="number")]),
        ],style={'max-width': '540px','border-spacing':'30px 10px'}),
    html.H6(''),
    html.Button('Submit the value to SA',id='SA_set'),
    html.Div(id='SA_setting_res'),
    html.Br(),
    html.Button('SA start to scan.',id='SA_reflash'),
    html.Div(id='SA_reflash_res'),
    html.Br(),
    html.Button('load SA plotting Image',id='SA_img_load'),
    html.Br(),
    html.Img(id='SA_img'),
    html.Br(),
])

#RAD.getSApng()

the_app = dash.get_app()        # Must specify due to @dash.callback limitations
@the_app.callback(Output('S_V1','value'),
          Output('S_V2','value'),
          Output('S_V3','value'),
          Output('S_V4','value'),
          Output('S_V5','value'),
          Output('S_V6','value'),
          Input('SA_sel','value'),
          )
def SA_para_get(channel):
    print("The value",channel,"type",type(channel))
    if channel is None:
        print("NonType")
        return [None,None,None,None,None,None]
    else:
        para=channelOpt[int(channel)-1]['SAPar']
        return para


@the_app.callback(Output('SA_setting_res','children'),
          Input('SA_set','n_clicks'),
          State('S_V1','value'),
          State('S_V2','value'),
          State('S_V3','value'),
          State('S_V4','value'),
          State('S_V5','value'),
          State('S_V6','value'),
          State('SA_sel','value'),
          )
def SA_set(n_clicks,cf,sp,rl,lg,rb,vb,channel):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if channel is None:
            #print("")
            return "will not change the IF switch, only the SA setting with the value"
        else:
            print(channel,channelOpt[int(channel)-1]['label'],cf,sp,rl,lg,rb,vb)
            result=channelOpt[int(channel)-1]['label']+str(cf)+str(sp)+str(rl)+str(lg)+str(rb)+str(vb)
            #Sp=channelOpt[channel-1]['SAPar'] no more needed
            re_01=RAD.CAB1417switch(channel,'SA')
            re=RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb)
            #time.sleep(2)
            return channelOpt[channel-1]['label']+re_01+"And SA parameter"+re

@the_app.callback(Output('SA_reflash_res','children'),Input('SA_reflash','n_clicks'))
def SA_reflash(n_clicks):
    if n_clicks is None:
        print('In scan none',n_clicks)
        return "Please press button for scans!"
    else:
        print('In scan button',n_clicks)
        #T.mytime_now()
        SA.save_plot()
        time.sleep(2)
        return "End of the scans, please reload the SA pltting image."


@the_app.callback(Output('SA_img','src'),Input('SA_img_load','n_clicks'))
def SA_got_img(n_clicks):
    if n_clicks is None:
        print('In got image None',n_clicks)
        return ""
    else:
        print('In got image else',n_clicks)
        return dash.get_asset_url('SA_plot.png')

