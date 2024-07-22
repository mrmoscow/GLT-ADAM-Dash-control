#!/home/obscon/bin/cpy3

import argparse
import subprocess
import sys,os, datetime
sys.path.append("../module")
import ReceiverADAM as RAD
#from channelOpt  import channelOpt
from channelTest  import channelOpt


def newChanninInput(value,para):
    for channel in channelOpt:
        if str(channel['value']) == str(value):
            text2=' {\'label\':\'%s\', \'value\':%s, \'gr\':\'%s\',' % (channel['label'],channel['value'],channel['gr'])
            text3='\'SAPar\':[%.1e,%.1e,%d,%d,%.1e,%d]},' % (para[0],para[1],para[2],para[3],para[4],para[5])
            print (text2+text3)
            return text2+text3


def saveintofile(label,choice,newPara):
    command="grep -n '"+label+"' ../module/channelTest.py | grep -v '#' | awk '{print $1}'"
    p = subprocess.Popen(command, shell=True,
              stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    line_number = int(p.decode().split(":\n")[0])
    today = datetime.date.today().strftime('%Y/%m/%d')
    insert_text0 = "# Edit by script at"+today+"\n"
    insert_test1 = "#"
    insert_test2 = newChanninInput(choice,newPara)+"\n"
    # 讀取文件內容
    with open('../module/channelTest.py', 'r') as file:
        lines = file.readlines()
        # 在指定行後插入文本
        lines.insert(line_number-1, insert_text0)
        lines.insert(line_number,   insert_test1)
        lines.insert(line_number+2, insert_test2)
    # 將修改後的內容寫回文件
    with open('../module/channelTest.py', 'w') as file:
        file.writelines(lines)


def checkinput(para):
    numberornot=[]
    vallist=[]
    for value in para:
        try:
            # Convert it into integer
            val = int(value)
            numberornot.append(1)
            vallist.append(val)
            #print("Input is an integer number. Number = ", val)
        except ValueError:
            try:
                # Convert it into float
                val = float(value)
                numberornot.append(1)
                vallist.append(val)
                #print("Input is a float  number. Number = ", val)
            except ValueError:
                numberornot.append(0)
                vallist.append(0)
                #print("No.. input is not a number. It's a string")
    if 0 in numberornot:
        return False,vallist
    else:
        return True,vallist

def showLabel():
    for index,channel in enumerate(channelOpt):
        if index%2 == 1:
            print('%2s: %-31s '% (channel['value'],channel['label']),end ="\n")
        else:
            print('%2s: %-31s '% (channel['value'],channel['label']),end =" ")

def getvaluelist():
    valuelist=[]
    for channel in channelOpt:
        valuelist.append(str(channel['value']))
    return valuelist

def getLabPar(value):
    for channel in channelOpt:
        if str(channel['value']) == str(value):
            return channel['label'],channel['SAPar']


def showPara(value,label,para,ptype="old"):
    if ptype == "new":
        print("\nThe new SA parameter of ",label,"is:")
    else:
        print(label,"located at CH",str(value),"and SA parameter is")
    print("Center Frequency(Hz):  ",para[0])
    print("SPAN(Hz):              ",para[1])
    print("Reference Lavel(dBm):  ",para[2])
    print("Scale(dB/div):         ",para[3])
    print("RBW(Hz):               ",para[4])
    print("VBW(Hz):               ",para[5])

def main():
    showLabel()
    while 1:
        choice = input("Input channel number you want to modified, h for help, q for exit:")
        #print("you choice" , value + "!")
        if choice == "q":
            return
        if choice == "h":
            os.system('clear')
            showLabel()
            print("There are total 44 channel connection to SA.")
        if str(choice) in getvaluelist():
            while 1:
                os.system('clear')
                label,oldPara=getLabPar(choice)
                showPara(choice,label,oldPara)
                print ("Do you like to modified the SA parameter of this cannel? ")
                choice2 = input("y for yes, n for channel choice, q for exit:")
                if choice2 in ("q", "quit","exit"):
                    os.system('clear')
                    return
                if choice2 in ("n", "no","No","NO"):
                    os.system('clear')
                    showLabel()
                    break
                if choice2 in ("y", "yes","YES"):
                    os.system('clear')
                    print("Please input the new parameter of",label,"\n")
                    newPara=[0,0,0,0,0,"a"]
                    newPara[0]=input("Center Frequency(Hz), old value is:"+str(oldPara[0])+" Hz, new value?:")
                    newPara[1]=input("SPAN(Hz), old value is:"+str(oldPara[1])+" Hz, newvalue?:")
                    newPara[2]=input("Reference Lavel(dBm), old value is:"+str(oldPara[2])+" dBm, new value?:")
                    newPara[3]=input("Scale (dBm/div), old value is:"+str(oldPara[3])+" dbm/div new value?:")
                    newPara[4]=input("RBW(Hz), old value is:"+str(oldPara[4])+" Hz, new value?:")
                    newPara[5]=input("VBW(Hz), old value is:"+str(oldPara[5])+" Hz, new value?:")
                    for index,newValue in enumerate(newPara):
                        if newValue == "":
                            newPara[index]=oldPara[index]
                    #check all nuber and saving
                    numberornot,newPara2=checkinput(newPara)
                    if numberornot == True:
                        #print("\n The new Parameter is ",newPara)
                        showPara(choice,label,newPara2,"new")
                        choice3 = input("Are you sure, the new value? (y for save):")
                        if choice3 in ("y", "yes","YES"):
                            saveintofile(label,choice,newPara2)
                            print ("Saving file now.")
                            return
                    else:
                        print("\nOne of the Parameter is not number, a number type is like 300, 3e8,-30")
                        input("press any key for input the value again:")

'''
                command="grep -n '"+label+"' ../module/channelTest.py | grep -v '#' | awk '{print $1}'"
                p = subprocess.Popen(command, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                line_number = int(p.decode().split(":\n")[0])
            #print(label,line_number)
            #newChanninInput(choice)
                insert_text0 = "# Edit by Johnson as script at 2024\n"
                insert_test1 = "#"
                insert_test2 = newChanninInput(choice)+"\n"
                # 讀取文件內容
                with open('../module/channelTest.py', 'r') as file:
                    lines = file.readlines()

                # 在指定行後插入文本
                lines.insert(line_number-1, insert_text0)
                lines.insert(line_number,   insert_test1)
                lines.insert(line_number+2, insert_test2)

                # 將修改後的內容寫回文件
                with open('../module/channelTest.py', 'w') as file:
                    file.writelines(lines)
                    '''


if __name__ == "__main__":
    main()
