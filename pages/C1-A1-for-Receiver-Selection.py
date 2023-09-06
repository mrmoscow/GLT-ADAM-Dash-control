import dash
from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate

import time
from datetime import datetime
import ReceiverADAM as RAD #module for this project

dash.register_page(__name__)


# Layout blocks
rx_opts = [
    {'label':'Rx1 (86GHz)', 'value':1}, {'label':'Rx2 (230GHz)', 'value':2},
    {'label':'Rx3 (345GHz)', 'value':3}, {'label':'Rx4(Undefinided)', 'value':4}]

ch_hex = {1:'FF00', 2:'AA00', 3: '5500', 4:'0000'}


layout = html.Div([
    #html.H3('ReceiverStatus'),
    html.H3('ReceiverSelect'),
    #html.H5('Select Receiver-WCA'),
    #dcc.Dropdown(id='Rx_sel', options=rx_opts,
    #             style={'max-width': '150px'}, placeholder='ReceiverSelect'),
    #html.H5('Tone'),
    #dcc.Dropdown(id='tone',
    #             options=[{'label':'Off','value':1},{'label':'On','value':2}],
    #             style={'max-width': '150px'}, placeholder='Tone On/OFF'),
    #html.H5('Select VGA control Voltage'),
    #dcc.Input(id='vga_in',type='number',min=0,max=10,debounce=True),

    html.Table([
        html.Tr([
            html.Th(['Select Receiver-WCA'],className='adj2'),
            html.Th(['Tone'],className='adj2'),
            html.Th(['VGA Control Voltage'],className='adj2'),
            ]),
        html.Tr([
            html.Td(dcc.Dropdown(id='Rx_sel', options=rx_opts,
                  style={'max-width': '230px'}, placeholder='ReceiverSelect'),className='adj2'),
            html.Td(dcc.Dropdown(id='tone',
            options=[{'label':'Off','value':1},{'label':'On','value':2}],
            style={'max-width': '150px'}, placeholder='Tone On/OFF'),className='adj2'),
            html.Td(dcc.Input(id='vga_in',type='number',min=0,max=10,debounce=True),className='adj2'),
            ]),
    ],className='adj2'),
    html.H6(''),
    html.Button('Submit',id='Rx_Set'),
    html.Div(id='Rx_setting_res'),
    html.Br()
])

the_app = dash.get_app()        # Must specify due to @dash.callback limitations
@the_app.callback(Output('Rx_setting_res','children'),
          Input('Rx_Set','n_clicks'),
          State('Rx_sel','value'),
          State('tone','value'),
          State('vga_in','value'),
          )
def set_5056_ch(n_clicks,rx,tone,volt):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if rx is None:
            rx=4
        if tone is None:
            tone=1
        if tone == 1:
            tone="Off"
        else:
            tone="On"
        try:
            print("The Rx now set to",rx,"with tone",tone)
            return RAD.set_Rx(rx,tone)
        except:
            return 'Error ##'


