import serial
import time
import math
from crcmod import mkCrcFun
from binascii import unhexlify


def crc16_modbus(s):
    crc16 = mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    return get_crc_value(s, crc16)


def get_crc_value(s, crc16):
    data = s.replace(' ', '')
    crc_out = hex(crc16(unhexlify(data))).upper()
    str_list = list(crc_out)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = ''.join(str_list[2:])
    return crc_data[:2] + ' ' + crc_data[2:]


def pressure_input_transform(num1=0, num2=0, num3=0, num4=0):
    p1 = hex(math.ceil(num1 / 0.6 * 409.5))
    p2 = hex(math.ceil(num2 / 0.6 * 409.5))
    p3 = hex(math.ceil(num3 / 0.6 * 409.5))
    p4 = hex(math.ceil(num4 / 0.6 * 409.5))

    str1 = p1[2:len(p1)].zfill(4)
    str2 = p2[2:len(p2)].zfill(4)
    str3 = p3[2:len(p3)].zfill(4)
    str4 = p4[2:len(p4)].zfill(4)

    str5 = crc16_modbus('01' + '10' + '00' + '01' + '00' + '04' + '08' + str1 + str2 + str3 + str4)
    crc_h = str5[3:5]
    crc_l = str5[0:2]

    return '01' + '10' + '00' + '01' + '00' + '04' + '08' + str1 + str2 + str3 + str4 + crc_h + crc_l


if __name__ == '__main__':
    s = serial.Serial('/dev/ttyUSB0', 9600, bytesize=8, stopbits=1, parity='N')
    d = bytes.fromhex(pressure_input_transform(0.25, 0, 0, 0))

    a = s.write(d)

    time.sleep(2)  # must stop
    s.close()

