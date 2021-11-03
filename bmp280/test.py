# BMP280 sensor
# https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test

import board
import digitalio
# note, use the BME lib here
from adafruit_bme280 import basic as adafruit_bme280
spi = board.SPI()
cs = digitalio.DigitalInOut(board.D6)  # GPIO6
sensor = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)

print('Temperature: {} degrees C'.format(sensor.temperature)) 
print('Pressure: {}hPa'.format(sensor.pressure))
print('Humidity: {}%'.format(sensor.humidity))
