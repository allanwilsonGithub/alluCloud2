# alluCloud2
AlluCloud project from 2017 onwards

Full deployment to fresh Windows7 host (physical or VM)
1. Install Win7
2. Install Python2.7
pip install requests

3. Install MySQL server 5.7.7 and MySql Workbench
	root pass = alluCloud2
	MySQL 5.7.7.0 installer on VM desktop
4. Install and configure GIT
	Install Putty > generate pub/priv keypair with PuttyGen password is always alluCloud2
	Upload pub key to codebasehq.com account (where alluCloud2 repo is)
	Open PuTTYgen and open the key (.ppk file) you have previously created. Once your key is 	open, you want to select Conversions -> Export OpenSSH key and save it to 	c:\users\tester\.ssh\id_rsa. After you have the key at that location, Git bash will 	recognize the key and use it.

5. Git clone alluCloud2
	git clone git@codebasehq.com:allucloud/allucloud/allucloud2.git

6. Add D:\DATA\git\alluCloud2\lib to PYTHONPATH

7. Add the correct local passwords to D:\DATA\git\alluCloud2\alluCloudCredentials.ini

TODO:
Get BOOK module working and linked to Weboutput
Get Deployment working properly
Get BOOK module backups working

Get it all on the internet with a Javascript frontend.