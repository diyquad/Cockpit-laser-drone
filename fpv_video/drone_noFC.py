#!/usr/bin/env python

'''
Drone noFC, no laserjust Cockpit and laser animation

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
from PIL import Image, ImageDraw, ImageFont
from sys import stdout
import RPi.GPIO as GPIO
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
    laserShot=None
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
       camera.start_preview(fullscreen=True,window=(0,0,480,640))
       #Add cockpit
       img = Image.open('/home/pi/fpv_video/cockpit.png')
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

       #Add Laser PNG for fire
       imgLaser = Image.open('/home/pi/fpv_video/laser.png')
       imgLaser = imgLaser.resize((640,480))
       laser = Image.new('RGBA', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
       laser.paste(imgLaser, (0, 0))
       laserOverlay = camera.add_overlay(laser.tobytes(), size=imgLaser.size,layer = 1)
       laserOverlay.alpha = 128

       #Add Explosion layer
       imgExpl = Image.open('/home/pi/fpv_video/explosion.png')
       imgExpl = imgExpl.resize((640,480))
       explosion = Image.new('RGBA', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
       explosion.paste(imgExpl, (0, 0))
       explOverlay = camera.add_overlay(explosion.tobytes(), size=imgExpl.size,layer = 1)
       explOverlay.alpha = 128

       try:
          while True:
              time.sleep(0.2)

       except KeyboardInterrupt:
          camera.remove_overlay(topOverlay)
          colorWipe(strip, Color(0, 0, 0), 0)  # Green wipe
          camera.close()
          vehicle.close()
          print "Cancelled"

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
