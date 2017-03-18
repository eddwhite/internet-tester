#!/bin/python3

import sqlite3 as db
import csv
from datetime import datetime, timedelta

csv_file = 'speed.csv'
db_file = 'speed.sqlite'


def main():
    # open connection to the database
    conn = db.connect(db_file, detect_types=db.PARSE_DECLTYPES | db.PARSE_COLNAMES)
    # if table doesn't exist, create it
    conn.execute('''CREATE TABLE IF NOT EXISTS raw (timestamp TIMESTAMP PRIMARY KEY,
                 id INTEGER, sponsor TEXT, name TEXT, distance REAL, ping REAL, 
                 download REAL, upload REAL)''')

    # iterate over csv file
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            # check if there was an internet connection
            if len(row) != 8:
                # crontab was running every 15 minutes
                cur_ts += timedelta(minutes=15)
                results = [cur_ts, 0] + [None for i in range(6)]

            else:
                # re-arrange row so timestamp is first element
                results = [row[3]] + [e for e in row[:3]] + [e for e in row[4:]]
                # keep track of current timestamp
                cur_ts = datetime.strptime(row[3], '%Y-%m-%dT%H:%M:%S.%f')
                # turn timestamp string into datetime object
                results[0] = cur_ts

            # add results to database
            conn.execute("INSERT INTO raw VALUES (?, ?, ?, ?, ?, ?, ?, ?)", results)

    # save changes to database and close
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
