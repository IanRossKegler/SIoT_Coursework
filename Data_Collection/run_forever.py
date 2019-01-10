import time
import subprocess
import datetime
import sys

process = subprocess.Popen(['python3', 'main.py'])

while True:
    status = process.poll()

    if status is not None and status != 0:
        f = open('errors.txt', 'w')
        f.write('420 error at ' + str(datetime.datetime.now()))
        f.close()
        y = open('errors.txt', 'w')
        y.write('restart at ' + str(datetime.datetime.now()))
        y.close()
        process = subprocess.Popen(['python3', 'main.py'])

    elif status == 0:
        f = open('errors.txt', 'w')
        f.write('420 error at ' + str(datetime.datetime.now()))
        f.close()
        sys.exit()

    else:
        time.sleep(1)
