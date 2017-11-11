#!/usr/bin/env python

import os
import time

db_user = 'root'
db_password = 'neerg42'

os.popen("mysqldump -u %s -p%s eventdb events eventtypes > deployment\db_backups\%s.sql" % (db_user,db_password,"eventsdb"))
os.popen("mysqldump -u %s -p%s booksdb authors categories formats rel_title_author series titles > deployment\db_backups\%s.sql" % (db_user,db_password,"booksdb"))