#!/usr/bin/python

'''
REWRITING 2015 >>>
'''

import os
import datetime
import shutil
import urllib2
import ftplib
from ftplib import FTP
import MySQLdb
import common.scripts.database_functions as database_functions
import ConfigParser

#Get variables from config file
#TODO: move this config file crap to db
import ConfigParser
config = ConfigParser.ConfigParser()
config.read("d:\\ALLUSTORE\\alluCloud\\alluCloud.conf")
list_authors_acc_to_breathing_status = config.get('BOOK', 'listAuthorsAccToBreathingStatus')
list_living_dead_unknown_authors = config.get('BOOK', 'listLivingDeadUnknownAuthors')
FTPBookDir = config.get('BOOK', 'FTPBookDir')
MYSQLPass = config.get('MySQL', 'MYSQLPass')
FtpServer = config.get('FTP', 'FtpServer')
FTPUser = config.get('FTP', 'FTPUser')
FTPPass = config.get('FTP', 'FTPPass')
everyBookRead = int(config.get('BOOK', 'showEveryBookRead'))
top100 = int(config.get('BOOK', 'showTop100'))

global_root_directory = database_functions.get_configuration_item('global_root_directory')

### MYSQL
LOCAL_ENV = ['localhost','root',MYSQLPass,'booksdb']
ENVIRONMENT = LOCAL_ENV
db_server = ENVIRONMENT[0]
db_user = ENVIRONMENT[1]
db_password = ENVIRONMENT[2]
default_table = ENVIRONMENT[3]

###Get Source Files
### GOOD 2015
def get_source_files_for_BOOK_module():
    files = ["indexTemplate.html",
             "indexAdvancedTemplate.html",
             "ToReadList.txt"]
    for file in files:
        global_root_dir = (str(global_root_directory).lstrip("'(('")).rstrip("',),)")
        path_to_source = global_root_dir + "\HTMLfiles\source\BOOK\\" + file
        shutil.copyfile(path_to_source,file.replace("Template",""))


###FTP
def send_file_to_allu_cloud_BOOK_by_FTP(filename):
    ftp = FTP(FtpServer)
    ftp.login(FTPUser,FTPPass)
    ftp.cwd(FTPBookDir)
    ftp.storlines("STOR " + filename, file(filename, "rb"))
    ftp.quit()

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

##############################################################################################
############################## THE BEEF ######################################################
##############################################################################################

#Get source files
### GOOD 2015
get_source_files_for_BOOK_module()

#Modify file
#LAST UPDATE
### GOOD 2015
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
###TODO##########################################THIS IS WHERE I AM"####################################################
titles_count = count_titles()

for line in f.readlines():
    if "Titles stats..." in line:
        n.write(line)
        n.write("Number of titles: %s <br>" % titles_count[0])
    else:
        n.write(line)

f.close()
n.close()
os.remove('index.html')
os.rename('indexnew.html','index.html')

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
        n.write("Number of titles in database:<font size=\"4\" face=\"arial\" color=\"66AACC\">%s</font><br>" % titles_count[0])
        n.write("Of which I have read a total of <font size=\"4\" face=\"arial\" color=\"66AA00\">%s</font><br>" % titles_read_count[0])
    else:
        n.write(line)

f.close()
n.close()
os.remove('index.html')
os.rename('indexnew.html','index.html')

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
#ToRead list


f = open('index.html','r')
n = open('indexnew.html','w')
listLines = open('ToReadList.txt','r')

for line in f.readlines():
    if "To Read List</font></p>" in line:
        n.write(line)
        for listLine in listLines:
            n.write(listLine + "<br>")
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

#Modify file
#Every Book Read
if everyBookRead == 1:
    includedYears=[2004,2005,2010,2011,2009,2008,2007,2006,2003,2012,2013,2014]
    for yearX in includedYears:
            f = open('index.html','r')
            n = open('indexnew.html','w')

            for line in f.readlines():
                if str(yearX)+ "</font></p>" in line:
                    listAllYear = listAllInYear(yearX)
                    n.write(line)
                    c = 0
                    for l in listAllYear:
                        if listAllYear[c][2] == '0':
                            n.write("<u><b>%s</u></b> <font size=\"4\" face=\"arial\" color=\"66AACC\">%s</font><br>" % (listAllYear[c][0],listAllYear[c][1]))
                        else:
                            n.write("<u><b>%s</u></b> <font size=\"4\" face=\"arial\" color=\"66AACC\">%s</font> %s<br>" % (listAllYear[c][0],listAllYear[c][1],listAllYear[c][2]))
                        c = c+1
                else:
                    n.write(line)

            f.close()
            n.close()
            os.remove('index.html')
            os.rename('indexnew.html','index.html')


#Modify file
#TOP 100
if top100 == 1:
	f = open('index.html','r')
	n = open('indexnew.html','w')

	TopRead100 = countRead100(1)
	TopUnread100 = countRead100(0)
	listAll100 = list100()


	for line in f.readlines():
		if "Top 100 List" in line:
			n.write(line)
			n.write("<br><font size=\"5\" face=\"arial\" color=\"66AA00\">Read:</font> %s" % TopRead100[0])
			n.write("<br><font size=\"5\" face=\"arial\" color=\"C00000\">Not read:</font> %s<br>" % TopUnread100[0])
			c = 0
			for l in listAll100:
                            if listAll100[c][4]==1:
                                fontColour="66AA00"
                            else:
                                fontColour="C00000"
                            if listAll100[c][3] == '0':
                                n.write("<br>%s: <u><b> %s </u></b> <font size=\"3\" face=\"arial\" color=\"%s\">%s</font>" % (listAll100[c][0],listAll100[c][1],fontColour,listAll100[c][2]))
                            else:
                                n.write("<br>%s: <u><b> %s </u></b> <font size=\"3\" face=\"arial\" color=\"%s\">%s</font>  %s" % (listAll100[c][0],listAll100[c][1],fontColour,listAll100[c][2],listAll100[c][3]))
                            c = c+1

		else:
			n.write(line)


	f.close()
	n.close()
	os.remove('index.html')
	os.rename('indexnew.html','index.html')

#Upload it again
if os.path.exists('indexAdvanced.html'):
    os.remove('indexAdvanced.html')
os.rename('index.html','indexAdvanced.html')
send_file_to_allu_cloud_BOOK_by_FTP('indexAdvanced.html')