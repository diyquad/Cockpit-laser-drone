'''
Create a FPV video preview
add a Cockpit to feed to be like in a plane
'''

import picamera
import time
import numpy
from PIL import Image, ImageDraw, ImageFont

def main():

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
       topOverlay = camera.add_overlay(pad.tobytes(), size=img.size)
       topOverlay.alpha = 128
       topOverlay.layer = 3

       time.sleep(0.5)
       try:
          while True:
              #topOverlayImage = pad.copy()
              #drawTopOverlay = ImageDraw.Draw(topOverlayImage)
              #drawTopOverlay.text((200, 15), topText, font=font, fill=(255, 0, 255))
              #topOverlay.update(topOverlayImage.tostring())
              time.sleep(1)

       except KeyboardInterrupt:
          camera.remove_overlay(topOverlay)
          print "Cancelled"


if __name__ == '__main__':
    import sys
    try:
        main()

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
