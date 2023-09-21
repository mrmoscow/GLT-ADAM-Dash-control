from os.path import exists
import sys
import socket
print(sys.version)
print(sys.version_info)
print(sys.version_info[1])
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient

coil_list={"S2":32,"S3":48,"S4":64,"S5":80}

adam_delay = 0.25


#co=ModbusClient('192.168.1.225',port=502,timeout=10)
#print("Link good",co)
#r = co.read_coils(14,5,unit=1)
#print("read coils good",r)
#intvalue=r.bits
#print(intvalue)


UDP_IP = "192.168.1.213"
UDP_PORT = 1025
MESSAGE = b"$016\r"

#print("UDP target IP: %s" %UDP_IP)
#print("UDP target port: %s" %UDP_PORT)
#print("message: %s" %MESSAGE)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

indata, addr = sock.recvfrom(1024)
print('recvfrom A44' + str(addr) + ': ' + indata.decode())
sock.close()


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.sendto( b"$016\r", ("192.168.1.215", 1025))

indata, addr = sock.recvfrom(1024)
print('recvfrom A45' + str(addr) + ': ' + indata.decode())

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

