#! /usr/bin/python3
#for 690 PM ADAM6017, (192.168.1.99)
import socket
import argparse
import re
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD


IP_ADAM6017='192.168.1.99'
DOstale=['DO-0: Off,   DO-1: Off',
         'DO-0: ON ,   DO-1: Off',
         'DO-0: Off,   DO-1: On',
         'DO-0: On ,   DO-1: On']

def get6017DO():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"$012\r", (IP_ADAM6017, 1025))
        indata, addr = sock.recvfrom(1024)
        a=int(indata.decode()[3])
        print("The DO of ADAM 6017 is  ",DOstale[a])
        return DOstale[a]
    except:
        print("Can not check the DO of ADAM6017")
        return "Unknow"

def get6017AI():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01\r", (IP_ADAM6017, 1025))
        indata, addr = sock.recvfrom(1024)
        numbers = re.findall(r'-?\d+\.\d+', indata.decode())
        nu = [float(number) for number in numbers[0:-1]]
        #print(nu)
        print("The Analogy of ADAM6017:")
        print("Ch-0 ( V):",nu[0],"  Ch-1 (V):",nu[1],"  Ch-2 (V):",nu[2],"  Ch-3(mV):",nu[3])
        print("Ch-4 (mV):",nu[4],"  Ch-5 (mV):",nu[5],"  Ch-6 (mV):",nu[6],"  Ch-7(mV):",nu[7])
        return nu
    except:
        return ['Unknow']*8


def enable_6017_do0():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01D01\r", (IP_ADAM6017, 1025))
        indata, addr = sock.recvfrom(1024)
        print("Tone on now with code",indata.decode())
        return indata.decode()
    except:
        return None

def disable_6017_do0():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01D00\r", (IP_ADAM6017, 1025))
        indata, addr = sock.recvfrom(1024)
        print("Tone off now,with code:",indata.decode())
        return indata.decode()
    except:
        return None


parser = argparse.ArgumentParser(description="690PM Control Script")
parser.add_argument("command", choices=["r", "tone-in", "tone-out"], help="Command: 'r' for read AI, 'tone-in' to enable DO0, 'tone-out' to disable DO0")

args = parser.parse_args()

if args.command == "r":
    get6017DO()
    get6017AI()
elif args.command == "tone-in":
    enable_6017_do0()
elif args.command == "tone-out":
    disable_6017_do0()

