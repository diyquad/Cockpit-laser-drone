#!/usr/bin/env python

import sys
import time
import serial

ser = serial.Serial("/dev/ttyAMA0" , baudrate=9600,  timeout=3.0)

while 1:
   x=ser.readline()
   print (x)
