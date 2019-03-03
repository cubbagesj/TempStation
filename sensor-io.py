import datetime
import time

import sqlite3 as lite
from sensorTools import sensorDatabase
from Adafruit_IO import Client

def get_current():
    db = sensorDatabase('/home/pi/TempStation/readings.db')
    door1 = db.dbGetLast(3002)[0][2]

    door2 = db.dbGetLast(3003)[0][2]

    door3 = db.dbGetLast(4001)[0][2]
        
    currentData = {
       #'date': db.dbGetLast(1001)[0][0],
       'masterTemp': db.dbGetLast(1003)[0][2]-7.5,
       'masterHumidity': db.dbGetLast(1004)[0][2]+10.3,
       'familyTemp': (db.dbGetLast(2003)[0][2])*1.8+32. -9.4,
       'familyHumidity': db.dbGetLast(2004)[0][2]+7.74,
       'outsideTemp': db.dbGetLast(1005)[0][2] * 1.8 + 32.0,
       'garageTemp': db.dbGetLast(3001)[0][2] * 1.8 + 32.0,
       'door1': door1,
       'door2': door2,
       'door3': door3
       }
    
    return currentData


if __name__ == "__main__":

    # Set up adafruit IO
    aio = Client('cubbagesj20879', '6a76fbbf0c46e84971cf5529f166c3ae3fde2b1d')

    #Loop forever
    while True:
        # Get the current readings
        currentData = get_current()

        # Post to adafruit
        for key in currentData.keys():
            aio.send(key.lower(), currentData[key])
            #print(key.lower(), currentData[key])

        time.sleep(300)
