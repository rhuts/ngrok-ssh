
"""
This script attempts to create an ngrok tunnel to allow ssh connections
from anywhere and emails the connection details. 

Requires Python 3.5+
"""

# Authors: Roman Huts <roman.h1234@gmail.com>
#
# License: < TO BE DETERMINED >

import os
import sys
import subprocess
import time
import requests
import json
import smtplib
import urllib.request

from config import authtoken, from_user, from_pwd, recipients, subject, body
from rh_log import RH_STATUS, log, logTuple


cwd = os.path.dirname(sys.argv[0])

@logTuple('Initializing ngrok')
def init_ngrok():

    # authenticate ngrok
    proc = subprocess.run([cwd + "/lib/ngrok", "authtoken", authtoken], stdout = subprocess.PIPE)
    print(proc.stdout.decode("utf-8").strip())

    if proc.returncode != 0:
        return RH_STATUS.FAIL, 'Failed to authenticate'

    # start ngrok tunnel and save url
    proc = subprocess.Popen([cwd + "/lib/ngrok", "tcp", '22'], stdout = subprocess.PIPE)

    time.sleep(2)

    localhost_url = "http://localhost:4040/api/tunnels" # url with tunnel details
    tunnel_url = requests.get(localhost_url).text # get the tunnel information
    j = json.loads(tunnel_url)

    tunnel_url = j['tunnels'][0]['public_url'] # do the parsing of the get request

    return RH_STATUS.OK, tunnel_url

@log('Sending email')
def send_email(user, pwd, recipients, subject, body):

    FROM = user
    TO = recipients if isinstance(recipients, list) else [recipients]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        return RH_STATUS.OK
    except:
        return RH_STATUS.FAIL

def internet_on():
    try:
        # google IP
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.request.URLError as err: 
        return False

@log('Waiting for an internet connection')
def wait_for_internet():
    while not internet_on():
        print('Waiting for a connection to the internet ...')
        time.sleep(2)
    return RH_STATUS.OK

def main():
    # log file
    original = sys.stdout
    log = open(cwd + '/log/ngrok_on_login.log', 'w+')
    sys.stdout = log

    wait_for_internet()

    status, tunnel_url = init_ngrok()

    send_email(from_user, from_pwd, recipients, subject, tunnel_url)

    print('Finished')
    sys.stdout = original

    return 0


if __name__ == '__main__':
    exit(main())