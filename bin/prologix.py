
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

#for vvm in Taipei Lab
ip="192.168.1.204"
addr="8"

#for vvm in Thule"  #ip="192.168.1.155" #addr="25"


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

def queryVVM(cmd):
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
    print(ret)
    return ret

def sendVVM(cmd):
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))
    sockGPIB.send(bytes(cmd + "\n",'ascii'))

def set_device():
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


def check_vvm():
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

check_vvm()

# Take Measurements
sendVVM("DAN OFF")
sendVVM("SENSE AVOL")
sendVVM("FORM LIN")
time.sleep(0.5)
avol = queryVVM("MEAS? AVOL")
sendVVM("SENSE BVOL")
sendVVM("FORM LIN")
time.sleep(0.5)
bvol = queryVVM("MEAS? BVOL")
sendVVM("SENSE PHASE")
sendVVM("FORM POL")
time.sleep(0.5)
phase = queryVVM("MEAS? PHASE")
time.sleep(0.5)
BA = queryVVM("MEAS? BA")
sendVVM("DAN ON")
#sendVVM("SYST:KEY 2")

print('A volts: ',str(avol),' B Volts: ',str(bvol),' B-A Phase: ',str(phase), "BA: ", str(BA))
print("End")
