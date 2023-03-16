import dash
from dash import html, dcc, callback, Input, Output
#from dash.exceptions import PreventUpdate

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
from datetime import datetime

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
           "A45_ReSl":'192.168.1.215'}

#Next list the 5056 card at which slite and the first coil position.
coil_list={"S2":32,\
           "S3":48,\
           "S4":64,\
           "S5":80}

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

def list_ADAM():
    print ("Next is the ADAD in List")
    for i,j in ADAM_list.items():
        print (i,j)
    print ("---End of the List ---")
    return


def check_ADAM():
    print ("Start to connect ADAMs")
    for i,j in ADAM_list.items():
        k= ModbusClient(j, port=502, timeout=10)
        if k.connect():
            print (i,j,"Good connection!")
        else:
            print (i,j,"*** Connection Failure ***")
    print ("--- End of connect ---")

def test_ADAM():
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


def check_ADAM_result(machine):
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
    elif ininstance(datain[0],bool):
        res=datain
    else:
        return 'Error 15'
    return res

def set_5056(machine,data,card_at='S3'):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return 'Error 01'
    data2=hex_to_BiList(data)
    print('Setting',machine,data,data2)
    if type(data2) is not list:
        return data2
    try:
        print(co.write_coils(coil_list[card_at], data2,unit=1))
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
        r = co.read_coils(coil_list[card_at],16,unit=1)
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
        print(co.write_register(channel+16,int(v/10.0*4095),unit=1))
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
        r = co.read_holding_registers(16,4,unit=1)
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
        r = co.read_holding_registers(8,7,unit=1)
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
        r = co.read_holding_registers(0,8,unit=1)
        intvalue=r.registers
        volts=[round(float(x)/65535.0*20-10.0,3) for x in intvalue]
        return volts[0:b]
    except:
        co.close()
        return ['Error 02']*b

### 6050 in A03-00/A10-00
def get_6050(machine,b=18):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return ['Error 01']*18
    try:
        r = co.read_coils(0,12,unit=1)
        res=r.bits[0:12]
        r2 = co.read_coils(12,6,unit=1)
        res.extend(r2.bits[0:6])
        br=["0" if i==0 else "1" for i in res]
        print(br)
        return br
    except:
        co.close()
        return ['Error 02']*18

