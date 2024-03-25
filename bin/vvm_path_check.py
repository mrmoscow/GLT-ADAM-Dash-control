#!/home/obscon/bin/cpy3

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
    parser.add_argument("-r","--receiver", help="Receiver number", nargs='?', default='1')
    #parser.add_argument('-p','--para', default=False, action='store_true',help="also change the parameter of SA")
    args = parser.parse_args()
    return args.receiver

receiver = get_opt()
if receiver not in ['86','230','345','1','2','3']:
    sys.exit("Error: The receiver should be in one of 1,2,3 or 86,230,300)
print(receiver)
checkLOList=[44,22,1,1,12,16,16,11,9,10]


i=1
png_files=[]
for channel in checkLOList:

    pngfile=f'../assets/CH{channel:02d}.png'
    plt_title=f'CH{channel:02d}:'+RAD.channelOpt[int(channel)-1]['label']
    cf,sp,rl,lg,rb,vb=RAD.channelOpt[int(channel)-1]['SAPar']
    if (channel==1 and i==3): # for 1st CH1
            pngfile=f'../assets/CH{channel:02d}.png'
            plt_title=f'CH{channel:02d}:'+RAD.channelOpt[int(channel)-1]['label']
            #cf,sp,rl,lg,rb,vb==[]
    if (channel==1 and i==3): # for 2nd CH1: zoom in 
    if (channel==16 and i==6): # for 1st CH16: 44.5Hz
    if (channel==16 and i==8): # for 2nd CH16: 18.5Hz    



    print(plt_title)
    print("Set CH",channel,RAD.channelOpt[int(channel)-1]['label'],"with Parameter",cf,sp,rl,lg,rb,vb)
    #RAD.CAB1417switch(int(channel),'SA')
    #RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb)

    print("waitting for: CH",f'{channel:02d}',"spectrum.","This one is",i,"of",len(checkLOList))
    #wait for IF path, 5 sec not enoght, 25sec o.k
    time.sleep(25)
    #SA.save_plot(pngfile,plt_title)
    print("complete")
    i=i+1
    png_files.append(pngfile)

now = datetime.now()
output_pdf="../assets/VVM_input_check_Rx"+receiver+now.strftime("_%Y-%m-%d-%H-%M.pdf")
print(output_pdf)
print("Start to generate the PDF file from png")
#combine_png_to_pdf(png_files, output_pdf)
