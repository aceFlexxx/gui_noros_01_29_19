#!/usr/bin/env python

import numpy as np
import rospy
import time
import message_filters
from std_msgs.msg import Int32MultiArray
from haptic_generator.msg import IntArray, WSArray
#from AD9833 import FrequencyController
from MAX518 import OutputController

class haptic_controller(OutputController):

    def __init__(self):

        rospy.init_node('haptic_control')

        self.haptic_name = rospy.get_param('~name')
        spi_address = rospy.get_param('~spi_address')
        i2c_address = rospy.get_param('~i2c_address')
        scale = rospy.get_param('~scale')

        #FrequencyController.__init__(self,spi_address)
        OutputController.__init__(self,i2c_address)
        time.sleep(1)

        self._A0max = 3.9*scale
        self._A1max = 1.05*scale


        self.ir_sub = rospy.Subscriber('/cursor_position/corrected', IntArray, self.actuation_callback, queue_size = 1)
        self.ws_sub = rospy.Subscriber('/cursor_position/workspace/'+self.haptic_name, WSArray, self.ws_callback, queue_size = 1)

        #initial publish
        self.DAC_output(0,0)
        self.last_intensity = 0
        self.ws = None

        rospy.on_shutdown(self.close)

        rospy.spin()

    def actuation_callback(self, ir_xy):
        ir_y = ir_xy.data[1]
        
        if self.ws:

            intensity = 0.0

            for i in range(self.ws.ystep):
                #print(ir_y,ir_xy.data[0])
                if list(self.ws.y_ws)[i*2] <= ir_y <= list(self.ws.y_ws)[i*2+1]:
                    ir_x = ir_xy.data[0]
                    intensity = list(self.ws.intensity)[ir_x]
                    #print(ir_y, list(self.ws.y_ws)[i*2], list(self.ws.y_ws)[i*2+1], ir_x, intensity, self._A0max*intensity, self._A1max*intensity)
                    break

                else:
                    intensity = 0

            if self._i2cbus:
                if (intensity >= self.last_intensity*0.95 or intensity <= self.last_intensity*0.975):
                    #print(intensity, ir_xy.data[0], ir_y)
                    self.DAC_output(self._A0max*intensity, self._A1max*intensity)
                    self.last_intensity = intensity

    def ws_callback(self, ws):
        self.ws = ws
        #print ws.y_ws

    def close(self):
        self.ws = None
        self.MAX518_close()
        #self.AD9833.close()

if __name__ == '__main__':
    controller = haptic_controller()
    
