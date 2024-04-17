#!/home/obscon/bin/cpy3

import argparse
import sys

sys.path.append("../module")
import ReceiverADAM as RAD


def get_opt():
    parser = argparse.ArgumentParser(description="For set the A44, A45 to Rx")
    parser.add_argument("-c","--channel", type=str, help="Rx channel, 1 for 86Rx, 2 for 230Rx, 3 for 345Rx, 4 for BackupRx, 0 for set all DO to O.",
    required=True)
    #parser.add_argument('-p','--para', default=False, action='store_true',help="also change the parameter of SA")
    args = parser.parse_args()
    return args.channel


channel = get_opt()
channel=int(channel)

print("Will set A44 to ",channel)
print(RAD.setN_6260("A44_ReSl",channel))


print("Will set A45 to ",channel)
print(RAD.setN_6260("A45_ReSl",channel))
