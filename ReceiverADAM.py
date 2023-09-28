import dash
from dash import html, dcc, callback, Input, Output
#from dash.exceptions import PreventUpdate

import socket
import time
from datetime import datetime
import requests

import sys
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient


#Next list the name and IP at GLT telescope
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

#Next list the 5056 card at which slite and the first coil position.
coil_list={"S2":32,"S3":48,"S4":64,"S5":80}

adam_delay = 0.25


#A1 = ModbusClient('192.168.1.207',port=502,timeout=10)

#[Error 01] '{ *** Connection Failure *** }'
#[Error 02] '{ *** Reading Failure *** }'
#[Error 03] 'AO/DO, Setting unsuccful '
#[Error 04] '{Not match the  Digital output format }'
#[Error 05] 'Digital output unfucceful'
#[Error 12] 'DO setting input formate issue: not 4 digital'
#[Error 13] 'DO setting input formate issue: not hex number'
#[Error 14] 'DO setting input formate issue: not only 1/0 '
#[Error 15] 'DO setting input issue: checking input value'
#[Error ##] 'Still need the definite'

def list_ADAMs():
    print ("Next is the ADAD in List")
    for i,j in ADAM_list.items():
        print (i,j)
    print ("---End of the List ---")
    return


def check_ADAMs():
    print ("Start to connect ADAMs")
    for i,j in ADAM_list.items():
        k= ModbusClient(j, port=502, timeout=10)
        if k.connect():
            print (i,j,"Good connection!")
        else:
            print (i,j,"*** Connection Failure ***")
    print ("--- End of connect ---")

def test_ADAMs():
    print ("Start to connect ADAMs")
    res=[]
    for i,j in ADAM_list.items():
        k= ModbusClient(j, port=502, timeout=10)
        if k.connect():
            print (i,j,"Good connection!")
            res.append(i+' ---> '+'Good connection!')
            res.append(html.Br())
            #res.append(Html.Br())
        else:
            print (i,j,"*** Connection Failure ***")
            res.append(i+' ---> '+'**Bad connection!')
            res.append(html.Br())
    print ("--- End of connect ---")
    res.append(html.Br())
    format_data = "%Y/%m/%d, %H:%M:%S,"
    res.append("Last update:"+datetime.now().strftime(format_data))
    return res


def check_ADAM(machine):
    message=''
    print  ("checking",machine,":",ADAM_list[machine])
    k=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    #k= ModbusClient(j, port=502, timeout=10)
    if k.connect():
        print (machine,":",ADAM_list[machine],"Good connection!")
        message +=machine+":"+ADAM_list[machine]+"  "+"Good connection!\n"
    else:
        print (machine,":",ADAM_list[machine],"*** Connection Failure ***")
        message +=machine+":"+ADAM_list[machine]+"  "+"**Bad connection!\n"
    time.sleep(0.5)
    return message


def hex_to_BiList(datain):
    if type(datain) is not list:
        if len(datain) != 4:
            return 'Error 12'
        try:
            b=list(format(int(datain,16),'b').zfill(16))
            res = [i== "1" for i in b]
        except ValueError:
            return 'Error 13'
    elif isinstance(datain[0], str):
        res = [i== "1" or i=="H" or i=="T" for i in datain]
    elif isinstance(datain[0], (int,float)):
        if all(i ==0 or i==1 for i in datain):
            res=[int(i) for i in datain]
        else:
            return 'Error 14'
    elif isinstance(datain[0],bool):
        res=datain
    else:
        return 'Error 15'
    return res

def set_6260(machine,data):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    try:
        print(co.write_coils(18, data,unit=1,slave=1))
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        return 'Setting Succeful'
    except:
        co.close()
        return 'Error 03'

def get_6260(machine,b=4):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        #return 'Error 01'
        return ['Error 01']*b
    try:
        r = co.read_coils(18,4,unit=1,slave=1)
        intvalue=r.bits
        b0=''.join(["0, " if i==0 else "1, " for i in intvalue])
        b1=["0" if i==0 else "1" for i in res]
        return b1
    except:
        co.close()
        return ['Error 02']*b


A4x_nfun = {1: "#010004\r", 2: "#010008\r",3: "#010010\r", 4: "#010020\r",0: "#010000\r"}

def setN_6260(machine,Rxnumber):
    MESSAGE = A4x_nfun[Rxnumber]
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.settimeout(1)
    try:
        sock.sendto(  MESSAGE.encode(), (ADAM_list[machine], 1025))
        indata, addr = sock.recvfrom(1024)
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
    except:
        return ['Error 03']*b

def getN_6260Rx(machine):
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


def set_6224(machine,channel,v):
    b=1
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*b
    try:
        print(co.write_register(channel,int(v/10.0*4095),unit=1,slave=1))
        time.sleep(adam_delay)
        return ['Setting Succeful']*b
    except:
        co.close()
        return ['Error 03']*b


def get_6224(machine,b =4):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*b
    try:
        r = co.read_holding_registers(0,4,unit=1,slave=1)
        intvalue=r.registers
        volts=[round(float(x)/4095.0*10.0,3) for x in intvalue]
        return volts[0:b]
    except:
        co.close()
        return ['Error 02']*b


def set_5056(machine,data,card_at='S3'):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return 'Error 01'
    data2=hex_to_BiList(data)
    print('Setting',machine,data,data2)
    if type(data2) is not list:
        return data2
    try:
        print(co.write_coils(coil_list[card_at], data2,unit=1,slave=1))
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        return 'Setting Succeful'
    except:
        co.close()
        return 'Error 03'


#5050 is DO.
def get_5056(machine,card_at='S3'):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return 'Error 01'
    try:
        r = co.read_coils(coil_list[card_at],16,unit=1,slave=1)
        intvalue=r.bits
        b0=''.join(["0, " if i==0 else "1, " for i in intvalue])
        return b0
    except:
        co.close()
        return 'Error 02'


def set_5024(machine,channel,v):
    b=1
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*b
    try:
        print(co.write_register(channel+16,int(v/10.0*4095),unit=1,slave=1))
        time.sleep(adam_delay)
        return ['Setting Succeful']*b
    except:
        co.close()
        return ['Error 03']*b

#5024 in A01-16/A11-16
def get_5024(machine,b = 4):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*b
    try:
        r = co.read_holding_registers(16,4,unit=1,slave=1)
        intvalue=r.registers
        volts=[round(float(x)/4095.0*10.0,3) for x in intvalue]
        return volts[0:b]
    except:
        co.close()
        return ['Error 02']*b

#5018 in A01-08/A11-08/A14-08/A17-08
def get_5018(machine,b = 7):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*b
    try:
        r = co.read_holding_registers(8,7,unit=1,slave=1)
        intvalue=r.registers
        Temps = [round(float(x)/65535.0*760.0,1) for x in intvalue]
        return Temps[0:b]
    except:
        co.close()
        return ['Error 02']*b

#5017 in A01-00/A11-00/A14-00/A17-00
def get_5017(machine,b = 8):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*b
    try:
        r = co.read_holding_registers(0,8,unit=1,slave=1)
        intvalue=r.registers
        volts=[round(float(x)/65535.0*20-10.0,3) for x in intvalue]
        return volts[0:b]
    except:
        co.close()
        return ['Error 02']*b

### 6050 in A03-00/A10-00
def set_6050(machine,data):
    # data is  [0,0,0,0,0,0], 6 list of 
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return 'Error 01'
    try:
        print(co.write_coils(16, data,unit=1,slave=1))
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        return 'Setting Succeful'
    except:
        co.close()
        return 'Error 03'

### 6050 in A03-00/A10-00
def get_6050(machine,b=18):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*18
    try:
        r = co.read_coils(0,12,unit=1,slave=1)
        res=r.bits[0:12]
        r2 = co.read_coils(16,6,unit=1,slave=1)
        res.extend(r2.bits[0:6])
        br=["0" if i==0 else "1" for i in res]
        print(br)
        return br
    except:
        co.close()
        return ['Error 02']*18


A4x_bits = {1:[1,0,0,0], 2:[0,1,0,0],3: [0,0,1,0], 4:[0,0,0,1]}
rx_bits = {1:[True, False, False, False], 2:[False, True, False, False],
    3: [False, False, True, False], 4:[False, False, False, True]}
# TureTable for A01- Receiver select
A01_hex = {1:'FC80', 2:'5400', 3: 'A800', 4:'0000'}
A01_hex_tone ={1:'FF80', 2:'5500', 3: 'AA00', 4:'0000'}

def set_Rx(rx_number,tone):
    if tone == 'On':
        rxIO_A01=A01_hex_tone[rx_number]
    else:
        rxIO_A01=A01_hex[rx_number]
    rxIO_A4x=A4x_bits[rx_number]
    # for module checking.
    #add A11 for tsys power meter switch.
    if 'Bad' in check_ADAM('A01'): return "Not Success: A01 Error-01"
    if 'Bad' in check_ADAM('A03'): return "Not Success: A03 Error-01"
    if 'Bad' in check_ADAM('A44_ReSl'): return "Not Success: A44r Error-01"
    if 'Bad' in check_ADAM('A45_ReSl'): return "Not Success: A45r Error-01"
    try:
        set_6050('A03',[0,0,0,0,0,0])
        time.sleep(0.5)
        r1=set_5056('A01','0000')
        time.sleep(0.5)
        r2=set_5056('A01',rxIO_A01)
        #set_6260('A44_ReSl',rxIO_A4x)
        #set_6260('A45_ReSl',rxIO_A4x)
        setN_6260('A44_ReSl',rx_number)
        setN_6260('A45_ReSl',rx_number)
        #res="The Rx is now at"+tone
        #print(r1)
        return 'The Rx is now at Rx_'+str(rx_number)+' with tone '+tone
    except:
        return "Error 09: not running into try zone in set_Rx."

def set_SA(machine,centFreq,span,refLevel,scale,rbw,vbw):
    print (machine,centFreq,span,refLevel,scale,rbw,vbw)
    print (ADAM_list[machine])
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ADAM_list[machine],5025))
    data = "*IDN?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print(dataFromServer.decode())
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ADAM_list[machine],5025))
        data = "*IDN?\n"
        clientSocket.send(data.encode())
        dataFromServer = clientSocket.recv(1024)
        print(dataFromServer.decode())

        data = 'FREQ:CENT'+" {:.0f} ".format(centFreq) +'Hz\n'
        print(data)
        clientSocket.send(data.encode())

        data = "FREQ:SPAN {:.0f} Hz\n".format(span)
        print(data)
        clientSocket.send(data.encode())

        data = "DISP:WIND:TRAC:Y:RLEV {:.0f} dBm\n".format(refLevel)
        print(data)
        clientSocket.send(data.encode())

        data= "DISP:SEM:VIEW:WIND:TRAC:Y:PDIV {:.0f} dB\n".format(scale)
        print(data)
        clientSocket.send(data.encode())

        data= "BAND {:.0f} Hz\n".format(rbw)
        print(data)
        clientSocket.send(data.encode())

        data= "BAND:VID {:.0f} Hz\n".format(vbw)
        print(data)
        clientSocket.send(data.encode())
        return 'Setting Succeful'
    except:
        print('Error 01')
        return 'Error 01'


def getSApng():
    url = "http://192.168.1.221/Agilent.SA.WebInstrument/Screen.png"
    try:
        response = requests.get(url)
        with open("./assets/SA_image.png", "wb") as f:
            f.write(response.content)
        return 'Reflash SA PNG file succesfule'
    except:
        return 'Reflash SA PNG file failed'

#The SAPar:[Center Frequency(Hz),SPAN(Hz),Reference Lavel (dBm),Scale(dB/div),RBW(Hz),VBW(Hz)]
channelOpt =[
 {'label':'EHT1_POL0 IF 4-9 GHz',    'value':1,  'gr':'P1A',   'SAPar':[8E9,1E10,-40,5,3E6,300]},
 {'label':'EHT1_POL0 BB 6-8 GHz',    'value':2,  'gr':'P1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL0 BB 4-6 GHz',    'value':3,  'gr':'P1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL1 BB 4-6 GHz',    'value':4,  'gr':'P1A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT1_POL1 IF 4-9 GHz',    'value':5,  'gr':'P1B',   'SAPar':[8E9,1E10,-40,5, 3E6,300]},
 {'label':'EHT1_POL1 BB 6-8 GHz',    'value':6,  'gr':'P1B',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'10Mhz-Left rack',         'value':7,  'gr':'P1B',   'SAPar':[1E7,200,10,10, 1,1]},
 {'label':'100MHz',                  'value':8,  'gr':'P1B',   'SAPar':[1E8,200,10,10, 1,1]},
 {'label':'ContDet Input LHC 4-8GHz','value':9,  'gr':'P2A',   'SAPar':[6E9,8E9,-60,2, 3E6,300]},
 {'label':'ContDet Input RHC 4-8GHz','value':10, 'gr':'P2A',   'SAPar':[6E9,8E9,-60,2, 3E6,300]},
 {'label':'VVM Input (Rx) 50 MHz',   'value':11, 'gr':'P2A',   'SAPar':[5E7,200,-40,10, 1,1]},
 {'label':'VVM Input (Ref) 50 MHz',  'value':12, 'gr':'P2A',   'SAPar':[5E7,200,0,10, 1,1]},
 {'label':'5.95 GHz',                'value':13, 'gr':'P2B',   'SAPar':[5.9E9,200,0,10, 1,1]},
 {'label':'0.5 or 1.5 GHz',          'value':14, 'gr':'P2B',   'SAPar':[1E9,1.6E9,0,10, 3E6,300]},
 {'label':'31.5 MHz',                'value':15, 'gr':'P2B',   'SAPar':[3.15E7,200,-50,10, 1, 1]},
 {'label':'44.5 or 18.5MHz',         'value':16, 'gr':'P2B',   'SAPar':[31.5E6,50E6,-40,10, 1,1]},
 {'label':'NotAssigned',             'value':17, 'gr':'S17',   'SAPar':[4.0E9,1.0E9,0,10, 10E4,1E5]},
 {'label':'NotAssigned',             'value':18, 'gr':'S18',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'EHT1_LO_6GHz',            'value':19, 'gr':'S19',   'SAPar':[6E9,200,10,10, 1,1]},
 {'label':'EHT1_LO_7GHz',            'value':20, 'gr':'S20',   'SAPar':[7E9,200,10,10, 1,1]},
 {'label':'NotAssigned',             'value':21, 'gr':'S21',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Ref1+Ref3 (Test)',        'value':22, 'gr':'S22',   'SAPar':[27E9,20E9,20,10, 3E6,300]},
 {'label':'EHT2_POL0 IF 4-9',        'value':23, 'gr':'P3A',   'SAPar':[8E9,1E10,-40,5,3E6,300]},
 {'label':'EHT2_POL0 BB 6-8 GHz',    'value':24, 'gr':'P3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL0 BB 4-6 GHz',    'value':25, 'gr':'P3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL1 BB 4-6 GHz',    'value':26, 'gr':'P3A',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'EHT2_POL1 IF 4-9 GHz',    'value':27, 'gr':'P3B',   'SAPar':[8E9,1E10,-40,5, 3E6,300]},
 {'label':'EHT2_POL1 BB 6-8 GHz',    'value':28, 'gr':'P3B',   'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
 {'label':'3.85 GHz',                'value':29, 'gr':'P3B',   'SAPar':[3.85E9,200,10,10, 1,1]},
 {'label':'8.15 GHz',                'value':30, 'gr':'P3B',   'SAPar':[8.15E9,200,10,10, 1,1]},
 {'label':'2.048 GHz',               'value':31, 'gr':'P4A',   'SAPar':[2.048E9,200,10,10, 1,1]},
 {'label':'NotAsssigned',            'value':32, 'gr':'P4A',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'EHT2 LO (6GHz)',          'value':33, 'gr':'P4A',   'SAPar':[6E9,200,10,10, 1,1]},
 {'label':'EHT2 LO (7GHz)',          'value':34, 'gr':'P4A',   'SAPar':[7E9,200,10,10, 1,1]},
 {'label':'NotAssigned',             'value':35, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':36, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':37, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':38, 'gr':'P4B',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':39, 'gr':'S39',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':40, 'gr':'S40',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':41, 'gr':'S41',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'NotAssigned',             'value':42, 'gr':'S42',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Spectrum path (RF Swwitch #1)',   'value':43, 'gr':'S43',   'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
 {'label':'Ref1(18-32GHz)',                  'value':44, 'gr':'S44',   'SAPar':[25E9,20E9,-15,5, 3E6,300]},
  ]


def S5_table(gr):
    if gr == 'P1A':
        A14_S5=[True,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'P1B':
        A14_S5=[False,True,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'P2A':
        A14_S5=[False,False,True,False,False,False,False,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'P2B':
        A14_S5=[False,False,False,True,False,False,False,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S17':
        A14_S5=[False,False,False,False,False,False,True,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S18':
        A14_S5=[False,False,False,False,True,False,True,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S19':
        A14_S5=[False,False,False,False,False,True,True,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S20':
        A14_S5=[False,False,False,False,True,True,True,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S21':
        A14_S5=[False,False,False,False,False,False,False,True]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S22':
        A14_S5=[False,False,False,False,False,False,True,True]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'P3A':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[True,False,False,False,False,False,False,False]
    if gr == 'P3B':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,True,False,False,False,False,False,False]
    if gr == 'P4A':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,True,False,False,False,False,False]
    if gr == 'P4B':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,True,False,False,False,False]
    if gr == 'S39':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,False,False,True,False]
    if gr == 'S40':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,True,False,True,False]
    if gr == 'S41':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,False,True,True,False]
    if gr == 'S42':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,True,True,True,False]
    if gr == 'S43':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S44':
        A14_S5=[False,False,False,False,False,False,False,False]
        A15_S5=[False,False,False,False,False,False,True,True]
    return A14_S5,A15_S5


def CAB1417switch(channel,mode):
    #print(channel,mode)
    co14=ModbusClient(ADAM_list["A14"],port=502,timeout=10)
    co17=ModbusClient(ADAM_list["A17"],port=502,timeout=10)
    if not co14.connect():      # True / False
        return 'Error 01, CAB-A14 not responding. check power and connectivity'
    if not co17.connect():      # True / False
        return 'Error 01, CAB-A17 not responding. check power and connectivity'
    if mode == 'init':
        data=[False]*16*4
        try:
            print(co14.write_coils(32,data,unit=1,slave=1))
            print(co17.write_coils(32,data,unit=1,slave=1))
            return "init the A14 & A17 well"
        except:
            #print("file to init A14 & A17")
            return "false to init the A14 & A17, checking the result"
    if channel not in range(1,44+1):
        #print(channel, "which out of channel number")
        return str(channel)+"is out of channel range, please check."
    ##Start to cal DO tables
    if ((channel-1)//22) == 0:
        machine='A14'
        S2_do=(channel-1)
        S3_doStart=(channel-1)//4*4
        S3_doTable=[False]*4 ; S3_doTable[((channel-1)%4)]=True
        S4_doStart=(channel-1)//4*4
        S4_doTable=[False]*4 ; S4_doTable[((channel-1)%4)]=True
    if ((channel-1)//22) == 1:
        machine='A17'
        S2_do=(channel-23)
        S3_doStart=(channel-23)//4*4
        S3_doTable=[False]*4 ; S3_doTable[((channel-23)%4)]=True
        S4_doStart=(channel-23)//4*4
        S4_doTable=[False]*4 ; S4_doTable[((channel-23)%4)]=True
    A14_S5_doTable,A17_5S_doTable= S5_table(channelOpt[channel-1]['gr'])
    if mode == 'PM':
        if channel in [17,18,19,20,21,22,39,40,41,42,43,44]:
            return "You choise, Channel "+str(channel)+" for PowerMeter but it only for Spectrum, please check"
        print("in PM",channel, machine, S2_do, S3_doStart, S3_doTable,A14_S5_doTable,A17_5S_doTable)
        if machine == 'A14':
            try:
                print(co14.write_coils(32+S2_do,[True],unit=1,slave=1))
                print(co14.write_coils(48+S3_doStart,S3_doTable,unit=1,slave=1))
                return "Channel "+str(channel)+" set to PowerMeter"
            except:
                return "Faile during Channel "+str(channel)+" set to Spectrum."
        if machine == 'A17':
            try:
                print(co17.write_coils(32+S2_do,[True],unit=1,slave=1))
                print(co17.write_coils(48+S3_doStart,S3_doTable,unit=1,slave=1))
                return "Channel "+str(channel)+" set to PowerMeter"
            except:
                return "Faile during Channel "+str(channel)+" set to Spectrum."
    if mode == 'SA':
        print("in SA",channel ,machine, S2_do, S4_doStart, S4_doTable,A14_S5_doTable,A17_5S_doTable)
        if channel in [17,18,19,20,21,22,39,40,41,42,43,44]:
            try:
                #only A14 A17 S5
                print(co14.write_coils(80,A14_S5_doTable,unit=1,slave=1))
                print(co17.write_coils(80,A14_S5_doTable,unit=1,slave=1))
                return "Channel "+str(channel)+" set to Spectrum."
            except:
                return "Faile during Channel "+str(channel)+" set to Spectrum."
        if machine == 'A14':
            try:
                print(co14.write_coils(32+S2_do,[False],unit=1,slave=1));time.sleep(adam_delay)
                print(co14.write_coils(64+S4_doStart,S4_doTable,unit=1,slave=1));time.sleep(adam_delay)
                print("for 14",co14.write_coils(80,A14_S5_doTable,unit=1,slave=1))
                print("for 17",co17.write_coils(80,A17_S5_doTable,unit=1,slave=1))
                return "Channel "+str(channel)+" set to Spectrum."
            except:
                return "Faile during Channel "+str(channel)+" set to Spectrum."
        if machine == 'A17':
            try:
                print(co17.write_coils(32+S2_do,[False],unit=1,slave=1));time.sleep(adam_delay)
                print(co17.write_coils(64+S4_doStart,S4_doTable,unit=1,slave=1));time.sleep(adam_delay)
                print("for 14",co14.write_coils(80,A14_S5_doTable,unit=1,slave=1))
                print("for 17",co17.write_coils(80,A17_S5_doTable,unit=1,slave=1))
                return "Channel "+str(channel)+" set to Spectrum."
            except:
                return "Faile during Channel "+str(channel)+" set to Spectrum."
    else:
        return "not in any mode, check the input mode"


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

        #print(dataFromServerA.decode(),dataFromServerB.decode())
        #print(format(float(dataFromServerA.decode()),'.2f'),format(float(dataFromServerA.decode()),'.2f'))
        return format(float(dataFromServerA.decode()),'.2f'),format(float(dataFromServerB.decode()),'.2f')
    except:
        print ("fail to get power Meter")
        return 'Fail to get power','Faill to get power'

