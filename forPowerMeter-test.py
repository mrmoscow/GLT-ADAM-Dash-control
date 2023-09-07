import socket

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
           "SA1":'192.168.1.221',\
           "ROT":'192.168.1.228',\
           "PM1":'192.168.1.202',\
           "PM2":'192.168.1.203',\
           "PM3":'192.168.1.218',\
           "PM4":'192.168.1.219'}

'''
Keysight Technologies,N1914A,MY57470013,A2.01.15
Keysight Technologies,N1914A,MY57460010,A2.01.15

-7.15793018E+001
 -7.54288645E+001

('-7.15793018E+001\n', '-7.54288645E+001\n')
Keysight Technologies,N1914A,MY57470013,A2.01.15

Agilent Technologies,N1914A,MY56410032,A2.01.12

-7.20515456E+001
 -7.32431239E+001

('-7.20515456E+001\n', '-7.32431239E+001\n')
'''

def get_Power(machine):
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ADAM_list[machine],5025))
        #data = "*IDN?\n"
        ##clientSocket.send(data.encode())
        #dataFromServer = clientSocket.recv(1024)
        #print(dataFromServer.decode())

        data = 'FETC1?\n'
        clientSocket.send(data.encode())
        dataFromServerA = clientSocket.recv(1024)

        data = 'FETC2?\n'
        clientSocket.send(data.encode())
        dataFromServerB = clientSocket.recv(1024)

        print(dataFromServerA.decode(),dataFromServerB.decode())
        return float(dataFromServerA.decode()),float(dataFromServerB.decode())
    except:
        print ("file to get power Meter")
        return 'Faill to get power'


print(get_Power('PM1'))
print(get_Power('PM4'))
