#import dash_core_components as dcc, dash_html_components as html
#from dash.dependencies import Input, Output
import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

from pymodbus.client import ModbusTcpClient as ModbusClient
import time

dash.register_page(__name__)
#from app import app, all_pages

A45_volt = ModbusClient('192.168.1.214', port=502, timeout=10)
A45_Rx_sel = ModbusClient('192.168.1.215', port=502, timeout=10)
VGA_raw2volt = 10/4095  # seems to be linear
adam_delay = 0.25       # sec

def get_VGA(addr):
    if not A45_volt.connect():      # True / False
        return '{ *** Connection Failure *** }'
    try:
        r = A45_volt.read_holding_registers(addr,1)
        return r.registers[0] *VGA_raw2volt
    except:
        A45_volt.close()
        return '{ *** Reading Failure *** }'

def set_VGA(addr, v):
    if not A45_volt.connect():      # True / False
        return '{ *** Connection Failure *** }'
    try:
        A45_volt.write_register(addr, int(v/VGA_raw2volt))
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        return '<New Value Success>'
    except:
        A45_volt.close()
        return '{ *** Writing Failure *** }'

rx_bits = {1:[True, False, False, False], 2:[False, True, False, False],
    3: [False, False, True, False], 4:[False, False, False, True]}

def rx_id(bool_seq):
    for key, val in rx_bits.items():
        if bool_seq == val:
            return key
    return 'Unknown'

def get_rx():
    if not A45_Rx_sel.connect():
        return '{ *** Connection Failure *** }'
    try:
        r = A45_Rx_sel.read_coils(18, 4)
        return rx_id(r.bits[:4])
    except:
        A45_Rx_sel.close()
        return '{ *** Reading Failure *** }'

def set_rx(rd):
    if not A45_Rx_sel.connect():
        return '{ *** Connection Failure *** }'
    try:
        A45_Rx_sel.write_coils(18, rx_bits[rd])
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        return '<New Value Success>'
    except:
        A45_Rx_sel.close()
        return '{ *** Writing Failure *** }'

# Layout blocks
rx_opts = [
    {'label':'Rx 1', 'value':1}, {'label':'Rx 2', 'value':2}, 
    {'label':'Rx 3', 'value':3}, {'label':'Rx 4', 'value':4, 'disabled':True}]

# Web layout
layout = html.Div([
    html.H1('CAB-A45 Control'),
    dcc.Input(id='VGA-set-ch0', type='number', min=0, max=10, debounce=True,
        placeholder='VGA atten. (RHC) 0-10V'),
    html.Div(id='VGA-cur-ch0'), html.Br(),
    dcc.Input(id='VGA-set-ch1', type='number', min=0, max=10, debounce=True,
        placeholder='VGA atten. (LHC) 0-10V'),
    html.Div(id='VGA-cur-ch1'), html.Br(),
    dcc.Dropdown(id='rx-to-set', options=rx_opts, clearable=False,
        style={'max-width': '200px'}, placeholder='Select the receiver'),
    html.Div(id='rx-current'),
    html.Br(), dcc.Link('Back to Homepage', href='/')
])

#all_pages[0].append('/CAB-A45')         # URL
#all_pages[1].append('CAB-A45')          # Link Text
#all_pages[2].append(layout)             # Layout

# Callbacks
@callback(Output('VGA-cur-ch0', 'children'), Input('VGA-set-ch0', 'value'))
def VGA_set_ch0(val):
    ret = ''
    if val is not None:
        ret = set_VGA(0, val)
    return f'Current VGA attenuation (RHC)= {get_VGA(0)} V ' + ret

@callback(Output('VGA-cur-ch1', 'children'), Input('VGA-set-ch1', 'value'))
def VGA_set_ch1(val):
    ret = ''
    if val is not None:
        ret = set_VGA(1, val)
    return f'Current VGA attenuation (LHC)= {get_VGA(1)} V ' + ret

@callback(Output('rx-current', 'children'), Input('rx-to-set', 'value'))
def Rx_sel(val):
    ret = ''
    if val is not None:
        ret = set_rx(val)
    return f'Currently selected Rx = {get_rx()}' + ret

#if __name__ == '__main__':
#    app.layout = layout
#    app.run_server(debug=True, host='0.0.0.0', port='8051')
