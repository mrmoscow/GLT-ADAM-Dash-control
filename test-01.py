import dash
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
import ReceiverADAM as RAD #at main dir not
from datetime import datetime

#This is for test the set_6050
print(RAD.set_6050('A03',[0,0,0,0,0,0]))

#print(RAD.set_6050('A03',[0,0,0,0,1,1]))
#print(RAD.set_6050('A03',[0,0,0,1,0,0]))


# Next is for test set_Rx.
#print(RAD.set_Rx(1,'OFF'))
#print(RAD.set_Rx(2,'On'))




