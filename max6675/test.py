# Test the wrapper class for the DS18B20 sensors
import time
import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.getcwd()).parent))
from shared.MAX6675.MAX6675 import MAX6675

if __name__ == "__main__":
    sensors = []
    thermocouple = MAX6675()  # default CS pin
    sensors.append(thermocouple)
    while True:
        for s in sensors:
            print(f" {s.get_address()}={s.get_sensor_temp()}°C")
        time.sleep(1)
