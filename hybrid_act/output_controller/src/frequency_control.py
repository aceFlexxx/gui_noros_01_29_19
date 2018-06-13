#!/usr/bin/env python

import rospy
import time
import struct
from std_msgs.msg import UInt16
from Arduino import frequency_controller

class Arduino_Controller(frequency_controller):

    def __init__(self):
        rospy.init_node('output_control')
        
        self.haptic_name = rospy.get_param('~name')
        self.arduino_case = struct.pack('B',rospy.get_param('~arduino_case'))
        frequency_controller.__init__(self,port = '/dev/ttyACM0',baudrate = 57600)
        time.sleep(1)

        self.freq_sub = rospy.Subscriber('/'+self.haptic_name+'/frequency/', UInt16, self.freq_callback, queue_size = 1)

        rospy.on_shutdown(self.close)
        rospy.spin()

    def freq_callback(self, frequency):
        frequency = frequency.data
        if self.ser:
            self.send_receive_frequency(self.arduino_case,frequency)

    def close(self):
        self.closePort()

if __name__ == '__main__':
    controller = Arduino_Controller()
    
