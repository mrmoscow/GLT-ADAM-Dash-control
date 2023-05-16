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
    html.H3('A01 Status and Setting'),
    html.Button('A1 value check',id='a01-bo-check'),
    html.Br(),
    html.Div(children='Last update: Not once after this page reloac',id='a01-bo-result'),
    html.Br(),
    html.Table([
        html.Tr([html.Th(['Define on A1']),html.Th(['Return value'])]),
        html.Tr([html.Td(['LO1 Lock status']), html.Td(id='a01_V1')]),
        html.Tr([html.Td(['LO2 Lock status']), html.Td(id='a01_V2')]),
        html.Tr([html.Td(['24VDC source (typical 9.6V)']), html.Td(id='a01_V3')]),
        html.Tr([html.Td(['12VDC source(typical 4.8V)']), html.Td(id='a01_V4')]),
        html.Tr([html.Td(['5VDC source(typical 2V)']), html.Td(id='a01_V5')]),
        html.Tr([html.Td(['-5VDC source (typical -2V)']), html.Td(id='a01_V6')]),
        html.Tr([html.Td(['FAN1']),html.Td(id='a01_V7')]),
        html.Tr([html.Td(['FAN2']),html.Td(id='a01_V8')]),
    ]),
    html.H4('The Temperature state on A1'),
    html.Table([
        html.Tr([html.Th([' zone in A01']),html.Th(['Temperature'])]),
        html.Tr([html.Td(['SW1(MRG)']), html.Td(id='a01_T1')]),
        html.Tr([html.Td(['SW2(FLOOG)']), html.Td(id='a01_T2')]),
        html.Tr([html.Td(['SW3(FLOOG)']), html.Td(id='a01_T3')]),
        html.Tr([html.Td(['SW4(MRG-valon)']), html.Td(id='a01_T4')]),
        html.Tr([html.Td(['PA(MRG)']), html.Td(id='a01_T5')]),
        html.Tr([html.Td(['VGA/PA2 (upconvert)']), html.Td(id='a01_T6')]),
        html.Tr([html.Td(['LO1(31.5MHz)']),html.Td(id='a01_T7')]),
    ]),
    html.H4('Anglogy Output state (5024, in Voltage)'),
    html.Table([
        html.Tr([html.Th(['Define(AO)']),html.Th(['Value(Voltage)'])]),
        html.Tr([html.Td(['to VGA']), html.Td(id='a01_O1')]),
        html.Tr([html.Td(['NC2']), html.Td(id='a01_O2')]),
        html.Tr([html.Td(['NC3']), html.Td(id='a01_O3')]),
        html.Tr([html.Td(['NC4']), html.Td(id='a01_O4')]),
     ]),
    html.H4('Analogy Output Setting (5024,Voltage)'),
    html.Table([
        html.Tr([html.Th(['Define(AO)']),html.Th(['Value(Voltage)']),
                 html.Th(['Function']),html.Th(['Final Result'])]),
        html.Tr([html.Td('to VGA'),
                 html.Td(dcc.Input(id='a01_in01',type='number',min=0,max=10,debounce=True,
                         placeholder='VGA 0-10V')),
                 html.Td(html.Button('Set  VGA',id='a01_B01')),html.Td(id='a01_Q1')]),
        html.Tr([html.Td('NC2'),
                 html.Td(dcc.Input(id='a01_in02',type='number',min=0,max=10,debounce=True,
                         placeholder='NC2 0-10V')),
                 html.Td(html.Button('Set NC2',id='a01_B02')),html.Td(id='a01_Q2')]),
        html.Tr([html.Td('NC3'),
                 html.Td(dcc.Input(id='a01_in03',type='number',min=0,max=10,debounce=True,
                         placeholder='NC3 0-10V')),
                 html.Td(html.Button('Set NC3',id='a01_B03')),html.Td(id='a01_Q3')]),
        html.Tr([html.Td('NC4'),
                 html.Td(dcc.Input(id='a01_in04',type='number',min=0,max=10,debounce=True,
                         placeholder='NC4 0-10V')),
                 html.Td(html.Button('Set NC4',id='a01_B04')),html.Td(id='a01_Q4')])
        ],className='adj'),
    html.H4('5056 Digital Output Information'),
    html.Table([
        html.Tr([html.Td(children='Not value yet',id='a01-5056-result')])
    ]),
    #html.Div(id='a01-5056-result'),
    html.H4('Digital Output Setting(5056)'),
    html.Table([
        html.Tr([html.Th('Define(DO)'),html.Th('Value(4 digit hex humber for 16 on/off switch)'),
                 html.Th('Function'),html.Th('Final Result') ]),
        html.Tr([html.Td('Value to 5056(16 DO)'),
                 html.Td(dcc.Input(id='a01_inDO',type='text',debounce=True,placeholder='F02A')),
                 html.Td(html.Button('Set to 5056',id='a01_B_DO')),html.Td(id='a01-5056-r2') ])
        ],className='adj'),
    #html.H4('TTL channal selection'),
    #dcc.Dropdown(id='ch-to-set', options=rx_opts,
    #             style={'max-width': '200px'}, placeholder='Select the Channel'),
    #html.Button('Setting the TTL channal',id='a01_Rx_Set'),
    html.Div(id='a01-5056-r3'),
    html.Br()
])

'''
@callback(Output('a01-5056-r3','children'),
              Input('a01_Rx_Set','n_clicks'),Input('ch-to-set','value'))
def set_5056_ch(n_clicks,data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        data=ch_hex[data]
        print('data for set A01 5056 Channel',data)
        try:
            RAD.set_5056('A01',data)
            return RAD.get_5056('A01')
        except:
            return ['Error ##']
'''

@callback(Output('a01-5056-r2','children'),
              Input('a01_B_DO','n_clicks'),Input('a01_inDO','value'))
def set_5056_01(n_clicks,data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('data for set A01 5056',data)
        try:
            RAD.set_5056('A01',data)
            return RAD.get_5056('A01')
        except:
            return ['Error ##']


@callback(Output('a01-5056-result','children'),Input('a01-bo-check','n_clicks'),
          Input('a01-5056-r2','children'),Input('a01-5056-r3','children'),
          prevent_initial_call=True)
def update_5056_S3(n_clicks,n,m):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(1)
        try:
            return RAD.get_5056('A01')
        except:
            return "Error ##02"


@callback(Output('a01_Q1','children'),
              Input('a01_B01','n_clicks'),Input('a01_in01','value'))
def set_5024_01(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A01',0,volt)
            return RAD.get_5024('A01')[0]
        except:
            return ['Error ##']

@callback(Output('a01_Q2','children'),
              Input('a01_B02','n_clicks'),Input('a01_in02','value'))
def set_5024_02(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A01',1,volt)
            return RAD.get_5024('A01')[1]
        except:
            return ['Error ##']

@callback(Output('a01_Q3','children'),
              Input('a01_B03','n_clicks'),Input('a01_in03','value'))
def set_5024_03(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A01',2,volt)
            return RAD.get_5024('A01')[2]
        except:
            return ['Error ##']

@callback(Output('a01_Q4','children'),
              Input('a01_B04','n_clicks'),Input('a01_in04','value'))
def set_5024_04(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A01',3,volt)
            return RAD.get_5024('A01')[3]
        except:
            return ['Error ##']

@callback(Output('a01-bo-result','children'),
          Input('a01-bo-check','n_clicks'),
          Input('a01_Q1','children'),Input('a01_Q2','children'),
          Input('a01_Q3','children'),Input('a01_Q4','children'),
          Input('a01-5056-r2','children'),Input('a01-5056-r3','children'),
          prevent_initial_call=True)
def update_output_time(n_clicks,n,m,o,p,q,r):
    if n_clicks is None:
        return "Last update: Not once after this page reloac"
        raise PreventUpdate
    else:
        format_data = "%Y/%m/%d, %H:%M:%S,"
        return "Last update:"+datetime.now().strftime(format_data)

@callback(
    Output('a01_V1','children'),Output('a01_V2','children'),
    Output('a01_V3','children'),Output('a01_V4','children'),
    Output('a01_V5','children'),Output('a01_V6','children'),
    Output('a01_V7','children'),Output('a01_V8','children'),
    Input('a01-bo-check','n_clicks'))
def update_output_5017(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('Checking A01 (5017-> 5018->5024->5056)')
        #print(get_5017('A01'))
        try:
            return RAD.get_5017('A01')
        except:
            return ['Error ##']*8

@callback(
    Output('a01_T1','children'),Output('a01_T2','children'),
    Output('a01_T3','children'),Output('a01_T4','children'),
    Output('a01_T5','children'),Output('a01_T6','children'),
    Output('a01_T7','children'),
    Input('a01-bo-check','n_clicks'))
def update_output_5018(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(2)
        try:
            return RAD.get_5018('A01')
        except:
            return ['Error ##']*7

@callback(
    Output('a01_O1','children'),Output('a01_O2','children'),
    Output('a01_O3','children'),Output('a01_O4','children'),
    Input('a01-bo-check','n_clicks'),
    Input('a01_Q1','children'),Input('a01_Q2','children'),
    Input('a01_Q3','children'),Input('a01_Q4','children'),
    prevent_initial_call=True)
def update_output_5024(n_clicks,n,m,o,p):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(1)
        try:
            return RAD.get_5024('A01')
        except:
            return ['Error ##']*4

