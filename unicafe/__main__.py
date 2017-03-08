#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import argparse
import unicafe

APIURL ="http://messi.hyyravintolat.fi/publicapi" 
allprice = ["Edullisesti", "Maukkaasti", "Makeasti", "Kevyesti", "Bistro"]


def cli(restaurants, prices, hours, only_today, show_ingredients, show_nutrition, show_special, days):
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
            unicafe.get_hours(fooddata)
        print()
        unicafe.get_food(fooddata, prices, only_today, show_ingredients, show_nutrition, show_special, days)
        print()


def main():
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
    cli(r, p, args.o, args.t, args.i, args.n, args.s, args.d)


if __name__ == "__main__":
    # execute only if run as a script
    main()
