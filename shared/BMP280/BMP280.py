from flasktest.raspberry.raspberry import is_raspberrypi
from shared.sensorbase.sensorbase import TempSensor

if is_raspberrypi():
    import board
    import digitalio
    from adafruit_bme280 import basic as adafruit_bme280


# todo: rename these and create a base class of some sort
class BMP280(TempSensor):
    def __init__(self, spi, cs_pin=board.D6):
        super().__init__(f"spi_CSPIN_{cs_pin}T")  # use the CS pin as an SPI 'address'
        self.spi = spi
        self.device_path = f"T {cs_pin}" + self.get_address()
        self.sensor = adafruit_bme280.Adafruit_BME280_SPI(spi, digitalio.DigitalInOut(cs_pin))

        print('Temperature: {} degrees C'.format(self.sensor.temperature))

    def get_sensor_value(self):
        t = int(self.sensor.temperature*1000)/1000
        return t


class BMP280H(TempSensor):
    def __init__(self, spi, cs_pin=board.D6):
        super().__init__(f"spi_CSPIN_{cs_pin}H")  # use the CS pin as an SPI 'address'
        self.device_path = f"H {cs_pin}" + self.get_address()
        self.spi = spi
        self.sensor = adafruit_bme280.Adafruit_BME280_SPI(spi, digitalio.DigitalInOut(cs_pin))

        print('Humidity: {}%'.format(self.sensor.humidity))

    def get_sensor_value(self):
        h = int(self.sensor.humidity*1000)/1000
        return h

    @staticmethod
    def get_sensor_units():
        return r"%"


class BMP280P(TempSensor):
    def __init__(self, spi, cs_pin=board.D6):
        super().__init__(f"spi_CSPIN_{cs_pin}P")  # use the CS pin as an SPI 'address'
        self.device_path = f"P {cs_pin}" + self.get_address()
        self.spi = spi
        self.sensor = adafruit_bme280.Adafruit_BME280_SPI(spi, digitalio.DigitalInOut(cs_pin))

        print('Pressure: {}hPa'.format(self.sensor.pressure))

    def get_sensor_value(self):
        p = int(self.sensor.pressure*1000)/1000
        return p

    @staticmethod
    def get_sensor_units():
        return r"hPa"
