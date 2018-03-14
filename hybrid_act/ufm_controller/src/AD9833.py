#!/usr/bin/env python

import spidev
import time

class FrequencyController:

    def __init__(self, channel):
	self._spi = spidev.SpiDev()
	self._spi.open(0,channel)
	self._spi.max_speed_hz = 976000

    def _sendData(self, input1):
	tx_msb1 = input1>>8
	tx_lsb1 = input1 & 0xFF
	#self._spiEV.xfer2([tx_msb1,tx_lsb1])

	self._spi.xfer([tx_msb1])
	self._spi.xfer([tx_lsb1])

    def setup_sine(self,freq):
	word = long(round(freq*2.0**28)/25000000)
	MSB = (word & 0xFFFC000)>>14
	LSB = (word & 0x3FFF)
	
	LSB |= 0x4000					#Set bit 15 and 14 to 0 and 1
	MSB |= 0x4000					#Set bit 15 and 14 to 0 and 1

	phase = 0xC000
	
	self._sendData(0x2100)				#Control Register
        time.sleep(.001)
	self._sendData(LSB)
        time.sleep(.001)
	self._sendData(MSB)
        time.sleep(.001)
	self._sendData(phase)
        time.sleep(.001)
	self._sendData(0x2000)				#Exit Reset

    def setup_square(self,freq):
	word = int(round(float(freq*2**28))/25000000)
	MSB = (word & 0xFFFC000)>>14
	LSB = (word & 0x3FFF)
	
	LSB |= 0x4000					#Set bit 15 and 14 to 0 and 1
	MSB |= 0x4000					#Set bit 15 and 14 to 0 and 1

	phase = 0xC000
	
	self._sendData(0x2168)				#Control Register
	self._sendData(0x5893)
	self._sendData(0x4010)
	self._sendData(phase)
	self._sendData(0x2168)				#Exit Reset

    def stop_signal(self):
	self._sendData(0x0000)
	self._sendData(0x0068)

    def AD9833_close(self):
	if self._spi != None:
	    self.stop_signal()
	    self._spi.close()
	    self._spi = None

if __name__ == '__main__':
	FC = FrequencyController()
