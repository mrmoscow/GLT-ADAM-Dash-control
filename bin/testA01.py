from os.path import exists
import sys
print(sys.version)
print(sys.version_info)
print(sys.version_info[1])
if sys.version_info[1] == 7:
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient
if sys.version_info[1] == 11:
    from pymodbus.client import ModbusTcpClient as ModbusClient

ADAM_list={"A01":'192.168.1.207',\
           "A03":'192.168.1.201',\
           "A10":'192.168.1.217',\
           "A11":'192.168.1.206',\
           "A14":'192.168.1.208',\
           "PM4":'192.168.1.219'}

coil_list={"S2":32,"S3":48,"S4":64,"S5":80}

adam_delay = 0.25

def get_5056(machine,card_at='S3'):
    co=ModbusClient(ADAM_list[machine],port=502,timeout=10)
    if not co.connect():      # True / False
        return 'Error 01'
    print("Modbus link success",co)
    r = co.read_coils(coil_list[card_at],16,unit=1,slave=1)
    print("reading coils success", r)
    intvalue=r.bits
    b0=''.join(["0, " if i==0 else "1, " for i in intvalue])
    print("got B0 succesfuel")
    co.close()
    return b0



print("The A1 have 5017, 5018,5024,5056")

print("Next is the valud from 5056")
print(get_5056('A01'))

