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

def main():
    parser = argparse.ArgumentParser(description="record Power(db) from 4 Meter (2 channel for each)")

    parser.add_argument('-t','--time', type=int, default=60,
               help="total time(in seconds) for the scirp running. default is 60 seconds.")
    parser.add_argument('-i','--interval', type=int ,default=2,
              help="The interval time (in second) of re-flash, default is 2 second.")
    args = parser.parse_args()
    #return args.watt

    no_input = True
    #powerM1=[]
    #powerM2=[]
    #powerM3=[]
    powerM4=[]
    for i in  range(int(args.time/args.interval)):
        os.system('clear')
        print("\n    will record total ", args.time, "Seconds, for each",args.interval,
               "seconds. This is the", i+1 ,"times. \n \n ")
        #print("    PowerMeter 1 get",i,random.randint(3, 10),)
        #print("    PowerMeter 2 get",i,random.randint(4, 12),)
        print("     PowerMeter 1 get",RAD.get_Power('PM1'))
        print("     PowerMeter 2 get",RAD.get_Power('PM2'))
        print("     PowerMeter 3 get",RAD.get_Power('PM3'))
        powerM4.append(RAD.get_Power('PM4')[0])
        print("     PowerMeter 4 get",RAD.get_Power('PM4'),"Test for yface",calTsys(powerM4))
        time.sleep(args.interval)
#print(RAD.get_Power('PM1'))
#print("PowerMeter 1 get",RAD.get_Power('PM1'))
#print("PowerMeter 2 get",RAD.get_Power('PM2'))
#print("PowerMeter 3 get",RAD.get_Power('PM3'))
#print("PowerMeter 4 get",RAD.get_Power('PM4'))


if __name__ == "__main__":
    main()
