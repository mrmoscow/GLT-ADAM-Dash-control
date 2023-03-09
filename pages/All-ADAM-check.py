import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate
import ReceiverADAM as RAD

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time


dash.register_page(__name__)
#from app import app, all_pages
#app =dash.Dash(__name__, title='GLT Dashboard-Demo', update_title=None, serve_locally=False)



layout = html.Div([
    html.H3('ADAM Module Connection Checking'),
    html.Div(children='Link testing,Please watting',id='all-result'),
    dcc.Interval(id='interval',interval=40000,n_intervals=0),
    html.Hr(),
    html.Button('A01 Link Check', id='a01-link-check'),
    html.Br(),
    html.Div(id='a01-link-result'),
    html.Hr(),
    html.Button('A03 Link Check',id='a03-link-check'),
    html.Br(),
    html.Div(id='a03-link-result'),
    html.Hr(),
    html.Button('A10 Link Check',id='a10-link-check'),
    html.Br(),
    html.Div(id='a10-link-result'),
    html.Hr(),
    html.Button('A11 Link Check',id='a11-link-check'),
    html.Br(),
    html.Div(id='a11-link-result'),
    html.Hr(),
    html.Button('A14 Link Check',id='a14-link-check'),
    html.Br(),
    html.Div(id='a14-link-result'),
    html.Hr(),
    html.Button('A17 Link Check',id='a17-link-check'),
    html.Br(),
    html.Div(id='a17-link-result'),

    html.Hr(),
    html.Button('A44_volt Link Check',id='a44v-link-check'),
    html.Br(),
    html.Div(id='a44v-link-result'),
    html.Hr(),
    html.Button('A44_RS Link Check',id='a44r-link-check'),
    html.Br(),
    html.Div(id='a44r-link-result'),
    html.Hr(),
    html.Button('A45_volt Link Check',id='a45v-link-check'),
    html.Br(),
    html.Div(id='a45v-link-result'),
    html.Hr(),
    html.Button('A45_RS Link Check',id='a45r-link-check'),
    html.Br(),
    html.Div(id='a45r-link-result'),
    html.Br(),
])


@callback(Output('all-result', 'children'),
              Input('interval', 'n_intervals'))
def update_link(n):
    return RAD.test_ADAM()

@callback(
    Output(component_id='a01-link-result', component_property='children'),
    Input(component_id='a01-link-check', component_property='n_clicks'))
def update_link_a01(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A01')

@callback(Output('a03-link-result','children'),Input('a03-link-check','n_clicks'))
def update_link_a03(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A03')

@callback(Output('a10-link-result','children'),Input('a10-link-check','n_clicks'))
def update_link_a10(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A10')

@callback(Output('a11-link-result','children'),Input('a11-link-check', 'n_clicks'))
def update_link_a11(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A11')

@callback(Output('a14-link-result','children'),Input('a14-link-check', 'n_clicks'))
def update_link_a14(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A14')

@callback(Output('a17-link-result','children'),Input('a17-link-check', 'n_clicks'))
def update_link_a17(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A17')

@callback(Output('a44v-link-result','children'),Input('a44v-link-check', 'n_clicks'))
def update_link_a44v(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A44_volt')

@callback(Output('a44r-link-result','children'),Input('a44r-link-check', 'n_clicks'))
def update_link_a44r(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A44_ReSl')

@callback(Output('a45v-link-result','children'),Input('a45v-link-check', 'n_clicks'))
def update_link_a45v(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A45_volt')

@callback(Output('a45r-link-result','children'),Input('a45r-link-check', 'n_clicks'))
def update_linkt_a45r(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return RAD.check_ADAM_result('A45_ReSl')


