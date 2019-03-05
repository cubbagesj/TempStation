# homeData-io.py
# This script reads data being sent by the ESP8266 modules
# in the house.  To get readings, query each module and read
# the message
#
# This is a modification of the original homeData.py.  Instead of
# using the database, the readings are send to Adafruit IO.  Nothing
# is stored locally
#
# Last update: 
# sjc - 03/06/19 
#

import socket
import time
import os
from Adafruit_IO import Client

# open a socket to talk to the ESPs
# all modules listen to the same port 10000
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# ---------- SETUP Section ------------
#
# First need to get a list of available modules so we scan the network
# for modules. We send the \xAA message and wait for a response

moduleList = []
base = '192.168.1.'
UDPSock.settimeout(0.1)
for n in range(1,254):
    addr = '192.168.1.%s' % n
    print('Trying %s' % addr)
    try:
        UDPSock.sendto(b'\xAA',(addr, 10000)) 
        data, address = UDPSock.recvfrom(1024)
        print('Got %s from %s'% (data, address))
        moduleList.append((data, address[0]))
        time.sleep(5)
    except socket.timeout:
        pass

# Increase the socket timeout to wait for measurement
UDPSock.settimeout(5)

# Setup Adafruit IO
aio = Client('cubbagesj20879', '6a76fbbf0c46e84971cf5529f166c3ae3fde2b1d')

# Now go into the main measuring loop
while True:

    # Loop for each module
    for module in moduleList:
        
        # Send measure query and wait for response
        try:
            UDPSock.sendto(b'\xBB', (module[1],10000))
            data, address = UDPSock.recvfrom(1024)
            adata = data.decode('ascii')
            print(adata)

            try:
                message = adata.strip().split(":")

                # We only want to put certain values up from each ESP
                if message[0] == 'ESP1':
                    aio.send('mastertemp', float(message[8])-7.5)
                    aio.send('masterhumidity', float(message[11]) + 10.3)
                    aio.send('outsidetemp', float(message[14]) * 1.8 + 32.0)

                if message[0] == 'ESP2':
                    aio.send('familytemp', float(message[8]) * 1.8 + 32. -9.4)
                    aio.send('familyhumidity', float(message[11]) + 7.74)

                if message[0] == 'ESP3':
                    aio.send('garagetemp', float(message[2]) * 1.8 + 32.0)
                    aio.send('door1', int(message[5]))
                    aio.send('door2', int(message[8]))

                if message[0] == 'ESP4':
                    aio.send('door3', int(message[2]))

            except:
                pass

        except socket.timeout:
            pass

    # Sleep time set to 5 min
    time.sleep(300)
    
