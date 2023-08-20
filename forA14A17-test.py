
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import time
import ReceiverADAM as RAD


'''
1:8000,0100
2:s
3:s
4:s
5:4000,0100
6:s
7:s
8:s
9:2000,0100
10:s
11:s
12:s
13:1000,0100
14:s
15:s
16:s
17:0200,0100
18,0900,0100
19:,0100
20:0100
21:0100,0100
22:0300,0100


40:
41:0000,0600
42:0000,0e00
43:0000,0200
44:0000,0300
'''



for i in range(46):
    #print(i,(i-1)//4,(i-1)%4,(i-1)//22)
    if ((i-1)//22) == 0:
        machine='A14'
        S2_do=(i-1)
        S3_doStart=(i-1)//4*4+48
        S3_doTable=[False]*4 ; S3_doTable[((i-1)%4)]=True
        S4_doStart=(i-1)//4*4+64
        S4_doTable=[False]*4 ; S4_doTable[((i-1)%4)]=True
        A14_S5_doStart=
        A14_S5_doTable=RAD.hex_to_BiList('0100')
        A17_5S_doTable=
        A17_S5_doTable=RAD.hex_to_BiList('0100')
    else:
        machine='A17'
        S2_do=(i-23)
        S3_doStart=(i-23)//4*4+48
        S3_doTable=[False]*4 ; S3_doTable[((i-23)%4)]=True
        S4_doStart=(i-23)//4*4+64
        S4_doTable=[False]*4 ; S4_doTable[((i-23)%4)]=True

        A14_S5_doTable=RAD.hex_to_BiList('0100')
        A17_S5_doTable=RAD.hex_to_BiList('0100')
    #print(i,(i-1)//22,machine,S2_do,S3_doStart,S3_doTable)
    #print(i,machine,S2_do,A14_doStart)



def CAB1417switch(channel,mode):
    print(channel,mode)
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
    if mode is 'PM':
        if channel in [17,18,19,20,21,22,39,40,41,42,43,44]:
            #print(channel, "which out of channel number")
            return "Channel "+str(channel)+" only can shows in Spectrum, please check"
        #print ("into PM")
        if ((channel-1)//22) == 0:
            machine='A14'
            S2_do=(channel-1)
            S3_doStart=(channel-1)//4*4+48
            S3_doTable=[False]*4 ; S3_doTable[((channel-1)%4)]=True
            #print(co14.write_coils(32+i-1,True,unit=1))
            #print(co14.write_coils(48+S3_doStart,S3_doTable,unit=1))
        if ((channel-1)//22) == 1:
            machine='A17'
            S2_do=(channel-23)
            S3_doStart=(channel-23)//4*4+48
            S3_doTable=[False]*4 ; S3_doTable[((channel-23)%4)]=True
            #print(co17.write_coils(32+i-1,True,unit=1))
            #print(co17.write_coils(48+S3_doStart,S3_doTable,unit=1))
        print(machine,S2_do,S3_doStart,S3_doTable)
        try:
            if machine is 'A14':
                pass
                #print(co14.write_coils(32+S2_do,True,unit=1))
                #print(co14.write_coils(48+S3_doStart,S3_doTable,unit=1))
            if machine is 'A17':
                pass
                #print(co17.write_coils(32+S2_do,True,unit=1))
                #print(co17.write_coils(48+S3_doStart,S3_doTable,unit=1))
            return "Good 3"
        except:
            return "A14, A17 may have issue when setting ADAM."
    if mode is 'SA':
        if ((channel-1)//22) == 0:
            machine='A14'
            S2_do=(channel-1)
            S4_doStart=(channel-1)//4*4+48
            S4_doTable=[False]*4 ; S4_doTable[((channel-1)%4)]=True
            #print(co14.write_coils(32+i-1,True,unit=1))
            #print(co14.write_coils(48+S3_doStart,S3_doTable,unit=1))
        if ((channel-1)//22) == 1:
            machine='A17'
            S2_do=(channel-23)
            S4_doStart=(channel-23)//4*4+48
            S4_doTable=[False]*4 ; S4_doTable[((channel-23)%4)]=True
        print ("into SA")
        return "Good 2"

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
    print(i,CAB1417switch(i,'PM'))
