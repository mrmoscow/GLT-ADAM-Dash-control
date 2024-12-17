#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
from datetime import datetime
#from PIL import Image

sys.path.append("../module")
#import ReceiverADAM as RAD
#import SpecAnalyzer as SA
import hp8508 as hp


#ip="192.168.1.70"
#hp.get_vvm_info(ip)

for ip in ["192.168.1.74","192.168.1.155","192.168.1.204"]:
    print("Start to check the VVM in GreenLand")
    hp.get_vvm_info(ip)

print("End of the code")
