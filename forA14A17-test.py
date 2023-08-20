from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
import ReceiverADAM as RAD


for i in range(46):
    #print(i,(i-1)//4,(i-1)%4,(i-1)//22)
    if ((i-1)//22) == 0:
        machine='A14'
        S2_do=(i-1)
        S3_doStart=(i-1)//4*4+48
        S3_doTable=[False]*4 ; S3_doTable[((i-1)%4)]=True
        S4_doStart=(i-1)//4*4+64
        S4_doTable=[False]*4 ; S4_doTable[((i-1)%4)]=True
    else:
        machine='A17'
        S2_do=(i-23)
        S3_doStart=(i-23)//4*4+48
        S3_doTable=[False]*4 ; S3_doTable[((i-23)%4)]=True
        S4_doStart=(i-23)//4*4+64
        S4_doTable=[False]*4 ; S4_doTable[((i-23)%4)]=True


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

print(channelOpt[0])
print(channelOpt[1]['gr'])



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
        A14_S5=[False,True,False,False,True,False,True,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S19':
        A14_S5=[False,True,False,False,False,True,True,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S20':
        A14_S5=[False,True,False,False,True,True,True,False]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S21':
        A14_S5=[False,True,False,False,False,False,False,True]
        A15_S5=[False,False,False,False,False,False,False,True]
    if gr == 'S22':
        A14_S5=[False,True,False,False,False,False,True,True]
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
    #co14=ModbusClient(RAD.ADAM_list["A14"],port=502,timeout=10)
    #co17=ModbusClient(RAD.ADAM_list["A17"],port=502,timeout=10)
    #if not co14.connect():      # True / False
    #    return 'Error 01, CAB-A14 not responding. check power and connectivity'
    #if not co17.connect():      # True / False
    #    return 'Error 01, CAB-A17 not responding. check power and connectivity'
    if mode is 'init':
        data=[False]*16*4
        #print("will init A14 & A17 with",data)
        try:
            print(co14.write_coils(32,data,unit=1))
            print(co17.write_coils(32,data,unit=1))
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
        S3_doStart=(channel-1)//4*4+48
        S3_doTable=[False]*4 ; S3_doTable[((channel-1)%4)]=True
        S4_doStart=(channel-1)//4*4+48
        S4_doTable=[False]*4 ; S4_doTable[((channel-1)%4)]=True
    if ((channel-1)//22) == 1:
        machine='A17'
        S2_do=(channel-23)
        S3_doStart=(channel-23)//4*4+48
        S3_doTable=[False]*4 ; S3_doTable[((channel-23)%4)]=True
        S4_doStart=(channel-23)//4*4+48
        S4_doTable=[False]*4 ; S4_doTable[((channel-23)%4)]=True
    A14_S5_doTable,A17_5S_doTable= S5_table(channelOpt[channel-1]['gr'])
    if mode is 'PM':
        if channel in [17,18,19,20,21,22,39,40,41,42,43,44]:
            #print(channel, "which out of channel number")
            return "Channel "+str(channel)+" only can shows in Spectrum, please check"
        #print ("into PM")
        print("in PM",channel, machine, S2_do, S3_doStart, S3_doTable,A14_S5_doTable,A17_5S_doTable)
        try:
            if machine is 'A14':
                pass
                #print(co14.write_coils(32+S2_do,True,unit=1))
                #print(co14.write_coils(48+S3_doStart,S3_doTable,unit=1))
            if machine is 'A17':
                pass
                #print(co17.write_coils(32+S2_do,True,unit=1))
                #print(co17.write_coils(48+S3_doStart,S3_doTable,unit=1))
            return "Good 2"
        except:
            return "A14, A17 may have issue when setting ADAM."
    if mode is 'SA':
        print("in SA",channel ,machine, S2_do, S4_doStart, S4_doTable,A14_S5_doTable,A17_5S_doTable)
        if channel in [17,18,19,20,21,22,39,40,41,42,43,44]:
            #only A14 A17 S5
            return "Channel "+str(channel)+" set to Spectrum."
        if machine is 'A14':
            pass
                #print(co14.write_coils(32+S2_do,False,unit=1))
                #print(co14.write_coils(64+S4_doStart,S4_doTable,unit=1))
                #print(co14.write_coils(80,A14_S5_doTable,unit=1))
                #print(co17.write_coils(80,A17_S5_doTable,unit=1))
        if machine is 'A17':
            pass
                #print(co17.write_coils(32+S2_do,False,unit=1))
                #print(co17.write_coils(64+S4_doStart,S4_doTable,unit=1))
                #print(co14.write_coils(80,A14_S5_doTable,unit=1))
                #print(co17.write_coils(80,A17_S5_doTable,unit=1))        
        return "Good 3"

    else:
        return "not in any mode, check the input mode"
    '''
    try:
        print(co.write_coils(coil_list[card_at], data2,unit=1))
        time.sleep(adam_delay)  # must be padded before the consecutive reading
        return 'Setting Succeful'
    except:
        co.close()
        return 'Error 03'
        '''
#print(CAB1417switch(0,'init'))
#print(CAB1417switch(3,'PM'))
#print(CAB1417switch(10,'PM'))
#print(CAB1417switch(24,'PM'))
for i in range(46):
    CAB1417switch(i,'SA')
    #print(i,CAB1417switch(i,'PM'))
