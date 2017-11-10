#!/usr/bin/env python

'''
AlluCloud HOME_BACKUP module
'''
import shutil
import time
import logging
logging.basicConfig(filename="D:\\ALLUSTORE\\alluCloud\\alluCloud.log",level=logging.DEBUG,format='%(asctime)s %(message)s')

def delete_backup_and_recopy_to_USB_HDD():
    try:
        shutil.rmtree('F:\\allanBackupExtHDD\\')
    except:
        "failed to delete dir"

    time.sleep(2)
    shutil.copytree('D:\\ALLUSTORE\\allanBackupZIPS\\', 'F:\\allanBackupExtHDD\\allanBackupZIPS')
    logging.info("HOME_BACKUP: delete_backup_and_recopy_to_USB_HDD finished")

def delete_backup_and_recopy_to_QNAP_HDD():
    try:
        shutil.rmtree('Z:\\allanBackupZIPS\\')
    except:
        "failed to delete dir"

    time.sleep(2)
    shutil.copytree('D:\\ALLUSTORE\\allanBackupZIPS\\', 'Z:\\allanBackupZIPS')
    logging.info("HOME_BACKUP: delete_backup_and_recopy_to_QNAP_HDD finished")
