from flask import Flask, render_template
import datetime

import sqlite3 as lite
from sensorTools import sensorDatabase

app = Flask(__name__)

@app.route("/")
def current():
    db = sensorDatabase('readings.db')


    templateData = {
       'date': db.dbGetLast(1001)[0][0],
       'masterbrTemp': db.dbGetLast(1003)[0][2],
       'masterbrhumidity': db.dbGetLast(1004)[0][2],
       'familyrmTemp': (db.dbGetLast(2003)[0][2])*1.8+32,
       'familyrmhumidity': db.dbGetLast(2004)[0][2]
       }
    
    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=False)

