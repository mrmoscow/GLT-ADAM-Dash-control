from os.path import exists
import sys
print(sys.version)
print(sys.version_info)
print(sys.version_info[1])
if sys.version_info[1] == 7 or sys.version_info[1] == 9: 
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient

coil_list={"S2":32,"S3":48,"S4":64,"S5":80}

adam_delay = 0.25




