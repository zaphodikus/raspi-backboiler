# 1wire temperature sensor wrapper class
# DS18B20
import glob
import time
import re


class DS18B20(object):
    def __init__(self, address, device_path):
        self.address = address
        self.device_path = device_path

    @staticmethod
    def get_sensor_addresses():
        """
        :return: a dict of sensors
        """
        base_dir = '/sys/bus/w1/devices/'
        sensors = {}
        expr = re.compile('.*28-(.*)')
        #print("Sensors:")
        for df in glob.glob(base_dir + '28*'):
            #print(f"sensor address:{expr.match(df).group(1)}")
            sensors[expr.match(df).group(1)] = df
        return sensors

    @staticmethod
    def new_sensor(address, device_path):
        print(f"  Creating sensor {address} : {device_path}")
        return DS18B20(address, device_path)

    def get_address(self):
        return self.address

    def get_sensor_raw(self):
        print(f"  Read sensor {self.address} ")
        with open(self.device_path + '/w1_slave', 'r') as f:
            lines = f.readlines()
            return lines

    def get_sensor_temp(self):
        lines = self.get_sensor_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.get_sensor_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
