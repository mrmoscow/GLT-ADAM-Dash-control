
import socket
import matplotlib.pyplot as plt
from datetime import datetime


def save_plot(pngfile='./assets/SA_plot.png',plt_title="Spectrum"):
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
    #print("How many sweep points",dataFromServer.decode().rstrip())

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

    data = "BAND?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Band Frequency, RBW",dataFromServer.decode().rstrip())
    rbf=float(dataFromServer.decode())

    data = "BAND:VID?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Band VID Frequency, VBW",dataFromServer.decode().rstrip())
    vbf=float(dataFromServer.decode())

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

    #make the paak position. no result message. 
    data = "CALC:MARK1:MAX\n"
    clientSocket.send(data.encode())

    data = "CALC:MARK1:Y?\n\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Peak Power",dataFromServer.decode().rstrip())
    pkhia=float(dataFromServer.decode())

    data = "CALC:MARK1:X?\n\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print("Peak Frequency",dataFromServer.decode().rstrip())
    pkhif=float(dataFromServer.decode())

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
    if int(spf) == 200:
        xlabel="Frequency (Hz)"
        xstep=1.0
        for i in range(len(power)):
            freq.append((stf+(i)*stpf))

    else:
        xlabel="Frequency (GHz)"
        xstep=1.0e9
        for i in range(len(power)):
            freq.append((stf+(i)*stpf)/1E9)

    #print("Info,Power",len(power),type(power),type(power[0]),power[-1])
    #print("Info,Freq",len(freq),type(freq),type(freq[0]),freq[-1])
    #print("The time now",d)

    plt.plot(freq,power)
    plt.title(plt_title+"\n"+d)
    plt.xlabel(xlabel)
    plt.ylabel("Power(dBm)")
    plt.grid(True)
    plt.xlim((cff-spf/2.0)/xstep,(cff+spf/2.0)/xstep)
    plt.ylim(rlf-lgf*10.0, rlf)
    plt.yticks(range(int(rlf-lgf*10.0),int(rlf+lgf),int(lgf)))
    #
    #
    plt.text(0.75, 0.06, f"CENT {cff:.2e}Hz", transform=plt.gca().transAxes)
    plt.text(0.75, 0.01, f"SPAN {spf:.2e}Hz", transform=plt.gca().transAxes)

    plt.text(0.71, 0.95, f"Peak:{pkhia:.1f} dBm", transform=plt.gca().transAxes)
    plt.text(0.71, 0.90, f"Peak:{pkhif:.3e} Hz", transform=plt.gca().transAxes)

    plt.text(0.01, 0.06, f"RBW {rbf:.1e}Hz", transform=plt.gca().transAxes)
    plt.text(0.01, 0.01, f"VBW {vbf:.1e}Hz", transform=plt.gca().transAxes)
    plt.text(0.21, 0.95, f"Ref:{rlf:.0f}dBm", transform=plt.gca().transAxes)
    plt.text(0.01, 0.95, f"{lgf:.0f}dB/Div", transform=plt.gca().transAxes)

    #plt.savefig('./assets/SA_plot.png')
    plt.savefig(pngfile)
    plt.close()
    return None

if __name__ == "__main__":
    #save_plot('./assets/T2.png')
    save_plot()
