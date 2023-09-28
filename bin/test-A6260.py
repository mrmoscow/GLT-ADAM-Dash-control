from os.path import exists
import sys
import socket
#print(sys.version)
#print(sys.version_info)
#print(sys.version_info[1])
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient

coil_list={"S2":32,"S3":48,"S4":64,"S5":80}

adam_delay = 0.25

ADAM_list={"A01":'192.168.1.207',\
           "A03":'192.168.1.201',\
           "A10":'192.168.1.217',\
           "A11":'192.168.1.206',\
           "A14":'192.168.1.208',\
           "A17":'192.168.1.223',\
           "A44_volt":'192.168.1.212',\
           "A44_ReSl":'192.168.1.213',\
           "A45_volt":'192.168.1.214',\
           "A45_ReSl":'192.168.1.215',\
           "ATT":'192.168.1.225',\
           "SA1":'192.168.1.221',\
           "ROT":'192.168.1.228',\
           "PM1":'192.168.1.202',\
           "PM2":'192.168.1.203',\
           "PM3":'192.168.1.218',\
           "PM4":'192.168.1.219'}


A4x_nfun = {1: "#010004\r", 2: "#010008\r",3: "#010010\r", 4: "#010020\r",0: "#010000\r"}

def setN_6260(machine,Rxnumber):
    MESSAGE = A4x_nfun[Rxnumber]
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto(  MESSAGE.encode(), (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        #print('recvfrom' + str(addr) + ': ' + indata.decode())

        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
        sock.sendto( b"$016\r", (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        print('recvfrom Testing' + str(addr) + ': ' + indata.decode())
        sock.close()
        if MESSAGE[-3:-1] == indata.decode()[-3:-1]:
            return 'Setting Succeful'
        else:
            return 'Error 03'
    except:
        return 'Error 03'


def getN_6260(machine,b=4):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto( b"$016\r", (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
        a=[int(d) for d in str(bin(int(indata.decode()[-3:-1], 16))[2:].zfill(6))]
        a.reverse()
        return a[-b:]
    except :
        return ['Error 03']*b

print(getN_6260("A44_ReSl",6))
#print(getN_6260Rx("A44_ReSl"))

#print(getN_6260("A45_ReSl",6))
#print(getN_6260Rx("A45_ReSl"))

#print(setN_6260("A44_ReSl",2))
#print(setN_6260("A45_ReSl",2))
print(getN_6260("ATT",6))
#print(getN_6260Rx("ATT"))

'''
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

indata, addr = sock.recvfrom(1024)
print('recvfrom A44' + str(addr) + ': ' + indata.decode())
sock.close()

'''
#sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
#sock.sendto( b"$016\r", ("192.168.1.215", 1025))

#indata, addr = sock.recvfrom(1024)
#print('recvfrom A45' + str(addr) + ': ' + indata.decode())

A4x_bits = {1:[1,0,0,0], 2:[0,1,0,0],3: [0,0,1,0], 4:[0,0,0,1]}
A4x_nfun = {1: "#010004\r", 2: "#010008\r",3: "#010010\r", 4: "#010020\r",0: "#010000\r"}

#rxIO_A4x=A4x_bits[1]
MESSAGE = A4x_nfun[4]
#print("message: %s" %MESSAGE)

#sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
#sock.sendto( MESSAGE.encode(), ("192.168.1.225", 1025))

#indata, addr = sock.recvfrom(1024)
#print('recvfrom Testing' + str(addr) + ': ' + indata.decode())
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.settimeout(1)

try:
    sock.sendto( b"$016\r", ("192.168.1.223", 1025))
    indata, addr = sock.recvfrom(1024)
    print('recvfrom Testing' + str(addr) + ': ' + indata.decode())
    print(indata.decode()[-3:-1])
except socket.timeout:
    print("Time out")

#a=[int(d) for d in str(bin(int(indata.decode()[-3:-1], 16))[2:].zfill(6))]
#a.reverse()
#print(a)
#print(a[-4:])
#keys = [k for k, v in A4x_nfun.items() if v[-3:-1] == indata.decode()[-3:-1]]
#print(keys,len(keys))
#if len(keys) ==1 :
#    print(keys[0])

#keys = [k for k, v in A4x_nfun.items() if v[:-2] == indata.decode()]
#print(keys)
#b"#010000\r"
#b"#010001\r" , 2,4,8,
#b"#010020\r"
#MESSAGE = b"#010020\r"
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

#indata, addr = sock.recvfrom(1024)
#print('recvfrom ' + str(addr) + ': ' + indata.decode())


#MESSAGE = b"$016\r"
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

#indata, addr = sock.recvfrom(1024)
#print('recvfrom ' + str(addr) + ': ' + indata.decode())
