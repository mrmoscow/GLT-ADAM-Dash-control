from os.path import exists
import sys
import socket
sys.path.append("..")
import ReceiverADAM as RAD


if 'Bad' in RAD.check_ADAM('A44_ReSl'): sys.exit("Error A44 is not conection")
print(RAD.get_6260('A44_ReSl',6))

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

