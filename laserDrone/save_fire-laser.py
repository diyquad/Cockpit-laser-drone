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
from pymultiwii import MultiWii
from sys import stdout
import RPi.GPIO as GPIO
import IRModule

#global hit #number of time drone was hit
hit=0
fire=1
vivant=1
laserOverlay=None
camera=None

def main():
    global laserOverlay,camera,hit,vivant
    laserShot=None
    board = MultiWii("/dev/ttyACM0")
    """Creation de la video"""
    # Video Resolution
    VIDEO_HEIGHT = 960
    VIDEO_WIDTH = 1280
    # Cross Hair Image
    crossHair = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT),(0, 0, 0, 0))
    crossHairPixels = crossHair.load()
    with picamera.PiCamera() as camera:
       camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
       camera.framerate = 30
       camera.led = False
       overlay_renderer = None
       camera.start_preview(fullscreen=True,window=(0,0,720,1280))
       #Add cockpit
       img = Image.open('cockpit.png')
       img = img.resize((1280,960))

       # Add cockpit Image to FPV feed
       pad = Image.new('RGBA', (
           ((img.size[0] + 31) // 32) * 32,
           ((img.size[1] + 15) // 16) * 16,
           ))
       pad.paste(img, (0, 0))
       topOverlay = camera.add_overlay(pad.tobytes(), size=img.size)
       topOverlay.alpha = 128
       topOverlay.layer = 3

       #Add Laser PNG for fire
       imgLaser = Image.open('laser-fire.png')
       imgLaser = imgLaser.resize((1280,960))
       laser = Image.new('RGBA', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
       laser.paste(imgLaser, (0, 0))
       laserOverlay = camera.add_overlay(laser.tobytes(), size=imgLaser.size,layer = 1)
       laserOverlay.alpha = 128
       #laserOverlay.layer = 2

       #Add Explosion layer
       imgExpl = Image.open('explosion.png')
       imgExpl = imgExpl.resize((1280,960))
       explosion = Image.new('RGBA', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
       explosion.paste(imgExpl, (0, 0))
       explOverlay = camera.add_overlay(explosion.tobytes(), size=imgExpl.size,layer = 1)
       explOverlay.alpha = 128

       time.sleep(0.1)

       """Connection de la board Inav Mavlink"""

       board.getData(MultiWii.ATTITUDE)
       #print board.attitude #uncomment for regular printing
       message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(board.attitude['angx']),float(board.attitude['angy']),float(board.attitude['heading']),float(board.attitude['elapsed']))
       stdout.write("\r%s" % message )
       print "\r"


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
       irTxPin = 21 # --> PIN11/GPIO17
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(irTxPin, GPIO.OUT)
       GPIO.output(irTxPin, GPIO.HIGH)

       """----"""

       try:
          while True:
               while vivant==1:
                   if(hit>=4):
                       GPIO.output(irTxPin, GPIO.LOW)
                       explOverlay.layer = 5
                       vivant=0
                       print "Fin - Toucher #",hit, "fois"



       except KeyboardInterrupt:
          camera.remove_overlay(topOverlay)
          print "Cancelled"


def remote_callback(code):
    global hit,laserOverlay,vivant
    print('\r\r-----TOUCHER---')  # unknown code
    laserOverlay.layer = 4
    time.sleep(0.2)
    laserOverlay.layer = 2
    hit=hit+1
    print "Hit #:",hit,"\r"
    return

if __name__ == '__main__':
    import sys
    try:
        main()

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
