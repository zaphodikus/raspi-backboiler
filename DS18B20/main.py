# 1wire temperature sensor
# DS18B20
import glob
import time
import re

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def get_sensors():
    base_dir = '/sys/bus/w1/devices/'
    sensors = {}
    expr = re.compile('.*28-(.*)')
    print("Sensors:")
    for df in glob.glob(base_dir + '28*'):
        print(f"sensor address:{expr.match(df).group(1)}")
        sensors[expr.match(df).group(1)] = df
    return sensors


def get_sensor_raw(sensors, address):
    with open(sensors[address] + '/w1_slave', 'r') as f:
        lines = f.readlines()
        return lines


def get_sensor_temp(sensors, address):
    lines = get_sensor_raw(sensors, address)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


sensors = get_sensors()
while True:
    #print(f"Temperature: {read_temp()}°C")
    for sensor in sensors:
        v = get_sensor_temp(sensors, sensor)
        print(f"[{sensor}] = {v}°C")
    time.sleep(1)

