import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

from pymodbus.client import ModbusTcpClient as ModbusClient
import time
import ReceiverADAM as RAD
from datetime import datetime

dash.register_page(__name__)


# Layout blocks

Power_options = {
    'Rx1': ['80', '90', '100'],
    'Rx2': ['220', '230', '235'],
    'Rx3': ['320','330','340','350'],
}


layout = html.Div([
    html.H3('The attentuator to adjust Photionic LO power'),
    html.Button('A3 check',id='a03b-bo-check'),
    html.Br(),
    html.Div(id='a03b-bo-result'),
    html.H4('The DO status'),
    html.Table([
        html.Tr([html.Th(['Define on A3']),html.Th(['Return value'])]),
        html.Tr([html.Td(['DO  0']), html.Td(id='a03b_Do00')]),
        html.Tr([html.Td(['DO  1']), html.Td(id='a03b_Do01')]),
        html.Tr([html.Td(['DO  2']), html.Td(id='a03b_Do02')]),
        html.Tr([html.Td(['DO  3']), html.Td(id='a03b_Do03')]),
        html.Tr([html.Td(['DO  4']), html.Td(id='a03b_Do04')]),
        html.Tr([html.Td(['DO  5']), html.Td(id='a03b_Do05')]),
    ]),
    html.H4('Input the levels of attenuation (0-63)'),
    #html.Br(),
    #html.H6('0 dB is Minimum attenuation'),
    dcc.Input(id='att_Val',type='number',min=0,max=63,step=1,
              debounce=True,placeholder='between 0~63 '),
    html.Button('Submit',id='att_Set'),
    html.H6('0 is Minimum attenuation, (High LO power)'),
    html.Div(id='att_result'),
    #dcc.Dropdown(list(Power_options.keys()),'Rx1',id='rx-radio',style={'width':'50%','max-width':'400px'}),
    #dcc.Dropdown(id='level-radio',style={'max-width':'400px','width':'50%'}),
    html.Hr(),
    #html.Div(id='display-selected-values')
])

the_app = dash.get_app()        # Must specify due to @dash.callback limitations
@the_app.callback(Output('a03b-bo-result','children'),Input('a03b-bo-check','n_clicks'))
def update_output_time(n_clicks):
    if n_clicks is None:
        return "Last update: Not once after this page reloac"
        raise PreventUpdate
    else:
        format_data = "%Y/%m/%d, %H:%M:%S,"
        return "Last update:"+datetime.now().strftime(format_data)

@the_app.callback(
    Output('a03b_Do00','children'),Output('a03b_Do01','children'),
    Output('a03b_Do02','children'),Output('a03b_Do03','children'),
    Output('a03b_Do04','children'),Output('a03b_Do05','children'),
    Input('a03b-bo-check','n_clicks'))
def update_DO_6050(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('Checking A03 (DI and DO)')
        #print(get_5017('A01'))
        try:
            return RAD.get_6050('A03')[12:18]
        except:
            return ['Error ##']*6

@the_app.callback(Output('att_result','children'),
          Input('att_Set','n_clicks'),
          State('att_Val','value'),
          )
def update_att_A03(n_clicks,att):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            data=[int(x) for x in '{0:06b}'.format(63-att)]
            print(data)
            return data
        except:
            return "Fail"

'''
@the_app.callback(
    Output('level-radio', 'options'),
    Input('rx-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in Power_options[selected_country]]


@the_app.callback(
    Output('level-radio', 'value'),
    Input('level-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@the_app.callback(
    Output('display-selected-values', 'children'),
    Input('rx-radio', 'value'),
    Input('level-radio', 'value'))
def set_display_children(rx, level):
    return u' for LO Frequency{} GHz in {}'.format(level, rx,)
'''
