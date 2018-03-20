#!/usr/bin/python/env python

import smbus
import time

class OutputController(object):

    def __init__(self, address):
        self._bus = smbus.SMBus(1)
        self._address = address

    def DAC_output(self, output1, output2):
        output1 = int(output1/5.0*255)
        output2 = int(output2/5.0*255)

        self._bus.write_byte_data(self._address, 0x00, self._address)
        self._bus.write_byte_data(self._address, 0x00, 0x00)
        self._bus.write_byte_data(self._address, 0x00, output1)
        self._bus.write_byte_data(self._address, 0x01, 0x01)
        self._bus.write_byte_data(self._address, 0x01, output2)

    def MAX518_close(self):
        self._bus.close()
        
