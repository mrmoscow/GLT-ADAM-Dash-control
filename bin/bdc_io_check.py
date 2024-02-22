#! /usr/bin/python3

import argparse
from os.path import exists
import sys
import time
from datetime import datetime
from PIL import Image

sys.path.append("..")
import ReceiverADAM as RAD
import SpecAnalyzer as SA


def combine_png_to_pdf(png_files, pdf_file):
    images = []
    for file in png_files:
        image = Image.open(file)
        image = image.convert('RGB')
        images.append(image)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])

def get_opt():
    parser = argparse.ArgumentParser(description="For check the BDC siutaiton by using SA")
    parser.add_argument("-f","--lockFreq", help="Lock Frequency(FL)", nargs='?', default='200')
    #parser.add_argument('-p','--para', default=False, action='store_true',help="also change the parameter of SA")
    args = parser.parse_args()
    return args.lockFreq

lockFreq = get_opt()
#print(lockFreq)
checkLOList=[1,5,23,27,3,2,4,6,25,24,26,28]

i=1
png_files=[]
for channel in checkLOList:

    pngfile=f'../assets/CH{channel:02d}.png'
    plt_title=f'CH{channel:02d}:'+RAD.channelOpt[int(channel)-1]['label']
    if channel in [1,5,23,27]:
        ta=['RU of ','LU of ','RL of ','LL of '][[1,5,23,27].index(channel)]
        #print("in 1,5,23,27",index,ta),get ta from index 1,5,23,27
        plt_title=f'CH{channel:02d}:'+ta+lockFreq+'GHz'
    print(plt_title)
    cf,sp,rl,lg,rb,vb=RAD.channelOpt[int(channel)-1]['SAPar']
    print("Set CH",channel,RAD.channelOpt[int(channel)-1]['label'],"with Parameter",cf,sp,rl,lg,rb,vb)
    RAD.CAB1417switch(int(channel),'SA')
    RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb)

    print("waitting for: CH",f'{channel:02d}',"spectrum.","This one is",i,"of",len(checkLOList))
    #wait for IF path, 5 sec not enoght, 20sec o.k
    time.sleep(20)
    SA.save_plot(pngfile,plt_title)
    print("complete")
    i=i+1
    png_files.append(pngfile)

now = datetime.now()
output_pdf="../assets/GLT_receiver_output_check_"+lockFreq+now.strftime("_%Y-%m-%d-%H-%M.pdf")
#print(output_pdf)
print("Start to generate the PDF file from png")
combine_png_to_pdf(png_files, output_pdf)
