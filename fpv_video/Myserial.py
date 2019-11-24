import serial

test_string = "Je teste le port serie 1 2 3 4 5"
port_list = ['/dev/ttyS0','/dev/ttyAMA0','/dev/serial0']
for port in port_list:
  try:
    serialPort = serial.Serial(port, 9600, timeout = 2)
    print ("Port Serie ", port, " ouvert pour le test :")
    bytes_sent = serialPort.write(test_string)
    print ("Envoye ", bytes_sent, " octets")
    loopback = serialPort.read(bytes_sent)
    if loopback == test_string:
      print ("Recu ", len(loopback), "octets identiques. Le port", port, "fonctionne bien ! \n")
    else:
      print ("Recu des donnees incorrectes : ", loopback, " sur le port serie ", port, " boucle \n")
    serialPort.close()
  except IOError:
    print ("Erreur sur ", port, "\n")
