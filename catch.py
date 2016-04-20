#!/usr/bin/env python
import io
import os
import re
import sys
import json
import subprocess
import requests
import logging
from bottle import route, run, request, abort, auth_basic, parse_auth
from ConfigParser import SafeConfigParser

global cleared
cleared = False


# -- read login credentials  --
creds = SafeConfigParser()
creds.read('credentials.ini')

account = creds.get('main', 'account')
key = creds.get('main', 'key')
pwd = creds.get('main', 'pwd')
# -- end login creds section --


def check_pass():
#    auth = request.headers.get('Authorization')
#    username, password = parse_auth(auth)
#    auth_pass = False
#    print "checking"
#    if username == 'thioden':
    auth_pass = True
#        cleared = True
    return auth_pass

def update_order(store,payload,apikey,apipwd):
	# send POST request to the account
	s = requests.put(store, json=payload,  auth=(apikey,apipwd))
	if s.status_code != 201:				# if POST failed
		print s.status_code					# print error code
	return()

@route("/", method=['GET', 'POST'])
def index():
    if check_pass():
        if request.method == 'GET':
            print "ignore get reqs"
            return ' Nothing to see here, move along ...'

        elif request.method == 'POST':
            print 'Success'
            if request.headers.get('X-Shopify-Topic') == "orders/create":
    	        print 'Order Create webhook triggered'
                s = request.json
                orderid = str(s['id'])
                print orderid
                shop = account + orderid + ".json"
                load = {
                  "order": {
                    "id": orderid,
                    "channel":"online_store"
                  }
                }
                print load
                update_order(shop,load,key,pwd)
                return  'OK'

    return "OK"

run(host='67.193.99.9', port=80)
