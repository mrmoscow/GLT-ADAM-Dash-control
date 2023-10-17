import argparse
from os.path import exists
import sys
sys.path.append("..")
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient

import ReceiverADAM as RAD



def set_6050(machine,data):
    # data is  [0,0,0,0,0,0], 6 list of
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    time.sleep(adam_delay)  # must be padded before the consecutive reading
    if not co.connect():      # True / False
        return 'Error 01'
    try:
        print(co.write_coils(16, data,unit=1,slave=1))
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        return 'Setting Succeful'
    except:
        co.close()
        return 'Error 03'

def get_6050(machine,b=18):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    time.sleep(adam_delay)  # must be padded before the consecutive reading
    if not co.connect():      # True / False
        return ['Error 01']*18
    try:
        r = co.read_coils(0,12,unit=1,slave=1)
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        res=r.bits[0:12]
        r2 = co.read_coils(16,6,unit=1,slave=1)
        res.extend(r2.bits[0:6])
        br=["0" if i==0 else "1" for i in res]
        print(br)
        return br
    except:
        co.close()
        return ['Error 02']*18


print('This script  help to check the A03 (6050)')
print('Start to checking the  of A3')

result=RAD.get_6050('A03')
print(result[0:12])
print(result[12:])


print('This script  help to check the A10 (6050)')
print('Start to checking the  of A10')

result=RAD.get_6050('A10')
print(result[0:12])
print(result[12:])
