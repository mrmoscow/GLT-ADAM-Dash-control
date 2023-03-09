import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
import ReceiverADAM as RAD #at main dir not
from datetime import datetime

dash.register_page(__name__)


# Layout blocks
rx_opts = [
    {'label':'Ch 1', 'value':1}, {'label':'Ch 2', 'value':2},
    {'label':'Ch 3', 'value':3}, {'label':'Ch 4', 'value':4}]

ch_hex = {1:'FF00', 2:'AA00', 3: '5500', 4:'0000'}


layout = html.Div([
    html.H3('A17 Status and Setting'),
    html.Button('A17 value check',id='a17-bo-check'),
    html.Br(),
    html.Div(children='Last update: Not once after this page reloac',id='a17-bo-result'),
    html.Br(),
    html.Table([
        html.Tr([html.Th(['Define on A17']),html.Th(['Return value'])]),
        html.Tr([html.Td(['CH 0 (typical 0.083)']), html.Td(id='a17_V1')]),
        html.Tr([html.Td(['CH 1 (typical 0.087)']), html.Td(id='a17_V2')]),
        html.Tr([html.Td(['CH 2 (typical 6)']), html.Td(id='a17_V3')]),
        html.Tr([html.Td(['CH 3 (typical 6)']), html.Td(id='a17_V4')]),
        html.Tr([html.Td(['CH 4']), html.Td(id='a17_V5')]),
        html.Tr([html.Td(['CH 5']), html.Td(id='a17_V6')]),
        html.Tr([html.Td(['CH 6']), html.Td(id='a17_V7')]),
        html.Tr([html.Td(['CH 7']), html.Td(id='a17_V8')]),
    ]),
    html.H4('The Temperature state on A17'),
    html.Table([
        html.Tr([html.Th(['zone in A17']),html.Th(['Temperature'])]),
        html.Tr([html.Td(['Zone CH0']), html.Td(id='a17_T1')]),
        html.Tr([html.Td(['Zone CH1']), html.Td(id='a17_T2')]),
        html.Tr([html.Td(['Zone CH2']), html.Td(id='a17_T3')]),
        html.Tr([html.Td(['Zone CH3']), html.Td(id='a17_T4')]),
        html.Tr([html.Td(['Zone CH4']), html.Td(id='a17_T5')]),
        html.Tr([html.Td(['Zone CH5']), html.Td(id='a17_T6')]),
        html.Tr([html.Td(['Zone CH6']), html.Td(id='a17_T7')]),
    ]),
    html.H4('5056-S2 Digital Output Information'),
    html.Table([
        html.Tr([html.Td(children='Not value yet',id='a17_5056_S2_result')])
    ]),
    html.H4('Digital Output Setting(5056-S2)'),
    html.Table([
        html.Tr([html.Th(['Define(DO)']),html.Th(['Value(Dex for 16 digital)']),
                 html.Th(['Function']),html.Th(['Final Result'])]),
        html.Tr([html.Td(['Value to 5056-S2(16 DO)']),
                 html.Td(dcc.Input(id='a17_s2_inDO',type='text',debounce=True,placeholder='F02A')),
                 html.Td(html.Button('Set to 5056-S2',id='a17_s2_bo')),html.Td(id='a17_5056_s2_r2') ])
        ],className='adj'),
    ###Next if for S3    
    html.H4('5056-S3 Digital Output Information'),
    html.Table([
        html.Tr([html.Td(children='Not value yet',id='a17_5056_S3_result')])
    ]),
    html.H4('Digital Output Setting(5056-S3)'),
    html.Table([
        html.Tr([html.Th(['Define(DO)']),html.Th(['Value(Dex for 16 digital)']),
                 html.Th(['Function']),html.Th(['Final Result'])]),
        html.Tr([html.Td(['Value to 5056-S3(16 DO)']),
                 html.Td(dcc.Input(id='a17_s3_inDO',type='text',debounce=True,placeholder='F02A')),
                 html.Td(html.Button('Set to 5056-S3',id='a17_s3_bo')),html.Td(id='a17_5056_s3_r2') ])
        ],className='adj'),
    html.Br()
])


@callback(Output('a17_5056_s2_r2','children'),
              Input('a17_s2_bo','n_clicks'),Input('a17_s2_inDO','value'))
def set_5056_01(n_clicks,data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('data for set A17 5056 S3',data)
        try:
            RAD.set_5056('A17',data,'S2')
            return RAD.get_5056('A17')
        except:
            return ['Error ##']


@callback(Output('a17_5056_S2_result','children'),Input('a17-bo-check','n_clicks'))
          #Input('a17-5056-r2','children'),Input('a17-5056-r3','children'),
          #prevent_initial_call=True)
def update_5056_S3(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(1)
        try:
            return RAD.get_5056('A17','S2')
        except:
            return "Error ##02"

@callback(Output('a17_5056_s3_r2','children'),
              Input('a17_s3_bo','n_clicks'),Input('a17_s3_inDO','value'))
def set_5056_01(n_clicks,data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('data for set A17 5056 S3',data)
        try:
            RAD.set_5056('A17',data,'S3')
            return RAD.get_5056('A01')
        except:
            return ['Error ##']


@callback(Output('a17_5056_S3_result','children'),Input('a17-bo-check','n_clicks'))
          #Input('a17-5056-r2','children'),Input('a01-5056-r3','children'),
          #prevent_initial_call=True)
def update_5056_S3(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(1)
        try:
            return RAD.get_5056('A17')
        except:
            return "Error ##02"


@callback(Output('a17-bo-result','children'),
          Input('a17-bo-check','n_clicks'))
          #Input('a01-5056-r2','children'),Input('a01-5056-r3','children'),
          #prevent_initial_call=True)
def update_output_time(n_clicks):
    if n_clicks is None:
        return "Last update: Not once after this page reloac"
        raise PreventUpdate
    else:
        format_data = "%Y/%m/%d, %H:%M:%S,"
        return "Last update:"+datetime.now().strftime(format_data)

@callback(
    Output('a17_V1','children'),Output('a17_V2','children'),
    Output('a17_V3','children'),Output('a17_V4','children'),
    Output('a17_V5','children'),Output('a17_V6','children'),
    Output('a17_V7','children'),Output('a17_V8','children'),
    Input('a17-bo-check','n_clicks'))
def update_output_5017(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('Checking A17 (5017->5056(S3)->5018)')
        #print(get_5017('A01'))
        try:
            return RAD.get_5017('A17')
        except:
            return ['Error ##']*8

@callback(
    Output('a17_T1','children'),Output('a17_T2','children'),
    Output('a17_T3','children'),Output('a17_T4','children'),
    Output('a17_T5','children'),Output('a17_T6','children'),
    Output('a17_T7','children'),
    Input('a17-bo-check','n_clicks'))
def update_output_5018(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(2)
        try:
            return RAD.get_5018('A17')
        except:
            return ['Error ##']*7

