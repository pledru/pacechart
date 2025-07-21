import math
from datetime import datetime, timedelta


def get_duration(distance, speed):
    time = distance / speed
    hours = int(time)
    minutes = (time*60) % 60
    seconds = (time*3600) % 60
    #print("%d:%02d.%02d" % (hours, minutes, seconds))
    print("%d:%02d" % (hours, minutes))
    return (hours, minutes)

def get_arrival(start_time, duration):
    start_time_obj = datetime.strptime(start_time, "%H:%M:%S")

    duration = timedelta(hours=duration[0], minutes=duration[1])

    # Add the duration to the datetime object
    new_time_obj = start_time_obj + duration

    # Extract the time component from the new datetime object
    new_time_only = new_time_obj.time()

    # Print the result
    print("Original Time:", start_time)
    print("Added Duration:", duration)
    print("New Time:", new_time_only.strftime("%H:%M:%S"))


d = get_duration(34.5, 13)

get_arrival("6:00:00", d)
