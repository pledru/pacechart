#!/usr/bin/python3

"""
usage: route <datetime> <file>
usage: route <datetime> <file> -km

example: route 2025-05-03T06:00:00 data.txt

The file is of the format: start, end, miles, speed, stop
using a tab separator.
"""

import math
import sys
from datetime import date, datetime, time, timedelta


def get_duration(distance : float, speed : float) -> time:
    """
    Calculate the duration to cover the distance at the given speed
    :return the duration.
    """
    t = distance / speed
    hours = int(t)
    minutes = int((t*60) % 60)
    seconds = int((t*3600) % 60)
    return time(hours, minutes, seconds)


def get_arrival(start_time : str, duration : time) -> datetime:
    """
    Add a duration to a start time.
    :return the new date.
    """

    start_time_obj = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    duration = datetime.combine(date.min, duration) - datetime.min

    # Add the duration to the datetime object
    end_time_obj = start_time_obj + duration
    return end_time_obj


def read(f: str):
    entries = []
    with open(f, 'r') as file:
        header = True
        for line in file:
            line = line.strip()
            if header:
                header = False
                continue
            tokens = line.split('\t')
            start = None
            end = None
            speed = None
            distance = None
            stime = None
            for t in tokens:
                if t == '':
                    continue
                if start is None:
                    start = t
                    continue
                if end is None:
                    end = t
                    continue
                if distance is None:
                    distance = t
                    continue
                if speed is None:
                    speed = t
                    continue
                if stime is None:
                    stime = t
                    continue
            entry = {'start': start, 'end': end, 'speed': speed, 'distance': distance, 'stime': stime}
            entries.append(entry)
    return entries


def report(data : tuple, convert: bool):
    start = data[1].strftime("%Y-%m-%d %H:%M:%S")
    print(f"Start Time:\t {start}")
    end = data[2].strftime("%Y-%m-%d %H:%M")
    print(f"End Time:\t {end}")

    entries = data[0]
    fields = ["start", "end", "departure", "speed", "ride_time", "arrival_time",
              "distance", "cumulative", "stime", "elapsed_time"]
    speed = "mph"
    distance = "Miles"
    if convert:
        speed = "km/h"
        distance = "Kilometers"
    h = ["Start Location", "End Location", "Departure", speed, "Ride Time", "Arrival Time",
         distance, "Cumulative", "Stop Time", "Elapsed Time"]
    headers = {}
    i = 0
    for f in fields:
        headers[f] = h[i]
        i = i + 1

    entries.insert(0, headers)
    l = []
    for f in fields:
        l.append(max(len(e[f]) for e in entries))

    for entry in entries:
        i = 0
        for f in fields:
            print(entry[f], end="")
            lx = l[i] - len(entry[f]) + 1
            for j in range(lx):
                print(" ", end="")
            i = i + 1
        print(" ")


def calculate(start: str, file: str, convert: bool) -> tuple:
    """
    Read a data file and generate distances and times.
    """
    entries = read(file)
    cumulative_distance = 0
    # keep the initial start time
    start0 = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    for entry in entries:

        # the departure time in HH:MM
        entry["departure"] = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")

        distance = float(entry["distance"])
        speed = float(entry["speed"])
        d = get_duration(distance, speed)

        if convert:
            speed = speed * 1.60934
            entry["speed"] = f"{speed:.1f}"
            distance = distance * 1.60934
            entry["distance"] = f"{distance:.1f}"

        # the ride time for the segment in HH:MM
        entry["ride_time"] = d.strftime("%H:%M")

        at = get_arrival(start, d)
        # the arrival time for the segment in HH:MM
        entry["arrival_time"] = at.strftime("%H:%M")
        at_full = at.strftime("%Y-%m-%dT%H:%M:%S")

        # add the stop time
        stime = entry["stime"]
        stime_obj = datetime.strptime(stime, "%H:%M")
        # add the stop time
        st = get_arrival(at_full, stime_obj.time())

        cumulative_distance = cumulative_distance + distance
        entry["cumulative"] = f"{cumulative_distance:.1f}"

        # next start time
        start = st.strftime("%Y-%m-%dT%H:%M:%S")

        elapsed_time = st - start0
        total_elapsed_seconds = int(elapsed_time.total_seconds())
        hours_elapsed, remainder_seconds = divmod(total_elapsed_seconds, 3600)
        minutes_elapsed, _ = divmod(remainder_seconds, 60)
        entry["elapsed_time"] = f"{hours_elapsed}:{minutes_elapsed}"

    end = at
    return (entries, start0, end)

def main():
    start = sys.argv[1]
    file = sys.argv[2]
    convert = False
    if len(sys.argv) >= 4 and sys.argv[3] == "-km":
        convert = True

    entries = calculate(start, file, convert)
    report(entries, convert)

main()
