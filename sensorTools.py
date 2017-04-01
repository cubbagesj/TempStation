# sensorTools.py
#
# Copyright 20017 - Samuel J. Cubbage
#
# This file is part of the Home Sensor Tool kit
#

import sqlite3 as lite
import os

class sensorDatabase:
    """ This is a class for working with an sqlite database
    of sensor readings from various sensors connected to ESP8266 boards
    and possibly other IoT platforms.

    CLASS METHODS:

    __init__ - sets up the database path and other parameters
    """

    def __init__(self, dbName):
        """ The constructor needs the full pathname to the database file
        """

        # Check that path to database is valid
        if os.path.exists(dbName):
            self.dbName = dbName
        else:
            self.dbName = ""

    def dbQuery(self, query):
        """ Execute a pre-setup data base query and return results into
        a class property for use elsewhere
        """

        if self.dbName != "":

            con = lite.connect(self.dbName)

            with con:
                con.row_factory = lite.Row

                cur = con.cursor()

                # Execute the query
                cur.execute(query)

                # Stow the results
                self.dbData = cur.fetchall()

    def dbSelectSensor(self,sensorID, start='', end=''):
        """ Select all of the readings from one sensor.  Uses the sensor id
        to determine the table to pull from.  Default is to return all of the 
        readings. Can use start,end to select a range. Start by itself returns
        from start to end of table
        """

        # Start with an empty query
        query = ''

        # First determine the correct table using the sensor ID 
        # Table is defined by first digits
        tableID = int(sensorID/1000)

        query = 'SELECT * from ESP%d WHERE sensor= %d' % (tableID, sensorID)

        if end == '':
            if start != '':
                query = query + " and time > '%s'" % start
        else:
            query = query + " and time > '%s' and time <'%s'" %(start, end)
        
        query = query + ';'

        # Execute the query
        self.dbQuery(query)

    def dbClearTable(self, tableID, keepdays=2):
        """ Clear readings from a table. Default is to keep the last 2
        days of readings
        """

        # Start with an empty query
        query = ''

        # build delete command

        query = query + "DELETE FROM %s WHERE time < " % tableID

        # Add in date magic
        query = query + "datetime(CURRENT_TIMESTAMP,'localtime','-%d days');" % keepdays

        try:
            self.dbQuery(query)
        except:
            pass


    def dbSelectSensorDays(self,sensorID, days='2'):
        """ Select readings from one sensor for a certain number of days
        Uses the sensor id
        to determine the table to pull from.   
        """

        # Start with an empty query
        query = ''

        # First determine the correct table using the sensor ID 
        # Table is defined by first digits
        tableID = int(sensorID/1000)

        query = 'SELECT * from ESP%d WHERE sensor= %d' % (tableID, sensorID)

        query = query + " and time > datetime(CURRENT_TIMESTAMP,'localtime','-%d days');" % days
        

        # Execute the query
        self.dbQuery(query)
