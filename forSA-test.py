
import socket
import matplotlib.pyplot as plt


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('192.168.1.221',5025))
data = "*IDN?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode().rstrip())

data = "SWE:POIN?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode().rstrip())

data = "FORM:TRAC:DATA?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode().rstrip())

#data = "SWE:TIME?\n"
#clientSocket.send(data.encode())
#dataFromServer = clientSocket.recv(1024)
#print(dataFromServer.decode())

data = "FREQ:CENT?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print(dataFromServer.decode())
cff=float(dataFromServer.decode())

data = "FREQ:SPAN?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print("SPAN of Frequency",dataFromServer.decode())
spf=float(dataFromServer.decode())

data = "BAND:VID?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print("Band VID",dataFromServer.decode())


data = "DISP:WIND:TRAC:Y:RLEV1?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print("Y RLEV",dataFromServer.decode())
rlf=float(dataFromServer.decode())

data = "DISP:SEM:VIEW:WIND:TRAC:Y:PDIV?\n"
clientSocket.send(data.encode())
dataFromServer = clientSocket.recv(1024)
print("Y DIV/dB",dataFromServer.decode())
lgf=float(dataFromServer.decode())


data = "TRAC? TRACE1\n"
clientSocket.send(data.encode())
dataall=""
while True:
    dataFromServer = clientSocket.recv(2048)
    dataall=dataall+dataFromServer.decode()
    #print(dataall[-1])
    if "\n" in dataFromServer.decode():
        break
#print(dataall)


power=[float(x) for x in dataall.split(",")]

freq=[];stf=cff-spf/2.0;stpf=spf/len(power)
for i in range(len(power)):
    freq.append((stf+(i)*stpf)/1E9)

print("Info,Power",len(power),type(power),type(power[0]),power[-1])
print("Info,Freq",len(freq),type(freq),type(freq[0]),freq[-1])
#print(freq)
print(cff,spf,rlf,lgf)


#dataFromServer = clientSocket.recv(2048)
#print(dataFromServer.decode())


plt.plot(freq,power)
plt.title("Spectrum")
plt.xlabel("Frequency (GHz)")
plt.ylabel("Power(dBm)")
plt.grid(True)
plt.xlim((cff-spf/2.0)/1.0e9,(cff+spf/2.0)/1.0e9)
plt.ylim(rlf-lgf*10.0, rlf)
plt.yticks(range(int(rlf-lgf*10.0),int(rlf+lgf),int(lgf)))
t = ("RBW: , VBW"
     "SPAN,CENF,"
     "off the top or bottom!")
#plt.text(4, 1, t, ha='left')
plt.text(0.5, 0.5, 'matplot time',
     horizontalalignment='center',
     verticalalignment='center')

plt.savefig('./assets/SA_image.png')
#plt.show()
