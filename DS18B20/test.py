#
import time
from shared.DS18B20.ds18b20 import DS18B20

if __name__ == "__main__":
    sensors = DS18B20.get_sensors()
    while True:
        for i in range(0, len(sensors)):
            print(sensors[i].get_sensor_temp())
        time.sleep(1)
