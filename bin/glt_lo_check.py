#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
from datetime import datetime
#from PIL import Image

sys.path.append("../module")
import ReceiverADAM as RAD
import SpecAnalyzer as SA


def get_opt():
    parser = argparse.ArgumentParser(description="For check the LO siutaiton by using SA")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-r','--rxchange',action="store_true",help="let Rx change, defaule is no Rx(A1) change")
    args = parser.parse_args()
    return args.rxchange

rx_change = get_opt()

#channel=int(channel)
checkLOList=[7,8,15,14,14,31,29,13,30,19,20,33,34]
#CH14 must at 4 and 5. change i== if the list change. 
#checkLOList=[7,8,15,14,14,31]


i=1
png_files=[]
for channel in checkLOList:
    pngfile=f'../assets/CH{channel:02d}.png'
    plt_title=f'CH{channel:02d}:'+RAD.channelOpt[int(channel)-1]['label']
    if (channel==14 and i==4): # for 1st CH14
        print("in CH 14, Rx2")
        pngfile='../assets/CH14-Rx2.png'
        plt_title='CH14-Rx2:0.5GHz'
        if rx_change == True:
            RAD.set_5056('A01','5400')
    if (channel==14 and i==5):
        print("in CH 14, Rx1")
        pngfile='../assets/CH14-Rx1.png'
        plt_title='CH14-Rx2:1.5GHz'
        if rx_change == True:
            RAD.set_5056('A01','FC80')
        #R_IF from Rx1
    #maybe not need print("Will set CH",channel," to SA with Parameter")
    cf,sp,rl,lg,rb,vb=RAD.channelOpt[int(channel)-1]['SAPar']
    print("Set CH",channel,RAD.channelOpt[int(channel)-1]['label'],"with Parameter",cf,sp,rl,lg,rb,vb)
    RAD.CAB1417switch(int(channel),'SA')
    RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb)

    print("waitting for: CH",f'{channel:02d}',"spectrum.","This one is",i,"of",len(checkLOList))
    #wait for IF path, 5 sec not enoght, 20sec o.k
    time.sleep(25)
    SA.save_plot(pngfile,plt_title)
    print("complete")
    i=i+1
    png_files.append(pngfile)

now = datetime.now()
output_pdf=now.strftime("../assets/GLT_various-LO_check_%Y-%m-%d-%H-%M.pdf")
print("Start to generate the PDF file from png")
SA.combine_png_to_pdf(png_files, output_pdf)
