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
db = sensorDatabase('/home/pi/TempStation/readings.db')

# Setup the date label formatting
hours = mdates.HourLocator(interval=4)
minutes = mdates.MinuteLocator()

daysFmt = mdates.DateFormatter('%H:%M')

# Sensor cal corrections
cals = { 1001: 7.0, 1003: 9.4, 1002:-16.0, 1004:-10.3, 2001:5.75, 2002:2.0, 2003:7.55, 2004:-7.74}

# List of sensors to plot
# grouping sensors results in an overplot
plots = [(1001, 1003), (1002, 1004), (2001, 2003), (2002, 2004)]

for plot in plots:

    # Create a blank figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for sensor in plot:


        # Get the data from the past 2 days

        db.dbSelectSensorDays(sensor, days=2)
        xdata = []
        ydata = []
     
        for row in db.dbData:
            xdata.append(datetime.datetime.strptime(row[0],"%Y-%m-%d %H:%M:%S"))
            ydata.append(row[2]) 


        aydata = np.array(ydata, dtype=float) 
        
        # If we are plotting temp then convert to F
        if row[3] == 'C':
            aydata = aydata * 1.8 + 32.0

        # apply corrections
        aydata = aydata - cals[sensor]

        ax.plot(xdata, aydata)
    
    fig.autofmt_xdate()

    if row[3] == 'C' or row[3] == 'F':
        ax.set_ylabel('Temp (F)')

    if row[3] == 'RH':
        ax.set_ylabel('Relative Humidty (%)')

    ax.set_xlabel('Time')
    title = db.dbSensorName(sensor)
    ax.set_title(title+' - last 48 hrs')
   
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(daysFmt)
    #ax.xaxis.set_minor_locator(minutes)

 

    plt.grid('on')
    plt.savefig('/home/pi/TempStation/static/'+str(sensor)+'.png')


