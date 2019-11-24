#!/usr/bin/env python

"""show-attitude.py: Script to ask the MultiWii Board attitude and print it."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

from pymultiwii import MultiWii
from sys import stdout
import time

if __name__ == "__main__":


    board = MultiWii()
    board.start('/dev/ttyACM0')


    board.requestFrame(board.ATTITUDE)
    time.sleep(0.5)
    d = board.receivePacket('<3h', 6)
    if d:
        print '\nPitch:\t%.0f'%(float(d[1])/10.0)
        print 'Roll:\t%.0f'%(float(d[0])/10.0)
        print 'Yaw:\t%.0f'%(float(d[2]))
        print 'Test:\t',board.rx_attitude['angx']
    #printf(drone.sendFrame(drone.SET_RAW_RC, set_raw_rc, '<8H'), 1)
