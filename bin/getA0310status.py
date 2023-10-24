#! /home/obscon/bin/mpy3

import argparse
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD

def get_opt():
    parser = argparse.ArgumentParser(description="For retrun A03 A10 (6050)status")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-i','--infoo', default=False, action='store_true',help="just showing the infromation of A03 and A10")
    args = parser.parse_args()
    return args.para


para = get_opt()

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
