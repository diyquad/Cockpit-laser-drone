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

    board = MultiWii("/dev/ttyACM0")
    i=0
    try:
        while True:
            print "\r ####Boucle ",i
            v = board.getData(MultiWii.RC)
            r = board.rcChannels['roll']
            p = board.rcChannels['pitch']
            y = board.rcChannels['yaw']
            t = board.rcChannels['throttle']
            aux1 = board.rcChannels['aux1']
            aux2 = board.rcChannels['aux2']
            aux3 = board.rcChannels['aux3']
            aux4 = board.rcChannels['aux4']
            print "V==>",v
            if(i>5 and i<15 and v!=None):
                print "\r\r#########\r"
            	datas = [1500,1500,1800,1500]
                print "\rsend =",datas
                board.sendCMDreceiveATT(16,MultiWii.SET_RAW_RC,datas)
            	print "###########\r\r"
                time.sleep(1)

            i=i+1

    except Exception,error:
        print "Error on Main: "+str(error)
