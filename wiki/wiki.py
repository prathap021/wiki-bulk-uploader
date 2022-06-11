#!/usr/bin/python3

"""
    login.py
    MediaWiki API Demos
    Demo of `Login` module: Sending ` request to login
    MIT license
"""

import requests
import csv
import configparser

#Variables
S = requests.Session()
config = configparser.ConfigParser()
# Read Configurations
config.read('wiki-config.ini')
url = config["wiki-login"]["url"]
response_url = "%s/wiki/" % url
URL = "%s/w/api.php" % url
csv_file = config["DEFAULT"]["csv_file"]

def wiki_login():
	# Retrieve login token first
    PARAMS_0 = {
        'action':"query",
        'meta':"tokens",
        'type':"login",
        'format':"json"
    }    
    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()
    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    PARAMS_1 = {
        'action':"login",
        'lgname': config["wiki-login"]['username'],
        'lgpassword': config["wiki-login"]['password'],
        'lgtoken':LOGIN_TOKEN,
        'format':"json"
    }
    R = S.post(URL, data=PARAMS_1)
    
    PARAMS_2 = {
        'action':"query",
        'meta':"tokens",
        'type':"csrf",
        'format':"json"
    }
    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()
    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
    return CSRF_TOKEN

def upload_data_into_wiki(CSRF_TOKEN, row):
    PARAMS_3 = {
        "action": "edit",
        "format": "json",
        "title": row[0],
        "text": row[1],
        "summary": "Upload the word %s" % row[0],
        "token": CSRF_TOKEN
    }
    R = S.post(url=URL, data=PARAMS_3)
    print(R.url)
    print(R.json)


CSRF_TOKEN = wiki_login()
#Trigger point
with open(csv_file,'r') as csvfile:
    csvreader=csv.reader(csvfile)
    fields=next(csvreader)
    for row in csvreader:
        R = S.get(url=response_url)
        if R.status_code != "":
            print ("Add the word %s into wiki media" % row[0])
            upload_data_into_wiki(CSRF_TOKEN, row)


