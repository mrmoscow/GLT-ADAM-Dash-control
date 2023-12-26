import argparse
from os.path import exists
import sys
sys.path.append("..")
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient

import ReceiverADAM as RAD

def getN_6224(machine,b =4):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        #sock.sendto( b"$016\r", (ADAM_list[machine], 1025))
        sock.sendto( b"#01\r", ('192.168.1.212', 1025))
        indata, addr = sock.recvfrom(1024)
        print(indate.decode)
        return indate.decode()
    except:
        return ['Error 02']*b


def setN_6224(machine,channel,v):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01BC010800\r", ('192.168.1.212', 1025))
        indata, addr = sock.recvfrom(1024)
        print(indate.decode)
        return ['Setting Succeful']
    except:
        co.close()
        return ['Error 03']



print('Start to checking the AO of A44')

try:
#    print ("The AO of A44 is")
    print (getN_6224('A44_volt'))
except:
    print('Error ##', "The get_6224 of A44_volt get issues")
'''

try:
    print ("The AO result of A44 is")
    print (RAD.get_6224('A45_volt'))
except:
    print('Error ##', "The get_6224 of A45_volt get issues")
'''
