import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

from pymodbus.client import ModbusTcpClient as ModbusClient
import time
import ReceiverADAM as RAD #at main dir not

dash.register_page(__name__)


layout = html.Div([
    html.H3('A11 Status and Setting'),
    html.Button('A11 value check',id='a11-bo-check'),
    html.Br(),
    html.Table([
        html.Tr([html.Th(['Define on A11']),html.Th(['Return value'])]),
        html.Tr([html.Td(['LHC power detector']), html.Td(id='a11_V1')]),
        html.Tr([html.Td(['RHC power detector']), html.Td(id='a11_V2')]),
        html.Tr([html.Td(['5.95GHz LO(typical locked about 5V)']), html.Td(id='a11_V3')]),
        html.Tr([html.Td(['15VDC source(typical 6V)']), html.Td(id='a11_V4')]),
        html.Tr([html.Td(['12VDC source(typical 4.8V)']), html.Td(id='a11_V5')]),
        html.Tr([html.Td(['VGA1 (LHC in)']), html.Td(id='a11_V6')]),
        html.Tr([html.Td(['VGA2 (RHC in)']),html.Td(id='a11_V7')]),
        html.Tr([html.Td(['VGA3(CAB-A1 in)']),html.Td(id='a11_V8')]),
    ]),
    html.H4('The Temperature state on A11'),
    html.Table([
        html.Tr([html.Th([' zone in A11']),html.Th(['Temperature'])]),
        html.Tr([html.Td(['VGA1']), html.Td(id='a11_T1')]),
        html.Tr([html.Td(['VGA2']), html.Td(id='a11_T2')]),
        html.Tr([html.Td(['VGA3']), html.Td(id='a11_T3')]),
        html.Tr([html.Td(['PA1(on Rx path)']), html.Td(id='a11_T4')]),
        html.Tr([html.Td(['PA2(on reference path)']), html.Td(id='a11_T5')]),
        html.Tr([html.Td(['NC']), html.Td(id='a11_T6')]),
        html.Tr([html.Td(['NC']),html.Td(id='a11_T7')]),
    ]),
    html.H4('Anglogy Output state (5024, in Voltage)'),
    html.Table([
        html.Tr([html.Th(['Define(AO)']),html.Th(['Value(Voltage)'])]),
        html.Tr([html.Td(['VGA1']), html.Td(id='a11_O1')]),
        html.Tr([html.Td(['VGA2']), html.Td(id='a11_O2')]),
        html.Tr([html.Td(['VGA3']), html.Td(id='a11_O3')]),
        html.Tr([html.Td(['NC4']), html.Td(id='a11_O4')]),
     ]),
    #html.H4('Analogy Output Setting (5024,Voltage)'),
    #html.Table([
    #    html.Tr([html.Th(['Define(AO)']),html.Th(['Value(Voltage)']),
    #             html.Th(['Function']),html.Th(['Final Result'])]),
    #    html.Tr([html.Td(['VGA1']),
    #             html.Td(dcc.Input(id='a11_in01',type='number',min=0,max=10,debounce=True,
    #                     placeholder='VGA1 0-10V')),
    #             html.Td(html.Button('Set VGA1',id='a11_B01')),html.Td(id='a11_Q1')]),
    #    html.Tr([html.Td(['VGA2']),
    #             html.Td(dcc.Input(id='a11_in02',type='number',min=0,max=10,debounce=True,
    #                     placeholder='VGA2 0-10V')),
    #             html.Td(html.Button('Set VGA2',id='a11_B02')),html.Td(id='a11_Q2')]),
    #    html.Tr([html.Td(['VGA3']),
    #             html.Td(dcc.Input(id='a11_in03',type='number',min=0,max=10,debounce=True,
    #                     placeholder='VGA3 0-10V')),
    #             html.Td(html.Button('Set VGA3',id='a11_B03')),html.Td(id='a11_Q3')]),
    #    html.Tr([html.Td(['NC4']),
    #             html.Td(dcc.Input(id='a11_in04',type='number',min=0,max=10,debounce=True,
    #                     placeholder='NC4 0-10V')),
    #             html.Td(html.Button('Set NC4',id='a11_B04')),html.Td(id='a11_Q4')]),
    #    ]),
    html.H4('5056 Digital Output Information'),
    html.Div(id='a11-5056-result'),
    #html.H4('Digital Output Setting(5056)'),
    #html.Table([
    #    html.Tr([html.Th(['Define(DO)']),html.Th(['Value(Dex for 16 digital)']),
    #             html.Th(['Function']),html.Th(['Final Result'])]),
    #    html.Tr([html.Td(['Value to 5056(16 DO)']),
    #             html.Td(dcc.Input(id='a11_inDO',type='text',debounce=True,placeholder='F02A')),
    #             html.Td(html.Button('Set to 5056',id='a11_B_DO')),html.Td(id='a11-5056-r2') ])
    #]),
    html.Br()
])


'''
@callback(Output('a11-5056-r2','children'),
              Input('a11_B_DO','n_clicks'),Input('a11_inDO','value'))
def set_5056_01(n_clicks,data):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('data for set A11 5056',data)
        try:
            RAD.set_5056('A11',data)
            return RAD.get_5056('A11')
        except:
            return ['Error ##']
'''

@callback(Output('a11-5056-result','children'),Input('a11-bo-check','n_clicks'))
def update_output0(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            return RAD.get_5056('A11')
        except:
            return "Error ##02"

'''
@callback(Output('a11_Q1','children'),
              Input('a11_B01','n_clicks'),Input('a11_in01','value'))
def set_5024_01(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A11',0,volt)
            return RAD.get_5024('A11')[0]
        except:
            return ['Error ##']

@callback(Output('a11_Q2','children'),
              Input('a11_B02','n_clicks'),Input('a11_in02','value'))
def set_5024_02(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A11',1,volt)
            return RAD.get_5024('A11')[1]
        except:
            return ['Error ##']

@callback(Output('a11_Q3','children'),
              Input('a11_B03','n_clicks'),Input('a11_in03','value'))
def set_5024_03(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A11',2,volt)
            return RAD.get_5024('A11')[2]
        except:
            return ['Error ##']

@callback(Output('a11_Q4','children'),
              Input('a11_B04','n_clicks'),Input('a11_in04','value'))
def set_5024_04(n_clicks,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            RAD.set_5024('A11',3,volt)
            return RAD.get_5024('A11')[3]
        except:
            return ['Error ##']
'''

@callback(
    Output('a11_V1','children'),Output('a11_V2','children'),
    Output('a11_V3','children'),Output('a11_V4','children'),
    Output('a11_V5','children'),Output('a11_V6','children'),
    Output('a11_V7','children'),Output('a11_V8','children'),
    Input('a11-bo-check','n_clicks'))
def update_output1(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('Checking A11 (5017-> 5018->5024->5056)')
        #print(get_5017('A11'))
        try:
            return RAD.get_5017('A11')
        except:
            return ['Error ##']*8

@callback(
    Output('a11_T1','children'),Output('a11_T2','children'),
    Output('a11_T3','children'),Output('a11_T4','children'),
    Output('a11_T5','children'),Output('a11_T6','children'),
    Output('a11_T7','children'),
    Input('a11-bo-check','n_clicks'))
def update_output2(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(1)
        try:
            return RAD.get_5018('A11')
        except:
            return ['Error ##']*7

@callback(
    Output('a11_O1','children'),Output('a11_O2','children'),
    Output('a11_O3','children'),Output('a11_O4','children'),
    Input('a11-bo-check','n_clicks'))
def update_output3(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(2)
        try:
            return RAD.get_5024('A11')
        except:
            return ['Error ##']*4

