#!/usr/bin/python/env python

import smbus
import time

class OutputController:

    def __init__(self, address):
        self._bus = smbus.SMBus(0)
        self._address = address

    def DAC_output(self, output1, output2):
        self._bus.write_byte(address, address)
        self._bus.write_byte(address, 0x00)
        self._bus.write_byte(address, output1)
        self._bus.write_byte(address, 0x01)
        self._bus.write_byte(address, output1)
        
