# logger scratchpad
# the logger is independent of the sqlite and uses a filter and then a wrapper to write to the DB
from math import sin, radians
from datetime import datetime, timedelta
import time
from deadband import DeadbandBase


def sine_source():
    # a dummy test-data generator
    a = -180
    while True:
        #for a in range(-180, 180): # 'a' stands for 'angle'
        s = int(sin(radians(a))*1000)/10 + 50
        yield s
        a += 1
        if a == 180:
            a = -180


if __name__ == "__main__":
    ivl = timedelta(seconds=2)
    print(ivl)
    filter = DeadbandBase(ivl, 5)
    # or
    filter = DeadbandBase("00:00:02", 5)
    for v in sine_source():
        if filter.exceeded(datetime.now(), v):
            print(datetime.now().strftime("%M:%S.%f") + ' ' + format(v, '.2f'))  # format to remove rounding
        time.sleep(0.1)
