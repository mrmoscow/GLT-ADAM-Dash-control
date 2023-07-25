
import socket
import ReceiverADAM as RAD #module for this project

'''
# Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
try:
    #print(clientSocket.connect(("192.168.1.221",5025)))
    print(clientSocket.connect(("192.168.1.222",5025)))
    data = "*IDN?\n"
    clientSocket.send(data.encode())
    dataFromServer = clientSocket.recv(1024)
    print(dataFromServer.decode())

    anycf=7E9
    data = 'FREQ:CENT'+" {:.0f} ".format(anycf) +'Hz\n'
    print(data)
    clientSocket.send(data.encode())

    anysp=1000000000
    data = "FREQ:SPAN {:.0f} Hz\n".format(anysp)
    print(data)
    clientSocket.send(data.encode())

    anyrl=-40
    data = "DISP:WIND:TRAC:Y:RLEV {:.0f} dBm\n".format(anyrl)
    print(data)
    clientSocket.send(data.encode())

    anylg=10
    data= "DISP:SEM:VIEW:WIND:TRAC:Y:PDIV {:.0f} dB\n".format(anylg)
    print(data)
    clientSocket.send(data.encode())

    anyrb=3E6
    data= "BAND {:.0f} Hz\n".format(anyrb)
    print(data)

    anyvb=300
    data= "BAND:VID {:.0f} Hz\n".format(anyvb)
    print(data)

except:
    print('Error 01')
'''



def set_SA(machine,centFreq,span,refLevel,scale,rbw,vbw):
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((machine,5025))
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
        return 'Error 01'

#for SA

'''
   strcpy(anycf,argv[1]);
   strcpy(anysp,argv[2]);
   strcpy(anylg,argv[3]);
   strcpy(anyrl,argv[4]);
   strcpy(anyrb,argv[5]);
   strcpy(anyvb,argv[6]);
      sprintf(message,"FREQ:CENT %s Hz\n",anycf);
      sprintf(message,"FREQ:SPAN %s Hz\n",anysp);
      sprintf(message,"BAND %s Hz\n",anyrb);
      sprintf(message,"BAND:VID %s Hz\n",anyvb);
      sprintf(message,"DISP:WIND:TRAC:Y:RLEV %s dBm\n",anyrl);
      sprintf(message,"DISP:SEM:VIEW:WIND:TRAC:Y:PDIV %s dB\n",anylg);
'''

#The SAPar:[Center Frequency(Hz),SPAN(Hz),Reference Lavel (dBm),Scale(dB/div),RBW(Hz),VBW(Hz)]
channelOpt =[
    {'label':'EHT1_POL0 IF 4-9 GHz',    'value':1,  'SAPar':[8E9,1E10,-40,5,3E6,300]},
    {'label':'EHT1_POL0 BB 6-8 GHz',    'value':2,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT1_POL0 BB 4-6 GHz',    'value':3,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT1_POL1 BB 4-6 GHz',    'value':4,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'EHT1_POL1 IF 4-9 GHz',    'value':5,  'SAPar':[8E9,1E10,-40,5, 3E6,300]},
    {'label':'EHT1_POL1 BB 6-8 GHz',    'value':6,  'SAPar':[1.5E9,2.9E9,-30,5, 3E6,300]},
    {'label':'10Mhz-Left rack',         'value':7,  'SAPar':[1E7,200,10,10, 1,1]},
    {'label':'100MHz',                  'value':8,  'SAPar':[1E8,200,10,10, 1,1]},

    {'label':'ContDet Input LHC 4-8GHz',        'value':9,  'SAPar':[6E9,8E9,-60,2, 3E6,300]},
    {'label':'ContDet Input RHC 4-8GHz',        'value':10, 'SAPar':[6E9,8E9,-60,2, 3E6,300]},
    {'label':'VVM Input (Rx) 50 MHz',           'value':11, 'SAPar':[5E7,200,-40,10, 1,1]},
    {'label':'VVM Input (Ref) 50 MHz',          'value':12, 'SAPar':[5E7,200,0,10, 1,1]},
    {'label':'5.95 GHz',                        'value':13, 'SAPar':[5.9E9,200,0,10, 1,1]},
    {'label':'0.5 or 1.5 GHz',                  'value':14, 'SAPar':[1E9,1.6E9,0,10, 3E6,300]},
    {'label':'31.5 MHz',                        'value':15, 'SAPar':[3.15E7,200,-50,10, 1, 1]},
    {'label':'Ref1 (SG) couple out',            'value':16, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},

    {'label':'NotAssigned',                     'value':17, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':18, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':19, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':20, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':21, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Ref1+Ref3 (18.5-33.5G)',          'value':22, 'SAPar':[1500,29000,-30,5, 30000,300]},
    {'label':'NotAssigned',                     'value':35, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':36, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':37, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Ref1 (SG) couple out',            'value':38, 'SAPar':[1.1E9,4.4E9,0,10, 1E4,1E4]},
    #note here
    {'label':'NotAssigned',                     'value':39, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':40, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':41, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'NotAssigned',                     'value':42, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Spectrum path (RF Swwitch #1)',   'value':43, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    {'label':'Ref1(18-32GHz)',                  'value':44, 'SAPar':[2.2E9,4.4E9,0,10, 1E4,1E4]},
    ]


#print(channelOpt)
#print(channelOpt[1])
print(type(channelOpt))
print(type(channelOpt[1]))
print(channelOpt[1]['SAPar'])
'''
for dicc in channelOpt:
    print(dicc['label'],dicc['value'],dicc['SAPar'][0],dicc['SAPar'][0]*3)


for dicc in channelOpt:
    del dicc['SAPar']
    print(dicc)
'''
d_k = 'SAPar'
channel_02 = [{k : v for k, v in s.items() if k != d_k} for s in channelOpt]
d_v = 'NotAssigned'
channel_03 = [s for s in channelOpt if not(s['label'] == 'NotAssigned')]
channel_04 = [{k : v for k, v in s.items() if k != d_k} for s in channelOpt if not(s['label'] == 'NotAssigned')]
#print(channel_O2)
#print(channel_03)

#for sub in channelOpt:
#    for key,val in sub.items():
#        print(key,val)

print(channel_02)
print(channel_03)
print(channel_04)
Sp=channelOpt[1]['SAPar']
#set_SA("192.168.1.221",Sp[0],Sp[1],Sp[2],Sp[3],Sp[4],Sp[5])
