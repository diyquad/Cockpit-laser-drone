#!/usr/bin/env python

'''
Create a FPV video feed with a cockpit
And Manage a Quadcopter to fire and get shot by another drone
with IR
After 4 strike drone has to land.

'''
__author__ = "DIYQuad"
__copyright__ = "Copyright 2019 diyquad"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "diyquad"
__email__ = "diyquad@gmail.com"
__status__ = "Development"

import picamera
import time
#import numpy
from PIL import Image, ImageDraw, ImageFont
from sys import stdout
import RPi.GPIO as GPIO
import IRModule
from dronekit import connect, VehicleMode
from rpi_ws281x import Color, PixelStrip, ws

#global hit #number of time drone was hit
strike=0
fire=1
vivant=1
laserOverlay=None
explOverlay=None
camera=None
vehicle = None
LED_COUNT = 4        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.WS2811_STRIP_RGB

def main():
    global laserOverlay,explOverlay,camera,strike,vivant,vehicle
    """LED strip configuration"""
    print "led"
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    colorWipe(strip, Color(255, 255, 255), 0)  # Green wipe
    print "led ok"
    laserShot=None
    """Connexion to drone"""
    connection_string = "/dev/ttyACM0"
    vehicle = connect(connection_string, wait_ready=False)
    if vehicle.armed:
        print "Vehicule armed"
    # Create PixelStrip object with appropriate configuration.

    # Intialize the library (must be called once before other functions).
    strip.begin()
    """Creation de la video"""
    # Video Resolution
    VIDEO_HEIGHT = 480
    VIDEO_WIDTH = 640
    # Cross Hair Image
    crossHair = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT),(0, 0, 0, 0))
    crossHairPixels = crossHair.load()
    with picamera.PiCamera() as camera:
       camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
       camera.rotation = 180
       camera.framerate = 30
       camera.led = False
       overlay_renderer = None
       camera.start_preview(fullscreen=True,window=(0,0,720,1280))
       #Add cockpit
       img = Image.open('cockpit.png')
       img = img.resize((640,480))
       # Add cockpit Image to FPV feed
       pad = Image.new('RGBA', (
           ((img.size[0] + 31) // 32) * 32,
           ((img.size[1] + 15) // 16) * 16,
           ))
       pad.paste(img, (0, 0))
       cockiptOverlay = camera.add_overlay(pad.tobytes(), size=img.size)
       cockiptOverlay.alpha = 128
       cockiptOverlay.layer = 3

       topText = "Alt: 310m       Spd: 45km/h         Dir: N"
       textOverlayCanvas = Image.new("RGBA", (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
        # Use Roboto font (must be downloaded first)
       font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)
       topOverlay = camera.add_overlay(pad.tobytes(), size=img.size)
       topOverlay.alpha = 128
       topOverlay.layer = 4
       print "im"
       topOverlayImage = textOverlayCanvas.copy()
       topOverlay = camera.add_overlay(pad.tobytes(), size=(640,60), layer=3, alpha=128, fullscreen=False, window=(0,20,640,60))
       print "im"

       #Add Laser PNG for fire
       imgLaser = Image.open('laser.png')
       imgLaser = imgLaser.resize((640,480))
       laser = Image.new('RGBA', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
       laser.paste(imgLaser, (0, 0))
       laserOverlay = camera.add_overlay(laser.tobytes(), size=imgLaser.size,layer = 1)
       laserOverlay.alpha = 128

       #Add Explosion layer
       imgExpl = Image.open('explosion.png')
       imgExpl = imgExpl.resize((640,480))
       explosion = Image.new('RGBA', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
       explosion.paste(imgExpl, (0, 0))
       explOverlay = camera.add_overlay(explosion.tobytes(), size=imgExpl.size,layer = 1)
       explOverlay.alpha = 128

       time.sleep(0.1)

       """Connection de la board Inav Mavlink"""
       print "RC Channels:",vehicle.channels

       """Connection du IR RX"""
       irRxPin = 16
       irRx = IRModule.IRRemote(callback='DECODE')
       GPIO.setwarnings(False)
       GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
       GPIO.setup(irRxPin,GPIO.IN)   # set irPin to input
       GPIO.add_event_detect(irRxPin,GPIO.BOTH,callback=irRx.pWidth)
       irRx.set_verbose(False)
       #Set function to be call when a IR message is received (drone has been hit)
       irRx.set_callback(drone_Hit)

       """Connection du IR TX"""
       irTxPin = 21
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(irTxPin, GPIO.OUT)
       GPIO.output(irTxPin, False)
       """--Gestion des LEDS--"""


       try:
          print " System status: %s" % vehicle.system_status.state
          print "--->Lancement du drone<---"
          colorWipe(strip, Color(255, 0, 0), 0)  # Green wipe
          while True:
              #print vehicle.channels,"\r"
              time.sleep(0.1)
              if (vehicle.channels['7']>1100):
                  #fire
                  print "\rFIRE\r"
                  print vehicle.channels
                  laserOverlay.layer = 5
                  GPIO.output(irTxPin, True)
                  time.sleep(0.2)
                  laserOverlay.layer = 1
                  GPIO.output(irTxPin, False)
              if (strike>=4):
                  #check number of impact on our drone
                  explOverlay.layer = 5
                  vivant=0
                  print "End striked ",strike, "times"
                  time.sleep(3)
                  explOverlay.layer = 1
                  strike=0




       except KeyboardInterrupt:
          camera.remove_overlay(topOverlay)
          colorWipe(strip, Color(0, 0, 0), 0)  # Green wipe
          camera.close()
          vehicle.close()
          print "Cancelled"

'''
When IR Receiver detect message
means drone has been hit by other one.
'''
def drone_Hit(code):
    if code==-1 or code==0:
        return
    global strike,laserOverlay,vivant,vehicule
    print('\r\r-----YOU GOT HIT---',code)  # unknown code
    strike=strike+1
    print "Strike #:",strike,"\r"
    return

'''
# Define functions which animate LEDs in various ways.
'''
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

if __name__ == '__main__':
    import sys
    try:
        main()

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
