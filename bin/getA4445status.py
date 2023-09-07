
import argparse
from os.path import exists
import sys
sys.path.append("..")

co=ModbusClient('192.168.1.213',port=502,timeout=10)
print("Link good",co)
r = co.read_coils(18,4,unit=1,slave=1)
print("read coils good",j co)
intvalue=r.bits
b0=''.join(["0, " if i==0 else "1, " for i in intvalue])
b1=["0" if i==0 else "1" for i in res]
print(b1)


print('Start to checking A44 (DO)')
try:
    print ("The DO result of A44 is")
    print (RAD.get_6260('A44_ReSl'))
except:
    print('Error ##', "The get_6260_A44_ReSl don't finishe")


print('Start to checking A44 (AO)')
try:
    print ("The AO result of A44 is")
    print (RAD.get_6224('A44_volt'))
except:
    print('Error ##', "The get_6224_A44_volt don't finishe")


print('Start to checking A44 (DO)')
try:
    print ("The DO result of A44 is")
    print (RAD.get_6260('A44_ReSl'))
except:
    print('Error ##', "The get_6260_A44_ReSl don't finishe")


print('Start to checking A44 (AO)')
try:
    print ("The AO result of A44 is")
    print (RAD.get_6224('A45_volt'))
except:
    print('Error ##', "The get_6224 of A45_volt don't finishe")
