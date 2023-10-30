#! /usr/bin/python3
#for 690 PM ADAM6017, (192.168.1.99)
import socket
import argparse
import re
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD

#sock.sendto( b"$01BRC02\r", ('192.168.1.99', 1025))
sock.sendto( b"#01\r", ('192.168.1.99', 1025))
indata, addr = sock.recvfrom(1024)
print(indata.decode())
print(indata.decode().split('+'))
print(re.split(r'[+-]',indata.decode()))

#sock.sendto( b"#010\r", ('192.168.1.99', 1025))
#sock.sendto( b"#011\r", ('192.168.1.99', 1025))
#indata, addr = sock.recvfrom(1024)
#print(indata.decode())

sock.sendto( b"$012\r", ('192.168.1.99', 1025))
indata, addr = sock.recvfrom(1024)
print(indata.decode(),indata.decode()[0:3],indata.decode()[3])
#the all result, fitst 3 to test o.k, [3]is the result
#[3]=0 or 2 tone off
#[3]=1 or 3 tone on

#sock.sendto( b"#01D00\r", ('192.168.1.99', 1025)) # DO 0 off
#sock.sendto( b"#01D01\r", ('192.168.1.99', 1025)) # DO 0 on
#sock.sendto( b"#01D11\r", ('192.168.1.99', 1025)) # DO 1 on
#sock.sendto( b"#01D01\r", ('192.168.1.99', 1025))
#indata, addr = sock.recvfrom(1024)
#print(indata.decode())


def get6017AI(machine):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        numbers = re.findall(r'-?\d+\.\d+', indata.decode())
        numbers = [float(number) for number in numbers[0:-1]]
        print(numbers)

        sock.sendto( b"#012\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        DOout=indata.decode()[3]
        return indata.decode()
    except:
        return None

def enable_6017_do0():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01D01\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        print(indata.decode())
        return indata.decode()
    except:
        return None

def disable_6017_do0():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"#01D00\r", ('192.168.1.99', 1025))
        indata, addr = sock.recvfrom(1024)
        print(indata.decode())
        return indata.decode()
    except:
        return None


parser = argparse.ArgumentParser(description="690PM Control Script")
parser.add_argument("command", choices=["r", "tone-in", "tone-out"], help="Command: 'r' for read AI, 'tone-in' to enable DO0, 'tone-out' to disable DO0")

args = parser.parse_args()

if args.command == "r":
    read_ai_values()
elif args.command == "tone-in":
    enable_do0()
elif args.command == "tone-out":
    disable_do0()

