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
    #board = MultiWii("/dev/serial0")
    #board.sendCMD(8,MultiWii.RESET_CONF,[])

    try:
        while True:
            board.getData(MultiWii.ATTITUDE)
            #print board.attitude #uncomment for regular printing
            # Fancy printing (might not work on windows...)
            message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(board.attitude['angx']),float(board.attitude['angy']),float(board.attitude['heading']),float(board.attitude['elapsed']))
            stdout.write("\r ATTITUDE: %s" % message )
            print "\r"
            board.getData(MultiWii.RAW_IMU)
            message = "ax = {:+.0f} \t ay = {:+.0f} \t az = {:+.0f} gx = {:+.0f} \t gy = {:+.0f} \t gz = {:+.0f} mx = {:+.0f} \t my = {:+.0f} \t mz = {:+.0f} \t elapsed = {:+.4f} \t" .format(float(board.rawIMU['ax']),float(board.rawIMU['ay']),float(board.rawIMU['az']),float(board.rawIMU['gx']),float(board.rawIMU['gy']),float(board.rawIMU['gz']),float(board.rawIMU['mx']),float(board.rawIMU['my']),float(board.rawIMU['mz']),float(board.attitude['elapsed']))
            stdout.write("\r RAW IMU: %s" % message )

            print "\r GPS",board.getData(MultiWii.RAW_GPS)
            #board.arm()
            # End of fancy printing
            #print "-->debut rc channel"
            #       ROLL/PITCH/YAW/THROTTLE/AUX1/AUX2/AUX3AUX4
            #data = [1500,1550,1600,1560,1800,1800,1800,1800]
            #board.sendCMD(16,MultiWii.SET_RAW_RC,data)
            #board.sendCMDreceiveATT(16,MultiWii.SET_RAW_RC,data)
            #print board.rcChannels['yaw'],"--",board.rcChannels['pitch']
            "\r ---------- \r"

            #set only remote_callback
            #get current RC channel value to keep
            #except roll
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
            data = [r,p,y,t,aux1,aux2,aux3,aux4]
            print "DATA:",data
            print "\r",v,"\r"
            print "----<--->----"
            altitude = board.getData(MultiWii.ALTITUDE)
            box = board.getData(MultiWii.BOX)
            print "Altitude:",altitude," - box:",box
            if(i%2==1):
                print "--------"
                print "\r\r\r Dans test RAW RC"
            	data2 = [r,p,1200,y,1800,1800,1800,1800]
            	#board.arm()
            	board.sendCMDreceiveATT(16,MultiWii.SET_RAW_RC,data2)
                #data3 = [990,990,1200,990]
                #board.sendCMDreceiveATT(8,MultiWii.SET_RAW_RC,data3)
            	v = board.getData(MultiWii.RC)
            	print "\r -------> RC -->:",v,"\r"
            	print "----fin raw rc----\r\r"
                time.sleep(0.2)
                #data = [r,p,y,990,990,990,990,990]
            	#board.arm()
            	#print board.sendCMDreceiveATT(16,MultiWii.SET_RAW_RC,data)'''


            #board.sendCMDreceiveATT(16,MultiWii.BOX,data)
            #print(board.getData(MultiWii.ATTITUDE))
            #print "----<--gg->----"
            i = i+1

            #board.sendCMDreceiveATT(16,MultiWii.SET_RAW_RC,data)
            #board.sendCMDreceiveATT(16,MultiWii.RC,data)
            #print(board.getData(MultiWii.ATTITUDE))
            print " \rFIN BOUCLE \r\r\r"

            time.sleep(0.2)

    except Exception,error:
        print "Error on Main: "+str(error)
