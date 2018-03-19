#!/usr/bin/env python

import numpy as np
import rospy
import message_filters
from std_msgs.msg import Int32MultiArray
from ufm_controller.msg import IntArray, WSArray
from AD9833 import FrequencyController
from MAX518 import OutputController

class Ufm_controller(FrequencyController, OutputController):

    def __init__(self):

        FrequencyController.__init__(self,0)
        OutputController.__init__(self,0x2c)

        rospy.init_node('ufm_control')
        self._A0max = 3.9
        self._A1 = 1.05

        self.param_pub = rospy.Publisher('/ufm_parameters', Int32MultiArray, queue_size=0)

        self.ir_sub = rospy.Subscriber('/cursor_position/corrected', IntArray, self.actuation_callback)
        self.ws_sub = rospy.Subscriber('/cursor_position/workspace/ufm', WSArray, self.ws_callback)

        #initial publish
        self.param_pub.publish(Int32MultiArray(data=[0,0]))
        self.DAC_output(0.0,0.0)

        self.ws = None

        rospy.spin()

    def actuation_callback(self, ir_xy):
        ir_y = ir_xy.data[1]
        
        if self.ws:
            self.ws.ystep
            self.ws.y_ws

            intensity = 0.0

            for i in range(self.ws.ystep):
                if list(self.ws.y_ws)[i*2] <= ir_y <= list(self.ws.y_ws)[i*2+1]:
                    ir_x = ir_xy.data[0]
                    intensity = list(self.ws.intensity)[ir_x]
                    break

            self.DAC_output(self._A0*intensity, self._A1*intensity)
            #print(self._A0*intensity, self._A1*intensity)

    def ws_callback(self, ws):
        self.ws = ws

if __name__ == '__main__':
    controller = Ufm_controller()
