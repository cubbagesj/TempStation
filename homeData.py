# homeData.py
# This script reads data being sent by the ESP8266 modules
# in the house.  To get readings, query each module and read
# the message
#
# The readings are stored in the readings.db database.  The database
# has a table for each esp unit
#
# Last update: 
# sjc - 7/16/17
#

import socket
import time
import sqlite3 as lite

# open a socket to talk to the ESPs
# all modules listen to the same port 10000
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
    except socket.timeout:
        pass

# Increase the socket timeout to wait for measurement
UDPSock.settimeout(5)

# Now go into the main measuring loop
while True:

    # Loop for each module
    for module in moduleList:
        
        # Send measure query and wait for response
        try:
            UDPSock.sendto(b'\xBB', (module[1],10000))
            data, address = UDPSock.recvfrom(1024)
            print(data)

            try:
                message = data.strip().split(":")
                # Handle messages from each module individually

                # Insert the values into database
                #
                # Start by creating the command string that the values will be put into
                names = "INSERT INTO " + message[0] + " ( time, sensor, reading, unit"
                names = names + ") VALUES (  ?, ?, ?, ?) "

                # Now we need to loop for all of the readings.  Sensor readings come 
                # in groups of three values.  Total number of sensors is:
                #   ((len(message) - 1)//3) 
                for cnt in range((len(message) - 1) // 3):

                    values = [time.strftime("%Y-%m-%d") +" "+ time.strftime("%H:%M:%S")]
                    values.append( message[1 + (cnt*3)])
                    values.append( message[2 + (cnt*3)])
                    values.append( message[3 + (cnt*3)])

                    # Now enter the readings in the database
                    con = lite.connect('readings.db')
                    with con:
                        cur = con.cursor()
                        cur.execute(names, values)

            except:
                pass
        except socket.timeout:
            pass

        # Now we wait until time to poll again
        # Sleep time set to 5 min
    time.sleep(300)
    
