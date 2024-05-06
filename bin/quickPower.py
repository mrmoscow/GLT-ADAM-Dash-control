#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
from datetime import datetime
sys.path.append("../module")
import ReceiverADAM as RAD



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

    outfile=open("../assets/powerRecorder-quick.txt","a")
    for i in  range(int(args.time/timeint)):
        os.system('clear')
        print("    will record total ", args.time, "Seconds, for each",intshow,
               "seconds. This is the", i+1 ,"times. \n \n ")
        p1=RAD.get_Power('PM1')
        p2=RAD.get_Power('PM2')
        p3=RAD.get_Power('PM3')
        p4=RAD.get_Power('PM4')
        rtime=datetime.utcnow().strftime("%m-%d %H:%M:%S.%f,")

        outfile.write('{}{} {}{}{}\n'.format(rtime,p1,p2,p3,p4))
        print("     PowerMeter 1 -",p1)
        print("     PowerMeter 2 -",p2)
        print("     PowerMeter 3 -",p3)
        print("     PowerMeter 4 -",p4)
        time.sleep((args.interval/1000.0)-0.211)
    outfile.close()

#print(RAD.get_Power('PM1'))
#print("PowerMeter 1 get",RAD.get_Power('PM1'))


if __name__ == "__main__":
    main()
