#! /usr/bin/python3
#for 690 PM ADAM6017, (192.168.1.99)
import socket
import argparse
import re
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.settimeout(1)

#sock.sendto( b"$01BRC02\r", ('192.168.1.99', 1025))
#sock.sendto( b"#01\r", ('192.168.1.99', 1025))
#indata, addr = sock.recvfrom(1024)
#print(indata.decode())
#print(indata.decode().split('+'))
#print(re.split(r'[+-]',indata.decode()))

#sock.sendto( b"#010\r", ('192.168.1.99', 1025))
#sock.sendto( b"#011\r", ('192.168.1.99', 1025))
#indata, addr = sock.recvfrom(1024)
#print(indata.decode())

#sock.sendto( b"$012\r", ('192.168.1.99', 1025))
#indata, addr = sock.recvfrom(1024)
#print(indata.decode(),indata.decode()[0:3],indata.decode()[3])
#a=int(indata.decode()[3])
#the all result, fitst 3 to test o.k, [3]is the result
#[3]=0 or 2 tone off
#[3]=1 or 3 tone on

#sock.sendto( b"#01D00\r", ('192.168.1.99', 1025)) # DO 0 off
#sock.sendto( b"#01D01\r", ('192.168.1.99', 1025)) # DO 0 on
#sock.sendto( b"#01D11\r", ('192.168.1.99', 1025)) # DO 1 on
#sock.sendto( b"#01D01\r", ('192.168.1.99', 1025))
#indata, addr = sock.recvfrom(1024)
#print(indata.decode())

DOstale=['DO-0: Off,   DO-1: Off',
         'DO-0: ON ,   DO-1: Off',
         'DO-0: Off,   DO-1: On',
         'DO-0: On ,   DO-1: On']

def get6017DO():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"$012\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        a=int(indata.decode()[3])
        print("The DO of ADAM 6017 is  ",DOstale[a])
        return DOstale[a]
    except:
        return "Unknow"

def get6017AI():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        numbers = re.findall(r'-?\d+\.\d+', indata.decode())
        nu = [float(number) for number in numbers[0:-1]]
        #print(nu)
        print("The Analogy of ADAM6017:")
        print("Ch-0 ( V):",nu[0],"  Ch-1 (V):",nu[1],"  Ch-2 (V):",nu[2],"  Ch-3(mV):",nu[3])
        print("Ch-4 (mV):",nu[4],"  Ch-5 (mV):",nu[5],"  Ch-6 (mV):",nu[6],"  Ch-7(mV):",nu[7])
        return indata.decode()
    except:
        return None


def enable_6017_do0():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01D01\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        print("Tone on now with code",indata.decode())
        return indata.decode()
    except:
        return None

def disable_6017_do0():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01D00\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        print("Tone off now,with code:",indata.decode())
        return indata.decode()
    except:
        return None


parser = argparse.ArgumentParser(description="690PM Control Script")
parser.add_argument("command", choices=["r", "tone-in", "tone-off"], help="Command: 'r' for read AI, 'tone-in' to enable DO0, 'tone-off' to disable DO0")

args = parser.parse_args()

if args.command == "r":
    get6017DO()
    get6017AI()
elif args.command == "tone-in":
    enable_6017_do0()
elif args.command == "tone-off":
    disable_6017_do0()

