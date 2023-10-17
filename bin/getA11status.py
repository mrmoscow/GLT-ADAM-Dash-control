#! /usr/bin/python3

import argparse
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD


def get_opt():
    parser = argparse.ArgumentParser(description="For retrun A11 status")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-p','--para', default=False, action='store_true',help="for backup using")
    args = parser.parse_args()
    return args.para


para = get_opt()
#channel=int(channel)

if 'Bad' in RAD.check_ADAM('A11'): sys.exit("Error A11 is not conection")


print("The A11 have 5017, 5018,5024,5056")

print("From 5017:",RAD.get_5017('A11'))

print("From 5018",RAD.get_5018('A11'))

print("From 5024",RAD.get_5024('A11'))

print("Next from 5056")
print(RAD.get_5056('A11'))

