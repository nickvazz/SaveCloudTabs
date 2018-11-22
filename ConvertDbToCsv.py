import sqlite3
import getpass
import subprocess
import pandas as pd

def getDeviceName(location):
	script = 'scutil --get {}'.format(location)
	name = subprocess.Popen([script], stdout=subprocess.PIPE, shell=True)
	name = name.communicate()[0]
	return name.decode("utf-8").strip()

def importdb(db):
	conn = sqlite3.connect(db)
	c = conn.cursor()
	
	c.execute("SELECT device_name, device_uuid from cloud_tab_devices")
	iCloud_devices = c.fetchall()


	# find the time in the columns to add to dataframe
#	command = "SHOW COLUMNS FROM cloud_tabs" 
#	c.execute(command)
#	print (c.fetchall())
	
	command = "SELECT device_uuid, title, url from cloud_tabs" 
	c.execute(command)

	return (iCloud_devices, c.fetchall())

if __name__ == '__main__':
	local_user = getpass.getuser()
	db_file_path = '/Users/{}/Library/Safari/CloudTabs.db'.format(local_user)

	local_devices = [getDeviceName('LocalHostName'), getDeviceName('ComputerName')]
	
	iCloud_devices, records = importdb(db_file_path)
	local_ids = [device[1] for device in iCloud_devices if device[0] in local_devices]

	tabs = [list(r) for r in records if r[0] not in local_ids]
	df = pd.DataFrame(tabs, columns=['ids','title','url']).drop('ids',axis=1)
	print (df.head())	
