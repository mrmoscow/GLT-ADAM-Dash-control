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
        return yfact

#def getpowerTest(PM):
#    return "-68.5","-70.25"

def main():
    parser = argparse.ArgumentParser(description="record Power(db) from 4 Meter (2 channel for each)")

    parser.add_argument('-t','--time', type=int, default=60,
               help="total time(in seconds) for the scirp running. default is 60 seconds.")
    parser.add_argument('-i','--interval', type=int ,default=2,
              help="The interval time (in second) of re-flash, default is 2 second.")
    args = parser.parse_args()
    #return args.watt

    power1a=[];power1b=[];power2a=[];power2b=[]
    power3a=[];power3b=[];power4a=[];power4b=[]

    for i in  range(int(args.time/args.interval)):
        os.system('clear')
        print("\n    will record total ", args.time, "Seconds, for each",args.interval,
               "seconds. This is the", i+1 ,"times. \n \n ")
        p1=getpowerTest('PM1');power1a.append(float(p1[0])); power1b.append(float(p1[1]))
        p2=getpowerTest('PM2');power2a.append(float(p2[0])); power2b.append(float(p2[1]))
        p3=getpowerTest('PM3');power3a.append(float(p3[0])); power3b.append(float(p3[1]))
        p4=getpowerTest('PM4');power4a.append(float(p4[0])); power4b.append(float(p4[1]))
        #print("     PowerMeter 1 get",i,random.randint(3, 10),)
        #print("     PowerMeter 2 get",i,random.randint(4, 12),)
        print("     PowerMeter 1 get",p1," y-factor",calTsys(power1a),calTsys(power1b))
        print("     PowerMeter 2 get",p2," y-factor",calTsys(power2a),calTsys(power2b))
        print("     PowerMeter 3 get",p3," y-factor",calTsys(power3a),calTsys(power3b))
        print("     PowerMeter 4 get",p4," y-factor",calTsys(power4a),calTsys(power4b))
        time.sleep(args.interval)
#print(RAD.get_Power('PM1'))
#print("PowerMeter 1 get",RAD.get_Power('PM1'))


if __name__ == "__main__":
    main()
