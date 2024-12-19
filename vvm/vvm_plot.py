#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
from datetime import datetime
#from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("../module")
#import ReceiverADAM as RAD
#import SpecAnalyzer as SA


def plot_vvm(filename,form_mod):
    [first,loc2,form_mod2,t1,t2]=filename.rstrip('.txt').split("_")
    print(filename,first,loc2,form_mod2,t1,t2)
    #timenow=t1+"_"+t2
    timeWritetoFile, timecount, phase, ba = np.genfromtxt(filename,unpack="True")
    #print(len(phase),max(timecount))

    fig1=plt.figure()
    ax = fig1.add_subplot(1,1,1)
    plt.plot(timecount,phase,'b.',markersize=2)
    plt.axis([0, round(timecount[-1]), -180,180])
    major_ticks = np.arange(-180, 181, 20)
    minor_ticks = np.arange(-180, 181, 5)
    plt.xlabel('Time (seconds)', fontsize=18)
    plt.ylabel('Phase (degrees)', fontsize=18)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    #and a corresponding grid
    #ax.grid(which='both')
    #titleForFig="Phase " + " RF = " + str(LO) + ' GHz '
    #plt.title(file.split(".")[0]+"GHz", fontsize=15)
    #pltfigname="Phase" + "_"  + timenow + "_" + str(j) + "_" + str(powerRF) + '_RF' + str(LO) +  ".png"
    pltfigname=filename.rsplit(".",1)[0]+".png"
    #print(filename.split("."))
    plt.savefig(pltfigname)
    plt.show()

def get_opt():
    parser = argparse.ArgumentParser(description=
         "For plot the vvm data. (phase VS Time)")
    parser.add_argument("-f", "--filename", type=str, help="The filename you want to deal with. if not input will plot the loast one in t5.")
    args = parser.parse_args()
    return args


opt = get_opt()


if opt.filename:
    filename=opt.filename

else:
    directory = '../assets/'

    # 查找以 'example' 開頭的檔案
    #files = [f for f in os.listdir(directory) if f.startswith('vvm_')]
    files = [f for f in os.listdir(directory) if f.startswith('vvm_') and f.endswith('.txt')]

    # 找出檔案的完整路徑
    file_paths = [os.path.join(directory, f) for f in files]

    # 根據檔案的最後修改時間排序，選擇最新的檔案
    latest_file = max(file_paths, key=os.path.getmtime)
    print(f"The latest file is: {latest_file}")
    filename=latest_file

plot_vvm(filename,5)
