
import socket
import matplotlib.pyplot as plt
from datetime import datetime
import math

# set_SA() at RAD

def autotune():
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect(('192.168.1.221',5025))
        #data = "*IDN?\n"
        #clientSocket.send(data.encode())
        #dataFromServer = clientSocket.recv(1024)
        #print(dataFromServer.decode().rstrip())
        data = "FREQ:TUNE:IMM\n"
        clientSocket.send(data.encode())
        data ="*OPC?\n"
        clientSocket.send(data.encode())
        dataFromServer = clientSocket.recv(1024)
        #print(dataFromServer.decode().rstrip())
        if dataFromServer.decode().rstrip() == "1":
            print( 'SA(192.168.1.221) Auto_Tune Successful')
        return 'AutoTune Succeful'

    except:
        print('Error 01')
        return 'Error 01'
    finally:
        clientSocket.close()


def set_p_SA(para,value):
    """
    para:
        cf -> FREQ:CENT
        sp -> FREQ:SPAN
        rl -> DISP:WIND:TRAC:Y:RLEV
        lg -> DISP:SEM:VIEW:WIND:TRAC:Y:PDIV
        rb -> BAND
        vb -> BAND:VID
    value, Hz (cf, sp, rb,vb), dBm(rl), or dB(lg)
    """
    SA_IP = "192.168.1.221"
    SA_PORT = 5025

    para_map = {
        "cf": "FREQ:CENT {:.0f} Hz\n",
        "sp": "FREQ:SPAN {:.0f} Hz\n",
        "rl": "DISP:WIND:TRAC:Y:RLEV {:.0f} dBm\n",
        "lg": "DISP:SEM:VIEW:WIND:TRAC:Y:PDIV {:.0f} dB\n",
        "rb": "BAND {:.0f} Hz\n",
        "vb": "BAND:VID {:.0f} Hz\n",
    }
    if para not in para_map:
        return f"Error: unknown parameter '{para}'"

    cmd = para_map[para].format(value)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            clientSocket.connect((SA_IP, SA_PORT))

            # send setting command
            clientSocket.sendall(cmd.encode())
            print("Send:", cmd.rstrip())

        return "Setting Successful"

    except Exception as e:
        print("Error:", e)
        return f"Error: {e}"


def format_freq(x_hz: float,
                max_decimals: int = 9,
                sig: int = 12,
                prefer: 'str | None' = None) -> str:
    """
    Format a frequency value (in Hz) into a human-friendly string like:
    - 100GHz
    - 10MHz
    - 20.1232203GHz

    Parameters
    ----------
    x_hz : float
        Frequency in Hz.
    max_decimals : int
        Maximum number of decimal places to show.
    sig : int
        Reserved for controlling rounding / floating-point noise (currently unused).
    prefer : str | None
        Force a specific unit: 'Hz', 'kHz', 'MHz', or 'GHz'.
        If None, the function automatically selects a suitable unit.

    Returns
    -------
    str
        Formatted frequency string with unit.
    """
    # Handle None, NaN, or infinite values safely
    if x_hz is None or not math.isfinite(x_hz):
        return "NaN"

    # Supported units and their scale factors relative to Hz
    units = [("Hz", 1.0), ("kHz", 1e3), ("MHz", 1e6), ("GHz", 1e9)]
    unit_map = {u: s for u, s in units}

    # Choose the unit:
    # - if 'prefer' is given, force that unit
    # - otherwise, automatically pick based on magnitude
    if prefer is not None:
        scale = unit_map[prefer]
        unit = prefer
    else:
        ax = abs(x_hz)
        if ax >= 1e9:
            unit, scale = "GHz", 1e9
        elif ax >= 1e6:
            unit, scale = "MHz", 1e6
        elif ax >= 1e3:
            unit, scale = "kHz", 1e3
        else:
            unit, scale = "Hz", 1.0

    # Convert to the chosen unit
    v = x_hz / scale

    # Round first to reduce floating-point artifacts like 19.9999999997
    v = round(v, max_decimals)

    # If the value is effectively an integer, show no decimals.
    # Otherwise, show up to max_decimals and trim trailing zeros.
    if abs(v - round(v)) < 10**(-(max_decimals - 1)):
        s = f"{int(round(v))}"
    else:
        s = f"{v:.{max_decimals}f}".rstrip("0").rstrip(".")

    # Return concatenated value + unit (e.g., "20.123GHz")
    return f"{s}{unit}"


def save_plot(pngfile='./assets/SA_plot.png', plt_title="Spectrum", ch=0):
    now = datetime.now()
    d = now.strftime("%Y-%m-%d, %H:%M:%S")

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('192.168.1.221',5025))
    data = "*IDN?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    #print("From machine",dataFromServer.decode().rstrip(),"at 192.168.1.221")

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
    #next for ch44.
    mkforA=pkhif*4.0+0.0315*1E9
    mkforB=mkforA*3.0

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

    #plt.text(0.75, 0.06, f"CENT {cff:.2e}Hz", transform=plt.gca().transAxes)
    plt.text(0.75, 0.06, f"CENT {format_freq(cff,  max_decimals=4)}",
        transform=plt.gca().transAxes)
    #plt.text(0.75, 0.01, f"SPAN {spf:.2e}Hz", transform=plt.gca().transAxes)
    plt.text(0.75, 0.01, f"SPAN {format_freq(spf,  max_decimals=4)}", 
        transform=plt.gca().transAxes)

    plt.text(0.71, 0.95, f"Peak:{pkhia:.1f} dBm", transform=plt.gca().transAxes)
    #plt.text(0.71, 0.90, f"Peak:{pkhif:.3e} Hz", transform=plt.gca().transAxes)
    plt.text(0.71, 0.90, f"Peak: {format_freq(pkhif, max_decimals=6)}", 
        transform=plt.gca().transAxes)
   
    #plt.text(0.01, 0.06, f"RBW {rbf:.1e}Hz", transform=plt.gca().transAxes)
    #plt.text(0.01, 0.01, f"VBW {vbf:.1e}Hz", transform=plt.gca().transAxes)
    plt.text(0.01, 0.06, f"RBW {format_freq(rbf, max_decimals=2)}", 
             transform=plt.gca().transAxes)
    plt.text(0.01, 0.01, f"VBW {format_freq(vbf, max_decimals=2)}",
             transform=plt.gca().transAxes)
    plt.text(0.21, 0.95, f"Ref:{rlf:.0f}dBm", transform=plt.gca().transAxes)
    plt.text(0.01, 0.95, f"{lgf:.0f}dB/Div", transform=plt.gca().transAxes)

    #for ch44
    if ch ==44:
        plt.gca().tick_params(axis='x', labelbottom=False)
        #plt.text(0.8, 0.85, f"{format_freq(mkforA, max_decimals=4)}",
        #     transform=plt.gca().transAxes)
        #plt.text(0.8, 0.80, f"{format_freq(mkforB, max_decimals=4)}",
        #     transform=plt.gca().transAxes)

        plt.text(0.01, 0.16,
        "Mkr freq convert to " + r"$\mathbf{" + f"{format_freq(mkforA, max_decimals=4)}" + r"}$"
        + " for Rx86_above FLOOG",
        transform=plt.gca().transAxes
        )

        plt.text(0.01, 0.11,
        "Mkr freq convert to " + r"$\mathbf{" + f"{format_freq(mkforB, max_decimals=4)}" + r"}$"
        + " for Rx230/345_above FLOOG",
        transform=plt.gca().transAxes
        )
        #plt.text(0.01, 0.16, f"Mkr freq to {format_freq(mkforA, max_decimals=4)} for Rx86_above FLOOG",
        #     transform=plt.gca().transAxes)
        #plt.text(0.01, 0.11, f"Mkr freq to {format_freq(mkforB, max_decimals=4)} for Rx230/345_above FLOOG",
        #     transform=plt.gca().transAxes)

    plt.savefig(pngfile)
    plt.close()
    return None

if __name__ == "__main__":
    #save_plot('./assets/T2.png')
    save_plot()
