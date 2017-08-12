#!/usr/bin/env python3
#This module logs Temperature (C), Relative Humidity, and Barometric Pressure readings; and calculates Absolute Humidity and 
# Altitude from equations listed in the UC Davis Humidity Conversion note, and the NASA Technical Note found in Weather Background
# Research Resources Folder in Google Drive.  

import datetime
import time
import csv
import math
from itertools import count
from sense_hat import SenseHat

# Defines an int describing the time difference between GMT and Hawaii time
HOURS = 10 #hour difference 
TIMEDIFFERENCE = 60 * 60 * HOURS #difference in seconds 

# NOTE: To get this script to run startup, add it to `/etc/rc.local`.


# this function generates a 'schedule' iterator, which infinitely generates
# the amount of seconds between now, and the next scheduled reading, based
# on the supplied interval.
def make_schedule(interval):
    start = round(time.time(),2)
    sched = ((start + (i * interval)) - time.time() for i in count())
    return sched

# this function contains the core logic of the program, you should
# be able to simply change the `interval` variable to whatever you
# want, and add whatever core logic you need in order to assign
# the appropriate value to the `values` variable.
def main():
    sense = SenseHat()
    sense.clear()
    # the logging interval (in seconds).
    interval = 600
    # a generator which produces the target time of
    # the next reading.  Change its argument to whatever
    # interval you want to log at.
    schedule = make_schedule(interval)
    # Returns Hawaii time
    now = lambda: int(time.time()) - TIMEDIFFERENCE
    # timestamp formatted
    nowFormat = lambda: datetime.datetime.fromtimestamp(now()).strftime('%Y-%m-%d %H:%M:%S')
    # list of headers for the csv file.
    headers = ["Temp", "Rel. Hum", "Bar.Pres","Sat. VP", "Current VP", "Absolute Hum", "Altitude"]
    # use start-time in filename to prevent collisions.
    filename = "output-{}.csv".format(now)
    # open file inside `with` statement to ensure that
    # file is automatically closed when program ends.
    with open(filename,'w') as fp:
        # generate a csv writer obect.
        writer = csv.writer(fp)
        # write the headers to the file.
        writer.writerow((headers, "timestamp"))
        # begin main loop.
        for delta in schedule:
            # wait the `delta` between now and next reading time.
            if delta > 0.001:
                time.sleep(delta)
            # -------- BEGIN CORE PROGRAM LOGIC --------

            # write the actual logic if your program here,
            # resulting in a list name `values`.
            temp = sense.get_temperature()
            hum = sense.get_humidity()
            BP = sense.get_pressure()
            
            #calculating saturated vapor pressure: 0.6108*exp(17.27*temp/(temp+237.3))
            SVP_exp = math.exp(17.21*temp/(temp+237.3)
            Sat_VP = 0.6108*SVP_exp
            #calculating current vapor pressure: 
            curr_VP = 0.01*hum*Sat_VP
            #calculating absolute Humidity 
            Abs_hum = 2165*curr_VP/(temp+273.16)
            #calculating altitude: ((BP*0.1/101.3)^(1/5.26) - 1)*(-293/0.0065)
            alt_1st = (BP*0.1/101.3)
            alt_pow = math.pow(alt_1st,1/5.26)
            alt = (alt_pow - 1)*(-293/0.0065)
            #convert values into list format
            temp_list = [temp]
            hum_list = [hum]
            BP_list = [BP]                   
            Sat_VP_list = [Sat_VP]
            curr_VP_list = [curr_VP]                   
            Abs_hum_list = [Abs_hum]                   
            Alt_list = [alt]                  
            # --------- END CORE PROGRAM LOGIC ---------
            # write the values to the target file, appending
            # the current time as the far right column.
            writer.writerow((temp_list,hum_list,BP_list,Sat_VP_list,curr_VP_list,Abs_hum_list,Alt_list,now(),nowFormat()))
            # force python3 to actually write the value immediately
            # instead of buffering (so we don't lose data when pgrm dies).
            fp.flush()


# this statement will trigger the `main` function
# if and only if this file is loaded as an executable.
if __name__ == '__main__':
    main()

