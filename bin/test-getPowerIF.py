from os.path import exists
import sys
import socket
import time
#print(sys.version)
#print(sys.version_info)
#print(sys.version_info[1])
if sys.version_info[1] == 7 or sys.version_info[1] == 9:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient


sys.path.append("..")
import ReceiverADAM as RAD




#if 'Bad' in RAD.check_ADAM('A14'): sys.exit("Error A14 is not conection")
#if 'Bad' in RAD.check_ADAM('A17'): sys.exit("Error A17 is not conection")

channelOpt=RAD.channelOpt
PMIFsetall= [
    {'gr':'P1A','mac':'A14','S3star': 0, 'valuestar':1},
    {'gr':'P1B','mac':'A14','S3star': 4, 'valuestar':5},
    {'gr':'P2A','mac':'A14','S3star': 8, 'valuestar':9},
    {'gr':'P2B','mac':'A14','S3star':12, 'valuestar':13},
    {'gr':'P3A','mac':'A17','S3star': 0, 'valuestar':23},
    {'gr':'P3B','mac':'A17','S3star': 4, 'valuestar':27},
    {'gr':'P4A','mac':'A17','S3star': 8, 'valuestar':31},
    {'gr':'P4B','mac':'A17','S3star':12, 'valuestar':35},
    ]

def gotopt(gr):
    return [{k : v for k, v in s.items() if k in ['label','value']} for s in channelOpt if s['gr'] == gr]

def PMIFset(gr):
    return [{k : v for k, v in s.items()}  for s in PMIFsetall if s['gr'] == gr]

def getPowIF(IFgroup):
    co14=ModbusClient(RAD.ADAM_list["A14"],port=502,timeout=10)
    co17=ModbusClient(RAD.ADAM_list["A17"],port=502,timeout=10)
    if not co14.connect():      # True / False
        return 'Error 01, CAB-A14 not responding. check power and connectivity',0
    if not co17.connect():      # True / False
        return 'Error 01, CAB-A17 not responding. check power and connectivity',0
    if sum([True for s in PMIFsetall if s['gr'] == gr]) ==0:
        return 'Error,PowerMeter group not in the list,  maybe you have a typo?',0
<<<<<<< HEAD
    IFgr=gotopt(IFgroup)
    PMif=PMIFset(IFgroup)[0]
=======
>>>>>>> 34f152edeb4b9acef4273f252e3d56a44be7320f
    s3=[int(x) for x in RAD.get_5056(PMif['mac'],'S3').split(',')[PMif['S3star']:PMif['S3star']+4]]
    s2=[int(x) for x in RAD.get_5056(PMif['mac'],'S2').split(',')[PMif['S3star']:PMif['S3star']+4]]
    #s3=[int(x) for x in "1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,".split(',')[PMif['S3star']:PMif['S3star']+4]]
    #s2=[int(x) for x in "1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,".split(',')[PMif['S3star']:PMif['S3star']+4]]
    print(s3,s2)
    if sum(s3) != 1:
        #print ("no  fit")
        return 'Unknow',0
    else:
        #print("fit")
        #whichOpen=s3.index(1)
        if s2[s3.index(1)] != 1:
            return 'Unknow (IF may set to SA)',0
        else:
            return IFgr[s3.index(1)]['label'],IFgr[s3.index(1)]['value']


for gr in ['P1A','P1B','P2A','P2B','P3A','P3B','P4A','P4B']:
    re0,re1=getPowIF(gr)
    print("Power Meter",gr[1],"channel",gr[2], ", Now IF get at channel",re1,re0)
    time.sleep(0.5)
