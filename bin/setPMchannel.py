#! /usr/bin/python3

import argparse
from os.path import exists
import sys
sys.path.append("..")
import ReceiverADAM as RAD


def get_opt():
    parser = argparse.ArgumentParser(description="For set the input channel to PowerMeter")
    parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    args = parser.parse_args()
    return args.channel


channel = get_opt()
channel=int(channel)
print("Will set channel",channel," to PowerMeter")
print(RAD.CAB1417switch(channel,'PM'))
