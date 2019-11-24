#Initial Pi Zero overlay + recording code

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

       crosshairImg = Image.open('red-crosshair-png-2.png')
       crosshairImg = crosshairImg.resize((100,100))
       sizeH = (VIDEO_HEIGHT/2) - 50
       sizeW = (VIDEO_WIDTH/2) - 50

       crossHair.paste(crosshairImg, (sizeW,sizeH))

       img = crossHair.copy()
       #overlay_renderer = camera.add_overlay(img.tostring(), layer = 3, alpha = 100)


       time.sleep(0.5)
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
             if not overlay_renderer:
                 overlay_renderer = camera.add_overlay(img.tobytes(), layer = 3, alpha = 100)
             else:
                 overlay_renderer.update(img.tobytes())

             time.sleep(1)

       finally:
          camera.remove_overlay(overlay_renderer)

if __name__ == '__main__':
    import sys
    try:
        main()
    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
