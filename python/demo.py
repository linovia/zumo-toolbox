from struct import pack, unpack
import serial
import time
import logging
from datetime import datetime


PORT = "/dev/cu.usbmodem1421"
logger = logging.getLogger(__name__)

arduino = serial.Serial(PORT, 115200, timeout=1)
# arduino = serial.Serial(PORT, 9600, timeout=1)
time.sleep(5)  # give the connection a second to settle

status = True


def echo(chr):
    arduino.write(b"\x01" + chr + b"\x00\x00")
    result = arduino.read()
    print(result)


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


LEFT_MOTOR = 0x04
RIGHT_MOTOR = 0x08


class Zumo(object):
    PACKET_SIZE = 4

    def send_data(self, data):
        trailing_size = self.PACKET_SIZE - len(data)
        data = data + b'\x00' * trailing_size
        arduino.write(data)
        print('Sent: %s' % str(data))

    def echo(self, chr):
        """
        Returns a single byte.
        """
        data = pack('>Bxxx', chr)
        self.send_data(data)
        result = arduino.read(2)
        print(result)

    def led(self, on=False):
        """
        Turns `on` the LED.
        """
        data = pack('>BBxx', 2, int(on))
        self.send_data(data)

    def motor(self, speed=0, left=False, right=False):
        """
        Set `left` and/or `right` motors at `speed`
        """
        select = (LEFT_MOTOR if left else 0) | (RIGHT_MOTOR if right else 0)
        data = pack('>Bhx', select, speed)
        self.send_data(data)
        print(arduino.read(2))
        print(arduino.read(2))
