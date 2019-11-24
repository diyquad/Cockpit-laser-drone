#!/usr/bin/env python
# -*- coding: windows-1250 -*-

import sys
import picamera
import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

os.system("clear")
def main():

	# initialise picamera
	with picamera.PiCamera() as camera:
		camera.resolution = (1024, 768)
		camera.rotation   = 180
		camera.crop       = (0.0, 0.0, 1.0, 1.0)

		# display camera preview
		camera.start_preview()
		# realtime updates the overlayed layer
		overlay_renderer = None
		while True:
			with open ("source.txt", "r") as myfile:
				data=myfile.read()
			img = Image.new("RGB", (1024, 768))
			text = time.strftime('%d.%m.%y-%H:%M:%S', time.gmtime())
			fontpath = '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'
			draw = ImageDraw.Draw(img)
			draw.font = ImageFont.truetype(fontpath, 16, encoding='unic')
			draw.multiline_text((10,10), text.decode('utf-8'), (255, 255, 255))
			draw.multiline_text((20,30), data.decode('utf-8') , (255, 255, 255))
			if not overlay_renderer:
				overlay_renderer = camera.add_overlay(img.tobytes(),
				layer=3,
				size=img.size,
				alpha=128);
			else:
				overlay_renderer.update(img.tobytes())

if __name__ == '__main__':
	import sys
	try:
		main()
	except:
		print 'Unexpected error... : ', sys.exc_info()[0], sys.exc_info()[1]
