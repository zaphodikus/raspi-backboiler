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
from sensors import DbMAX6675Sensor, DbSensorDatabase, \
    DbBMP280TemperatureSensor, DbBMP280HumiditySensor, DbBMP280PressureSensor

from shared.thread.sensorthread import ThreadWithReturnValue
from shared.sensorbase.sensorbase import TempSensor
from shared.MAX6675.MAX6675 import MAX6675
from shared.BMP280.BMP280 import BMP280, BMP280H, BMP280P
from shared.sensor_config import SystemConfig

# temporary
from flasktest.raspberry.raspberry import is_raspberrypi
if is_raspberrypi():
    import board
    import busio


if __name__ == "__main__":
    if is_raspberrypi():
        # use the "live" DB on a ramdisk to save SD card
        db = DbSensorDatabase(db_root_path=SystemConfig.ramdisk_path)
    else:
        db = DbSensorDatabase()
    hw_sensors = []
    db_sensors = {}

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

#    temp_sensor = BMP280(spi_bus)  # default CS GPIO 6
#    spi_addr = temp_sensor.get_address()
#    print(f"BMP280(T) address : {spi_addr}")
#    hw_sensors.append(temp_sensor)
#    db_sensors[spi_addr] = DbBMP280TemperatureSensor(db.get_connection(), spi_addr)
#    pressure_sensor = BMP280P(spi_bus)  # default CS GPIO 6
#    spi_addr = pressure_sensor.get_address()
#    print(f"BMP280(P) address : {spi_addr}")
#    hw_sensors.append(pressure_sensor)
#    db_sensors[spi_addr] = DbBMP280HumiditySensor(db.get_connection(), spi_addr)
#    humidity_sensor = BMP280H(spi_bus)  # default CS GPIO 6
#    spi_addr = humidity_sensor.get_address()
#    print(f"BMP280(P) address : {spi_addr}")
#    hw_sensors.append(humidity_sensor)
#    db_sensors[spi_addr] = DbBMP280PressureSensor(db.get_connection(), spi_addr)

    while True:
        ts = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        #print(ts)

        i=0
        value = hw_sensors[i].get_sensor_value()
        print(f"Sync read {hw_sensors[i].get_address():12} = {value}{hw_sensors[i].get_sensor_units()}")
        # th = []
        # for s in hw_sensors:
        #     th.append(ThreadWithReturnValue(target=s.get_sensor_value))
        #     th[len(th)-1].start()
        # for i in range(0, len(hw_sensors)):
        #     #
        #     start = time.time()
        #     value = th[i].wait_result()
        #     end = time.time()
        #     print(f"Async read {hw_sensors[i].get_address():12} = {value}{hw_sensors[i].get_sensor_units()}")
        #     # write live value to database
        #     db_sensors[hw_sensors[i].get_address()].set(value)
        #
