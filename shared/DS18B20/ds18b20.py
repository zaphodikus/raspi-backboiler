# 1wire temperature sensor wrapper class
# DS18B20
import glob
import time
import re

class RawSensor(object):
    def __init__(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def get_sensor_value(self):
        raise Exception("NotImplementedError")

    @staticmethod
    def get_sensor_units():
        raise Exception("NotImplementedError")


class TempSensor(RawSensor):
    def __init__(self, address):
        super().__init__(address)

    @staticmethod
    def get_sensor_units():
        return r"°C"


class DS18B20(TempSensor):
    def __init__(self, address, device_path):
        super().__init__(address)
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
        print(f"  Creating DB18B20 {address} : {device_path}")
        return DS18B20(address, device_path)

    def get_sensor_raw(self):
        #print(f"  Read sensor {self.address} ")
        with open(self.device_path + '/w1_slave', 'r') as f:
            lines = f.readlines()
            return lines

    def get_sensor_value(self):
        """
        Note: DS18B20 takes about 900 ms to read the file, so this has
        to be background tasked
        """
        lines = self.get_sensor_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.get_sensor_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
