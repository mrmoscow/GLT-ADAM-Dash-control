#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
from datetime import datetime
#from PIL import Image

sys.path.append("../module")
#import ReceiverADAM as RAD
#import SpecAnalyzer as SA
import hp8508 as hp
import socket


ip="192.168.1.155"

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

def sendVVM(cmd):
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))
    sockGPIB.send(bytes(cmd + "\n",'ascii'))

def queryVVM(cmd):
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sockGPIB.settimeout(3.0)
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

def CheckError():
    sockGPIB = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sockGPIB.settimeout(1.0)
    sockGPIB.connect((ip, 1234))

    sockGPIB.send(b"SYST:ERR?\n")
    sockGPIB.send(b"++read eoi\n")

    s = None

    try:
        s = sockGPIB.recv(4096)
    except socket.timeout:
        s = ""

    if s[:1] != "0":
       print (s)


#ip="192.168.1.155"
hp.get_vvm_info(ip)
print("next is check_vvm")
check_vvm()


print("next is got AVOL.")
sendVVM("DAN OFF")
sendVVM("SENSE AVOL")
sendVVM("FORM LIN")
time.sleep(0.5)
avol = queryVVM("MEAS? AVOL")
print('A volts: ',str(avol))


print("End of the code")
