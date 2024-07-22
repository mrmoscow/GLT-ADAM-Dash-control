#!/home/obscon/bin/cpy3

import argparse
import sys

sys.path.append("../module")
import ReceiverADAM as RAD




def get_opt():
    parser = argparse.ArgumentParser(description="For retrun A30(6050 at B2 192.168.1.30)status")
    #parser.add_argument("-c","--channel", type=str, help="channel to SA  [1..44]",required=True)
    parser.add_argument('-i','--increase', type=int,
                      help='increase the attenuation by the value you input')
    parser.add_argument('-d','--decrease', type=int,
                        help='lower the attenuation by the value you input')
    parser.add_argument('-v', '--value', type=int,  help='The aattenuation value you want to set')
    args = parser.parse_args()
    return args.value,args.increase,args.decrease



def dec_to_6bit(n, invert=False):
    if n < 0 or n > 63:
        raise ValueError("Input must be between 0 and 63 inclusive.")
    # Convert the decimal number to a 6-bit binary string
    binary_representation = f"{n:06b}"
    # Convert the binary string to a list of integers
    binary_list = [int(bit) for bit in binary_representation]
    # If invert is True, invert the binary list
    if invert:
        binary_list = [1 - bit for bit in binary_list]
    return binary_list

# Test the function with various inputs
print(dec_to_6bit(0))           # Output: [0, 0, 0, 0, 0, 0]
print(dec_to_6bit(1))           # Output: [0, 0, 0, 0, 0, 1]
print(dec_to_6bit(40))          # Output: [1, 1, 1, 1, 1, 1]
#print(dec_to_6bit(0, invert=True))  # Output: [1, 1, 1, 1, 1, 1]
#print(dec_to_6bit(1, invert=True))  # Output: [1, 1, 1, 1, 1, 0]
#print(dec_to_6bit(40, invert=True)) # Output: [0, 0, 0, 0, 0, 0]



def bin_to_dec(binary_list, invert=False):
    if len(binary_list) != 6 or not all(bit in (0, 1) for bit in binary_list):
        raise ValueError("Input must be a list of six 0s and 1s.")
    # If invert is True, invert the binary list
    if invert:
        binary_list = [1 - bit for bit in binary_list]
    # Convert the binary list to a string
    binary_string = ''.join(map(str, binary_list))

    # Convert the binary string to a decimal number
    decimal_number = int(binary_string, 2)
    return decimal_number

# Test the function with various inputs
print(bin_to_dec([0, 0, 0, 0, 0, 0]))               # Output: 0
print(bin_to_dec([0, 0, 0, 0, 0, 1]))               # Output: 1
print(bin_to_dec([1, 1, 1, 1, 1, 1]))               # Output: 63
#print(bin_to_dec([0, 0, 0, 0, 0, 0], invert=True))  # Output: 63
#print(bin_to_dec([0, 0, 0, 0, 0, 1], invert=True))  # Output: 62
#print(bin_to_dec([1, 1, 1, 1, 1, 1], invert=True))  # Output: 0

value,increase,decrease = get_opt()

print('This script  help to check the A3 (6050)')
print('Start to checking the  of A3')

RAD.check_ADAM('A03')
result=RAD.get_6050('A03')
print(result[0:12])
print(result[12:])

#RAD.set_6050('A30',[1,0,0,0,0,0])
#RAD.set_6050('A30',dec_to_6bit(42))
result=RAD.get_6050('A03')
print(result[12:],list(map(int, result[12:])))
print(bin_to_dec(list(map(int, result[12:]))) )
oldvalue=int(bin_to_dec(list(map(int, result[12:]))))
print("The attenoue at A3 value before setting is",oldvalue )

if value is not None:
    print(f"The all value: {value}")
    RAD.set_6050('A03',dec_to_6bit(int(value)))
else:
    print("未傳入整數參數")

if increase is not None:
    print(f"increase value is : {increase}")
    RAD.set_6050('A03',dec_to_6bit(int(oldvalue+increase)))
else:
    print("No increase value ")

if decrease is not None:
    print(f"The decrease value is: {decrease}")
    RAD.set_6050('A03',dec_to_6bit(int(oldvalue-decrease)))
else:
    print("No decrease value ")

result=RAD.get_6050('A03')
print("The new A3 att value is",bin_to_dec(list(map(int, result[12:]))) )
