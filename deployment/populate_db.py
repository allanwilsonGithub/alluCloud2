#!/usr/bin/python
# This Python file uses the following encoding: utf-8

'''
Populate data for alluCloud2 on MySQL server
'''

import MySQLdb

data = "alluCloud2"

def execute_MySQL_command_table_level(db_server, db_user, db_password, database, query,):
    db = MySQLdb.connect(db_server, db_user, db_password, database)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    db.close()

def insert_into_database(db_server, db_user, db_password, database, query,):
    db = MySQLdb.connect(db_server, db_user, db_password, database)
    cursor = db.cursor()
    try:
        # Execute the SQL command
        cursor.execute(query)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

### CREATE EVENT STRUCTURE ###
db_server = 'localhost'
db_user = 'root'
db_password = 'alluCoud2'

def get_input_string_from_backup(database_name,table_name):
    return_line = 0
    f = open('db_backups/%s.sql' %database_name,'r')
    for line in f.readlines():
        if "INSERT INTO" in line and table_name in line:
            return_line = line
    if return_line == 0:
        print "No backup exists for...\nDatabase: %s\nTable: %s\nFile: %s.sql" % (database_name,table_name,database_name)
    else:
        return return_line

### Data for table `events`
#TODO make this data come from last backup and not justa a static line
if data == "alluCloud2":
    insert_string = get_input_string_from_backup("eventsdb1","events1")
    insert_into_database(db_server, db_user, db_password, "eventdb1", insert_string)
elif data == "sample":
    insert_into_database(db_server, db_user, db_password, "eventdb1", "INSERT INTO `events1` VALUES (1,1,'Allan Wilson','2016-01-13',1974,1,'My birthday'),(2,2,'Do this task','2015-10-13',1974,0,'Dont forget'),(3,3,'Christmas','2016-12-25',1974,1,'Santa comes down the chimney'),(4,4,'Big music gig','2016-11-25',1974,0,'Personal event'),(5,5,'Put stocking out for kids','2016-12-25',1974,1,'Remember this!');")

### Data for table `eventtypes`
insert_into_database(db_server, db_user, db_password, "eventdb1", "INSERT INTO `eventtypes1` VALUES (1,'Birthday','Set recurring to 1'),(2,'Task','Set recurring 0'),(3,'PublicEvent','Recurring to 1 for these'),(4,'PersonalEvent','Probably doesnt recur'),(5,'Reminder','No recurring probably');")

