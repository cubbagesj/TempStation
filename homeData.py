# homeData.py
# This script reads data being sent by the ESP8266 modules
# in the house.  Each module is set to broadcast a UDP message
# with its readings to 192.168.1.226:21567
#
# The readings are stored in the readings.db database.  The database
# has a table for each esp unit
#
# Last update: 
# sjc - 3/16/17
#

import socket
import time
import sqlite3 as lite

# open a socket to listen for data on
# all modules send to the same port
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

listen_addr = ("", 21567)
UDPSock.bind(listen_addr)



while True:
    data, addr = UDPSock.recvfrom(1024)

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
    
