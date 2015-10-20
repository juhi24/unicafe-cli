#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import sys
import codecs
import datetime
import argparse
import re
from termcolor import colored
from textwrap import TextWrapper

APIURL ="http://messi.hyyravintolat.fi/publicapi" 
allprice = ["Edullisesti", "Maukkaasti", "Makeasti", "Kevyesti"]
today = datetime.date.today()
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
wrapper = TextWrapper(width=70)

def noptheses(s):
    return re.sub('\s+\([^()]*\)', '', s)

def apidate2date(apidate):
    d=datetime.datetime.strptime(apidate.split(' ')[1], "%d.%m").date()
    d=d.replace(year=today.year)
    return d

def thisweek(date):
    return today.isocalendar()[1] == date.isocalendar()[1]

def daterangestr(date1, date2):
    return date1 if date1 == date2 else date1 + " - " + date2

def gethours(fooddata):
    timetype = "lounas"
    opentime = None
    closetime = None
    daystrs = []
    for time in fooddata["information"][timetype]["regular"]:
        opentime = time["open"]
        closetime = time["close"]
        days = []
        for day in time["when"]:
            if day and not day == "previous":
                days.append(day)
            elif days:
                daystrs.append([", ".join(days), opentime+"-"+closetime])
                days=[]

    for dayset,hours in daystrs:
        print dayset + ": " + hours

    extimes = []
    for i in range(2):
        for extime in fooddata["information"][timetype]["exception"]:
            if extime["from"] and extime["to"]:
                days = daterangestr(extime["from"], extime["to"])
                status = "Suljettu" if extime["closed"] else extime["open"] + "-" + extime["close"]
                extimes.append(days + ": " + status)
        if extimes:
            print colored("Poikkeukset", 'red')
            print ", ".join(extimes)
            break
        else:
            timetype = "business"

def getfood(fooddata, prices, only_today, show_ingredients, show_nutrition, show_special):
    for fd in fooddata["data"]:
        if not fd["data"]:
            continue

        menudate = apidate2date(fd["date"])

        if menudate == today:
            print colored(fd["date"], attrs=['bold'])
        elif menudate < today or not thisweek(menudate):
            continue
        else:
            print fd["date"]

        for f in filter(lambda x: x["price"]["name"] in prices, fd["data"]):
            price = f["price"]["name"]
            notes = []
            note = ""
            if not price == "Edullisesti":
                notes.append(price)

            if show_special:
                notes.extend(f["meta"]["0"])

            if notes:
                note = " (" + ", ".join(notes) + ")"

            print "  " + f["name"] + note

            if show_ingredients and f["ingredients"]:
                ingredients = colored("Ingredients: ", attrs=['bold'])
                ingredients += colored(f["ingredients"].replace('\n', ' '), 'grey')
                if show_ingredients < 2:
                    ingredients = noptheses(ingredients)
                for i in wrapper.wrap(ingredients):
                    print "    " + colored(i, 'grey')

            if show_nutrition and f["nutrition"]:
                nutrition = colored("Nutririon: ", attrs=['bold'])
                nutrition += colored(f["nutrition"].replace('\n', ' '), 'grey')
                for i in wrapper.wrap(nutrition):
                    print "    " + colored(i, 'grey')

        if menudate == today and only_today:
            break

def main(restaurants, prices, hours, only_today, show_ingredients, show_nutrition, show_special):
    allrestaurants = json.load(urllib2.urlopen(APIURL+"/restaurants"))["data"]
    restaurants = filter(lambda r: r["name"] in restaurants, allrestaurants)

    if not restaurants:
        print "restaurant not found"
        exit(2)

    for restaurant in restaurants:
        fooddata = json.load(urllib2.urlopen(APIURL + "/restaurant/" + str(restaurant["id"])))
        print restaurant["name"]
        print '='*len(restaurant["name"])
        if hours:
            gethours(fooddata)
        print
        getfood(fooddata, prices, only_today, show_ingredients, show_nutrition, show_special)
        print

parser = argparse.ArgumentParser(description="Get Unicafe lunch lists")
parser.add_argument("restaurant", nargs="?")
parser.add_argument("-r", metavar="restaurant", nargs="+", action="append", help="name of restaurant")
parser.add_argument("-p", metavar="prices", nargs="*", action="append", choices=allprice, help="only lunches in these price categories")
parser.add_argument("-o", action="count", help="show business times")
parser.add_argument("-t", action="count", help="only today's list")
parser.add_argument("-i", action="count", help="show ingredients, use twice to show everything")
parser.add_argument("-n", action="count", help="show nutrition information")
parser.add_argument("-s", action="count", help="show special diet information")
parser.add_argument("-v", action="count", help="show verbose information about lunches. same as -i -n -s.")
p = None

args = parser.parse_args()
r = [args.restaurant] if args.restaurant else map(lambda r: r[0], args.r)
p = allprice if not args.p else map(lambda p: p[0], args.p)

if args.v:
    args.i = 1
    args.n = 1
    args.s = 1

main(r, p, args.o, args.t, args.i, args.n, args.s)
