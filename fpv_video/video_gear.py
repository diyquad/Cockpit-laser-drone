from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
import cv2

stream = VideoGear(source=0).start() #Open live webcam video stream on first index(i.e. 0) USB device

writer = WriteGear(output_filename = 'Output.mp4') #Define writer with output filename 'Output.mp4'

# infinite loop
while True:

	frame = stream.read()
	# read frames

	# check if frame is None
	if frame is None:
		#if True break the infinite loop
		break

	# do something with frame here

	# write frame to writer
        writer.write(frame)

        # Show output window
	cv2.imshow("Output Frame", frame)

	key = cv2.waitKey(1) & 0xFF
	# check for 'q' key-press
	if key == ord("q"):
		#if 'q' key-pressed break out
		break

cv2.destroyAllWindows()
# close output window

stream.stop()
# safely close video stream
writer.close()
# safely close writer
