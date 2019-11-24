import pylirc
import time
import RPi.GPIO as GPIO
print "Setting up GPIO"
LED_PIN = 24 #ledje aanzetten
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, True)


sockid = pylirc.init("myProg","/home/pi/.lircrc")
while True:
    s = pylirc.nextcode(1)

    while(s):
    	for (code) in s:
            print 'Command: ', code["config"] #For debug: Uncomment this
            #				line to see the return value of buttons
    	if(not blocking):
    		s = pylirc.nextcode(1)
    	else:
    		s = []
