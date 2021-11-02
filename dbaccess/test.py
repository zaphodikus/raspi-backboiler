# Read all temp sensors and write their datas into the table.
# Note:
#   Added a multi-threaded function, but the reading of the 1WD seems to
#   still just be taking ~900ms between samples and so you might hit a
#   1 second delay. So it helps, but not much to use a thread.
#
import sqlite3 as sql
import datetime, time
import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from shared.DS18B20.ds18b20 import DS18B20, TempSensor
from shared.MAX6675.MAX6675 import MAX6675
from sensors import DbDS18B20Sensor, DbMAX6675Sensor, DbSensorDatabase
from threading import Thread
from flasktest.raspberry.raspberry import is_raspberrypi
from shared.sensor_config import SystemConfig

class ThreadWithReturnValue(Thread):
    # https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)

    def wait_result(self, *args):
        Thread.join(self, *args)
        return self._return
    

if __name__ == "__main__":
    if is_raspberrypi():
        db = DbSensorDatabase(db_root_path=SystemConfig.ramdisk_path)
    else:
        db = DbSensorDatabase()
    address_DS18B20 = DS18B20.get_sensor_addresses()
    hw_sensors = []
    db_sensors = {}

    for k in address_DS18B20:
        print(f"Adding '{k}' AS '{address_DS18B20[k]}'")
        hw_sensors.append(DS18B20.new_sensor(k, address_DS18B20[k]))
        db_sensors[k] = DbDS18B20Sensor(db.get_connection(), k)
    thermocouple = MAX6675()  # default CS pin
    spi_addr = thermocouple.get_address()
    print(f"MAX6675 address : {spi_addr}")
    hw_sensors.append(thermocouple)
    db_sensors[spi_addr] = DbMAX6675Sensor(db.get_connection(), spi_addr)
    #print(hw_sensors)

    while True:
        th = []
        for s in hw_sensors:
            th.append(ThreadWithReturnValue(target=s.get_sensor_temp))
            th[len(th)-1].start()
        for i in range(0, len(hw_sensors)):
            #
            start = time.time()
            temp = th[i].wait_result()
            end = time.time()
            print(f"Async read temp {hw_sensors[i].get_address():12}={temp}°C")
            # write live value to database
            db_sensors[hw_sensors[i].get_address()].set(temp)
        time.sleep(1)
