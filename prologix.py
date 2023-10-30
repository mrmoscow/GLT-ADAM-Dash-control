
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

global ip, addr  #for vvm in Taipei Lab
ip="192.168.1.204"
addr="8"
#"192.168.1.155 : 25 for vvm in Thule"


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
    #print(res.decode())
    return ret

def sendVVM(cmd):
    sockGPIB.send(bytes(cmd + "\n"),'ascii')

def init_device():
    #global sockGPIB

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

    cmd = b"*CLS"
    sockGPIB.send(cmd + b"\n")
    time.sleep(1.0)
    CheckError()

    cmd = b"*IDN?"
    sockGPIB.send(cmd + b"\n")
    sockGPIB.send(b"++read eoi\n")
    time.sleep(1.0)
    try:
      s = sockGPIB.recv(4096)
    except socket.timeout:
      s = ""
    CheckError()

    cmd = b"*RST"
    sockGPIB.send(cmd + b"\n")
    time.sleep(1.0)
    CheckError()

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


print("start main")
sockGtest = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
sockGtest.settimeout(1.0)
print(ip)
sockGtest.connect((ip, 1234))
sockGtest.send(b"++mode\n")
time.sleep(1.0)
indata = sockGtest.recv(4096)
print(indata.decode())

sockGtest.send(b"++auto\n")
time.sleep(1.0)
indata = sockGtest.recv(4096)
print(indata.decode())

sockGtest.send(b"++addr\n")
time.sleep(1.0)
indata = sockGtest.recv(4096)
print(indata.decode())

#except:
#    print("in except")

print("End")
