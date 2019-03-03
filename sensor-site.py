from flask import Flask, render_template
import datetime

import sqlite3 as lite
from sensorTools import sensorDatabase

app = Flask(__name__)

@app.route("/")
def current():
    db = sensorDatabase('/home/pi/TempStation/readings.db')
    door1status = db.dbGetLast(3002)[0][2]
    if door1status == 0:
        door1 = 'Closed'
    else:
        door1 = 'Open'

    door2status = db.dbGetLast(3003)[0][2]
    if door2status == 0:
        door2 = 'Closed'
    else:
        door2 = 'Open'

    door3status = db.dbGetLast(4001)[0][2]
    if door3status == 0:
        door3 = 'Closed'
    else:
        door3 = 'Open'
        
    templateData = {
       'date': db.dbGetLast(1001)[0][0],
       'masterbrTemp': db.dbGetLast(1003)[0][2]-7.5,
       'masterbrhumidity': db.dbGetLast(1004)[0][2]+10.3,
       'familyrmTemp': (db.dbGetLast(2003)[0][2])*1.8+32. -9.4,
       'familyrmhumidity': db.dbGetLast(2004)[0][2]+7.74,
       'outsideTemp': db.dbGetLast(1005)[0][2] * 1.8 + 32.0,
       'garageTemp': db.dbGetLast(3001)[0][2] * 1.8 + 32.0,
       'door1': door1,
       'door2': door2, 
       'door3': door3 
       }
    
    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=False)

