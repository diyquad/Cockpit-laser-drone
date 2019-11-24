#!/usr/bin/env python

"""drone.py: le drone pi+inav+Ir laser game"""
'''
Create a FPV video preview
add a Cockpit to feed to be like in a plane
'''
__author__ = "Elie"
__copyright__ = "Copyright 2019 Elie"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Elie"
__email__ = "xxx@gmail.com"
__status__ = "Development"

import picamera
import time
import numpy
from PIL import Image, ImageDraw, ImageFont
from sys import stdout
import RPi.GPIO as GPIO
import IRModule
from dronekit import connect, VehicleMode

#global hit #number of time drone was hit
strike=0
fire=1
vivant=1
laserOverlay=None
explOverlay=None
camera=None
vehicle = None

def main():
    global laserOverlay,explOverlay,camera,strike,vivant,vehicle
    laserShot=None
    connection_string = "/dev/ttyACM0"
    vehicle = connect(connection_string, wait_ready=False)
    if vehicle.armed:
        print "Vehicule armed"
    print " System status: %s" % vehicle.system_status.state

    """Connection du IR RX"""
    irRxPin = 16
    irRx = IRModule.IRRemote(callback='DECODE')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
    GPIO.setup(irRxPin,GPIO.IN)   # set irPin to input
    print('Starting IR remote sensing using DECODE function and verbose setting equal True ')
    GPIO.add_event_detect(irRxPin,GPIO.BOTH,callback=irRx.pWidth)
    irRx.set_verbose(False)
    irRx.set_callback(remote_callback)
    print('Use ctrl-c to exit program')

    """Connection du IR TX"""
    irTxPin = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(irTxPin, GPIO.OUT)
    GPIO.output(irTxPin, GPIO.LOW)


    """----"""
    try:
      while True:
          if (board.rcChannels['aux3']>1500):
              #fire
              GPIO.output(irTxPin, GPIO.HIGH)
              time.sleep(0.2)
              laserOverlay.layer = 1
              GPIO.output(irTxPin, GPIO.LOW)
          if (strike>=4):
              #check number of impact on our drone
              explOverlay.layer = 5
              vivant=0
              print "End striked ",hit, "times"
              time.sleep(3)

    except KeyboardInterrupt:
      camera.remove_overlay(topOverlay)
      print "Cancelled"

'''
When IR Receiver detect message
means drone has been hit by other one.
'''
def remote_callback(code):
    global hit,laserOverlay,vivant,vehicule
    print('\r\r-----YOU GOT HIT---')  # unknown code
    strike=strike+1
    print "Strike #:",strike,"\r"
    #get actual values from RC
    vehicle.mode = VehicleMode("Circle")

    start = time.time()
    #to overide RC need to set cmd for more than 1sec
    while elapsed < 1:
        board.sendCMD(8,MultiWii.SET_RAW_RC,data)
        elapsed = time.time() - start
        time.sleep(0.3)
    #put back initial RC values or get stick values
    data = [rc_values['roll'],rc_values['pitch'],rc_values['yaw'],rc_values['throttle'] ]
    board.sendCMD(8,MultiWii.SET_RAW_RC,data)
    return

if __name__ == '__main__':
    import sys
    try:
        main()

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]



'''
board.getData(MultiWii.ATTITUDE)
message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(board.attitude['angx']),float(board.attitude['angy']),float(board.attitude['heading']),float(board.attitude['elapsed']))
stdout.write("\r%s" % message )
print "\r"

p = board.rcChannels['pitch']
r = board.rcChannels['roll']
y = board.rcChannels['yaw']
t = board.rcChannels['throttle']
print "throlle:",t, "yaw:",y,"pitch:",p," roll:",r
print "\r"


if vivant==1:
    if(hit>=4):
        GPIO.output(irTxPin, GPIO.LOW)
        explOverlay.layer = 5
        vivant=0
        print "Fin - Toucher #",hit, "fois"
time.sleep(0.1)
'''
