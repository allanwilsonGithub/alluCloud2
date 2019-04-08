#!/usr/bin/python

"""
Diplay time in another country
"""

import datetime
import pytz

def get_time():
    print("Choose a timezone (0 to quit):")

    available_zones = {"1": "Europe/London",
                       "2": "Australia/Brisbane",
                       "3": "Europe/Helsinki"}

    for place in available_zones:
        print("{}: {}".format(place, available_zones[place]))

    choice = input()

    while choice:
        if choice == "0":
            break
        if choice in available_zones.keys():
            tz_to_display=pytz.timezone(available_zones[choice])
            print("The time in {} is {}".format(available_zones[choice],datetime.datetime.now(tz=tz_to_display)))
            break

        else:
            print("Choose again")