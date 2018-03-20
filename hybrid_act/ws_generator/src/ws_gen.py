#!/usr/bin/env python

import numpy as np
import rospy
import pyautogui
from ws_generator.msg import WSArray 
from ws_generator.msg import GuiMsg 


class ws_gen():

    def __init__(self):
        """"""
        self.ws_ufm_pub = rospy.Publisher('/cursor_position/workspace/ufm', WSArray, queue_size = 0)
        self.ws_ev_pub = rospy.Publisher('/cursor_position/workspace/ev', WSArray, queue_size = 0)

        self.gui_sub = rospy.Subscriber('/gui/workspace_msg', GuiMsg, self.generation_callback)

        rospy.init_node('ws_gen')

        self.x_max, self.y_max = pyautogui.size()
        self.x_max_half = x_max/2.0

        rospy.spin()
    
    def generation_callback(self, GuiMsg):
        """"""
        x0 = 150.0
        x1 = 30.0
        xd = 250.0

        ufm_intensity = []
        ev_intensity = []

        for x_index in range((x_max+1)/2):
            if (x_max_half-xd <= x_index):
                ufm_int = 1.0-(x_index-(x_max_half-xd))/(xd-x0)
                ufm_intensity.append(max(0,min(1,ufm_int)))

                ev_int = (x_index-(x_max_half-x0))/(x0-x1)
                ev_intensity.append(max(0,min(1,ev_int)))

            else:
                ufm_intensity.append(1.0)
                ev_intensity.append(0)
                
        for i in reversed(ufm_intensity):
            ufm_intensity.append(i)

        for i in reversed(ev_intensity):
            ev_intensity.append(i)
            
        ufm_msg = WSArray()
        ufm_msg.header.stamp = rospy.Time(0.0)
        ufm_msg.ystep = 2 
        ufm_msg.y_ws = GuiMsg.ufm_y  
        ufm_msg.intstep = 1
        ufm_msg.intensity = ufm_intensity
        

        ev_msg = WSArray()
        ev_msg.header.stamp = rospy.Time(0.0)
        ev_msg.ystep = 2
        ev_msg.y_ws = GuiMsg.ev_y  
        ev_msg.intstep = 1
        ev_msg.intensity = ev_intensity

        self.ws_ufm_pub.pub(ufm_msg)
        self.ws_ev_pub.pub(ev_msg)


if __name__ == '__main__':
    try:
        ws_gen_bump()
    except rospy.ROSInterruptException:
        pass
