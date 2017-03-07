#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import datetime
import argparse
import re
from termcolor import colored
from textwrap import TextWrapper

APIURL ="http://messi.hyyravintolat.fi/publicapi" 
allprice = ["Edullisesti", "Maukkaasti", "Makeasti", "Kevyesti", "Bistro"]
cheap = ["Edullisesti", "Aukio Edullisesti"]
today = datetime.date.today()
wrapper = TextWrapper(width=70)

def noptheses(s):
    return re.sub('\s+\([^()]*\)', '', s)

def apidate2date(apidate):
    datestr = apidate.split(' ')[1]
    day, month = map(int, datestr.split('.'))
    d = datetime.date(today.year, month, day)
    return d

def thisweek(date):
    return today.isocalendar()[1] == date.isocalendar()[1]

def daterangestr(date1, date2):
    return date1 if date1 == date2 else date1 + " - " + date2

def gethours(fooddata):
    timetype = "lounas"
    if not any(fooddata["information"][timetype]["regular"][0]["when"]):
        print("Avoinna:")
        timetype = "business"
    else:
        print("Lounasaika:")

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
        print(dayset + ": " + hours)

    extimes = []
    for i in range(2):
        for extime in fooddata["information"][timetype]["exception"]:
            if extime["from"] and extime["to"]:
                days = daterangestr(extime["from"], extime["to"])
                status = "Suljettu" if extime["closed"] else extime["open"] + "-" + extime["close"]
                extimes.append(days + ": " + status)
        if extimes:
            print(colored("Poikkeukset", 'red'))
            print(", ".join(extimes))
            break
        else:
            timetype = "business"

def getfood(fooddata, prices, only_today, show_ingredients, show_nutrition, show_special, days):
    for fd in fooddata["data"]:
        if not fd["data"]:
            continue

        menudate = apidate2date(fd["date"])

        if menudate < today or (not thisweek(menudate) and not days):
            continue

        if days == 0:
            break
        elif days:
            days -= 1

        if menudate == today:
            print(colored(fd["date"], attrs=['bold']))
        else:
            print(fd["date"])

        for f in fd["data"]:
            if prices and f["price"]["name"] not in prices:
                continue
        #for f in filter(lambda x: x["price"]["name"] in prices, fd["data"]):
            price = f["price"]["name"]
            notes = []
            note = ""
            if not price in cheap:
                notes.append(price)

            if show_special:
                notes.extend(f["meta"]["0"])

            if notes:
                note = " (" + ", ".join(notes) + ")"

            print("  " + f["name"] + note)

            if show_ingredients and f["ingredients"]:
                ingredients = colored("Sisältö: ", attrs=['bold'])
                ingredients += colored(f["ingredients"].replace('\n', ' '), 'grey')
                if show_ingredients < 2:
                    ingredients = noptheses(ingredients)
                for i in wrapper.wrap(ingredients):
                    print("    " + colored(i, 'grey'))

            if show_nutrition and f["nutrition"]:
                nutrition = colored("Ravintoarvot: ", attrs=['bold'])
                nutrition += colored(f["nutrition"].replace('\n', ' '), 'grey')
                for i in wrapper.wrap(nutrition):
                    print("    " + colored(i, 'grey'))

        if menudate == today and only_today:
            break

def main(restaurants, prices, hours, only_today, show_ingredients, show_nutrition, show_special, days):
    allrestaurants = json.loads(requests.get(APIURL+"/restaurants").text)["data"]
    restaurants = list(filter(lambda r: r["name"] in restaurants, allrestaurants))

    if not restaurants:
        print("restaurant not found")
        exit(2)

    for restaurant in restaurants:
        fooddata = json.loads(requests.get(APIURL + "/restaurant/" + str(restaurant["id"])).text)
        print(restaurant["name"])
        print('='*len(restaurant["name"]))
        if hours:
            gethours(fooddata)
        print()
        getfood(fooddata, prices, only_today, show_ingredients, show_nutrition, show_special, days)
        print()

parser = argparse.ArgumentParser(description="Get Unicafe lunch lists")
parser.add_argument("restaurant", nargs="?")
parser.add_argument("-r", metavar="restaurant", nargs="+", action="append", help="name of restaurant")
parser.add_argument("-p", metavar="prices", nargs="*", action="append", choices=allprice, help="only lunches in these price categories")
parser.add_argument("-o", action="store_true", help="show business times")
parser.add_argument("-t", action="store_true", help="only today's list")
parser.add_argument("-d", action="store", help="days", type=int)
parser.add_argument("-i", action="store_true", help="show ingredients, use twice to show everything")
parser.add_argument("-n", action="store_true", help="show nutrition information")
parser.add_argument("-s", action="store_true", help="show special diet information")
parser.add_argument("-v", action="store_true", help="show verbose information about lunches. same as -ins.")
p = None

args = parser.parse_args()
if args.restaurant:
    r = [args.restaurant]
elif args.r:
    r = list(map(lambda r: r[0], args.r))
else:
    parser.print_help()
    exit(1)

if not args.p:
    p = None
elif args.p:
    p = list(map(lambda p: p[0], args.p))
else:
    parser.print_help()
    exit(1)

if args.v:
    args.i = True
    args.n = True
    args.s = True

main(r, p, args.o, args.t, args.i, args.n, args.s, args.d)
