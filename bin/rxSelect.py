#!/home/obscon/bin/cpy3

import argparse
from os.path import exists
import sys
import subprocess
sys.path.append("..")
sys.path.append("/home/obscon/sfyen/GLT-ADAM-Dash-control")
import ReceiverADAM as RAD
#sys.path.append("/home/obscon/pointing")
#import rot2025
ROT = "/home/obscon/pointing/rot2025.py"


parser = argparse.ArgumentParser(description="For select GLT receiver, will move the M3 mirror to Rx, calibrator to sky,set the IF, LO path, also set the Tone Freq(another locked process needed.)")
parser.add_argument("receiver", type=str, help="The receiver one of ,86,230,345,off or rx1,rx2,rx3,rx4")
parser.add_argument("-t", "--tone", help="turn the tone on, (but don't move tone calibrator )",
                    action="store_true")
parser.add_argument("-n", "--nomirror", help="Don't move the M3 morror and Calibrator. Just LO/IF path",
                    action="store_true")

args = parser.parse_args()
if args.tone:
    print(" The tone is set to on")
    tone="On"
    cpos="tone"
else:
    tone="Off"
    cpos="sky"

if args.receiver not in ['86','230','345','rx1','rx2','rx3','rx4','off','Rx1','Rx2','Rx3','Rx4','rx86','rx230','rx345']:
    sys.exit("Receiver name Error: should be one of (rx86,rx230,rx345,off)")

if args.receiver in ['rx1','Rx1','86','rx86'] :rx=1;mpos="rx86"
if args.receiver in ['rx2','Rx2','230','rx230']:rx=2;mpos="rx230"
if args.receiver in ['rx3','Rx3','345','rx345']:rx=3;mpos="rx345"
if args.receiver in ['rx4','Rx4','off']:rx=4;mpos="guest1"
#print(args.receiver,rx)

if 'Bad' in RAD.check_ADAM('A01'): sys.exit("Error: A01 is not conection")
if 'Bad' in RAD.check_ADAM('A03'): sys.exit("Error: A03 is not conection")
if 'Bad' in RAD.check_ADAM('A44_ReSl'): sys.exit("Error: A44 is not conection")
if 'Bad' in RAD.check_ADAM('A45_ReSl'): sys.exit("Error: A45 is not conection")

try:
    print("All ADAM works, The receiver will set to ",mpos, "with tone",tone,"\n")
    RAD.set_Rx(rx,tone)
    #print("Receiver set to",rx)
    #Next is for moving mirror
    if args.nomirror:
        print("Mirrot & Calibration Postiton don't move")
    else:
        print("Now will moving the M3 mirror to",mpos, "and watch",cpos,"\n")
        result1 = subprocess.run(["cpy3", ROT, mpos , cpos],capture_output=True,
            text=True,check=True)
        print(result1.stdout)
        #print("Next is checking the mirrot & clibrator postion.")
        #result2 = subprocess.run(["cpy3", ROT, "Q"],capture_output=True,
        #    text=True)
        #print(result2.stdout)
        #pos=subprocess.run(["cpy3", ROT, "pos_list"],capture_output=True,text=True)

except subprocess.CalledProcessError as e:
    print("command Faile :", e.cmd)
    print("stderr:", e.stderr)
except Exception as e:
    print("Receiver setting failed:", e)
