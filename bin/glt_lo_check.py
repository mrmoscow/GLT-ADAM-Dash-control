#! /usr/bin/python3

import argparse
from os.path import exists
import sys
import time
sys.path.append("..")
import ReceiverADAM as RAD
import SpecAnalyzer as SA

def get_opt():
    parser = argparse.ArgumentParser(description="For check the LO siutaiton by using SA")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    #parser.add_argument('-p','--para', default=False, action='store_true',help="also change the parameter of SA")
    args = parser.parse_args()
    return args.channel,args.para


#para1,para2 = get_opt()

#channel=int(channel)
#checkLOList=[7,8,15,14,14,31,29,13,30,19,20,33,34]
checkLOList=[7,8,15]

i=1
for channel in checkLOList:
    #maybe not need print("Will set CH",channel," to SA with Parameter")
    cf,sp,rl,lg,rb,vb=RAD.channelOpt[int(channel)-1]['SAPar']
    print("Set CH",channel,RAD.channelOpt[int(channel)-1]['label'],"with Parameter",cf,sp,rl,lg,rb,vb)
    RAD.CAB1417switch(int(channel),'SA')
    RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb)
    print("waitting for: CH",+f'{channel:02d}',"spectrum.","This one is",i,'/',len(checkLOList))
    #wait for IF path, 5 sec not enoght, 20sec o.k
    time.sleep(20)
    #plot_and get_PDF
    pngfile='./CH'+f'{channel:02d}'+'.png'
    #print(pngfile)
    SA.save_plot(pngfile)
    print("complete")
    i=i+1


