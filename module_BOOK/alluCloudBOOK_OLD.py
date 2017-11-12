#!/usr/bin/python

import os
import datetime
import shutil
import urllib2
import ftplib
from ftplib import FTP
import MySQLdb
import common.scripts.database_functions as database_functions

### MYSQL
LOCAL_ENV = ['localhost','root',MYSQLPass,'booksdb']
ENVIRONMENT = LOCAL_ENV
db_server = ENVIRONMENT[0]
db_user = ENVIRONMENT[1]
db_password = ENVIRONMENT[2]
default_table = ENVIRONMENT[3]

def get_version():
    db = MySQLdb.connect(db_server, db_user, db_password, default_table)
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    db.close()
    return version

def query_database(query):
    db = MySQLdb.connect(db_server, db_user, db_password, default_table)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    db.close()

def get_authors_alive_or_dead(state):
    query = query_database("SELECT * FROM authors WHERE isAlive = %s" %state)
    return query
    a = 0
    for n in query:
        print "Operator Id: %s " % query[a][1]
        print "Operator Name: %s " % query[a][2]
        print "======================================="
        a = a+1

def count_authors_alive_or_dead(state):
    query = query_database("SELECT COUNT(authName) FROM booksdb.authors WHERE isAlive = %s" %state)
    return query

def count_titles():
    query = query_database("SELECT COUNT(title) FROM booksdb.titles")
    return query

def count_read_titles():
    query = query_database("SELECT COUNT(title) FROM booksdb.titles where alreadyRead=1")
    return query

def count_titles_without_corrosponding_authors():
    query = query_database("SELECT count(titles.title) FROM titles WHERE titleID NOT IN (SELECT rel_title_author.titleID from booksdb.rel_title_author)")
    return query

def display_titles_without_corrosponding_authors():
    query = query_database("SELECT titles.title FROM titles WHERE titleID NOT IN (SELECT rel_title_author.titleID from booksdb.rel_title_author)")
    return query

def count_all_authors():
    query = query_database("SELECT COUNT(authName) FROM booksdb.authors")
    return query

def priority_list():
    query = query_database("SELECT titles.priorityOfReading, authors.authName, titles.title, titles.comment FROM authors, titles, rel_title_author WHERE authors.authID = rel_title_author.authID AND titles.titleID = rel_title_author.titleID AND priorityOfReading != 0 ORDER BY priorityOfReading;")
    return query

def list100():
    query = query_database("SELECT titles.inTop100, authors.authName, titles.title, titles.comment, titles.alreadyRead FROM authors, titles, rel_title_author WHERE authors.authID = rel_title_author.authID AND titles.titleID = rel_title_author.titleID AND inTop100 != 0 ORDER BY inTop100;")
    return query

def countRead100(alreadyRead):
    query = query_database("SELECT count(titles.inTop100) FROM authors, titles, rel_title_author WHERE authors.authID = rel_title_author.authID AND titles.titleID = rel_title_author.titleID AND inTop100 != 0 AND alreadyRead = %s ORDER BY inTop100;" % alreadyRead)
    return query

def listAllInYear(yearValue):
    query = query_database("SELECT authors.authName, titles.title, titles.comment FROM authors, titles, rel_title_author WHERE authors.authID = rel_title_author.authID AND titles.titleID = rel_title_author.titleID AND yearRead = %s ORDER BY monthRead DESC;" % yearValue)
    return query


#Modify file
#Priority list
f = open('index.html','r')
n = open('indexnew.html','w')

priorityList = priority_list()

for line in f.readlines():
    if "Priority List" in line:
        n.write(line)
        n.write("ToRead list in order of priority...")
        a = 0
        for l in priorityList:
            n.write("<br>%s: <u><b> %s </u></b> <font size=\"3\" face=\"arial\" color=\"CC00FF\">%s</font>  %s" % (priorityList[a][0],priorityList[a][1],priorityList[a][2],priorityList[a][3]))
            a = a+1
    else:
        n.write(line)

f.close()
n.close()
os.remove('index.html')
os.rename('indexnew.html','index.html')

#Modify file
#LIST AUTHORS OF VARIOUS BREATHING STATUS
if list_living_dead_unknown_authors == 1:
	f = open('index.html','r')
	n = open('indexnew.html','w')

	dead_authors = get_authors_alive_or_dead(0)
	alive_authors = get_authors_alive_or_dead(1)
	dunno_authors = get_authors_alive_or_dead(2)
	countDead = count_authors_alive_or_dead(0)
	countAlive = count_authors_alive_or_dead(1)
	countDunno = count_authors_alive_or_dead(2)


	for line in f.readlines():
		if "Dead authors..." in line:
			n.write(line)
			n.write("Total: %s <br>" % countDead[0])
			a = 0
			for l in dead_authors:
				n.write("<br>%s " % dead_authors[a][1])
				a = a+1

		elif "Living authors..." in line:
			n.write(line)
			n.write("Total: %s <br>" % countAlive[0])
			b = 0
			for l in alive_authors:
				n.write("<br>%s " % alive_authors[b][1])
				b = b+1

		elif "breathing status" in line:
			n.write(line)
			n.write("Total: %s <br>" % countDunno[0])
			c = 0
			for l in dunno_authors:
				n.write("<br>%s " % dunno_authors[c][1])
				c = c+1

		else:
			n.write(line)


	f.close()
	n.close()
	os.remove('index.html')
	os.rename('indexnew.html','index.html')

#Modify file
#LIST AUTHORS ACCORDING TO BREATHING STATUS
if list_authors_acc_to_breathing_status == 1:
	f = open('index.html','r')
	n = open('indexnew.html','w')

	dunno_authors = get_authors_alive_or_dead(2)
	countDead = count_authors_alive_or_dead(0)
	countAlive = count_authors_alive_or_dead(1)
	countDunno = count_authors_alive_or_dead(2)
	allAuthors = count_all_authors()


	for line in f.readlines():
		if "Authors according to breathing status" in line:
			n.write(line)
			n.write("Total: %s<br>" % allAuthors[0])
			n.write("Alive: %s<br>" % countAlive[0])
			n.write("Dead: %s<br>" % countDead[0])
			n.write("Unknown: %s<br>" % countDunno[0])
			c = 0
			for l in dunno_authors:
				n.write("<br>Unknown: %s " % dunno_authors[c][1])
				c = c+1

		else:
			n.write(line)


	f.close()
	n.close()
	os.remove('index.html')
	os.rename('indexnew.html','index.html')

#Upload it again
send_file_to_allu_cloud_BOOK_by_FTP('index.html')

##############################################################################################
############################## ADVANCED BEEF #################################################
##############################################################################################



#Modify file
#LAST UPDATE
f = open('index.html','r')
n = open('indexnew.html','w')

for line in f.readlines():
    if "Last update..." in line:
        n.write("Updated: " + datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M"))
    elif "Day:" in line or "Date:" in line or "Time:" in line:
        pass
    else:
        n.write(line)

f.close()
n.close()
os.remove('index.html')
os.rename('indexnew.html','index.html')

#Modify file
#Count titles
f = open('index.html','r')
n = open('indexnew.html','w')

titles_count = count_titles()
titles_read_count = count_read_titles()

for line in f.readlines():
    if "Titles stats..." in line:
        n.write(line)
        n.write("Number of titles in database:" % titles_count[0])
        n.write("Of which I have read a total of " % titles_read_count[0])
    else:
        n.write(line)

f.close()
n.close()