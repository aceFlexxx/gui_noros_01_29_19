#! /usr/bin.env python
import serial
import time
import datetime
import struct

class Frequencies():
    def __init__(self, port = None, baudrate =115200, timeout=1):
        self._start_message = b'\x02'
        self._end_message = b'\xff\xff'
        self._pkgtimeout = 10
        self._pkgtimeout_timer = 0
        self._messagewaittime = 0.010
        self._droppedpackages = 0

        self._serial_recursions = 0
        self._serial_timer = 300
        if port:
            self.ser = serial.Serial(port = port,baudrate = baudrate , timeout = timeout)

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

    def get_frequency(self,n,m):
        if self.ser:
            self.ser.write(b'\x02')
            time.sleep(self._messagewaittime)
            
            self.sendinfo(n)

            self.sendinfo(m)

            data1 = self.ser.read(self.ser.inWaiting())
            #print('data1 ',data1)
            time.sleep(self._messagewaittime)
            parsedData1 = self._parseData(data1)
            time.sleep(self._messagewaittime)
            #print('parse1d', parsedData1)
             
            data2 = self.ser.read(self.ser.inWaiting())
            #print('data2 ',data2)
            time.sleep(self._messagewaittime)
            parsedData2 = self._parseData(data2)
            time.sleep(self._messagewaittime)
            #print('parsed2', parsedData2)

            try:
                if len(parsedData1) > 2 or not len(parsedData1):
                    raise ValueError('Bad Serial')
                #print('trying')
                output = []
                
                output.append(struct.unpack('>H',parsedData1[0:2])[0])
                output.append(struct.unpack('>H',parsedData2[0:2])[0])
                
                self._pkgtimeout_timer = 0
                return output
            except:
                print('fucked')
                self._pkgtimeout_timer += 1
                self._droppedpackages += 1
                if self._pkgtimeout_timer > self._pkgtimeout:
                    raise ValueError ('Bad Data')
                else:
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                    return self.get_frequency

        else:
            print ('Serial Communication not Established')
       
    def sendinfo(self, info):
        for i in range(2):
            self.ser.write(bytes([struct.pack('>H',info)[i]]))
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
    arduino = Frequencies(port = '/dev/cu.usbmodem1411', baudrate = 115200)
    for i in range(19,20):
        print(i,'and',i-9, arduino.get_frequency(i,i-9))

