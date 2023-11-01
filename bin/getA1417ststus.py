#!/home/obscon/bin/cpy3

import argparse
import sys
sys.path.append("..")
import ReceiverADAM as RAD

def get_opt():
    parser = argparse.ArgumentParser(description="For return A14 A17  status")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-i','--info', default=False, action='store_true',help="for future showing the info  of A14 and A17")
    args = parser.parse_args()
    return args.info


para = get_opt()

if 'Bad' in RAD.check_ADAM('A14'): sys.exit("Error A14 is not conection")
if 'Bad' in RAD.check_ADAM('A17'): sys.exit("Error A17 is not conection")


print("The A14/17 have 5017, 5018,and 4*5056")

print("From A14-5017:",RAD.get_5017('A14'))

print("From A14-5018:",RAD.get_5018('A14'))

print("Next is the DO valud of 4*5056 on A14")
print(RAD.get_5056('A14','S2'))
print(RAD.get_5056('A14','S3'))
print(RAD.get_5056('A14','S4'))
print(RAD.get_5056('A14','S5'))

print("From A17-5017:",RAD.get_5017('A17'))

print("From A17-5018:",RAD.get_5018('A17'))

print("Next is the DO valud of 4*5056 on A17")
print(RAD.get_5056('A17','S2'))
print(RAD.get_5056('A17','S3'))
print(RAD.get_5056('A17','S4'))
print(RAD.get_5056('A17','S5'))
