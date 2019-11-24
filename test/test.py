import serial

ser = serial.Serial("/dev/ttyAMA0" , baudrate=4800,  timeout=3.0)
print(" Port serie :  " + ser.name)



while True:
    ser.write(b'Ping\n')

    chaine = ser.readline()
    print(" Chaine recue :  " + chaine)
