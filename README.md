# Internet tester
Check internet connection and speed and add results to a database
Live website shows latest results and stats

## Setup data collection

install speedtest-cli (github link HERE)
```bash
crontab -e
*/15 * * * * /usr/bin/python3 ~/Workspace/internet-tester/internet_tester.py > /dev/null
```

## Setup webserver

install Apache
install Chart.js
```bash
npm install chart.js --save
```