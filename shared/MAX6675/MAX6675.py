import board
import busio
import digitalio
import time
from shared.DS18B20.ds18b20 import TempSensor

class MAX6675(TempSensor):
    def __init__(self, cs_pin=board.D5):
        """

        :param cs_pin: The pin to use for SPI chip select
        """
        super().__init__(f"spi{cs_pin}")  # use the CS pin as an SPI 'address'
        self._chip_select = cs_pin
        self.cs = digitalio.DigitalInOut(self._chip_select)  # normally GPIO 5
        self.cs.direction = digitalio.Direction.OUTPUT
        self.spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=4000000)  # 4MHz, chip can do 5MHz normally
        # Note: will run fine at 100KHz
        self.spi.unlock()
        self.raw = bytearray(2)

        # gobble the first conversion and any noise
        self.cs.value = False
        cnt = 0
        while self.spi.readinto(self.raw, end=1):
            print(',', end='')
            cnt += 1
            if cnt > 5:
                print("Bus error, SPI slave sent too many bytes")
        self.cs.value = True

    @staticmethod
    def convert_celcius(raw_val):
        if raw_val & 0x4:
            return float('NaN')
        # Check if signed bit is set.
        if raw_val & 0x80000000:
        # Negative value, take 2's compliment. Compute this with subtraction
        # because python is a little odd about handling signed/unsigned.
            raw_val >>= 3 # only need the 12 MSB
            raw_val -= 4096
        else:
            # Positive value, just shift the bits to get the value.
            raw_val >>= 3 # only need the 12 MSB
            # Scale by 0.25 degrees C per bit and return value.
        return raw_val * 0.25

    def get_sensor_temp(self):
        self.cs.value = False
        self.spi.readinto(self.raw, end=2)
        self.cs.value = True
        if self.raw is None or len(self.raw) != 2:
            raise RuntimeError('Did not read expected number of bytes from device!')
        value = self.raw[0] << 8 | self.raw[1]
        # print('Raw value: 0x{0:08X}'.format(value & 0xFFFFFFFF))
        # convert to a temperature
        return self.convert(value)
