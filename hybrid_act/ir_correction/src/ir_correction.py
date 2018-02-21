#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32MultiArray 

import os

if "SSH_CONNECTION" not in os.environ:
    import pyautogui
    RUN_FLAG = 1

else:
    RUN_FLAG = 0

class IR_Controller():
    
    def __init__(self, *args, **kargs):
        rospy.init_node('cursor_control')
        self.cursor_pub = rospy.Publisher('/cursor_position/corrected', Int32MultiArray, queue_size=0)
        self.raw_pub = rospy.Publisher('/cursor_position/raw', Int32MultiArray, queue_size=0)
        self.rate = 20

        self._xscale = 1 
        self._yscale = 1
        self._xoffset = 0
        self._yoffset = 0

        self.last_position = self.raw_position = list(pyautogui.position())
        self.cursor_correction()

        r = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            self.callback()
            r.sleep
           
    def callback(self):
        self.raw_position = list(pyautogui.position())

        if (self.raw_position != self.last_position):
            self.cursor_correction()

    def cursor_correction(self):
        self.raw_position_msg = Int32MultiArray(data=self.raw_position)
        self.raw_pub.publish(self.raw_position_msg)
        
        self.corrected_position = [int(self.raw_position[0]*self._xscale + self._xoffset), int(self.raw_position[1]*self._yscale + self._yoffset)]
        self.corrected_position_msg = Int32MultiArray(data=self.corrected_position)
        self.cursor_pub.publish(self.corrected_position_msg)

        pyautogui.moveTo(self.corrected_position[0], self.corrected_position[1])


if __name__ == '__main__':
    try:
        if RUN_FLAG:
            IR_Controller()

    except rospy.ROSInterruptException:
        pass
