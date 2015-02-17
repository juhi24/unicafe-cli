#!/usr/bin/env python

import urllib2
import json
import sys
import datetime

def istoday(date):
    d=datetime.datetime.strptime(date.split(' ')[1], "%d.%m").date()
    n=datetime.date.today()
    return d.month==n.month and d.day==n.day

if len(sys.argv) < 2:
    print "usage: " + sys.argv[0] + " <restaurant name> [price class]"
    print "example: " + sys.argv[0] + " Exactum Edullisesti"
   
    exit(1)

allprice = ["Edullisesti", "Maukkaasti", "Makeasti", "Kevyesti"]
price = allprice if len(sys.argv) == 2 else [sys.argv[2]]

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

    for f in filter(lambda x: x["price"]["name"] in price, fd["data"]):
        print "  " + f["name"]
