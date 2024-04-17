#!/home/obscon/bin/cpy3

import argparse
import sys
sys.path.append("../module")
import ReceiverADAM as RAD





def get_opt():
    parser = argparse.ArgumentParser(description="For get the dB value from 4 Power Meter")
    parser.add_argument('-w','--watt', default=False, action='store_true',help="return the result in watt")
    args = parser.parse_args()
    return args.watt

watt = get_opt()
if watt:
    print("sorry, code still in development")

#print(RAD.get_Power('PM1'))
print("PowerMeter 1 get",RAD.get_Power('PM1'))
print("PowerMeter 2 get",RAD.get_Power('PM2'))
print("PowerMeter 3 get",RAD.get_Power('PM3'))
print("PowerMeter 4 get",RAD.get_Power('PM4'))
