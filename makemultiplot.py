#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sensorTools import sensorDatabase


import sqlite3 as lite
import sys

# Create the data base object 
db = sensorDatabase('/home/pi/Documents/Python/TempStation/readings.db')

# Setup the date label formatting
hours = mdates.HourLocator(interval=4)
minutes = mdates.MinuteLocator()

daysFmt = mdates.DateFormatter('%H:%M')

 
# List of sensors to plot
plots = [1001, 1002, 1003, 1004, 2001, 2002, 2003, 2004]

for plot in plots:

    # Get the data from the past 2 days

    db.dbSelectSensorDays(plot, days=2)
    xdata = []
    ydata = []
     
    for row in db.dbData:
        xdata.append(datetime.datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S"))
        ydata.append(row[2]) 

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xdata, ydata)
    fig.autofmt_xdate()

    ax.set_ylabel(row[3])
    ax.set_xlabel('Time')
    ax.set_title(str(plot)+' - last 48 hrs')
   
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(daysFmt)
    #ax.xaxis.set_minor_locator(minutes)

 

    plt.grid('on')
    plt.savefig('./static/'+str(plot)+'.png')


