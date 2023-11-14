#!/asiaa/home/sfyen/miniconda3/envs/AIPython/bin/python3

import os
import os.path
import array
import time
import socket
import numpy
import matplotlib.pyplot as plt
#matplotlib.use('Agg')
import subprocess
import AmpPhaseToolsRanjani as APT
import glob, os, sys
#import  matplotlib.pyplot as plt
import shutil

#=====================================================================================

# Starting measurements on VVM

def VVM_MEAS():
    ip="192.168.1.204"
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))
    sockGPIB.send(b"SENSE PHASE\n")
    sockGPIB.send(b"FORM POL\n")
    sockGPIB.send(b"MEAS? PHASE\n")
    sockGPIB.send(b"++read eoi\n")
    try:
        phase = sockGPIB.recv(8192)
        phase = phase.decode().rstrip('\r\n')
    except sockGPIB.timeout:
        phase = ""
             #print(phase)  
    sockGPIB.send(b"SENSE BA\n")
    sockGPIB.send(b"FORM LIN\n")
    sockGPIB.send(b"MEAS? BA\n")
    sockGPIB.send(b"++read eoi\n")
    try:
        ba = sockGPIB.recv(8192)
        ba = ba.decode().rstrip('\r\n')
    except sockGPIB.timeout:
        ba = ""
    return phase, ba

#==============================================================================
if __name__ == '__main__':

    file=str(sys.argv[1])
    [t1,t2,j,powerRF,LO]=file.rstrip('.txt').split("_")[-5:]
    timenow=t1+"_"+t2
    LO=file.split("RF")[1].split(".")[0]
    print(file,timenow,j,powerRF,LO)

    #outfilename=filename
    timeWritetoFile, timecount, phase, ba = numpy.genfromtxt(file,unpack="True")
    print(len(phase))
    print(phase)
    #
    fig1=plt.figure()
    ax = fig1.add_subplot(1,1,1)
    plt.plot(timecount,phase,'b.',markersize=2)
    plt.axis([0, len(timecount)/2, -180,180])
    major_ticks = numpy.arange(-180, 181, 20)
    minor_ticks = numpy.arange(-180, 181, 5)
    plt.xlabel('Time (seconds)', fontsize=18)
    plt.ylabel('Phase (degrees)', fontsize=18)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)

    #and a corresponding grid
    ax.grid(which='both')
    titleForFig="Phase " + " RF = " + str(LO) + ' GHz '
    plt.title(titleForFig, fontsize=20)
    pltfigname="Phase" + "_"  + timenow + "_" + str(j) + "_" + str(powerRF) + '_RF' + str(LO) +  ".png"
    plt.savefig(pltfigname)
    plt.show()
#         matplotlib.pyplot.show()
#         matplotlib.pyplot.close(fig1)
    inpfilename=file.split("RF")
    #print(inpfilename)
    RFval=inpfilename[1].split(".")
    #print(RFval)
    outfilename=file.split(".")[0] + "_AllanVar" + ".txt"
    print(inpfilename,RFval,outfilename)

    RFvalnum=float(RFval[0])*1000.0
    LOvalnum=float(LO)*1000.0
    print(RFvalnum,LOvalnum)
    subprocess.call(["./computeAVRanjani", file, str(LOvalnum), "0.5", outfilename])

    timestamp, AllanVar, err = numpy.genfromtxt(outfilename, unpack="True")
    fnameout=file.split(".")[0] + "_AllanVar" + ".png"
    plt.plot(timestamp, AllanVar, marker='.', linestyle='-')
    ax = plt.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.semilogx
    plt.semilogy
    plt.grid()
    plt.title(file.split(".")[0])
    plt.xlabel("T (sec)")
    plt.ylabel("Allan dev")
    plt.xlim(1,10000)
    plt.ylim(1e-17, 1e-12)
    plt.savefig(fnameout)
    plt.show()
    plt.clf()


    #APT.bulkPhase(".txt", 0.5, ' ', 2, plot=False)
    print("End")
'''   
   for file in glob.glob("*-AV.txt"):
     timestamp, Phase2pt = numpy.genfromtxt(file, unpack="True")

     fname=file.split("-AV")
     fnameout=fname[0] + "-AV" + '.png'
     plt.plot(timestamp, Phase2pt, marker='.', linestyle='-')
     ax = plt.gca()
     ax.set_xscale('log')
     ax.set_yscale('log')
     plt.semilogx
     plt.semilogy
     plt.grid()
     plt.title(fname[0])
     plt.xlabel("T (sec)")
     plt.ylabel("2 pt Allan dev (fs)")
     plt.xlim(1,2000)
     plt.ylim(1, 100)
     plt.savefig(fnameout)
     plt.clf()



   dest_dir="/var/www/cgi-bin/GLT/VVMwkdir/" + timenowDirname
   for file in glob.glob("Phase_*.txt"):
       shutil.move(file,dest_dir)
   for file in glob.glob("Phase_*.png"):
       shutil.move(file,dest_dir)
   os.remove("/var/www/cgi-bin/GLT/lockfile_phase_stability")

'''
