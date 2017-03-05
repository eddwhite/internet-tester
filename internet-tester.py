#!/bin/python3

import subprocess as sub
import sqlite3 as db
from datetime import datetime as ts

db_file = 'speed.sqlite'

def main():
	print("Running speedtest-cli...")
	# run speedtest-cli and get results in csv format
	p = sub.Popen(['speedtest-cli', '--csv'], stdout=sub.PIPE, stderr=sub.PIPE)
	output, errors = p.communicate()

	# open connection to the database
	conn = db.connect(db_file, detect_types=db.PARSE_DECLTYPES|db.PARSE_COLNAMES)
	# if table doesn't exist, create it
	conn.execute('''CREATE TABLE IF NOT EXISTS results (timestamp TIMESTAMP PRIMARY KEY, 
				 id INTEGER, sponsor TEXT, name TEXT, distance REAL, ping REAL, 
				 download REAL, upload REAL)''')

	# if there are errors, internet is down
	if errors == b'':
		print("Adding results to database")
		# turn speedtest output into list
		results = str(output)[2:-3].split(',')
		assert(len(results) == 8)
		
	else:
		print("Internet down! Fuuuuuuuuu")
		# get error number
		errno = int(err_str.split('Errno ')[1].split(']')[0])
		# create results
		results = [ts.now().isoformat(), errno] + [None for i in range(6)]


	# add results to database
	conn.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?)", results)

	# save changes to database and close
	conn.commit()
	conn.close()


if __name__ == "__main__":
	main()
