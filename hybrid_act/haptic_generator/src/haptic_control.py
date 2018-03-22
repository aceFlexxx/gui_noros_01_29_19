#!/usr/bin/env python

import numpy as np
import rospy
import message_filters
from std_msgs.msg import Int32MultiArray
from haptic_generator.msg import IntArray, WSArray
from AD9833 import FrequencyController
from MAX518 import OutputController

class haptic_controller(FrequencyController, OutputController):

    def __init__(self):

        self.haptic_name = rospy.get_param('~name')
        spi_address = rospy.get_param('~spi_address')
        i2c_address = rospy.get_param('~i2c_address')
        scale = rospy.get_param('~scale')

        FrequencyController.__init__(self,spi_address)
        OutputController.__init__(self,i2c_address)

        rospy.init_node(self.haptic_name +'_control')
        self._A0max = 3.9*scale
        self._A1max = 1.05*scale

        self.param_pub = rospy.Publisher('/'+self.haptic_name+'_parameters', Int32MultiArray, queue_size=0)

        self.ir_sub = rospy.Subscriber('/cursor_position/corrected', IntArray, self.actuation_callback)
        self.ws_sub = rospy.Subscriber('/cursor_position/workspace/'+self.haptic_name, WSArray, self.ws_callback)

        #initial publish
        self.param_pub.publish(Int32MultiArray(data=[0,0]))
        self.DAC_output(0.0,0.0)

        self.ws = None

        rospy.spin()

    def actuation_callback(self, ir_xy):
        ir_y = ir_xy.data[1]
        
        if self.ws:

            intensity = 0.0

            for i in range(self.ws.ystep):
                if list(self.ws.y_ws)[i*2] <= ir_y <= list(self.ws.y_ws)[i*2+1]:
                    ir_x = ir_xy.data[0]
                    intensity = list(self.ws.intensity)[ir_x]
                    break

            self.DAC_output(self._A0max*intensity, self._A1max*intensity)
            #print(self._A0*intensity, self._A1*intensity)

    def ws_callback(self, ws):
        self.ws = ws

if __name__ == '__main__':
    controller = haptic_controller()
