#!/usr/bin/python
# coding: utf-8

import wiringpi2
import sys
import os
import struct
from time import sleep

# ===========================================================================
# Munin Plugin - Pressure
# ===========================================================================

is_config = len(sys.argv) == 2 and sys.argv[1] == "config"

if is_config:
    print "graph_title Relative Humidity (I2C)"
    print "graph_vlabel percent(%)"
    print "graph_category sensors"
    print "graph_scale no"
    print "graph_args --upper-limit 100 -l 0"
    print "HDC1000humid.label percent (%)"
else:
    wiringpi2.wiringPiSetup()
    i2c = wiringpi2.I2C()
    dev = i2c.setup(0x40)
    i2c.writeReg16(dev,0x02,0x10)   # Temp + Hidi 32-bit transfer mode, LSB-MSB inverted, why?
    i2c.writeReg8(dev,0x00,0x00)    # start conversion.
    sleep((6350.0 + 6500.0 +  500.0)/1000000.0) # wait for conversion.
    # LSB-MSB inverted, again...
    temp = ((struct.unpack('4B', os.read(dev,4)))[0] << 8 | (struct.unpack('4B', os.read(dev,4)))[1])
    hudi = ((struct.unpack('4B', os.read(dev,4)))[2] << 8 | (struct.unpack('4B', os.read(dev,4)))[3])
    os.close(dev) #Don't leave the door open.
    print "HDC1000humid.value %.2f" % (( hudi / 65535.0 ) * 100)
#   print "Temperature %.2f" % (( temp  / 65535.0) * 165 - 40 )