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


def combine_png_to_pdf(png_files, output_pdf):
    # Open the first image
    img1 = Image.open(png_files[0])
    # Get the dimensions of the first image
    width, height = img1.size
    # Create a new image with the same dimensions as the first image
    combined_img = Image.new('RGB', (width, height * len(png_files)))
    # Paste each PNG image into the combined image
    for i, png_file in enumerate(png_files):
        img = Image.open(png_file)
        combined_img.paste(img, (0, i * height))
    # Save the combined image as a PDF
    combined_img.save(output_pdf, "PDF", resolution=100.0)


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
png_files=[]
for channel in checkLOList:
    #maybe not need print("Will set CH",channel," to SA with Parameter")
    cf,sp,rl,lg,rb,vb=RAD.channelOpt[int(channel)-1]['SAPar']
    print("Set CH",channel,RAD.channelOpt[int(channel)-1]['label'],"with Parameter",cf,sp,rl,lg,rb,vb)
    RAD.CAB1417switch(int(channel),'SA')
    RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb)
    print("waitting for: CH",f'{channel:02d}',"spectrum.","This one is",i,"of",len(checkLOList))
    #wait for IF path, 5 sec not enoght, 20sec o.k
    time.sleep(20)
    pngfile='./CH'+f'{channel:02d}'+'.png'
    #print(pngfile)
    SA.save_plot(pngfile)
    print("complete")
    i=i+1
    png_files.append(pngfile)

now = datetime.now()
#d = now.strftime("GLTvarious-LOcheck_%Y-%m-%d-%H:%M")
output_pdf=now.strftime("GLT_various-LO_check_%Y-%m-%d-%H:%M.pdf")
print("Start to generate the PDF file from png")
combine_png_to_pdf(png_files, output_pdf)
