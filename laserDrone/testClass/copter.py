#!/usr/bin/env python

"""copter.py: Class for copter"""

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

class Copter:

    """Class initialization"""
    def __init__(self, serPort):
        self.message = {'angx':0,'angy':0}
        self.camera = ();
        #Demarrage de la board
        self.board  = MultiWii("/dev/ttyACM0")

    def launchFPV(self):
        # Video Resolution
        VIDEO_HEIGHT = 960
        VIDEO_WIDTH = 1280

        with picamera.PiCamera() as self.camera:
           self.camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
           self.camera.framerate = 30
           self.camera.led = False
           overlay_renderer = None

           self.camera.start_preview(fullscreen=True,window=(0,0,720,1280))

           img = Image.open('cockpit.png')
           img = img.resize((1280,960))
           # Create an image padded to the required size with
           # mode 'RGB'
           pad = Image.new('RGBA', (
               ((img.size[0] + 31) // 32) * 32,
               ((img.size[1] + 15) // 16) * 16,
               ))
           pad.paste(img, (0, 0))
           # Add the overlay with the padded image as the source,
           # but the original image's dimensions
           topOverlay = self.camera.add_overlay(pad.tobytes(), size=img.size)
           overlay_renderer = 1
           topOverlay.alpha = 128
           topOverlay.layer = 3
           time.sleep(0.5)

    def closeFPV(self):
        self.camera.close()
