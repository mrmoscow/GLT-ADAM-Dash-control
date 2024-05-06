#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
from datetime import datetime
sys.path.append("../module")
sys.path.append('/home/obscon/common-py/')
import ReceiverADAM as RAD
import dsm



def calTsys(power):
    #len(power)
    if len(power) < 10:
        return "000.0"
    elif len(power) < 20:
        power.sort()
        yfact=sum(power[2:4])-sum(power[-4:-2])
        tsys=0.0
        return f'{yfact:.2f}'
    else:
        power.sort()
        yfact=sum(power[2:4])-sum(power[-4:-2])
        return f'{yfact:.2f}'


def main():
    parser = argparse.ArgumentParser(description="record Power(db) from 4 Meter (2 channel for each)")

    parser.add_argument('-t','--time', type=int, default=60,
               help="total time(in seconds) for the scirp running. default is 60 seconds.")
    parser.add_argument('-i','--interval', type=int ,default=1000,
              help="The interval time (in milli second) of re-flash, default is 1000 millisecond.")
    parser.add_argument('-f','--fast', choices=['PM1', 'PM2', 'PM3','PM4'],default='PM1',
              help="which PowerMeter you want to use in fast mode( i less 250), Default is PM1")
    args = parser.parse_args()
    #return args.watt

    power1a=[];power1b=[];power2a=[];power2b=[]
    power3a=[];power3b=[];power4a=[];power4b=[]
    timeint=(args.interval/1000.0)
    intshow=f'{timeint:.2f}'
    dsm.open()
    ACC = b"gltacc"
    MAC = b"gltMandC"
    T_hot,timestamp=dsm.read(MAC, b"DSM_RF_CRYOSTAT_AMBIENT_F")
    T_atm = dsm.read(ACC, b"DSM_WEATHER_TEMP_C_F")[0]+273.15
    dsm.close()

    if timeint < 250:
        PM=args.fast
        outfile=open("../assets/powerRecorder-q.txt","a")
        os.system('clear')
        print("\n    HotLoad Temp,",T_hot," [K], OutSide Temp",T_atm," [k]")
        print("    Quickly Power Recording Mode in process, please wait for ",
                args.time, "[Seconds]]\n \n ")
        for i in range(int(args.time/timeint)):
            p1=RAD.get_Power(PM)
            rtime=datetime.utcnow().strftime("%m-%d %H:%M:%S .%f,")
            outfile.write('{}{}, (From{})\n'.format(rtime,p1,PM))
            time.sleep(timeint)
        outfile.close()
    else:
        outfile=open("../assets/powerRecorder.txt","a")
        for i in  range(int(args.time/timeint)):
            os.system('clear')
            print("\n    HotLoad Temp,",T_hot," [K], OutSide Temp",T_atm," [k]")
            print("    will record total ", args.time, "Seconds, for each",intshow,
               "seconds. This is the", i+1 ,"times. \n \n ")
            p1=RAD.get_Power('PM1');power1a.append(float(p1[0])); power1b.append(float(p1[1]))
            p2=RAD.get_Power('PM2');power2a.append(float(p2[0])); power2b.append(float(p2[1]))
            p3=RAD.get_Power('PM3');power3a.append(float(p3[0])); power3b.append(float(p3[1]))
            p4=RAD.get_Power('PM4');power4a.append(float(p4[0])); power4b.append(float(p4[1]))
            rtime=datetime.utcnow().strftime("%m-%d %H:%M:%S .%f,")
            outfile.write('{}{} {}{}{}\n'.format(rtime,p1,p2,p3,p4))
            print("     PowerMeter 1 -",p1," y-factor (dB)",calTsys(power1a),calTsys(power1b))
            print("     PowerMeter 2 -",p2," y-factor (dB)",calTsys(power2a),calTsys(power2b))
            print("     PowerMeter 3 -",p3," y-factor (dB)",calTsys(power3a),calTsys(power3b))
            print("     PowerMeter 4 -",p4," y-factor (dB)",calTsys(power4a),calTsys(power4b))
            time.sleep(timeint-0.22)
        outfile.close()

#print(RAD.get_Power('PM1'))
#print("PowerMeter 1 get",RAD.get_Power('PM1'))


if __name__ == "__main__":
    main()
