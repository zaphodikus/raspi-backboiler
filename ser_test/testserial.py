#!/usr/bin/env python
import time
import serial
#

serOut = serial.Serial(
        port='COM6', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
serIn = serial.Serial(
        port='COM7', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

counter = 0

b = b"\x11\x34"
print("expect 4404")
print(int.from_bytes(b, byteorder='big', signed=False))

START_TEXT = b"\x02"
END_TEXT = b"\x03"
END_FIELD = b"\x09"
data = bytearray()
data.extend(START_TEXT)
data.extend("255".encode())
data.extend(END_FIELD)
data.extend("36.999".encode())
data.extend(END_TEXT)

data = b"\x02255\x0936.999\x03"
serOut.write(data)
response = bytearray()

while serIn.in_waiting:
        response.extend( serIn.read(1))

print(response)
address = ""
value = ""
_field = 0
for by in response:
    if by == int.from_bytes(START_TEXT, "big"):
        _field = by
        continue
    if by == int.from_bytes(END_FIELD, "big"):
        _field = by
        continue
    if by == int.from_bytes(END_TEXT, "big"):
        _field = by
        continue

    if _field == int.from_bytes(START_TEXT, "big"):
        address+=chr(by)

    if _field == int.from_bytes(END_FIELD, "big"):
        value+=chr(by)

print(address)
print(value)
