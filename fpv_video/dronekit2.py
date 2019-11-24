'''
Channel 1: Roll input
Channel 2: Pitch input
Channel 3: Throttle input
Channel 4: Yaw input
'''
from PIL import Image
import piexif
import math
import fractions
from dronekit import connect, VehicleMode
from time import sleep
import time
import datetime

def main():
    connection_string = "/dev/ttyACM0"
    # Connect to the Vehicle.
    print("Connecting to vehicle on: %s" % (connection_string,))
    vehicle = connect(connection_string, wait_ready=False)
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.armed = True
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    i=0
    while i<20:
        if i>5 and i<10:
            vehicle.channels.overrides['3'] = 1300
            time.sleep(1)
            vehicle.channels.overrides['3'] = None
        print "\r->",i
        print "\r--deb--\r"
        if i>8 and i<15:
            print "\r Channel values from RC Tx:", vehicle.channels
            # Set Ch2 override to 200 using indexing syntax
            vehicle.channels.overrides['1'] = 1700
            print "\r -- Override:",vehicle.channels.overrides
        if i>15
            time.sleep(1)
            vehicle.channels.overrides['1'] = None

        print "\r--fin--\r"
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        latitude = vehicle.location.global_frame.lat
        longitude = vehicle.location.global_frame.lon
        print "GPS - "+str(latitude)+":"+str(longitude)
        i=i+1
    # Close vehicle object before exiting script
    vehicle.armed = False
    vehicle.close()

def AddGPS(latitude,longitude,image):
    strLat = str(latitude)
    strLon = str(longitude)
    #on calcul les N S E W
    if latitude>=0:
    	latRef = 'N'
    else:
    	latRef='S'
    if longitude>=0:
    	lonRef = 'E'
    else :
    	lonRef='W'
    #On supprime la virugle
    strLat = strLat.replace('.','')
    strLon = strLon.replace('.','')
    #On charge la photo
    print("---debut---"+str(image))
    #on load les exif data
    exif_dict = piexif.load(image)
    #on ajoute les coordonnes
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = latRef
    exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = [int(strLat),10000000]
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = lonRef
    exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = [int(strLon), 10000000]
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image)
    print("---fin---")

#start process
if __name__ == '__main__':
    main()
