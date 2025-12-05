#!/home/obscon/bin/cpy3

import argparse
from os.path import exists
import sys
import subprocess
sys.path.append("..")
import ReceiverADAM as RAD
#sys.path.append("/home/obscon/pointing")
#import rot2025
ROT = "/home/obscon/pointing/rot2025.py"


#parser = argparse.ArgumentParser(description="For set the Tone,IF,LO path as given receiver")
parser = argparse.ArgumentParser(description="For select GLT receiver, will move the mirror, set the IF, LO path, also set the Tone Freq(another locked process needed.)")
parser.add_argument("receiver", type=str, help="The receiver one of ,86,230,345,off or rx1,rx2,rx3,rx4")
parser.add_argument("-t", "--tone", help="turn the tone on",
                    action="store_true")
#parser.add_argument("-test", "--", help="Setting the tone on",
#                    action="store_true")

args = parser.parse_args()
if args.tone:
    print(" The tone is set to on")
    tone="On"
else:
    tone="Off"

print(tone)
if args.receiver not in ['86','230','345','rx1','rx2','rx3','rx4','off','Rx1','Rx2','Rx3','Rx4']:
    sys.exit("Receiver name Error: should be one of (86,230,345,off)")

if args.receiver in ['86','rx1','Rx1'] :rx=1;mpos="rx86"
if args.receiver in ['230','rx2','Rx2']:rx=2;mpos="rx230"
if args.receiver in ['345','rx3','Rx3']:rx=3;mpos="rx345"
if args.receiver in ['off','rx4','Rx4']:rx=4;mpos="gust1"
#print(args.receiver,rx)

if 'Bad' in RAD.check_ADAM('A01'): sys.exit("Error: A01 is not conection")
if 'Bad' in RAD.check_ADAM('A03'): sys.exit("Error: A03 is not conection")
if 'Bad' in RAD.check_ADAM('A44_ReSl'): sys.exit("Error: A44 is not conection")
if 'Bad' in RAD.check_ADAM('A45_ReSl'): sys.exit("Error: A45 is not conection")

try:
    print("All ADAM works, The receiver will set to ",rx, "with tone ",tone)
    RAD.set_Rx(rx,tone)
    print("Receiver set to",rx)
    #Next is for moving mirror
    result1 = subprocess.run(["cpy3", "./rot2025.py", rrx,"sky"],capture_output=True,
        text=True)
    print(result1.stdout)
    print("Next is checking the mirrot & clibrator postion.")
    result2 = subprocess.run(["cpy3", "./rot2025.py", "Q"],capture_output=True,
        text=True)
    print(result2.stdout)

except subprocess.CalledProcessError as e:
    print("command Faile :", e.cmd)
    print("stderr:", e.stderr)
except Exception as e:
    print("Receiver setting failed:", e)
