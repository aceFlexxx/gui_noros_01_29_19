#! /usr/bin.env python
import serial
import time
import datetime
import struct

class frequency_controller(object): 
    def __init__(self, port = None, baudrate = 57600, timeout=1):
        self._start_message = b'\x02'
        self._end_message = b'\xff\xff'
        self._pkgtimeout = 10
        self._pkgtimeout_timer = 0
        self._messagewaittime = 0.025
        self._droppedpackages = 0

        self._serial_recursions = 0
        self._serial_timer = 300
        if port:
            self.ser = serial.Serial(port = port,baudrate = baudrate , timeout = timeout)
            self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
            self.ser.parity = serial.PARITY_NONE #set parity check: no parity
            self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits

        else:
            self.ser = None

    def initPort(self, port, baudrate, timeout = 1):
        if self.ser:
            self.ser.close()
        else:
            self.ser = serial.Serial(port = port,baudrate = baudrate , timeout = timeaout)

    def closePort(self):
        if self.ser:
            self.ser.close()

    def send_receive_frequency(self,arduino_case,freq):
        if self.ser:
            self.ser.write(arduino_case)
            time.sleep(self._messagewaittime)
            
            self.sendinfo(freq)

            rdata = self.ser.read(size=self.ser.in_waiting)
            time.sleep(self._messagewaittime)
            parsedData = self._parseData(rdata)

            try:
                if len(parsedData) > 2:
                    raise ValueError('Bad Serial')
                
                output = struct.unpack('>H', parsedData[0:2])[0]
                return output

            except:
                self._pkgtimeout_timer += 1
                self._droppedpackages += 1
                if self._pkgtimeout_timer > self._pkgtimeout:
                    raise ValueError ('Bad Data')
                else:
                    self.ser.flushInput()
                    self.ser.flushOutput()
                    return self.send_receive_frequency(arduino_case,freq)

        else:
            print ('Serial Communication not Established')
       
    def sendinfo(self, info):
        b = struct.pack('>H', info)
        for value in b:
            self.ser.write(value)
            time.sleep(self._messagewaittime)

    def _parseData(self,package):
        start_message_length = len(self._start_message)
        end_message_length = len(self._end_message)
        start_index = 0
        end_index = len(package)-1
        pkg_length = len(package)

        START_FLAG  = False
        END_FLAG = False

        for i in range(end_message_length, pkg_length):
            if package[-i:pkg_length+end_message_length-i] == self._end_message:
                end_index = pkg_length - i
                END_FLAG = True
                break

        if END_FLAG:
            self._serial_recursions = 0
            return package[len(self._start_message):end_index]

        if self._serial_recursions > self._serial_timer:
            return None

        else:
            self._serial_recursions += 1
            package = package + self.ser.read(self.ser.inWaiting())
            return self._parseData(package)

                        
if ( __name__ == "__main__" ):
    arduino = frequency_controller(port = '/dev/ttyACM1', baudrate = 57600)
    print(arduino.send_receive_frequency(b'\x02',10000))
    time.sleep(.1)

