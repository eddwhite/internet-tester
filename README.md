# Internet tester
Check internet connection and speed and add results to a database
Live website shows latest results and stats

## Setup
To start gathering internet speed data

install speedtest-cli (github link HERE)
crontab -e
*/15 * * * * /usr/bin/python3 ~/Workspace/internet-tester/internet_tester.py > /dev/null

To setup the webserver

install Apache
install Chart.js
```bash
npm install chart.js --save
```