import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

import time
import ReceiverADAM as RAD #at main dir not
from datetime import datetime

dash.register_page(__name__)


# Layout blocks


layout = html.Div([
    html.H3('A44/A45 Status and Setting'),
    html.Button('A44/45 check',id='a4445-bo-check'),
    html.Br(),
    html.Div(id='a44-bo-result'),
    html.H4('The DO status of A44'),
    html.Table([
        html.Tr([html.Th(['Define on A44']),html.Th(['Return value'])]),
        html.Tr([html.Td(['DO  0']), html.Td(id='a44_Do00')]),
        html.Tr([html.Td(['DO  1']), html.Td(id='a44_Do01')]),
        html.Tr([html.Td(['DO  2']), html.Td(id='a44_Do02')]),
        html.Tr([html.Td(['DO  3']), html.Td(id='a44_Do03')]),
        html.Tr([html.Td(['DO  4']), html.Td(id='a44_Do04')]),
        html.Tr([html.Td(['DO  5']), html.Td(id='a44_Do05')]),
    ]),
    html.H4('The DO status of A45'),
    html.Table([
        html.Tr([html.Th(['Define on A45']),html.Th(['Return value'])]),
        html.Tr([html.Td(['DO  0']), html.Td(id='a45_Do00')]),
        html.Tr([html.Td(['DO  1']), html.Td(id='a45_Do01')]),
        html.Tr([html.Td(['DO  2']), html.Td(id='a45_Do02')]),
        html.Tr([html.Td(['DO  3']), html.Td(id='a45_Do03')]),
        html.Tr([html.Td(['DO  4']), html.Td(id='a45_Do04')]),
        html.Tr([html.Td(['DO  5']), html.Td(id='a45_Do05')]),
    ]),
    html.Br(),
])

the_app = dash.get_app()        # Must specify due to @dash.callback limitations
@the_app.callback(Output('a44-bo-result','children'),Input('a4445-bo-check','n_clicks'))
def update_output_time(n_clicks):
    if n_clicks is None:
        return "Last update: Not once after this page reloac"
        raise PreventUpdate
    else:
        format_data = "%Y/%m/%d, %H:%M:%S,"
        return "Last update:"+datetime.now().strftime(format_data)

@the_app.callback(
    Output('a44_Do00','children'),Output('a44_Do01','children'),
    Output('a44_Do02','children'),Output('a44_Do03','children'),
    Output('a44_Do04','children'),Output('a44_Do05','children'),
    Input('a4445-bo-check','n_clicks'))
def update_output_A44_6260(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        print('Checking A44 (DO)')
        try:
            return RAD.getN_6260("A44_ReSl",6)
            #return RAD.get_6260('A44_ReSl')
        except:
            return ['Error ##']*6


@the_app.callback(
    Output('a45_Do00','children'),Output('a45_Do01','children'),
    Output('a45_Do02','children'),Output('a45_Do03','children'),
    Output('a45_Do06','children'),Output('a45_Do05','children'),
    Input('a4445-bo-check','n_clicks'))
def update_output_A44_6260(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(1)
        print('Checking A45 (DO)')
        try:
            return RAD.getN_6260("A45_ReSl",6)
            #return RAD.get_6260('A45_ReSl')
        except:
            return ['Error ##']*6

