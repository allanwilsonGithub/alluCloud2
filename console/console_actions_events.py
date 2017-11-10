#!/usr/bin/python

'''
Connections between cloud parts (FTP, MYSql, HTTP) for EVENT module
'''

import re
import MySQLdb
import subprocess

### MYSQL
LOCAL_ENV = ['localhost','root','neerg42','eventdb']
ENVIRONMENT = LOCAL_ENV
db_server = ENVIRONMENT[0]
db_user = ENVIRONMENT[1]
db_password = ENVIRONMENT[2]
default_table = ENVIRONMENT[3]

def insert_database(query):
    db = MySQLdb.connect(db_server, db_user, db_password, default_table)
    cursor = db.cursor()
    try:
        # Execute the SQL command
        cursor.execute(query)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

def add_event():
    print "1 = Birthday"
    print "2 = Task"
    print "3 = Public Event"
    print "4 = Personal Event"
    print "5 = Reminder"
    eventTypeValue = raw_input("Type :")
    eventNameValue = raw_input("Name : ")
    
    #Get and verify date
    print "Date format: 2017-08-16"
    eventDateValue = raw_input("Date : ")
    date_pattern = re.compile("(^[2][0][1][6-9]\-[0-1][0-9]\-[0-3][0-9])")
    while date_pattern.match(eventDateValue) == None:
        print "Date was in the wrong format!"
        eventDateValue = raw_input("Date : ")

    eventYearValue = raw_input("Year[press enter for 2017]:") or "2017"
    eventRecurringValue = raw_input("Recurring (0 or 1) : ")
    eventCommentValue = raw_input("Comment : ")
    query = "INSERT INTO events (eventType,eventName,date,year,recurring,comment) VALUES(%s, '%s', '%s', %s, %s, '%s')" % (eventTypeValue,eventNameValue,eventDateValue,eventYearValue,eventRecurringValue,eventCommentValue)
    insert_database(query)
    selectTestQuery = "SELECT * FROM eventdb.events where eventType = %s AND eventName = '%s' AND date = '%s' AND year = %s AND recurring = %s AND comment = '%s'" % (eventTypeValue,eventNameValue,eventDateValue,eventYearValue,eventRecurringValue,eventCommentValue)
    if select_from_datebase_as_test(selectTestQuery)[0][2] == str(eventNameValue):
        print "OK! Database was updated"
    else:
        print "Something went wrong. The database query failed to find the new data!"

def select_from_datebase_as_test(selectTestQuery):
    db = MySQLdb.connect(db_server, db_user, db_password, default_table)
    cursor = db.cursor()
    cursor.execute(selectTestQuery)
    result = cursor.fetchall()
    return result
    db.close()