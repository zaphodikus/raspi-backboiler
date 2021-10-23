# Test the wrapper class for the DS18B20 sensors
import time
import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from shared.DS18B20.ds18b20 import DS18B20

if __name__ == "__main__":
    sensorlist = DS18B20.get_sensor_addresses()
    sensors = []
    for k in sensorlist:
        print(f"adding {k} AS {sensorlist[k]}")
        sensors.append(DS18B20.new_sensor(k, sensorlist[k]))
    print(sensorlist)
    while True:
        for s in sensors:
            print(f" {s.get_address()}={s.get_sensor_temp()}°C")
        time.sleep(1)
