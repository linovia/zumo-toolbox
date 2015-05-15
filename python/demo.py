import serial
import time
import logging
from datetime import datetime


PORT = "/dev/cu.usbmodemfd121"

arduino = serial.Serial(PORT, 115200, timeout=1)
time.sleep(5)  # give the connection a second to settle

status = True


def blink():
    status = True
    while True:
        if status:
            arduino.write(b"\x02\x01\x00\x00")
            print("Up")
        else:
            arduino.write(b"\x02\x00\x00\x00")
            print("Down")
        status = not status
        time.sleep(0.2)
        result = arduino.read()
        print('Result: %s %s' % (result.decode('utf8'), type(result)))

    # arduino.write(b"\x01\x00\x00\x00")
    # result = arduino.read()
    # print('Ping: %s %s' % (result.decode('utf8'), type(result)))


class Zumo(object):
    logger = logging.getLogger(__name__)

    def led(self, on=False):
