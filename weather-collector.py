#!/usr/bin/env python3
import time
from sense_hat import SenseHat


def export_data(temp,hum,pres,ts,pos):
    text = "{}, {}, {}, {}, {}".format(temp,hum,pres,ts,pos)
    print(text)



def Main():
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


if __name__ == '__main__':
    Main()
