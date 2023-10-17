#! /usr/bin/python3

import argparse
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD


def get_opt():
    parser = argparse.ArgumentParser(description="For retrun A01 status")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-p','--para', default=False, action='store_true',help="also change the parameter of SA")
    args = parser.parse_args()
    return args.para


para = get_opt()

if 'Bad' in RAD.check_ADAM('A14'): sys.exit("Error A14 is not conection")
if 'Bad' in RAD.check_ADAM('A17'): sys.exit("Error A17 is not conection")


print("The A14/17 have 5017, 5018,and 4*5056")


print("From A14-5017:",RAD.get_5017('A14'))

print("From A14-5017:",RAD.get_5018('A14'))


print("Next is the valud from A14-4*5056")
print(RAD.get_5056('A14','S2'))
print(RAD.get_5056('A14','S3'))
print(RAD.get_5056('A14','S4'))
print(RAD.get_5056('A14','S5'))


print("From A17-5017:",RAD.get_5017('A17'))

print("From A17-5017:",RAD.get_5018('A17'))

print("Next is the valud from A17-4*5056")
print(RAD.get_5056('A17','S2'))
print(RAD.get_5056('A17','S3'))
print(RAD.get_5056('A17','S4'))
print(RAD.get_5056('A17','S5'))
