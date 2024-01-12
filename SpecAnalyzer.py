
import socket
import matplotlib.pyplot as plt
from datetime import datetime


def save_plot():
    now = datetime.now()
    d = now.strftime("%Y-%m-%d, %H:%M:%S")


    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('192.168.1.221',5025))
    data = "*IDN?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("From machine",dataFromServer.decode().rstrip(),"at 192.168.1.221")

    data = "SWE:POIN?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("How many sweep points",dataFromServer.decode().rstrip())

    #data = "FORM:TRAC:DATA?\n"
    #clientSocket.send(data.encode())
    #dataFromServer = clientSocket.recv(1024)
    #print(dataFromServer.decode().rstrip())

    #data = "SWE:TIME?\n"
    #clientSocket.send(data.encode())
    #dataFromServer = clientSocket.recv(1024)
    #print(dataFromServer.decode())

    data = "FREQ:CENT?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Frequency Center",dataFromServer.decode().rstrip())
    cff=float(dataFromServer.decode())

    data = "FREQ:SPAN?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("SPAN of Frequency",dataFromServer.decode().rstrip())
    spf=float(dataFromServer.decode())

    data = "BAND:VID?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Band VID",dataFromServer.decode().rstrip())


    data = "DISP:WIND:TRAC:Y:RLEV1?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Y RLEV",dataFromServer.decode().rstrip())
    rlf=float(dataFromServer.decode())

    data = "DISP:SEM:VIEW:WIND:TRAC:Y:PDIV?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Y DIV/dB",dataFromServer.decode().rstrip())
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


    power=[float(x) for x in dataall.split(",")]
    freq=[];stf=cff-spf/2.0;stpf=spf/len(power)
    for i in range(len(power)):
        freq.append((stf+(i)*stpf)/1E9)

    print("Info,Power",len(power),type(power),type(power[0]),power[-1])
    print("Info,Freq",len(freq),type(freq),type(freq[0]),freq[-1])
    print("The time now",d)
    #print(cff,spf,rlf,lgf)


    plt.plot(freq,power)
    plt.title("Spectrum \n"+d)
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
    #plt.text(0.5, 0.5, 'matplot time',
    #    horizontalalignment='center',
    #    verticalalignment='center')
    plt.text(0.02, 0.02, f"RBW {rbf:.2e}Hz", transform=plt.gca().transAxes)
    plt.text(0.83, 0.02, f"SPAN {spf:.2e}Hz", transform=plt.gca().transAxes)
    plt.text(0.2, 0.02, f"VBW {vbf:.2e}Hz", transform=plt.gca().transAxes)
    plt.text(0.8, 0.95, f"SWP {rlst:.2e}sec", transform=plt.gca().transAxes)
    plt.text(0.64, 0.02, f"CENT {cff:.2e}Hz", transform=plt.gca().transAxes)
    plt.text(0.02, 0.95, f"RL {rlf:.0f}dBm", transform=plt.gca().transAxes)
    plt.text(0.2, 0.95, f"Scale {lgf:.0f}dB/", transform=plt.gca().transAxes)
    plt.savefig('./assets/SA_plot.png')
    return None

if __name__ == "__main__":
    save_plot()
