#!/home/obscon/bin/cpy3

import argparse
import sys
sys.path.append("..")
import ReceiverADAM as RAD


print('This script  help to check the A44 and A45')

print('Start to checking the DO/AO of A44')
try:
    print ("The DO of A44 is", RAD.getN_6260("A44_ReSl",6))
except:
    print('Error ##', "The get_6260 of A44_ReSl get issues")

try:
    print ("The AO of A44 is", RAD.get_6224('A44_volt'))
except:
    print('Error ##', "The get_6224 of A44_volt get issues")


print('Start to checking the DO/AO of A45')
try:
    print ("The DO result of A45 is", RAD.getN_6260("A45_ReSl",6))
except:
    print('Error ##', "The get_6260 of A45_ReSl get issues")

try:
    print (R"The AO result of A44 is", RAD.get_6224('A45_volt'))
except:
    print('Error ##', "The get_6224 of A45_volt get issues")
