#####################################
#                                   #
#   SCRIPT QUI FONCTIONNE EN USB    #
#   PREND DES PHOTOS TANT QUE LE    #
#   BOUTTON RC TRANSMITTER CH7 PUSH #
#                                   #
#####################################
from PIL import Image
import piexif
import math
import fractions
from dronekit import connect, VehicleMode
from time import sleep
import time
from picamera import PiCamera
import datetime

def main():
    connection_string = "/dev/ttyACM0"
    # Connect to the Vehicle.
    print("Connecting to vehicle on: %s" % (connection_string,))
    vehicle = connect(connection_string, wait_ready=True)
    camera = PiCamera()
    today = datetime.datetime.now()
    while 1:
        print "Channel values from RC Tx:", vehicle.channels
        print "Channel 7 - ",vehicle.channels[7] #photo droite
        latitude = vehicle.location.global_frame.lat
        longitude = vehicle.location.global_frame.lon
        print "GPS - "+str(latitude)+":"+str(longitude)
        if vehicle.channels[7] <1500:
            print "photo"
            imageFinal = "photo_"+str( int(time.time()))+".jpg"
            #camera.capture(imageFinal)
            #camera.capture_continuous('image{timestamp}.jpg')
            camera.capture_sequence([
                'image%02d.jpg' % i
                for i in range(5)
                ])
            #AddGPS(latitude,longitude,imageFinal)
        else:
            print "--"
        sleep(0.1)
    # Close vehicle object before exiting script
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
