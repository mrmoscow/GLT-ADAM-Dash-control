#!/home/obscon/bin/cpy3

import argparse
import subprocess
import sys
sys.path.append("../module")
import ReceiverADAM as RAD
#from channelOpt  import channelOpt
from channelTest  import channelOpt

def showByValue(value):
    for channel in channelOpt:
        if str(channel['value']) == str(value):
            print("The channel",str(value),"is",channel['label'],
                    "\n and the SA paramter is",channel['SAPar'])
            return channel['label']


def newChanninInput(value):
    for channel in channelOpt:
        if str(channel['value']) == str(value):
            a=channel['SAPar']
            text2=' {\'label\':\'%s\', \'value\':%s, \'gr\':\'%s\',' % (channel['label'],channel['value'],channel['gr'])
            #print('\'label\':\'%s\', \'value\':%s, \'gr\':' % (channel['label'],channel['value']))
            text3='\'SAPar\':[%.1e,%.1e,%d,%d,%.1e,%d]},' % (a[0],a[1],a[2],a[3],a[4],a[5])
            print (text2+text3)
            return text2+text3

def showByGroup(gr):
    for channel in channelOpt:
        if channel['gr'] == gr:
            print(channel['label'],"is at channel",channel['value'])

def showLabel():
    for index,channel in enumerate(channelOpt):
        if index%2 == 1:
            print('%2s: %-31s '% (channel['value'],channel['label']),end ="\n")
        else:
            print('%2s: %-31s '% (channel['value'],channel['label']),end =" ")


def main():
    #for i in channelOpt:
    #    print(i)
    grouplist=[]
    valuelist=[]
    for channel in channelOpt:
        label = channel['label']
        SAPar = channel['SAPar']
        gr=channel['gr']
        if gr not in grouplist:
            grouplist.append(gr)
        valuelist.append(str(channel['value']))
        #print(f"Label: {label}, SAPar: {SAPar}")
    #print(grouplist)
    #print(valuelist)
    showLabel()
    while 1:
        choice = input("Input which channel you want to modified, h for help, q for exit:")
        #print("you choice" , value + "!")
        if choice == "q":
            return
        if choice == "h":
            print("There are total 44 channel for cahngg \n",
                    "You can also input p1, p2, p3, and o")
        if str(choice) in valuelist:
            label=showByValue(choice)
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

            return
        if choice =='p1':
            showByGroup("P1A")


if __name__ == "__main__":
    main()
