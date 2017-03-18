#!/bin/python3

import subprocess as sub
import sqlite3 as db
from datetime import datetime

db_file = "/home/edd/Workspace/internet-tester/speed.sqlite"
speedtest_path = "/usr/local/bin/speedtest-cli"


def add_to_db(data):
    # open connection to the database
    conn = db.connect(db_file, detect_types=db.PARSE_DECLTYPES | db.PARSE_COLNAMES)
    # if table doesn't exist, create it
    conn.execute('''CREATE TABLE IF NOT EXISTS raw (timestamp TIMESTAMP PRIMARY KEY,
            id INTEGER, sponsor TEXT, name TEXT, distance REAL, ping REAL,
            download REAL, upload REAL)''')

    # add data to database
    print(data)
    conn.execute("INSERT INTO raw VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)

    # save changes to database and close
    conn.commit()
    conn.close()


def main():
    print("Running speedtest-cli...")
    # run speedtest-cli and get results in csv format
    p = sub.Popen([speedtest_path, '--csv'], stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()

    # if there are errors, internet is down
    if errors == b'':
        print("Adding results to database")
        # turn speedtest output into list
        results = str(output)[2:-3].split(',')
        assert (len(results) == 8)
        # rearrange output so timestamp is first
        results = [results[3]] + [e for e in results[:3]] + [e for e in results[4:]]
        # turn timestamp string into datetime object
        results[0] = datetime.strptime(results[0], '%Y-%m-%dT%H:%M:%S.%f')

    else:
        print("Internet down! Fuuuuuuuuu")
        # get error number
        if output == b'':
            errno = 0
        else:
            errno = int(str(output).split('Errno ')[1].split(']')[0])
        # create results
        results = [datetime.now(), errno] + [None] * 6

    # add to database
    add_to_db(results)


if __name__ == "__main__":
    main()
