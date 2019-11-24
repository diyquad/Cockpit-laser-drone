#!/usr/bin/python

import picamera
import time
import numpy as np
import string
import random
import os

from PIL import Image, ImageDraw, ImageFont

# Video Resolution for recording
VIDEO_HEIGHT = 720
VIDEO_WIDTH = 1280

baseDir='/home/pi/fpv_video/' # directory where the video will be recorded

os.system('clear') # clear the terminal from any other text

# Create empty images to store text overlays


# Use Roboto font (must be downloaded first)
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)

with picamera.PiCamera() as camera:
   camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
   camera.framerate = 25
   camera.led = False
   camera.start_preview()

   topText = "Alt: 310m       Spd: 45km/h         Dir: N"

   img = Image.open('cockpit.png')
   # Create an image padded to the required size with
   # mode 'RGB'
   pad = Image.new('RGBA', (
       ((img.size[0] + 31) // 32) * 32,
       ((img.size[1] + 15) // 16) * 16,
       ))
   pad.paste(img, (0, 0))
   # Add the overlay with the padded image as the source,
   # but the original image's dimensions
   topOverlay = camera.add_overlay(pad.tobytes(), size=img.size)
   topOverlay.alpha = 128
   topOverlay.layer = 3

   try:
      while True:
         topOverlayImage = pad.copy()

         drawTopOverlay = ImageDraw.Draw(topOverlayImage)
         drawTopOverlay.text((200, 15), topText, font=font, fill=(255, 0, 255))

         topOverlay.update(topOverlayImage.tostring())


         time.sleep(1)

   except KeyboardInterrupt:
      camera.remove_overlay(topOverlay)

      print "Cancelled"

   finally:
      camera.remove_overlay(topOverlay)
