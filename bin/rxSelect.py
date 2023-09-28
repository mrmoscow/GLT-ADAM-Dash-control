#! /usr/bin/python3

import argparse
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD



parser = argparse.ArgumentParser(description="For set the Tone,IF,LO path as given receiver")
parser.add_argument("receiver", type=str, help="The receiver,86,230,345,off or rx1,rx2,rx3,rx4")
parser.add_argument("-t", "--tone", help="Setting the tone on",
                    action="store_true")

args = parser.parse_args()
if args.tone:
    print(" The tone is set to on")
    tone="On"
else:
    tone="Off"


if args.receiver not in ['86','230','345','rx1','rx2','rx3','rx4','off','Rx1','Rx2','Rx3','Rx4']:
    sys.exit("Error: The receiver should be in 86,230,300, or off")

if args.receiver in ['86','rx1','Rx1'] :rx=1
if args.receiver in ['230','rx2','Rx2']:rx=2
if args.receiver in ['345','rx3','Rx3']:rx=3
if args.receiver in ['off','rx4','Rx4']:rx=4
#print(args.receiver,rx)

if 'Bad' in RAD.check_ADAM('A01'): sys.exit("Error: A01 is not conection")
if 'Bad' in RAD.check_ADAM('A03'): sys.exit("Error: A03 is not conection")
if 'Bad' in RAD.check_ADAM('A44_ReSl'): sys.exit("Error: A44 is not conection")
if 'Bad' in RAD.check_ADAM('A45_ReSl'): sys.exit("Error: A45 is not conection")

try:
    print("All ADAM works, The receiver will set to ",rx, "with tone ",tone)
    print(RAD.set_Rx(rx,tone))
    print("Receiver set to",rx)
except:
    print("Receiver setting faile")
