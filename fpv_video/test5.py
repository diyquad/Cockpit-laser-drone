import picamera
from PIL import Image, ImageDraw, ImageFont
from time import sleep

textOverlayCanvas = Image.new("RGB", (704, 60))
# Use Roboto font (must be downloaded first)
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSerif.ttf", 20)
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()

    # Load the arbitrarily sized image
    img = Image.open('chapeau.png')
    # Create an image padded to the required size with
    # mode 'RGB'
    topText = 'coucou'
    pad = Image.new('RGB', (
        ((img.size[0] + 31) // 32) * 32,
        ((img.size[1] + 15) // 16) * 16,
        ))
    # Paste the original image into the padded one
    #pad.paste(img, (0, 0))
    textOverlayCanvas.paste
    # Add the overlay with the padded image as the source,
    # but the original image's dimensions
    topOverlay = camera.add_overlay(pad.tostring(), size=img.size, layer=3, alpha=128,window=(0,20,704,60))


    # Wait indefinitely until the user terminates the script
    while True:
        topOverlayImage = textOverlayCanvas.copy()

        drawTopOverlay = ImageDraw.Draw(topOverlayImage)
        drawTopOverlay.text((200, 15), topText, font=font, fill=(255, 0, 255))

        topOverlay.update(topOverlayImage.tostring())


        sleep(1)
