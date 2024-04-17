#!/home/obscon/bin/cpy3

import argparse
import sys
sys.path.append("../module")
import ReceiverADAM as RAD



def get_opt():
    #parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="This script will init the A14 & A17 (set all DO to L)")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    #parser.add_argument("-r","--rx", type=str, help="Receiver [0,2,4,6]",required=True)
    #parser.add_argument('-i','--init', default=False, action='store_true')
    args = parser.parse_args()
    return None


init=get_opt()
print("Will start to init the A14 and A17")
print(RAD.CAB1417switch(0,'init'))
