#!/home/obscon/bin/cpy3

import argparse
import os,sys,time,random
from datetime import datetime
#from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("../module")
#import ReceiverADAM as RAD
#import SpecAnalyzer as SA
import hp8508 as hp

def is_positive_integer(value):
    """
    Checks if the input value is a positive integer.

    Parameters:
        value (str): The input value to check.

    Returns:
        bool: True if the value is a positive integer, False otherwise.
        number(int):
    ToDo: how about input like:60*60*24*2 or 2E4....
    """
    try:
        number = int(value)
        if number > 0:
            return True,number
        else:
            return False,0
    except ValueError:
        return False,0

def file_vvm(ip,form_mod,timeint,totime):
    if ip == "192.168.1.74":
        loc2="Mas"
    elif ip == "192.168.1.155":
        loc2="LSC"
    elif ip == "192.168.1.204":
        loc2="RxC"
    else:
        loc2="UnK"

    timenow=time.strftime("%d%m%y_%H%M%S")
    outfilename="../assets/vvm_" + loc2 + "_t" + str(form_mod) + "_" + timenow + ".txt"
    outfile=open(outfilename,"w")
    timecount=0
    next_time = time.time()

    for i in range(int(totime/timeint)):
        timeWritetoFile=datetime.now().strftime("%Y/%m/%d_%H:%M:%S.%f")[:-4]
        print('%25s %8.1f' % (timeWritetoFile, timecount),end=", ")
        resultA, resultB = hp.get_vvm_AB(ip,form_mod)
        outfile.write('%25s %8.1f %20s %20s \n' % (timeWritetoFile, timecount, resultA, resultB))
        timecount += timeint
        next_time += timeint
        sleep_time=next_time - time.time()
        if sleep_time > 0.0:
            time.sleep(sleep_time)
    outfile.close()
    if form_mod == 5:
        print("End of the VVM data, will plot the Data")
        plot_vvm(outfilename,form_mod)

def data_vvm(ip,form_mod,timeint):
    try:
        print("Press Ctrl+C to quit the loop.")
        next_time = time.time()
        while True:
            hp.get_vvm_AB(ip,form_mod)
            next_time += timeint
            sleep_time=next_time - time.time()
            if sleep_time > 0.0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("\nLoop interrupted. Exiting.")

def plot_vvm(filename,form_mod):
    file_name = os.path.basename(filename)
    [first,loc2,form_mod2,t1,t2]=filename.rstrip('.txt').split("_")
    timeWritetoFile, timecount, phase, ba = np.genfromtxt(filename,unpack="True")

    fig1=plt.figure()
    ax = fig1.add_subplot(1,1,1)
    plt.plot(timecount,phase,'b.',markersize=2)
    plt.axis([0, round(timecount[-1]), -180,180])
    major_ticks = np.arange(-180, 181, 20)
    minor_ticks = np.arange(-180, 181, 5)
    plt.title(f"Plot for {file_name}")  # Use file name as title
    plt.xlabel('Time (seconds)', fontsize=18)
    plt.ylabel('Phase (degrees)', fontsize=18)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
    pltfigname=filename.rsplit(".",1)[0]+".png"
    plt.savefig(pltfigname)
    #plt.show()
    plt.clf()

def positive_int(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"Invalid value: {value}. It must be a positive integer.")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid value: {value}. It must be an integer.")


def get_opt():
    parser = argparse.ArgumentParser(description=
         """Control and monitor GLT VVM machine.
        There are 3 vector meter on GLT. 1.at Maser-House(.74), 2. at LSC(.155), 3. Rx-Cabin(.204),
        For long time recording, using screen (screen -S before code, when data recording: ctrl+a than d )""")
    parser.add_argument("-i", "--ip", type=str,
            choices=["74","155","204","70"],
            help="IP address of the Vector Meter")
    parser.add_argument("-d", "--direct", type=str, choices=["on","off"], help="Turn on/off the Direct output mode          ")
    parser.add_argument("-f", "--format", type=int, choices=[1, 2, 3, 4, 5], help="Data format, 5 for B-A(degree)               and B/A(ratio)")
    parser.add_argument("-r", "--record", type=str, choices=["y","n"], help="Into the file recording mode or not(just show up the value).")
    parser.add_argument("-t", "--time", type=positive_int, help="A positive integer for recording time in second")
    args = parser.parse_args()
    #if args.record and not (args.ip and args.format):
    #    parser.error("The --record requires both --ip and --format to be specified.")

    return args



opt = get_opt()

timeint=0.5
#in secconds, defaule 
#file_vvm("192.168.1.70",2,timeint,25)
#data_vvm("192.168.1.70",3,timeint)


if opt.ip:
    mac_input="from -i option"
    ip0=opt.ip

else:
    print("----------------------------------------")
    print("\nSelect VVM (HP8508A):\n")
    print("(a) At Maser House(.74)")
    print("(b) At LSC (.155)")
    print("(c) At Rx Cabin (.204)")
    #print("----------------------------------------")

    while True:
        mac_input= input("Please input your choise (a, b, c) :")
        if mac_input in ["a","A","74","1"]:
            ip0="74"
            break
        elif mac_input in ["b","B","155","2"]:
            ip0="155"
            break
        elif mac_input in ["c","C","204","3"]:
            ip0="204"
            break
        elif mac_input in ["d","D","70","4"]:
            ip0="70"
            break
        elif mac_input in ["q","Q","exit","quit"]:
            sys.exit()
        else:
            print ("-----Input error-----")
ip_map ={
        "74":  {"ip":"192.168.1.74" , "gpip":"8" , "loc":"Maser House"},
        "155": {"ip":"192.168.1.155", "gpip":"25", "loc":"Left Side Cabin"},
        "204": {"ip":"192.168.1.204", "gpip":"25", "loc":"Rx Cabin"},
        "70":  {"ip":"192.168.1.70" , "gpip":"25", "loc":"Taipei Lab"},
    }

ip=ip_map[ip0]["ip"]
gpip_add = ip_map[ip0]["gpip"]
loc = ip_map[ip0]["loc"]

print("Your Input",mac_input,"for",ip,"at",loc,"and GPIP addreess",gpip_add,"\n")

print("Checkiing the Instance status")
hp.get_vvm_info(ip)


print("----------------------------------------")
if opt.direct:
    print("The dirct output mode now will be",opt.direct)
    if opt.direct == "on":
        print("Turn on Direct Mode and bye bye!")
        hp.sendVVM(ip,"DAN ON")
        sys.exit()
    if opt.direct == "off":
        print("Turn off Direct Mode and bye bye!")
        hp.sendVVM(ip,"DAN OFF")
        sys.exit()

if opt.format:
    print("-f option using, Now you are using formate type",opt.format)
    form_mod=opt.format
else:
    #print("-f option No using ")
    while  True:
        dout_input=input("\nDo you want to switch to Direct output mode? y/n:")
        if dout_input in ["y","Y","yes","Yes","YES"]:
            print("Will set the Vector Meter",ip,"into Direct output Mode")
            dout_mod=True
            break
        elif dout_input in ["n","N","no","No","NO"]:
            print("Please choise the recording parameter.")
            dout_mod=False
            break
        elif dout_input in ["q","Q","exit","quit"]:
            sys.exit()
        else:
            print ("-----Input error-----")
    ##Mod
    if dout_mod:
        print("The code will set the",ip,"into Direct output mode")
        hp.sendVVM(ip,"DAN ON")
        sys.exit()

    print("----------------------------------------")
    print("\nSelect Display/Record format:\n")
    print("1-> B input(dB),  & B-A (degree)")
    print("2-> B input(mV),  & B-A (degree)")
    print("3-> A input(dB),  & B input(dB)")
    print("4-> A input(mV),  & B input(mV)")
    print("5-> B-A (degree), & B/A (ratio)")
    while  True:
        form_input=input("Please input your choice (1,2,3,4,5):")
        if form_input in ["1","a","A"]:
            print("Will using option 1-> B input(dB) & B-A (degree)")
            form_mod=1
            #form_des="B input(dB) & B-A (degree)"
            break
        elif form_input in ["2","b","B"]:
            print("Will using option 2-> B input(mV) & B-A (degree)")
            form_mod=2
            #form_des="B input(mV) & B-A (degree)"
            break
        elif form_input in ["3","c","C"]:
            print("Will using option 3-> A input(dB) & B input(dB)")
            form_mod=3
            #form_des="A input(dB) & B input(dB)"
            break
        elif form_input in ["4","d","D"]:
            print("Will using option 4-> A input(mV) & B input(mV)")
            form_mod=4
            #form_des="A input(mV) & B input(mV)"
            break
        elif form_input in ["5","e","E"]:
            print("Will using option 5-> B-A (degree), & B/A (ratio)")
            form_mod=5
            #form_des="B-A (degree) & B/A (ratio)"
            break
        elif form_input in ["q","Q","exit","quit"]:
            sys.exit()
        else:
            print ("-----Input error-----")


form_map ={
        1:{"descript":"B input(dB) & B-A (degree)"},
        2:{"descript":"B input(mV) & B-A (degree)"},
        3:{"descript":"A input(dB) & B input(dB)"},
        4:{"descript":"A input(mV) & B input(mV)"},
        5:{"descript":"B-A (degree) & B/A (ratio)"},
    }
form_des=form_map[form_mod]["descript"]


if opt.record:
    ##print("-r, recording  option using, Now you will recording data",opt.record)
    if opt.record == "y":
        re_mod=True
    else:
        re_mod=False
else:
    #print("-r, time not using, manual input.")
    print("----------------------------------------\n")
    while  True:
        re_input=input("Do you want to Recording data? y/n:")
        if re_input in ["y","Y","yes","Yes","YES"]:
            print("Will using",ip,"with format",form_mod,"->",form_des)
            re_mod=True
            '''
            while  True:
                time_input=input("Input the recording time(in Seconds)?:")
                #correct,time=False,30
                correct,all_time=is_positive_integer(time_input)
                if time_input in ["q","Q","exit","quit"]:
                    break
                if correct:
                    print("The time you input is",all_time,"Seconds")
                    break
                else:
                    print("Time format mistake, re-try")
                    continue
              '''
            break
        elif re_input in ["n","N","no","No","NO"]:
            re_mod=False
            break
        elif re_input in ["q","Q","exit","quit"]:
            sys.exit()

if opt.time:
    print("-t, time option using, Recording data for",opt.time,"Seconds")
    all_time=opt.time
else:
    #print("-t, time not using,")
    if re_mod:
        print("----------------------------------------\n")
        while  True:
            time_input=input("Input the recording time(in Seconds)?:")
            #correct,time=False,30
            correct,all_time=is_positive_integer(time_input)
            if time_input in ["q","Q","exit","quit"]:
                sys.exit()
            if correct:
                print("The time you input is",all_time,"Seconds")
                break
            else:
                print("Time format mistake, re-try")
                continue


if re_mod:
    print("--------------------------------")
    print("Will Recording Data using vvm:",ip,", For",all_time,"Seconds\n"
            "in format",form_mod,"->",form_des)
    #Next if for Recording.
    file_vvm(ip,form_mod,timeint,all_time)
    #Back to Normal setting if dev
    #hp.sendVVM(ip,"DAN OFF")
    #print("DAN Turn off, exit the code, GoodBye")
    sys.exit()
else:
    #Next is for show the data
    data_vvm(ip,form_mod,timeint)
    #Back to Nrrmal Setting if dev
    #hp.sendVVM(ip,"DAN OFF")
    #print("DAN Turn off, exit the code, GoodBye")
    sys.exit()

print("End of the code")
