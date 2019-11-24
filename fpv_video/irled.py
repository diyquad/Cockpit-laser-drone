import time
import RPi.GPIO as GPIO
import IRModule

def main():
    try:
        """Connection du IR RX"""
        irRxPin = 16
        irRx = IRModule.IRRemote(callback='DECODE')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
        GPIO.setup(irRxPin,GPIO.IN)   # set irPin to input
        GPIO.add_event_detect(irRxPin,GPIO.BOTH,callback=irRx.pWidth)
        irRx.set_verbose(False)
        #Set function to be call when a IR message is received (drone has been hit)
        irRx.set_callback(drone_Hit)

        '''while True:
            time.sleep(1)'''
        """Connection du IR TX"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.OUT)
        while True:
            GPIO.output(27, GPIO.HIGH) # led on
            time.sleep(1)
            GPIO.output(27, GPIO.LOW) # led on

    except KeyboardInterrupt:
        # here you put any code you want to run before the program
        # exits when you press CTRL+C
        print "exit\n" # print value of counter


    finally:
        GPIO.cleanup() # this ensures a clean exit

def drone_Hit(code):
    print('\r\r-----YOU GOT HIT---',code)  # unknown code
    print "Strike #:\r"
    return

if __name__ == '__main__':
    import sys
    try:
        main()

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
