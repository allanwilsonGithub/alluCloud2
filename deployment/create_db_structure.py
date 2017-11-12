#!/usr/bin/python

'''
Create fresh alluCloud2 structure on MySQL server
Will first remove old structure if it exists
'''

import MySQLdb

def execute_MySQL_command_db_level(db_server, db_user, db_password, query,):
    db = MySQLdb.connect(db_server, db_user, db_password)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    db.close()

def execute_MySQL_command_table_level(db_server, db_user, db_password, database, query,):
    db = MySQLdb.connect(db_server, db_user, db_password, database)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    db.close()

### CREATE EVENT STRUCTURE ###
db_server = 'localhost'
db_user = 'root'
db_password = 'alluCloud2'

execute_MySQL_command_db_level(db_server, db_user, db_password, "DROP DATABASE IF EXISTS `eventdb1`;")
execute_MySQL_command_db_level(db_server, db_user, db_password, "CREATE DATABASE eventdb1;")
execute_MySQL_command_table_level(db_server, db_user, db_password, "eventdb1", "DROP TABLE IF EXISTS `events1`;")
execute_MySQL_command_table_level(db_server, db_user, db_password, "eventdb1", "CREATE TABLE `events1` (`eventID` int(11) NOT NULL AUTO_INCREMENT,`eventType` int(11) DEFAULT '0',`eventName` varchar(255) DEFAULT '0',`date` date DEFAULT '2000-00-20',`year` year(4) DEFAULT '2020',`recurring` int(11) DEFAULT '0',`comment` varchar(255) DEFAULT '0',PRIMARY KEY (`eventID`)) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;")
execute_MySQL_command_table_level(db_server, db_user, db_password, "eventdb1", "DROP TABLE IF EXISTS `eventtypes1`;")
execute_MySQL_command_table_level(db_server, db_user, db_password, "eventdb1", "CREATE TABLE `eventtypes1` (`eventTypeID` int(11) NOT NULL AUTO_INCREMENT,`typeName` varchar(200) NOT NULL,`comment` varchar(255) DEFAULT '0',PRIMARY KEY (`eventTypeID`)) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;")