import sqlite3
import getpass
import subprocess
import csv
import datetime
import argparse 


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

	command = "SELECT device_uuid, title, url from cloud_tabs" 
	c.execute(command)

	return (iCloud_devices, c.fetchall())

def main():
	local_user = getpass.getuser()
	db_file_path = '/Users/{}/Library/Safari/CloudTabs.db'.format(local_user)

	local_devices = [getDeviceName('LocalHostName'), getDeviceName('ComputerName')]
	
	iCloud_devices, records = importdb(db_file_path)
	local_ids = [device[1] for device in iCloud_devices if device[0] in local_devices]

	
	parser = argparse.ArgumentParser(description="Save your open Safari tabs to a csv file.")
	parser.add_argument("--all", "-a", default=False, type=bool, help="If you want to keep local devices, bool type")
	args = parser.parse_args()
	if args.all == True:
		local_ids = []

	tabs = [list(r)[1:] for r in records if r[0] not in local_ids]
	time = datetime.datetime.now().strftime("%m-%d-%Y-%I-%M-%S")
		
	with open('{}.csv'.format(time), mode='w') as csv_file:
		fieldnames = ['title','url']
		
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(fieldnames)
		writer.writerows(tabs)


if __name__ == '__main__':
	main()
