#!/usr/bin/env python

import urllib2
import json
import sys
import datetime

APIURL ="http://messi.hyyravintolat.fi/publicapi" 
allprice = ["Edullisesti", "Maukkaasti", "Makeasti", "Kevyesti"]
today = datetime.date.today()

def apidate2date(apidate):
    d=datetime.datetime.strptime(apidate.split(' ')[1], "%d.%m").date()
    d=d.replace(year=today.year)
    return d

def thisweek(date):
    return today.isocalendar()[1] == date.isocalendar()[1]

if len(sys.argv) < 2:
    print "usage: " + sys.argv[0] + " <restaurant name> [price class]"
    print "example: " + sys.argv[0] + " Exactum Edullisesti"
   
    exit(1)

price = allprice if len(sys.argv) == 2 else [sys.argv[2]]

restaurants = json.load(urllib2.urlopen(APIURL+"/restaurants"))["data"]

restaurant = None

for r in restaurants:
    if r["name"] == sys.argv[1]:
        restaurant = r
        break

if not restaurant:
    print "restaurant not found"
    exit(2)

fooddata = json.load(urllib2.urlopen(APIURL + "/restaurant/" + str(restaurant["id"])))

for fd in fooddata["data"]:
    if not fd["data"]:
        continue

    menudate = apidate2date(fd["date"])
    if menudate == today:
        print '\033[1m' + fd["date"] + '\033[0m'
    elif menudate < today or not thisweek(menudate):
        continue
    else:
        print fd["date"]

    for f in filter(lambda x: x["price"]["name"] in price, fd["data"]):
        fprice = f["price"]["name"]
        print "  " + f["name"] + ("" if fprice=="Edullisesti" else " (" + fprice + ")")
