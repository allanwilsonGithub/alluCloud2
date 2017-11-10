#!/usr/bin/python

import os
import datetime
import urllib2
import ftplib
import shutil
from ftplib import FTP
import MySQLdb
import smtplib
from email.MIMEText import MIMEText
import logging
logging.basicConfig(filename="D:\\ALLUSTORE\\allucloud\\alluCloud2\\alluCloud.log",level=logging.DEBUG,format='%(asctime)s %(message)s')


monthsToShow = 12
sendEmail = 1

###EMAIL
def send_mail(text):
   msg = MIMEText(text)
   msg['Subject'] = 'AlluCloud Event'
   msg['From'] = "AlluCloud"
   msg['Reply-to'] = "AlluCloud"
   msg['To'] = "allan@allanwilson.net"
   s = smtplib.SMTP()
   s.connect("smtp.dnainternet.net")
   s.sendmail("allan@allanwilson.net","allan@allanwilson.net", msg.as_string())
   s.close()

### MYSQL
LOCAL_ENV = ['localhost','root','neerg42','eventdb']
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

def count_all_events():
    query = query_database("SELECT count(eventName) FROM eventdb.events;")
    return query

def list_events(months):
    query = query_database("SELECT events.date, events.eventName, events.comment, eventtypes.typeName FROM events, eventtypes WHERE events.date between CURDATE() AND DATE_ADD(CURDATE(),INTERVAL %s MONTH) AND eventtypes.eventTypeID = events.eventType ORDER BY events.date" % months)
    return query
	
def get_all_old_dates():
    query = query_database("SELECT date from eventdb.events where events.date < CURDATE()")
    return query

def update_database(query):
    db = MySQLdb.connect(db_server, db_user, db_password, default_table)
    cursor = db.cursor()
    try:
       cursor.execute(query)
       db.commit()
    except:
       db.rollback()
    db.close()

def update_old_dates_in_database_to_next_year():
    '''
    Any date older than today is updated to next year
    '''
    old_dates_list = get_all_old_dates()
    for oldDate in old_dates_list:
            oldDate = oldDate[0]
            newDate = str(oldDate)
            oldYear = str(oldDate.strftime("%Y"))
            print "Old year=", oldYear
            newYear = str(datetime.datetime.now().year+1)
            print "New Year=", newYear
            newDate = newDate.replace(oldYear, newYear, 1)
            query = "UPDATE eventdb.events SET events.date='%s' WHERE events.date='%s' AND events.recurring=1" %(newDate,oldDate)
            print query
            update_database(query)

def get_birth_year(name):
    query = query_database("SELECT year FROM eventdb.events WHERE eventName = \"%s\"" % name)
    return query
    
def query_config_database(query):
    db = MySQLdb.connect('localhost','root','neerg42','dashdb')
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
    db.close()

###SETUP EMAIL TEXT
emailText = []

##Update EVENT dates
update_old_dates_in_database_to_next_year()

#LAST UPDATE
f = open('module_EVENT\\indexTemplate.html', 'r')
n = open('indexnew.html','w')

for line in f.readlines():
    if "Last update..." in line:
        n.write("Last updated... " + datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M") + "<br>")
        emailText.append("Updated: " + datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M"))
        logging.info("EVENT Updated: " + datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M"))
    elif "Day:" in line or "Date:" in line or "Time:" in line:
        pass
    else:
        n.write(line)

f.close()
n.close()
os.rename('indexnew.html','index.html')

#Modify file
#List events
f = open('index.html','r')
n = open('indexnew.html','w')

events_list = list_events(monthsToShow)
emailText.append("===============================")
for line in f.readlines():
    if "Event Type" in line:
        n.write(line)
        a = 0
        for l in events_list:
            if events_list[a][3]=="Birthday":
                fontColour="66AA00"
            elif events_list[a][3]=="Task":
                fontColour="66AACC"
            elif events_list[a][3]=="PublicEvent":
                fontColour="CC6633"
            elif events_list[a][3]=="Reminder":
                fontColour="yellow"
            else:
                fontColour="9933CC"
            diffYear=int((events_list[a][0]).strftime("%Y"))
            diffMonth=int((events_list[a][0]).strftime("%m"))
            diffDay=int((events_list[a][0]).strftime("%d"))
            days_to_go = (datetime.date(diffYear,diffMonth,diffDay) - datetime.date.today()).days
            if days_to_go==0:
                days_to_go="Today"

            ###AGE##########
            birth_year = get_birth_year(events_list[a][1])
            birthYear = int(birth_year[0][0])
            from_date=datetime.date(birthYear,diffMonth,diffDay)
            to_date=datetime.date.today()
            leap_day_anniversary_Feb28=True
            age = to_date.year - from_date.year
            try:
                anniversary = from_date.replace(year=to_date.year)
            except ValueError:
                assert from_date.day == 29 and from_date.month == 2
                if leap_day_anniversary_Feb28:
                    anniversary = datetime.date(to_date.year, 2, 28)
                else:
                    anniversary = datetime.date(to_date.year, 3, 1)
            if to_date < anniversary:
                age -= 1
            if age <0:
                age = ""
            ################


            n.write("<tr BGCOLOR=\"%s\"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (fontColour,days_to_go,events_list[a][1],events_list[a][2],age,events_list[a][0],events_list[a][3]))
            emailText.append("%s days to go...     %s     %s   %s     %s     %s" % (days_to_go,events_list[a][1],events_list[a][2],events_list[a][0],events_list[a][3],age))
            a = a+1
    else:
        n.write(line)

f.close()
n.close()
os.remove('index.html')
os.rename('indexnew.html','index.html')

shutil.copy('index.html','./web_ready_files/eventIndex.html')
os.remove('index.html')

###EMAIL######################
str_list = []
for n in emailText:
    str_list.append(n)
    str_list.append("\n")
textToMail = ''.join(str_list)

if sendEmail == 1:
    send_mail(str(textToMail))
##########################
