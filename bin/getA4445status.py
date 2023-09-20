
import argparse
from os.path import exists
import sys
sys.path.append("..")
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient


co=ModbusClient('192.168.1.225',port=502,timeout=10)
print("Link good",co)
r = co.read_coils(18,1)
print("read coils good",r)
intvalue=r.bits

#b0=''.join(["0, " if i==0 else "1, " for i in intvalue])
#b1=["0" if i==0 else "1" for i in b0]
#print(b1)

print('This script  help to check the A44 and A45')
print('Start to checking the DO of A44')
try:
    print ("The DO of A44 is")
    print (RAD.get_6260('A44_ReSl'))
except:
    print('Error ##', "The get_6260 of A44_ReSl get issues")


print('Start to checking the AO of A44')
try:
    print ("The AO of A44 is")
    print (RAD.get_6224('A44_volt'))
except:
    print('Error ##', "The get_6224 of A44_volt get issues")


print('Start to checking the DO of A45')
try:
    print ("The DO result of A44 is")
    print (RAD.get_6260('A45_ReSl'))
except:
    print('Error ##', "The get_6260 of A45_ReSl get issues")


print('Start to checking the AO of A45')
try:
    print ("The AO result of A44 is")
    print (RAD.get_6224('A45_volt'))
except:
    print('Error ##', "The get_6224 of A45_volt get issues")
