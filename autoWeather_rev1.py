#!/usr/bin/env python3
#revision 1
import time
import csv
from itertools import count
from sense_hat import SenseHat

# NOTE: To get this script to run startup, add it to `/etc/rc.local`.


# this function generates a 'schedule' iterator, which infinitely generates
# the amount of seconds between now, and the next scheduled reading, based
# on the supplied interval.
def make_schedule(interval):
    start = round(time.time(),2)
    sched = ((start + (i * interval)) - time.time() for i in count())
    return sched

def export_data(temp,hum,pres,ts,pos):
    text = "{}, {}, {}, {}, {}".format(temp,hum,pres,ts,pos)
    print(text)

# this function contains the core logic of the program, you should
# be able to simply change the `interval` variable to whatever you
# want, and add whatever core logic you need in order to assign
# the appropriate value to the `values` variable.
def main():
    # the logging interval (in seconds).
    interval = 1
    # a generator which produces the target time of
    # the next reading.  Change its argument to whatever
    # interval you want to log at.
    schedule = make_schedule(interval)
    # shortcut to generate current time.
    now = lambda: int(time.time())  
    # list of headers for the csv file.
    headers = ["temp", "hum", "pres", "time", "pos"]

    # use start-time in filename to prevent collisions.
    filename = "output-{}.csv".format(now())
    # open file inside `with` statement to ensure that
    # file is automatically closed when program ends.
    with open(filename,'w') as fp:
        # generate a csv writer obect.
        writer = csv.writer(fp)
        # write the headers to the file.
        writer.writerow((headers)
        # begin main loop.
        for delta in schedule:
            # wait the `delta` between now and next reading time.
           if delta > 0.001:
               time.sleep(delta)
               export_data("temp","hum","pres","time","pos")
               sense = SenseHat()
               sense.clear()    
               while True:
                   time.sleep(600)
                   ts = int(time.time()) 
                   temp = sense.get_temperature()
                   hum = sense.get_humidity()
                   pres = sense.get_pressure()
                   pos = sense.get_compass_raw()
                   export_data(temp,hum,pres,ts,pos)

               values = [temp, hum, pres, time, pos]      
            # --------- END CORE PROGRAM LOGIC ---------
            # write the values to the target file, appending
            # the current time as the far right column.
               writer.writerow((values,now()))
            # force python3 to actually write the value immediately
            # instead of buffering (so we don't lose data when pgrm dies).
#           fp.flush()


# this statement will trigger the `main` function
# if and only if this file is loaded as an executable.
if __name__ == '__main__':
    main()



