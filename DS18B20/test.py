# Test the wrapper class for the DS18B20 sensors
import time
import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from shared.DS18B20.ds18b20 import DS18B20

if __name__ == "__main__":
    sensors = DS18B20.get_sensors()
    j = DS18B20()
    print(sensors)
    while True:
        for k in sensors:
            print(f"addr:{k} = {j.get_sensor_temp(k)}°C")
        time.sleep(1)
