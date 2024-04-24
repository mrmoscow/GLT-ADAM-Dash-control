#!/home/obscon/bin/cpy3

import argparse
import sys
sys.path.append("../module")
import ReceiverADAM as RAD
from channelTest  import channelOpt

def main():
    #for i in channelOpt:
    #    print(i)
    for channel in channelOpt:
        label = channel['label']
        SAPar = channel['SAPar']
        print(f"Label: {label}, SAPar: {SAPar}")


    
    # 要更改的 label
    target_label = 'EHTT_POL0 IF 4-9 GHz'

    # 新的 SAPar 值
    new_SAPar = [9E9, 2E10, -50, 6, 5E6, 500]  # 這裡只是一個示例

    # 遍歷 channelOpt 列表
    for channel in channelOpt:
        if channel['label'] == target_label:
            # 找到目標 label，進行修改
            channel['SAPar'] = new_SAPar
            break

    # 將修改後的內容寫回檔案
    with open('../module/channelTest.py', 'a') as file:
        file.write("channelOpt = [\n")
        for channel in channelOpt:
            file.write("    " + str(channel) + ",\n")
        file.write("  ]\n")

if __name__ == "__main__":
    main()
