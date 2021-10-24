# Read all temp sensors and write their datas into the table
import sqlite3 as sql
import datetime, time
import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from shared.DS18B20.ds18b20 import DS18B20, TempSensor
from shared.MAX6675.MAX6675 import MAX6675
from sensors import DbDS18B20Sensor, DbMAX6675Sensor, DbSensorDatabase

if __name__ == "__main__":
    db = DbSensorDatabase()
    address_DS18B20 = DS18B20.get_sensor_addresses()
    hw_sensors = []
    db_sensors = {}
    for k in address_DS18B20:
        print(f"adding {k} AS {address_DS18B20[k]}")
        hw_sensors.append(DS18B20.new_sensor(k, address_DS18B20[k]))
        db_sensors[k] = DbDS18B20Sensor(db.get_connection(), k)
    thermocouple = MAX6675()  # default CS pin
    hw_sensors.append(thermocouple)
    print(hw_sensors)

    while True:
        for s in hw_sensors:
            temp = s.get_sensor_temp()
            print(f" {s.get_address()}={temp}°C")
            db_sensors[s.get_address()].set(temp)
        time.sleep(1)
