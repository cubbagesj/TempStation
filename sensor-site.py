from flask import Flask, render_template
import datetime

import sqlite3 as lite

app = Flask(__name__)

@app.route("/")
def current():
    con = lite.connect('readings.db')
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM ESP1 WHERE ID = (SELECT MAX(ID) FROM ESP1)")

        row = cur.fetchone()

        templateData = {
           'date': row["time"],
           'time': row["time"],
           'outside': row["reading"],
           'masterbr': row["reading"],
           'waterhtr': row["reading"],
           'basement': row["reading"],
           'humidity': row["reading"],
           'furn_out': row["reading"],
           'furn_in' : row["reading"],
           'onboard' : row["reading"]
           }
    
    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=False)

