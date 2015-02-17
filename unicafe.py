#!/usr/bin/env python

import urllib2
import json
import sys
import datetime

def istoday(date):
    d=datetime.datetime.strptime(date.split(' ')[1], "%d.%m").date()
    n=datetime.date.today()
    return d.month==n.month and d.day==n.day

if len(sys.argv) != 2:
    print "usage: " + sys.argv[0] + " <restaurant name>"
    exit(1)

restaurants = json.load(urllib2.urlopen("http://messi.hyyravintolat.fi/publicapi/restaurants"))["data"]

restaurant = None

for r in restaurants:
    if r["name"] == sys.argv[1]:
        restaurant = r
        break

if not restaurant:
    print "restaurant not found"
    exit(2)

fooddata = json.load(urllib2.urlopen("http://messi.hyyravintolat.fi/publicapi/restaurant/" + str(restaurant["id"])))

for fd in fooddata["data"]:
    if not fd["data"]:
        continue
    if istoday(fd["date"]):
        print '\033[1m' + fd["date"] + '\033[0m'
    else:
        print fd["date"]

    for f in fd["data"]:
        print "  " + f["name"]
