import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

import time
import ReceiverADAM as RAD #at main dir not
#from bin.690pm as PM
from datetime import datetime

dash.register_page(__name__)


# Layout blocks

layout = html.Div([
    html.H3('690 Phaase Monitor Status and Setting'),
    html.Button('DO and AI check',id='5017-DO-check'),
    html.Br(),
    html.Div(children='Last update: Not once after this page reloac',id='690-DO-result'),
    html.Br(),
    html.Table([
        html.Tr([html.Th(['Define on ADAM 6017']),html.Th(['Return value'])]),
        html.Tr([html.Td(['CH_0(V) ']), html.Td(id='690_V1')]),
        html.Tr([html.Td(['CH_1(V)']), html.Td(id='690_V2')]),
        html.Tr([html.Td(['CH_2(V)']), html.Td(id='690_V3')]),
        html.Tr([html.Td(['CH_3(mV)']), html.Td(id='690_V4')]),
        html.Tr([html.Td(['CH_4(mV)']), html.Td(id='690_V5')]),
        html.Tr([html.Td(['CH_5(mV)']), html.Td(id='690_V6')]),
        html.Tr([html.Td(['CH_6(mV)']),html.Td(id='690_V7')]),
        html.Tr([html.Td(['CH_7(mV)']),html.Td(id='690_V8')]),
    ]),
    html.H4('The DO state on ADAM 6017'),
    html.Table([
        html.Tr([html.Th(['-------']),html.Th(['--------'])]),
        html.Tr([html.Td(['Result']), html.Td(id='690_DO')]),
    ]),
])

the_app = dash.get_app()        # Must specify due to @dash.callback limitations

@the_app.callback(Output('690-DO-result','children'),
          Input('5017-DO-check','n_clicks'),
          prevent_initial_call=True)
def update_output_time(n_clicks):
    if n_clicks is None:
        return "Last update: Not once after this page reloac"
        raise PreventUpdate
    else:
        format_data = "%Y/%m/%d, %H:%M:%S,"
        return "Last update:"+datetime.now().strftime(format_data)

@the_app.callback(
    Output('690_V1','children'),Output('690_V2','children'),
    Output('690_V3','children'),Output('690_V4','children'),
    Output('690_V5','children'),Output('690_V6','children'),
    Output('690_V7','children'),Output('690_V8','children'),
    Input('5017-DO-check','n_clicks'))
def update_output_5017(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        try:
            return ['In Test']*8
        except:
            return ['Error ##']*8


@the_app.callback(
    Output('690_DO','children'),Input('5017-DO-check','n_clicks'))
def update_output_DO5017(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        time.sleep(2)
        try:
            return 'In Test'
        except:
            return 'Error ##'

