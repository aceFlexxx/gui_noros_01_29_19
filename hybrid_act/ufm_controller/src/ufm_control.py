#!/usr/bin/env python

import numpy as np
import rospy
import message_filters
from std_msgs.msg import Int32MultiArray
from ufm_controller.msg import IntArray

class Ufm_controller(AD9833, MAX518):

    def __init__(self):
        super(AD9833, self).__init__(0)
        super(MAX518, self).__init__(0x2C)

        rospy.init_node('ufm_control')
        self._A0 = 3.5
        self._A1 = 1.0

        self.param_pub = rospy.Publisher('/ufm_parameters', Int32MultiArray, queue_size=0)

        self.ir_sub = rospy.Subscriber('/cursor_position/corrected', IntArray, actuation_callback)
        self.ws_sub = rospy.Subscriber('/cursor_position/workspace/ufm', WSArray, ws_callback)

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
                if self.ws.y_ws[i*2] <= ir_y <= list[i*2+1]:
                    ir_x = ir_xy.data[0]
                    intensity = self.ws.instensity[ir_x]
                    break

            self.DAC_output(self._A0*intensity, self._A1*intensity)
            print(self._A0*intensity, self._A1*intensity)

    def ws_callback(self, ws):
        self.ws = ws

if __name__ = '__main__':
    controller = Ufm_controller()
