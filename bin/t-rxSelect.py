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

#print(tone)
result1 = subprocess.run(["cpy3", "./rot2025.py","Q"],capture_output=True,
        text=True)
print(result1.stdout)
