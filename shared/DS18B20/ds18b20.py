# 1wire temperature sensor wrapper class
# DS18B20
import glob
import time
import re


class DS18B20(object):
    def __init__(self):
        self.sensors = self.get_sensors()

    @staticmethod
    def get_sensors():
        base_dir = '/sys/bus/w1/devices/'
        sensors = {}
        expr = re.compile('.*28-(.*)')
        print("Sensors:")
        for df in glob.glob(base_dir + '28*'):
            print(f"sensor address:{expr.match(df).group(1)}")
            sensors[expr.match(df).group(1)] = df
        return sensors

    def sensor_addresses(self):
        return self.sensors.keys()

    def get_sensor_raw(self, address):
        with open(self.sensors[address] + '/w1_slave', 'r') as f:
            lines = f.readlines()
            return lines

    def get_sensor_temp(self, address):
        lines = self.get_sensor_raw(address)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.get_sensor_raw(address)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
