import RPi.GPIO as GPIO
import time

LaserGPIO = 21

print "Debut envoi"
GPIO.setmode(GPIO.BCM)
GPIO.setup(LaserGPIO, GPIO.OUT)
while True:
    print 'Laser=on'
    GPIO.output(LaserGPIO, GPIO.HIGH)
    time.sleep(1)
    print 'Laser=off'
    GPIO.output(LaserGPIO, GPIO.LOW)
    time.sleep(1)
