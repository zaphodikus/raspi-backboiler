# SPI K type thermououple
# MAX6675
import time
import board
import busio
import digitalio
# /dev/spidev0.0 does not exist

print('hello')
cs = digitalio.DigitalInOut(board.D5)  # GPIO 5
cs.direction = digitalio.Direction.OUTPUT

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
while not spi.try_lock():
    pass
spi.configure(baudrate=4000000)
# will run fine at 100KHz
#spi.configure(baudrate=100000)
spi.unlock()

def convert(v):
    if v & 0x4:
        return float('NaN')
    # Check if signed bit is set.
    if v & 0x80000000:
    # Negative value, take 2's compliment. Compute this with subtraction
    # because python is a little odd about handling signed/unsigned.
        v >>= 3 # only need the 12 MSB
        v -= 4096
    else:
        # Positive value, just shift the bits to get the value.
        v >>= 3 # only need the 12 MSB
        # Scale by 0.25 degrees C per bit and return value.
    return v * 0.25

raw = bytearray(2)
# gobble the first conversion and any noise
cs.value = False
cnt=0
while spi.readinto(raw, end=1):
    print(',', end='')
    cnt+=1
    if cnt > 5:
        print("Bus error, SPI slave sent too many bytes")
cs.value = True
time.sleep(0.1)

while True:
    cs.value = False
    spi.readinto(raw, end=2)
    cs.value = True
    if raw is None or len(raw) != 2:
        raise RuntimeError('Did not read expected number of bytes from device!')
    value = raw[0] << 8 | raw[1]
    #print('Raw value: 0x{0:08X}'.format(value & 0xFFFFFFFF))
    # convert to a temperature
    temp = convert(value)
    print(f"Thermocouple: {temp}°C")
    time.sleep(1)
    #cs.value = False
    