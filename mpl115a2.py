#!/usr/bin/python
# -*- coding: utf-8 -*-

import smbus
import time

def convert_coefficient(msb, lsb, total_bits, fractional_bits, zero_pad):
    data = (msb << 8) | lsb
    period = float(1 << 16 - total_bits + fractional_bits + zero_pad)

    if (msb >> 7) == 0:
        result = float(data / period)
    else:
        result = -float(((data ^ 0xFFFF) + 1) / period)

    return result

def get_hectopascal():

    i2c = smbus.SMBus(1)
    address = 0x60

    i2c.write_byte_data(address, 0x12, 0x01)
    time.sleep(0.003)

    block = i2c.read_i2c_block_data(address, 0x00, 12) 

    a0 = convert_coefficient(block[4], block[5], 16, 3, 0)
    b1 = convert_coefficient(block[6], block[7], 16, 13, 0)
    b2 = convert_coefficient(block[8], block[9], 16, 14, 0)
    c12 = convert_coefficient(block[10], block[11], 14, 13, 9)

    padc = (block[0] << 8 | block[1]) >> 6
    tadc = (block[2] << 8 | block[3]) >> 6

    c12x2 = c12 * tadc
    a1 = b1 + c12x2
    a1x1 = a1 * padc
    y1 = a0 + a1x1
    a2x2 = b2 * tadc
    pcomp = y1 + a2x2

    pressure = (pcomp * 65 / 1023) + 50
    hectopascal = pressure * 10

    return hectopascal

print get_hectopascal()