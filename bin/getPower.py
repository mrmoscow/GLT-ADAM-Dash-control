#! /usr/bin/python3

import argparse
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD


def get_opt():
    parser = argparse.ArgumentParser(description="For get the dB value from Power Meter")
    parser.add_argument('-w','--watt', default=False, action='store_true',help="return the result in watt")
    args = parser.parse_args()
    return args.watt


watt = get_opt()
if watt:
    print("sorry, code still in development")

print(RAD.get_Power('PM1'))
print("Power1 get",RAD.get_Power('PM1'))
print("Power2 get",RAD.get_Power('PM2'))
print("Power3 get",RAD.get_Power('PM3'))
print("Power4 get",RAD.get_Power('PM4'))

