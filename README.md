# alluCloud2
AlluCloud project from Apr 2019 onwards

# Functions
#### Console
Make a shortcut to GUIMenu.py on desktop

Play Random Track : Plays random music track from local collection

Add Event : Adds an entry to EVENT module

Delete USB HDD and copy everything again : copy all local ZIP backup files to USB
 
Delete QNAP HDD and copy everything again : copy all local ZIP backup files to QNAP box

## Home Backup
Creates a directory of ZIP files on the local disk

Only recreates a zip file when files change

Use GUI to copy these files to either USB HDD or QNAP

## Event Module

Database of birthdays, tasks, reminders

Email is sent every day with ordered list of upcoming events

Formatted webpage is also generated locally

## DEPLOYMENT

Full deployment to fresh Windows7 host (physical or VM)
1. Install Win7
2. Install Python2.7
pip install requests

3. Install MySQL server 5.7.7 and MySql Workbench
	root pass = alluCloud2
	MySQL 5.7.7.0 installer on VM desktop
4. Git clone alluCloud2
	git clone https://github.com/allanwilsonGithub/alluCloud2.git

6. Add D:\DATA\git\alluCloud2\lib to PYTHONPATH

7. Add the correct local passwords to D:\DATA\git\alluCloud2\alluCloudCredentials.ini