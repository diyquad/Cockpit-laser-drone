#Initial Pi Zero overlay + recording code

import picamera
import time
import numpy
from PIL import Image, ImageDraw, ImageFont


# Video Resolution
VIDEO_HEIGHT = 960
VIDEO_WIDTH = 1280

# Cross Hair Image
crossHair = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT))
crossHairPixels = crossHair.load()


with picamera.PiCamera() as camera:
   camera.resolution = (VIDEO_WIDTH, VIDEO_HEIGHT)
   camera.framerate = 30
   camera.led = False
   camera.start_preview(fullscreen=True,window=(0,0,720,1280))
   camera.start_recording('timestamped.h264')

   img = crossHair.copy()
   overlay = camera.add_overlay(img.tostring(), layer = 3, alpha = 100)

   time.sleep(1)
   try:
      while True:
         text = time.strftime('%H:%M:%S', time.gmtime())
         img = crossHair.copy()
         draw = ImageDraw.Draw(img)
         draw.font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 50)
         draw.rectangle([(0,0),(1280,100)], fill=(255,69,0), outline=None)
         draw.rectangle([(0,860),(1280,960)], fill=(255,69,0), outline=None)
         draw.text((600, 50), text, (255, 255, 255))
         draw.text((600, 910), text, (255, 255, 255))
         overlay.update(img.tostring())
         camera.wait_recording(0.9)

   finally:
      camera.remove_overlay(overlay)
      camera.stop_recording()
