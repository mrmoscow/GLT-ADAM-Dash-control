import argparse
from os.path import exists
import sys
import socket
sys.path.append("..")
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient

import ReceiverADAM as RAD

try:
    print (RAD.get_6224('A45_volt'))
except:
    print('Error ##', "The get_6224 of A45_volt get issues")


try:
    print (RAD.set_6224('A45_volt',0,3.0))
except:
    print('Error ##', "The get_6224 of A45_volt get issues")


try:
    print (RAD.get_6224('A45_volt'))
except:
    print('Error ##', "The get_6224 of A45_volt get issues")
