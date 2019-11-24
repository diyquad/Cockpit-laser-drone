import pylirc

pylirc.init("myProg","/home/pi/.lircrc") # /home/pi/.lircrc
list = pylirc.nextcode()
print list
if list is not None:
    for code in list:
        if code == 'myVariable':
            t=1
#irsend SEND_ONCE led KEY_POWER

#import subprocess
#rtn = subprocess.call(["irsend", "SEND_ONCE", "ac", "KEY_POWER"])
# rtn should equal 0 if command ran without error
