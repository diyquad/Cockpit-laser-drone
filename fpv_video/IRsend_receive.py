import RPi.GPIO as GPIO
import time
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
    #irRx.set_verbose(False)
    #irRx.set_callback(remote_callback)
    print('Use ctrl-c to exit program')

    """Connection du IR RX2"""
    irRxPin2 = 20
    irRx2 = IRModule.IRRemote(callback='DECODE')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
    GPIO.setup(irRxPin2,GPIO.IN)   # set irPin to input
    print('Starting IR remote sensing using DECODE function and verbose setting equal True ')
    GPIO.add_event_detect(irRxPin2,GPIO.BOTH,callback=irRx2.pWidth)
    irRx2.set_verbose(False)
    irRx2.set_callback(remote_callback)

    """Connection du IR TX"""
    irTxPin = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(irTxPin, GPIO.OUT)
    GPIO.output(irTxPin, GPIO.LOW)


    while True:
        GPIO.output(irTxPin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(irTxPin, GPIO.LOW)
        time.sleep(1)





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
