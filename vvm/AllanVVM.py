
import os
import os.path

import array
import time
import socket
import numpy
import matplotlib.pyplot as plt
import subprocess
import glob, os, sys
#import shutil

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

    tottime=int(sys.argv[1])
    numRepeats=int(sys.argv[2])
    LO=sys.argv[3]
    powerRF=sys.argv[4]

    print(tottime,numRepeats,LO,powerRF)

    timenow=time.strftime("%d%m%y_%H%M%S")
    timenowDirname=time.strftime("%Y-%m-%d_%H:%M:%S")
    newpath="/home/sfyen/python/vvm/VVMwkdir/"+ timenowDirname
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for j in range(1,numRepeats+1):
        outfilename="./VVMwkdir/Phase" + "_"  + timenow + "_" + str(j) + "_" + str(powerRF) + '_RF' + str(LO) + '.txt'
        outfile=open(outfilename,"w")
        timecount=0
        for i in range(tottime*2):
            phase, ba = VVM_MEAS()
            timeWritetoFile=time.strftime("%Y/%m/%d_%p_%I:%M:%S")
            outfile.write('%30s %8.1f %20s %20s \n' % (timeWritetoFile, timecount, phase, ba))
            print('%30s %8.1f %20s %20s' % (timeWritetoFile, timecount, phase, ba))
            time.sleep(0.35)
            timecount=timecount+0.5
        outfile.close()
    print("End of the data, stat to plotting" )
    timeWritetoFile, timecount, phase, ba = numpy.genfromtxt(outfilename,unpack="True")
    print(timecount,phase,ba)
#         Plot phase
    fig1=plt.figure()
    ax = fig1.add_subplot(1,1,1)
    plt.plot(timecount,phase,'b.',markersize=2)
    plt.axis([0, len(timecount)/2, -180,180])
    major_ticks = numpy.arange(-180, 180, 20)
    minor_ticks = numpy.arange(-180, 180, 5)
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
#         matplotlib.pyplot.close(fig1)




