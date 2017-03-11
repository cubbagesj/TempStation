# homeData.py
# This script reads data being sent by the ESP8266 modules
# in the house.  Each module is set to broadcast a UDP message
# with its readings to 192.168.1.226:21567
#
# This script reads the messages and parses the readings, then
# posts the readings to adafruit IO.  I was using Initial State but 
# stopped because of limits on free streams
#
# Last update: 
# sjc - 1/30/17
#

import socket
from Adafruit_IO import Client
from sense_hat import SenseHat

# open a socket to listen for data on
# all modules send to the same port
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listen_addr = ("", 21567)
UDPSock.bind(listen_addr)

#Set up the adafruit client
aio = Client('6a76fbbf0c46e84971cf5529f166c3ae3fde2b1d')

shttempf = shthumidity = dhttempf = dhthumidity = 0.0
sht2tempf = sht2humidity = Sitempf = Sihumidity = 0.0
# Setup sense hat
#sense = SenseHat()

while True:
    data, addr = UDPSock.recvfrom(1024)

    print(data)

    try:
        message = data.strip().split(":")
        # Handle messages from each module individually

        if message[0] == 'ESP1':
            # ESP1 has a DHT22 and an SHT31D module
            if message[1] == 'DHT':
                shttempf = float(message[2]) * (9.0/5.0) + 32.0
                shthumidity = float(message[3])
            if message[4] == 'SHT':
                dhttempf = float(message[5])
                dhthumidity = float(message[6])

            # Now send to adafruit
            aio.send('InsideTemp', shttempf)
            aio.send('InsideHum', shthumidity)
            aio.send('InsideTemp2', dhttempf)
            aio.send('InsideHum2', dhthumidity)

        if message[0] == 'ESP2':
            # ESP2 has a DHT22 and an Si7021 module
            if message[1] == 'DHT':
                sht2tempf = float(message[2]) * (9.0/5.0) + 32.0
                sht2humidity = float(message[3])
            if message[4] == 'Si':
                Sitempf = float(message[5]) * (9.0/5.0) + 32.0
                Sihumidity = float(message[6])

            # Now send to adafruit
            aio.send('InsideTemp3', sht2tempf)
            aio.send('InsideHum3', sht2humidity)
            aio.send('OutsideTemp', Sitempf)
            aio.send('OutHumid', Sihumidity)

        # Now do senseHat
        #tempf = sense.get_temperature_from_humidity() * (9.0/5.0) + 32.0
        #aio.send('InsideTemp3', tempf)
        #aio.send('InsideHum3', sense.humidity)

    except:
        pass
    
