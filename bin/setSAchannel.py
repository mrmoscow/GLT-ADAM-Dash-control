#!/home/obscon/bin/cpy3

import argparse
import sys

sys.path.append("../module")
import ReceiverADAM as RAD




def get_opt():
    parser = argparse.ArgumentParser(description="For set the input channel to SA port")
    parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-p','--para', default=False, action='store_true',help="also change the parameter of SA")
    args = parser.parse_args()
    return args.channel,args.para


channel,para = get_opt()
channel=int(channel)
if para:
    print("Will set channel",channel," to SA with Parameter")
    print(RAD.CAB1417switch(channel,'SA'))
    cf,sp,rl,lg,rb,vb=RAD.channelOpt[int(channel)-1]['SAPar']
    print(channel,RAD.channelOpt[int(channel)-1]['label'],cf,sp,rl,lg,rb,vb)
    print(RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb))
else:
    print("Will set channel",channel," to SA")
    print(RAD.CAB1417switch(channel,'SA'))
