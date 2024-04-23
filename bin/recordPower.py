#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
sys.path.append("../module")
import ReceiverADAM as RAD




def calTsys(power):
    #len(power)
    if len(power) < 10:
        return "000.0"
    elif len(power) < 20:
        power.sort()
        #print(power)
        #print(power[2:4],power[-4:-2])
        yfact=sum(power[2:4])/sum(power[-4:-2])
        tsys=0.0
        return f'{yfact:.2f}'
    else:
        power.sort()
        yfact=sum(power[2:4])/sum(power[-4:-2])
        return f'{yfact:.2f}'

def main():
    parser = argparse.ArgumentParser(description="record Power(db) from 4 Meter (2 channel for each)")

    parser.add_argument('-t','--time', type=int, default=60,
               help="total time(in seconds) for the scirp running. default is 60 seconds.")
    parser.add_argument('-i','--interval', type=int ,default=1000,
              help="The interval time (in milli second) of re-flash, default is 1000 millisecond.")
    args = parser.parse_args()
    #return args.watt

    power1a=[];power1b=[];power2a=[];power2b=[]
    power3a=[];power3b=[];power4a=[];power4b=[]
    timeint=(args.interval/1000.0)
    intshow=f'{timeint:.2f}'
    for i in  range(int(args.time/timeint)):
        os.system('clear')
        print("\n    will record total ", args.time, "Seconds, for each",intshow,
               "seconds. This is the", i+1 ,"times. \n \n ")
        #p1=getpowerTest('PM1');power1a.append(float(p1[0])); power1b.append(float(p1[1]))
        p1=RAD.get_Power('PM1');power1a.append(float(p1[0])); power1b.append(float(p1[1]))
        p2=RAD.get_Power('PM2');power2a.append(float(p2[0])); power2b.append(float(p2[1]))
        p3=RAD.get_Power('PM3');power3a.append(float(p3[0])); power3b.append(float(p3[1]))
        p4=RAD.get_Power('PM4');power4a.append(float(p4[0])); power4b.append(float(p4[1]))
        #print("     PowerMeter 1 get",i,random.randint(3, 10),)
        #print("     PowerMeter 2 get",i,random.randint(4, 12),)
        print("     PowerMeter 1 get",p1," y-factor",calTsys(power1a),calTsys(power1b))
        print("     PowerMeter 2 get",p2," y-factor",calTsys(power2a),calTsys(power2b))
        print("     PowerMeter 3 get",p3," y-factor",calTsys(power3a),calTsys(power3b))
        print("     PowerMeter 4 get",p4," y-factor",calTsys(power4a),calTsys(power4b))
        time.sleep((args.interval/1000.0))
#print(RAD.get_Power('PM1'))
#print("PowerMeter 1 get",RAD.get_Power('PM1'))


if __name__ == "__main__":
    main()
