
import os
import os.path
import array
import time
import socket
import subprocess
import glob, os, sys
import shutil

# Special characters to be escaped
LF   = 0x0A
CR   = 0x0D
ESC  = 0x1B
PLUS = 0x2B

#IP ofprologix  addr for GPIP setting
#ip="192.168.1.70"
#addr="8"

#for vvm from Taipei Lan than to JCMT
#ip="192.168.1.204" #addr="8"

#for vvm in Thule"  
#ip="192.168.1.204" #addr="25"
#ip="192.168.1.155" #addr="25"
#ip="192.168.1.74"  #addr="8"

#==============================================================================
def IsSpecial(data):
    return data in (LF, CR, ESC, PLUS)

#==============================================================================
def CheckError():
    sockGPIB.send(b"SYST:ERR?\n")
    sockGPIB.send(b"++read eoi\n")

    s = None

    try:
        s = sockGPIB.recv(4096)
    except socket.timeout:
        s = ""

    if s[:1] != "0":
       print (s)

#==============================================================================
def queryVVM(ip,cmd):
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))

    sockGPIB.send(bytes(cmd + "\n",'ascii'))
    sockGPIB.send(b"++read eoi\n")
    try:
       ret = sockGPIB.recv(8192)
       ret = ret.decode().rstrip('\r\n')
    except socket.timeout:
       ret = ""
    #print(ret)
    return ret

def sendVVM(ip,cmd):
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))
    sockGPIB.send(bytes(cmd + "\n",'ascii'))

def set_device(ip):
    # Open TCP connect to port 1234 of GPIB-ETHERNET
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))

    # Set mode as CONTROLLER
    sockGPIB.send(b"++mode 1\n")

    # Set HP8508A address
    #sockGPIB.send("++addr " + addr + "\n")

    # Turn off read-after-write to avoid "Query Unterminated" errors
    sockGPIB.send(b"++auto 0\n")

    # Read timeout is 500 msec
    sockGPIB.send(b"++read_tmo_ms 500\n")

    # Do not append CR or LF to GPIB data
    sockGPIB.send(b"++eos 3\n")

    # Assert EOI with last byte to indicate end of data
    sockGPIB.send(b"++eoi 1\n")


def check_vvm(ip):
    # Open TCP connect to port 1234 of GPIB-ETHERNET
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))
    print("start checing the prologix GPIB-Ethenet at IP", ip)

    sockGPIB.connect((ip, 1234))

    sockGPIB.send(b"++mode\n")
    time.sleep(0.5)
    indata = sockGPIB.recv(4096)
    print("The prologix at mode",indata.decode().rstrip('\r\n'))

    sockGPIB.send(b"++auto\n")
    time.sleep(0.5)
    indata = sockGPIB.recv(4096)
    print("The Auto mode is",indata.decode().rstrip('\r\n'))

    sockGPIB.send(b"++addr\n")
    time.sleep(0.5)
    indata = sockGPIB.recv(4096)
    print("GPIP address",indata.decode().rstrip('\r\n'))

    sockGPIB.send(b"*IDN?\n")
    sockGPIB.send(b"++read eoi\n")
    time.sleep(0.5)
    try:
        indata = sockGPIB.recv(4096)
        print("The IDN of the Inststance is ",indata.decode().rstrip('\r\n'))
    except socket.timeout:
        print("Can not get the Instance information")

def get_vvm_AB(ip,ftype):
    if ftype == 0:
        sendVVM(ip,"DAN OFF")
        sendVVM(ip,"FORM LIN")
        sendVVM(ip,"FORM POL")
        time.sleep(0.05)
        avol = queryVVM(ip,"MEAS? AVOL")
        time.sleep(0.05)
        bvol = queryVVM(ip,"MEAS? BVOL")
        time.sleep(0.05)
        phase = queryVVM(ip,"MEAS? PHASE")
        time.sleep(0.05)
        BA = queryVVM(ip,"MEAS? BA")
        print('A volts: ',str(avol),' B Volts: ',str(bvol),' B-A Phase: ',str(phase), "BA: ", str(BA))
        return BA,phase
    elif ftype ==1:
        sendVVM(ip,"DAN OFF")
        sendVVM(ip,"FORM LOG")
        sendVVM(ip,"FORM POL")
        time.sleep(0.05)
        bvol = queryVVM(ip,"MEAS? BVOL")
        time.sleep(0.05)
        phase = queryVVM(ip,"MEAS? PHASE")
        print('B Input(dB): ',str(bvol),' B-A Phase(deg): ',str(phase))
        return bvol,phase
    elif ftype==2:
        sendVVM(ip,"DAN OFF")
        sendVVM(ip,"FORM LIN")
        sendVVM(ip,"FORM POL")
        time.sleep(0.05)
        bvol = queryVVM(ip,"MEAS? BVOL")
        time.sleep(0.05)
        phase = queryVVM(ip,"MEAS? PHASE")
        print('B Input(mV): ',str(bvol),' B-A Phase(deg): ',str(phase))
        return bvol,phase
    elif ftype ==3:
        sendVVM(ip,"DAN OFF")
        sendVVM(ip,"FORM LOG")
        sendVVM(ip,"FORM POL")
        time.sleep(0.05)
        avol = queryVVM(ip,"MEAS? AVOL")
        time.sleep(0.05)
        bvol = queryVVM(ip,"MEAS? BVOL")
        print('A Input(dB): ',str(avol),' B Input(dB): ',str(bvol))
        return avol,bvol
    elif ftype ==4:
        sendVVM(ip,"DAN OFF")
        sendVVM(ip,"FORM LIN")
        sendVVM(ip,"FORM POL")
        time.sleep(0.05)
        avol = queryVVM(ip,"MEAS? AVOL")
        time.sleep(0.05)
        bvol = queryVVM(ip,"MEAS? BVOL")
        print('A Input(mV): ',str(avol),' B Input(mV): ',str(bvol))
        return avol,bvol
    else:
        return 0.0,0.0
        #ip="192.168.1.70"
#check_vvm(ip)
#get_vvm_AB(ip,0)

'''
# Take Measurements
sendVVM(ip,"DAN OFF")
sendVVM(ip,"SENSE AVOL")
sendVVM(ip,"FORM LIN")
time.sleep(0.5)
avol = queryVVM(ip,"MEAS? AVOL")
sendVVM(ip,"SENSE BVOL")
sendVVM(ip,"FORM LIN")
time.sleep(0.5)
bvol = queryVVM(ip,"MEAS? BVOL")
sendVVM(ip,"SENSE PHASE")
sendVVM(ip,"FORM POL")
time.sleep(0.5)
phase = queryVVM(ip,"MEAS? PHASE")
time.sleep(0.5)
BA = queryVVM(ip,"MEAS? BA")
#sendVVM("DAN ON")
#sendVVM("SYST:KEY 2")

print('A volts: ',str(avol),' B Volts: ',str(bvol),' B-A Phase: ',str(phase), "BA: ", str(BA))
print("End")
'''
