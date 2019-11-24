#!/usr/bin/env python

# Control Lasermodule from Raspberry Pi
# https://raspberrytips.nl/laser-module-aansturen-via-gpio/

import RPi.GPIO as GPIO
import time

LaserGPIO = 4 # --> PIN11/GPIO17

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LaserGPIO, GPIO.OUT)
    GPIO.output(LaserGPIO, GPIO.HIGH)

def loop():
    while True:
          print 'Laser=on'
          GPIO.output(LaserGPIO, GPIO.HIGH) # led on
          time.sleep(1.0)
          print 'Laser=off'
          GPIO.output(LaserGPIO, GPIO.LOW) # led off
          time.sleep(1.0)

def destroy():
    GPIO.output(LaserGPIO, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()

try:
    loop()

except KeyboardInterrupt:
    destroy()
