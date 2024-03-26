#!/asiaa/home/sfyen/miniconda3/envs/AIPython/bin/python3

#/asiaa/home/sfyen/miniconda3/envs/AIPython/bin/python3 ./plotVVM.py Phase_191223_145753_1_1_RF648.txt

import os, sys
import time
import socket
import numpy
import matplotlib.pyplot as plt
import subprocess
import AmpPhaseToolsRanjani as APT


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
    #The file must generate from 
    file=str(sys.argv[1])
    [t1,t2,j,powerRF,LO]=file.rstrip('.txt').split("_")[-5:]
    timenow=t1+"_"+t2
    LO=file.split("RF")[1].split(".")[0]
    print(file,timenow,j,powerRF,LO)

    timeWritetoFile, timecount, phase, ba = numpy.genfromtxt(file,unpack="True")
    print(len(phase))
    #print(phase)

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
    plt.title(file.split(".")[0]+"GHz", fontsize=15)
    #pltfigname="Phase" + "_"  + timenow + "_" + str(j) + "_" + str(powerRF) + '_RF' + str(LO) +  ".png"
    pltfigname=file.split(".")[0]+".png"
    plt.savefig(pltfigname)
    plt.show()
    plt.clf()
    outfilename=file.split(".")[0] + "_AllanVar" + ".txt"
    #print(RFval,outfilename)

    #RFvalnum=float(RFval[0])*1000.0
    LOvalnum=float(LO)*1000.0
    print("outfilename",outfilename,"LOvalnum",LOvalnum)
    subprocess.call(["./computeAVRanjani", file, str(LOvalnum), "0.5", outfilename])

    timestamp, AllanVar, err = numpy.genfromtxt(outfilename, unpack="True")
    fnameout=file.split(".")[0] + "-AllanVar" + ".png"
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

    #print("Start to bulkPhase")
    APT.onePhase(file, 0.5, ' ', 2,plot=False)
    #APT.bulkPhase(".txt", 0.5, ' ', 2, plot=False)

    fileAV=file.split(".")[0] + "-AV" + ".txt"
    timestamp, Phase2pt = numpy.genfromtxt(fileAV, unpack="True")
    fnameout=file.split(".")[0] + "-AV" + ".png"
    print(fnameout)
    plt.plot(timestamp, Phase2pt, marker='.', linestyle='-')
    ax = plt.gca()
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.semilogx
    plt.semilogy
    plt.grid()
    plt.title(file.split(".")[0])
    plt.xlabel("T (sec)")
    plt.ylabel("2 pt Allan dev (fs)")
    plt.xlim(1,2000)
    plt.ylim(1, 100)
    plt.savefig(fnameout)
    plt.show()
    plt.clf()


'''
   dest_dir="/var/www/cgi-bin/GLT/VVMwkdir/" + timenowDirname
   for file in glob.glob("Phase_*.txt"):
       shutil.move(file,dest_dir)
   for file in glob.glob("Phase_*.png"):
       shutil.move(file,dest_dir)
   os.remove("/var/www/cgi-bin/GLT/lockfile_phase_stability")

'''
