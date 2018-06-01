#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import Float
from MAX518 import MAX518_Controller

class Output_Controller(MAX518_Controller):

    def __init__(self):
        rospy.init_node('output_control')

        self.haptic_name = rospy.get_param('~name')
        spi_address = rospy.get_param('~spi_address')
        i2c_address = rospy.get_param('~i2c_address')
        scale = rospy.get_param('~scale')

        OutputController.__init__(self,i2c_address)
        time.sleep(1)

        self._A0max = 3.9*scale
        self._A1max = 1.05*scale


        self.int_sub = rospy.Subscriber('/cursor_position/intensity/'+self.haptic_name, Float, self.int_callback, queue_size = 1)

        rospy.on_shutdown(self.close)
        rospy.spin()

    def int_callback(self, intensity):
        intensity = intensity.data
        if self._i2cbus:
            self.DAC_output(self._A0max*intensity, self._A1max*intensity)

    def close(self):
        self.MAX518_close()

if __name__ == '__main__':
    controller = Output_Controller()
    
