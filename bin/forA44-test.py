import argparse
import sys

sys.path.append("../module")
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
