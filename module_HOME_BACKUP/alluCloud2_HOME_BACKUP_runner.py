#!/usr/bin/env python

'''
AlluCloud HOME_BACKUP module
Maintains a directory of password protected zip files which can be copied at any time to an external USB HDD
'''
import time
import re
import os
import zipfile
import os.path, time
import datetime
import subprocess
import logging
logging.basicConfig(filename="D:\\ALLUSTORE\\allucloud\\alluCloud2\\alluCloud.log",level=logging.DEBUG,format='%(asctime)s %(message)s')

how_old_can_a_backup_be_before_recreating_zip = 10
backup_source_dir = "D:/ALLUSTORE/allanBackup"
photos_source_dir = "D:/ALLUSTORE/allanBackup/photos"
path_to_photos_dir= "D:/ALLUSTORE/allanBackup\photos"
local_zip_dir = "D:/ALLUSTORE/allanBackupZIPS/"
create_zip_list = []



#####################################

def maintain_local_backup_zips(source_dir,photos_source_dir):
    #get full list of dirs
    source_directories= listdirs(backup_source_dir)
    source_directories.remove(path_to_photos_dir)
    source_directories_photos= listdirs(photos_source_dir)
    full_directory_list = source_directories + source_directories_photos

    print "!AlluCloud2 HOME_BACKUP started!(check log for more info)"
    logging.info("HOME_BACKUP: Backup directory: %s"  % backup_source_dir)
    logging.info("HOME_BACKUP: Zip is updated when changes are %s days old" % how_old_can_a_backup_be_before_recreating_zip)
    print "---------------------------"

    for dirpath in full_directory_list:
        #print "Checking: ", dirpath
        dirname = dirpath.rpartition("\\")[2]

        # Create new zip if there's not one
        zip_file_path = local_zip_dir + dirname + ".rar"

        if os.path.isfile(zip_file_path):
            #print "...zip file found."
            
            # How long since zip was created?
            zip_create_date = os.path.getctime(zip_file_path)
            days_since_zip_created = (int(time.time()) - zip_create_date)/86400
            # print dirname,".rar created", days_since_zip_created, "days ago"

            # When was the DIR last modified?
            first_modification_after_zip_creation = -1
            for root, dirnames, filenames in os.walk(dirpath):
                for filename in filenames:
                    file_path = root + '/' + filename
                    modified = os.path.getmtime(file_path)
                    time_difference_in_secs = int(time.time()) - int(modified)
                    days_since_last_file_mod = int(time_difference_in_secs)/86400
                    # print filename, "was modified", days_since_last_file_mod, "days ago"

                    #Get first modification after zip created
                    if days_since_last_file_mod < days_since_zip_created:
                        if days_since_last_file_mod > first_modification_after_zip_creation:
                            first_modification_after_zip_creation = days_since_last_file_mod
   
            #If files have been modified more than n days since the zip was created we need a new ZIP...
            if first_modification_after_zip_creation == -1:
                logging.info("HOME_BACKUP: %s : No changes since zip was created" % dirname)
                print "%s : No changes since zip was created" % dirname
            elif first_modification_after_zip_creation > how_old_can_a_backup_be_before_recreating_zip:
                print "New content has existed for %s days without being added to zip" % first_modification_after_zip_creation
                logging.info("HOME_BACKUP: New content has existed for %s days without being added to zip" % first_modification_after_zip_creation)
                print "Limit is set to %s days" % how_old_can_a_backup_be_before_recreating_zip
                logging.info("HOME_BACKUP: Limit is set to %s days" % how_old_can_a_backup_be_before_recreating_zip)
                print "Time to recreate %s" % zip_file_path
                logging.info("HOME_BACKUP: Time to recreate %s" % zip_file_path)
                os.remove(zip_file_path)
                #Sleep here to avoid windows file system tunnelling
                time.sleep (30)
                create_zip_list.append(dirpath)
            else:
                countdown_to_recreate_zip = how_old_can_a_backup_be_before_recreating_zip - first_modification_after_zip_creation
                print "%s : New content has existed for %s days without being added to zip. Limit is %s days so recreating zip in %s days" % (dirname,first_modification_after_zip_creation,how_old_can_a_backup_be_before_recreating_zip,countdown_to_recreate_zip)
                logging.info("HOME_BACKUP: %s : New content has existed for %s days without being added to zip. Limit is %s days so recreating zip in %s days" % (dirname,first_modification_after_zip_creation,how_old_can_a_backup_be_before_recreating_zip,countdown_to_recreate_zip))

        else:
            print "File wasn't found. creating... %s" % zip_file_path
            logging.info("HOME_BACKUP: File wasn't found. creating... %s" % zip_file_path)
            create_zip_list.append(dirpath)

    zip_the_dirs(create_zip_list)

def listdirs(folder):
        return [
            d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
            if os.path.isdir(d)
    ]
    
def zip_the_dirs(create_zip_list):
    #Create a zip from given directory list
    for dir in create_zip_list:
        newRarName = local_zip_dir + dir.rpartition("\\")[2] + ".rar"
        dirToCopy = dir + "//*.*"
        cmd = '"C://Program Files//WinRAR//WinRAR.exe" a -pneerg42neerg42 -r -t \"%s\" \"%s\"' % (newRarName,dirToCopy)
        subprocess.call(cmd)



logging.info("HOME_BACKUP: AlluCloud2 HOME_BACKUP started")
maintain_local_backup_zips(backup_source_dir,photos_source_dir)
logging.info("HOME_BACKUP: AlluCloudHOME_BACKUP stopped")