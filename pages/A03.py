import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
import ReceiverADAM as RAD #at main dir not
from datetime import datetime

dash.register_page(__name__)


# Layout blocks


layout = html.Div([
    html.H3('A03 Status and Setting'),
    html.Button('A3 fake check',id='a03-bo-check'),
    html.Br(),
    html.Div(id='a03-bo-result'),
    html.H4('The DI status '),
    html.Table([
        html.Tr([html.Th(['Define on A3']),html.Th(['Return value'])]),
        html.Tr([html.Td(['DI  0']), html.Td(id='a03_DI00')]),
        html.Tr([html.Td(['DI  1']), html.Td(id='a03_DI01')]),
        html.Tr([html.Td(['DI  2']), html.Td(id='a03_DI02')]),
        html.Tr([html.Td(['DI  3']), html.Td(id='a03_DI03')]),
        html.Tr([html.Td(['DI  4']), html.Td(id='a03_DI04')]),
        html.Tr([html.Td(['DI  5']), html.Td(id='a03_DI05')]),
        html.Tr([html.Td(['DI  6']), html.Td(id='a03_DI06')]),
        html.Tr([html.Td(['DI  7']), html.Td(id='a03_DI07')]),
        html.Tr([html.Td(['DI  8']), html.Td(id='a03_DI08')]),
        html.Tr([html.Td(['DI  9']), html.Td(id='a03_DI09')]),
        html.Tr([html.Td(['DI 10']), html.Td(id='a03_DI10')]),
        html.Tr([html.Td(['DI 11']), html.Td(id='a03_DI11')]),
    ]),
    html.H4('The DO status'),
    html.Table([
        html.Tr([html.Th(['Define on A3']),html.Th(['Return value'])]),
        html.Tr([html.Td(['DO  0']), html.Td(id='a03_Do00')]),
        html.Tr([html.Td(['DO  1']), html.Td(id='a03_Do01')]),
        html.Tr([html.Td(['DO  2']), html.Td(id='a03_Do02')]),
        html.Tr([html.Td(['DO  3']), html.Td(id='a03_Do03')]),
        html.Tr([html.Td(['DO  4']), html.Td(id='a03_Do04')]),
        html.Tr([html.Td(['DO  5']), html.Td(id='a03_Do05')])
    ]),
    #html.H4('Digital Output Setting(5056)'),
    #html.Table([
    #    html.Tr([html.Th(['Define(DO)']),html.Th(['Value(Dex for 16 digital)']),
    #             html.Th(['Function']),html.Th(['Final Result'])]),
    #    html.Tr([html.Td(['Value to 5056(16 DO)']),
    #             html.Td(dcc.Input(id='a01_inDO',type='text',debounce=True,placeholder='F02A')),
    #             html.Td(html.Button('Set to 5056',id='a01_B_DO')),html.Td(id='a01-5056-r2') ])
    #]),
    html.Br()
])


@callback(Output('a03-bo-result','children'),Input('a03-bo-check','n_clicks'))
def update_output_time(n_clicks):
    if n_clicks is None:
        return "Last update: Not once after this page reloac"
        raise PreventUpdate
    else:
        format_data = "%Y/%m/%d, %H:%M:%S,"
        return "Last update:"+datetime.now().strftime(format_data)

@callback(
    Output('a03_DI00','children'),Output('a03_DI01','children'),
    Output('a03_DI02','children'),Output('a03_DI03','children'),
    Output('a03_DI04','children'),Output('a03_DI05','children'),
    Output('a03_DI06','children'),Output('a03_DI07','children'),
    Output('a03_DI08','children'),Output('a03_DI09','children'),
    Output('a03_DI10','children'),Output('a03_DI11','children'),
    Output('a03_Do00','children'),Output('a03_Do01','children'),
    Output('a03_Do02','children'),Output('a03_Do03','children'),
    Output('a03_Do04','children'),Output('a03_Do05','children'),
    Input('a03-bo-check','n_clicks'))
def update_output_5017(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('Checking A03 (DI and DO)')
        #print(get_5017('A01'))
        try:
            return RAD.get_6050('A01')
        except:
            return ['Error ##']*8
'''
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
        time.sleep(1)
        try:
            return RAD.get_5018('A01')
        except:
            return ['Error ##']*7
'''
