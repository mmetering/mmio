"""
Driver for the EX9055D digital IO relay.
"""

import minimalmodbus
from django.conf import settings
from time import sleep
import serial
import logging

logger = logging.getLogger(__name__)


class EX9055DM(minimalmodbus.Instrument):
    """
    Instrument class for the EX9055D-M Modbus RTU digital IO module.
    """

    def __init__(self, address):
        self.address = address

        minimalmodbus.Instrument.__init__(self, settings.MODBUS_PORT, address)
        self.serial.timeout = 0.5  # sec
        self.serial.baudrate = 19200
        self.serial.parity = serial.PARITY_NONE
        self.serial.bytesize = 8
        self.serial.stopbits = 1

    def write_output(self, pin, value):
        sleep(0.002)
        if value == 0 or value == 1:
            self.write_bit(pin, value, functioncode=5)
        else:
            raise ValueError('Output value can only be either 0 or 1.')

    def read_output(self, pin):
        sleep(0.002)
        return self.read_bit(pin, functioncode=1)

    def read_input(self, pin):
        sleep(0.002)
        return self.read_bit(pin, functioncode=2)
