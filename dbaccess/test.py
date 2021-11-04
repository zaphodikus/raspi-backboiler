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
from sensors import DbDS18B20Sensor, DbMAX6675Sensor, DbSensorDatabase, \
    DbBMP280TemperatureSensor, DbBMP280HumiditySensor, DbBMP280PressureSensor
from threading import Thread
from flasktest.raspberry.raspberry import is_raspberrypi
from shared.sensor_config import SystemConfig
if is_raspberrypi():
    import board
    import busio


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


# temporary
from shared.DS18B20.ds18b20 import TempSensor
if is_raspberrypi():
    import digitalio
    from adafruit_bme280 import basic as adafruit_bme280


class BMP280(TempSensor):
    def __init__(self, spi, cs_pin=board.D6):
        super().__init__(f"spi_CSPIN_{cs_pin}T")  # use the CS pin as an SPI 'address'
        self.sensor = adafruit_bme280.Adafruit_BME280_SPI(spi, digitalio.DigitalInOut(cs_pin))

        print('Temperature: {} degrees C'.format(self.sensor.temperature))

    def get_sensor_temp(self):
        return self.sensor.temperature


class BMP280H(TempSensor):
    def __init__(self, spi, cs_pin=board.D6):
        super().__init__(f"spi_CSPIN_{cs_pin}H")  # use the CS pin as an SPI 'address'
        self.sensor = adafruit_bme280.Adafruit_BME280_SPI(spi, digitalio.DigitalInOut(cs_pin))

        print('Humidity: {}%'.format(self.sensor.humidity))

    def get_sensor_temp(self):
        return self.sensor.humidity


class BMP280P(TempSensor):
    def __init__(self, spi, cs_pin=board.D6):
        super().__init__(f"spi_CSPIN_{cs_pin}P")  # use the CS pin as an SPI 'address'
        self.sensor = adafruit_bme280.Adafruit_BME280_SPI(spi, digitalio.DigitalInOut(cs_pin))

        print('Pressure: {}hPa'.format(self.sensor.pressure))

    def get_sensor_temp(self):
        return self.sensor.pressure


if __name__ == "__main__":
    if is_raspberrypi():
        # use the "live" DB on a ramdisk to save SD card
        db = DbSensorDatabase(db_root_path=SystemConfig.ramdisk_path)
    else:
        db = DbSensorDatabase()
    address_DS18B20 = DS18B20.get_sensor_addresses()
    hw_sensors = []
    db_sensors = {}

    # Start 1WD
    for k in address_DS18B20:
        print(f"Adding '{k}' AS '{address_DS18B20[k]}'")
        hw_sensors.append(DS18B20.new_sensor(k, address_DS18B20[k]))
        db_sensors[k] = DbDS18B20Sensor(db.get_connection(), k)
    # start SPI
    print(f"Starting SPI, lock bus...'")
    spi_bus = busio.SPI(board.SCLK, board.MOSI, board.MISO)
    while not spi_bus.try_lock():
        pass
    spi_bus.configure(baudrate=4000000)  # 4MHz, chip can do 5MHz normally
    # Note: will run fine at 100KHz
    spi_bus.unlock()

    thermocouple = MAX6675(spi_bus)  # default CS GPIO 5
    spi_addr = thermocouple.get_address()
    print(f"MAX6675 address : {spi_addr}")
    hw_sensors.append(thermocouple)
    db_sensors[spi_addr] = DbMAX6675Sensor(db.get_connection(), spi_addr)

    temp_sensor = BMP280(spi_bus)  # default CS GPIO 6
    spi_addr = temp_sensor.get_address()
    print(f"BMP280(T) address : {spi_addr}")
    hw_sensors.append(temp_sensor)
    db_sensors[spi_addr] = DbBMP280TemperatureSensor(db.get_connection(), spi_addr)
    pressure_sensor = BMP280P(spi_bus)  # default CS GPIO 6
    spi_addr = pressure_sensor.get_address()
    print(f"BMP280(P) address : {spi_addr}")
    hw_sensors.append(pressure_sensor)
    db_sensors[spi_addr] = DbBMP280HumiditySensor(db.get_connection(), spi_addr)
    humidity_sensor = BMP280H(spi_bus)  # default CS GPIO 6
    spi_addr = humidity_sensor.get_address()
    print(f"BMP280(P) address : {spi_addr}")
    hw_sensors.append(humidity_sensor)
    db_sensors[spi_addr] = DbBMP280PressureSensor(db.get_connection(), spi_addr)

    print(hw_sensors)

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
