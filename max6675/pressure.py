# pressure sensor on SPI
import board
import busio
import digitalio
import time
import sys

def const(a):
    return a

_BME280_REGISTER_SOFTRESET = const(0xE0)
_BME280_REGISTER_CTRL_HUM = const(0xF2)
_BME280_REGISTER_STATUS = const(0xF3)
_BME280_REGISTER_CTRL_MEAS = const(0xF4)
_BME280_REGISTER_CONFIG = const(0xF5)
_BME280_REGISTER_TEMPDATA = const(0xFA)
_BME280_REGISTER_HUMIDDATA = const(0xFD)


class BMP280(object):
    def __init__(self, cs_pin=board.D6):
        self._chip_select = cs_pin
        self.cs = digitalio.DigitalInOut(self._chip_select)  # normally GPIO 5
        self.cs.direction = digitalio.Direction.OUTPUT
        self.spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=4000000)  # 4MHz, chip can do 5MHz normally
        # Note: will run fine at 100KHz
        self.spi.unlock()
        self.raw = bytearray(20)
        
    def read(self):
        self.cs.value = False
        register = _BME280_REGISTER_TEMPDATA
        self.spi.write(bytes([register & 0xFF]))
        incount = self.spi.readinto(self.raw, end=1)
        print(incount)
        self.cs.value = True    
        
        
bm = BMP280()
bm.read()

