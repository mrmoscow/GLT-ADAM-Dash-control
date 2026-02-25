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

def png_to_grid(png_files,out_png,
    cell_size=None,margin=20, gap=20,                   
    bg_color=(255, 255, 255)  # background = white
):

    imgs = [Image.open(p).convert("RGBA") for p in png_files]

    if cell_size is None:
        cell_w = max(im.width for im in imgs)
        cell_h = max(im.height for im in imgs)
    else:
        cell_w, cell_h = cell_size

    def fit_to_cell(im):
        im = im.copy()
        im.thumbnail((cell_w, cell_h), Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
        x = (cell_w - im.width) // 2
        y = (cell_h - im.height) // 2
        cell.paste(im, (x, y), im)
        return cell

    cells = [fit_to_cell(im) for im in imgs]
    #2 rows, each 4 png
    cols = 4
    rows = 2

    out_w = margin * 2 + cols * cell_w + (cols - 1) * gap
    out_h = margin * 2 + rows * cell_h + (rows - 1) * gap
    canvas = Image.new("RGBA", (out_w, out_h), bg_color + (255,))

    for i in range(4):
        x = margin + i * (cell_w + gap)
        y = margin
        canvas.paste(cells[i], (x, y), cells[i])
    for j in range(4):
        x = margin + j * (cell_w + gap)
        y = margin + (cell_h + gap)
        canvas.paste(cells[4 + j], (x, y), cells[4 + j])
    canvas.convert("RGB").save(out_png, "PNG")

def get_opt():
    parser = argparse.ArgumentParser(description="For check the BDC siutaiton by using SA")
    parser.add_argument("-f","--lockFreq", help="Lock Frequency(FL)", nargs='?', default='200')
    #parser.add_argument('-p','--para', default=False, action='store_true',help="also change the parameter of SA")
    args = parser.parse_args()
    return args.lockFreq

checkLOList=[7,31,30,44,19,20,33,34]
i=1
png_files=[]

for channel in checkLOList:
    pngfile=f'../assets/CH{channel:02d}.png'
    plt_title=f'CH{channel:02d}:'+RAD.channelOpt[int(channel)-1]['label']
    cf,sp,rl,lg,rb,vb=RAD.channelOpt[int(channel)-1]['SAPar']
    #print("Set CH",channel,RAD.channelOpt[int(channel)-1]['label'],"with Parameter",cf,sp,rl,lg,rb,vb)
    
    RAD.CAB1417switch(int(channel),'SA')
    RAD.set_SA('SA1',cf,sp,rl,lg,rb,vb)
    print("waitting for: CH",f'{channel:02d}',"spectrum.","This one is",i,"of",len(checkLOList))
    #wait for IF path, 5 sec not enoght, 20sec o.k
    time.sleep(25)

    #auto tune for ch44
    if (channel==44):
        #atuotone.
        print("In channel 44, will auto tune the SA.")
        SA.autotune()
        time.sleep(5)

    SA.save_plot(pngfile,plt_title)
    print("complete")
    i=i+1
    png_files.append(pngfile)

now = datetime.now()
output_pdf="../spectrum/spec_check"+now.strftime("_%Y-%m-%d-%H-%M.pdf")
output_png="../spectrum/spec_check"+now.strftime("_%Y-%m-%d-%H-%M.png")
print("Start to combine each png into PDF and png( /spectrum/spec_check...)")
combine_png_to_pdf(png_files, output_pdf)
png_to_grid(png_files,output_png)
