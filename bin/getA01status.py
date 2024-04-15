#!/home/obscon/bin/cpy3

import argparse
import sys

sys.path.append("../module")
import ReceiverADAM as RAD

def get_opt():
    parser = argparse.ArgumentParser(description="For retrun A01 status")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-i','--info', default=False, action='store_true',help="using in future.")
    args = parser.parse_args()
    return args.info


para = get_opt()
#channel=int(channel)

if 'Bad' in RAD.check_ADAM('A01'): sys.exit("Error A01 is not conection")


print("The A1 have 5017, 5018,5024,5056")

print("From 5017:",RAD.get_5017('A01'))

print("From 5018",RAD.get_5018('A01'))

print("From 5024",RAD.get_5024('A01'))

print("Next from 5056")
print(RAD.get_5056('A01'))

