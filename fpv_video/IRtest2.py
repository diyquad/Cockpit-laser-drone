import RPi.GPIO as GPIO
import time
import subprocess
from sys import stdout
import IRModule


def main():
    """Connection du IR RX1"""
    irRxPin = 4
    irRx = IRModule.IRRemote(callback='DECODE')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
    GPIO.setup(irRxPin,GPIO.IN)   # set irPin to input
    print('Starting IR remote sensing using DECODE function and verbose setting equal True ')
    GPIO.add_event_detect(irRxPin,GPIO.BOTH,callback=irRx.pWidth)
    irRx.set_verbose(False)
    irRx.set_callback(remote_callback)
    print('Use ctrl-c to exit program')

    while True:
        #Tirer()
        time.sleep(1)




def Tirer():
    subprocess.call(["/home/pi/fpv_video/rawCode2"])


'''
When IR Receiver detect message
means drone has been hit by other one.
'''
def remote_callback(codev):
    print('\r\r-----TOUCHER---')  # unknown code
    print 'Toucher #:\r'
    print codev
    return

if __name__ == '__main__':
    import sys
    try:
        main()

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
