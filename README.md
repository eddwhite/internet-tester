# Internet tester
Check internet connection and speed and add results to a database
Live website shows latest results and stats

## Setup
install speedtest-cli (github link HERE)
crontab -e
*/15 * * * * /usr/bin/python3 ~/Workspace/internet-tester/internet-tester.py > /dev/null

