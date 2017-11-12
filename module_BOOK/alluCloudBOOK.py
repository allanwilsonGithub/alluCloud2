#!/usr/bin/python

import os
import datetime
import shutil
import urllib2
import ftplib
from ftplib import FTP
import MySQLdb
import alluCloudUtils

### MYSQL
MySQLPass = str(alluCloudUtils.get_MySQLPass())

LOCAL_ENV = ['localhost','root',MySQLPass,'booksdb']
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


#Create Fresh Index.html
shutil.copyfile("module_BOOK/index_template.html","index.html")

#Last Update
f = open('index.html','r')
n = open('index_new.html','w')

for line in f.readlines():
    if "Updated..." in line:
        n.write("<li class=\"list-group-item\">Last Update: " + datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M") + "</li>\n")
    else:
        n.write(line)

f.close()
n.close()
os.remove('index.html')
os.rename('index_new.html','index.html')

#Number of Titles
f = open('index.html','r')
n = open('index_new.html','w')

for line in f.readlines():
    if "Titles stats..." in line:
        n.write("<li class=\"list-group-item\">Titles in database: " + str(count_titles()[0][0]) + " </li>\n")
        n.write("<li class=\"list-group-item\">I have read: " + str(count_read_titles()[0][0]) + " </li>\n")
    else:
        n.write(line)

f.close()
n.close()
os.remove('index.html')
os.rename('index_new.html','index.html')

#Populate Years
includedYears=[2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
for yearX in includedYears:
    f = open('index.html','r')
    n = open('index_new.html','w')
    for line in f.readlines():
        if str(yearX)+ "_Mark" in line:
            listAllYear = listAllInYear(yearX)
            c = 0
            for l in listAllYear:
                n.write("<li class=\"list-group-item\"><b>" + listAllYear[c][0] + "</b> : <font color=\"green\">" + listAllYear[c][1] + "</font> : " + listAllYear[c][2] + "</li>\n")
                c += 1
        else:
            n.write(line)
    f.close()
    n.close()
    os.remove('index.html')
    os.rename('index_new.html','index.html')

shutil.copyfile("index.html","module_BOOK/index.html",)
os.remove('index.html')