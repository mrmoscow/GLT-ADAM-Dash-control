import argparse
import sys
import ReceiverADAM as RAD



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
