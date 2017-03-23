#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script to extract data from the readings database and make a plot
import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


import sqlite3 as lite
import sys

con = lite.connect('/home/pi/Documents/Python/TempStation/readings.db')


hours = mdates.HourLocator(interval=4)
minutes = mdates.MinuteLocator()

daysFmt = mdates.DateFormatter('%H:%M')

with con:

    # Get data from the past two days
    delta = datetime.timedelta(2)
    past = datetime.datetime.now() - delta

    symbol = past.strftime("%Y-%m-%d %H:%M:%S")

    t = (symbol,)

    cur = con.cursor()
    cur.execute('SELECT time, reading from ESP1 where sensor = 1002 and time>?', t)
     
    data = cur.fetchall()

    xdata = []
    ydata = []
    
    for row in data:
        xdata.append(datetime.datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S"))
        ydata.append(row[1]) 

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xdata, ydata)
    fig.autofmt_xdate()
 
    ax.set_ylabel('Temp  (C)')
    ax.set_xlabel('Time')
    ax.set_title('Temp - last 48 hrs')
   
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(daysFmt)
    #ax.xaxis.set_minor_locator(minutes)

 

    plt.grid('on')
    plt.savefig('/home/pi/Documents/Python/TempStation/humidity2.png')
#    plt.show()

