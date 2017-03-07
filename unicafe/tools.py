# coding: utf-8
import re
import datetime
from termcolor import colored
from textwrap import TextWrapper

today = datetime.date.today()
cheap = ["Edullisesti", "Aukio Edullisesti"]
wrapper = TextWrapper(width=70)


def no_ptheses(s):
    return re.sub('\s+\([^()]*\)', '', s)


def apidate2date(apidate):
    datestr = apidate.split(' ')[1]
    day, month = map(int, datestr.split('.'))
    d = datetime.date(today.year, month, day)
    return d


def this_week(date):
    return today.isocalendar()[1] == date.isocalendar()[1]


def date_range_str(date1, date2):
    return date1 if date1 == date2 else date1 + " - " + date2


def get_hours(fooddata):
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
                days = date_range_str(extime["from"], extime["to"])
                status = "Suljettu" if extime["closed"] else extime["open"] + "-" + extime["close"]
                extimes.append(days + ": " + status)
        if extimes:
            print(colored("Poikkeukset", 'red'))
            print(", ".join(extimes))
            break
        else:
            timetype = "business"


def get_food(fooddata, prices, only_today, show_ingredients, show_nutrition, show_special, days):
    for fd in fooddata["data"]:
        if not fd["data"]:
            continue

        menudate = apidate2date(fd["date"])

        if menudate < today or (not this_week(menudate) and not days):
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
                    ingredients = no_ptheses(ingredients)
                for i in wrapper.wrap(ingredients):
                    print("    " + colored(i, 'grey'))

            if show_nutrition and f["nutrition"]:
                nutrition = colored("Ravintoarvot: ", attrs=['bold'])
                nutrition += colored(f["nutrition"].replace('\n', ' '), 'grey')
                for i in wrapper.wrap(nutrition):
                    print("    " + colored(i, 'grey'))

        if menudate == today and only_today:
            break