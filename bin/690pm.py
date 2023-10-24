#! /usr/bin/python3
#for 690 PM ADAM6017, (192.168.1.99)
import argparse
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD


def get6017DO(machine):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"$016\r", (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        keys = [k for k, v in A4x_nfun.items() if v[-3:-1] == indata.decode()[-3:-1]]
        #print(keys)
        if len(keys) == 1:
            return keys[0]
        else:
            return None
    except:
        return None

def get6017AI(machine):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"$01M\r", (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        print(indata.decode())

        sock.sendto( b"$01BRC01\r", (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        print(indata.decode())

        sock.sendto( b"#01\r", (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        print(indata.decode())

        sock.sendto( b"$012\r", (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        print(indata.decode())

        #b"#01D01\r"  
        #b"#01D00\r"

    except:
        return None


parser = argparse.ArgumentParser(description="")
parser.add_argument("-t", "--tone", type=str,help="off, on, for set the tone off or on")
parser.add_argument("-s", "--status", help="Readback the status including 8 AL  cahannel and 2DO channel",
                    action="store_true")

args = parser.parse_args()

if args.status:
    print(" will just show the status")
else:
    print(" will do tone change")

#if args.tone not in ['86','230','345','rx1','rx2','rx3','rx4','off','Rx1','Rx2','Rx3','Rx4']:
#    sys.exit("Error: The receiver should be in 86,230,300, or off")

print(args.tone)

#if 'Bad' in RAD.check_ADAM('690'): sys.exit("Error: 690PM is not conection")

