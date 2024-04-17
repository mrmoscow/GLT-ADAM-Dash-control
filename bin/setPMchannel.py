#!/home/obscon/bin/cpy3

import argparse
import sys

sys.path.append("../module")
import ReceiverADAM as RAD



def get_opt():
    parser = argparse.ArgumentParser(description="For set the input channel to PowerMeter")
    parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    args = parser.parse_args()
    return args.channel

def main():
    channel = get_opt()
    channel=int(channel)
    print("Will set channel",channel," to PowerMeter")
    print(RAD.CAB1417switch(channel,'PM'))


if __name__ == "__main__":
    main()
