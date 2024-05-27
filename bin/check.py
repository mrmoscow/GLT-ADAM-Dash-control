#!/home/obscon/bin/cpy3

import argparse
import sys

sys.path.append("../module")
import ReceiverADAM as RAD

def get_opt():
    parser = argparse.ArgumentParser(description="For checking all things")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-i','--info', default=False, action='store_true',help="using in future.")
    args = parser.parse_args()
    return args.info


para = get_opt()
#channel=int(channel)

#def adamitem(IPList):
#    return [{k : v} if k[0] == 'A' for k, v in IPList.items()}]


#print(RAD.ADAM_list)
'''
for key, value in RAD.ADAM_list.items():
    if key[0] == 'A':
        print(key, value)
'''

a={k:v for k,v in RAD.ADAM_list.items() if k[0]=='A'}
b={k:v for k,v in RAD.ADAM_list.items() if k[0]!='A'}

print(a)
print(b)


#print(RAD.ADAM_list)



#print()
