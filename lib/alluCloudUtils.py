#!/usr/bin/python

def get_MySQLPass():
    f = open('alluCloudCredentials.ini', 'r')
    lines = f.readlines()
    for line in lines:
        if "MySQL password" in line:
            MySQLPass = (line.split(":")[1]).rstrip()
            return MySQLPass

def get_HomeBackupZipPass():
    f = open('alluCloudCredentials.ini', 'r')
    lines = f.readlines()
    for line in lines:
        if "Home Backup ZIP password" in line:
            HomeBackupZipPass = (line.split(":")[1]).rstrip()
            return HomeBackupZipPass