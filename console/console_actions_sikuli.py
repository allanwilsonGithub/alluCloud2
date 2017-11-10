#!/usr/bin/env python

'''
AlluCloud HOME_BACKUP module
'''

import os
import subprocess
import logging
logging.basicConfig(filename="D:\\ALLUSTORE\\alluCloud\\alluCloud.log",level=logging.DEBUG,format='%(asctime)s %(message)s')

def open_facebook():
    try:
        subprocess.Popen(["D:\\ALLUSTORE\\Programs\\sikuli\\runsikulix.cmd", "-r", "D:\\ALLUSTORE\\Programs\\sikuli\\openFacebook.sikuli"])
    except:
        "failed to open Facebook"

    logging.info("Opened Facebook")

def open_workflowy():
    try:
        subprocess.Popen(["D:\\ALLUSTORE\\Programs\\sikuli\\runsikulix.cmd", "-r", "D:\\ALLUSTORE\\Programs\\sikuli\\openWorkflowy.sikuli"])
    except:
        "failed to open Workflowy"

    logging.info("Opened Workflowy")

def open_freecodecamp():
    try:
        subprocess.Popen(["D:\\ALLUSTORE\\Programs\\sikuli\\runsikulix.cmd", "-r", "D:\\ALLUSTORE\\Programs\\sikuli\\openFreecodecamp.sikuli"])
    except:
        "failed to open Freecodecamp"

    logging.info("Opened Freecodecamp")



def open_allan_wilson_net():
    try:
        subprocess.Popen(["D:\\ALLUSTORE\\Programs\\sikuli\\runsikulix.cmd", "-r", "D:\\ALLUSTORE\\Programs\\sikuli\\openAllanWilsonNet.sikuli"])
    except:
        "failed to open Own Website"

    logging.info("Opened Own Website")