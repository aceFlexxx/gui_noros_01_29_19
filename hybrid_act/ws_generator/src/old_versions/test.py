#! /usr/bin/env python
import csv
import wx
import numpy as np
import os
import rospy
#from ws_generator.msg import WSArray
from std_msgs.msg import String

import main
import utils


##############################################################################80
#class Texture:
#    """"""
#    def __init__(self, id, shape):
#        """Constructor"""
#        self.id = id
#        self.shape = shape

##############################################################################80

class Frame(utils.GuiFrame):
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        #self.ws_ufm_pub = rospy.Publisher('/cursor_position/workspace/ufm', WSArray, queue_size = 0)
        #self.ws_ev_pub = rospy.Publisher('/cursor_position/workspace/ev', WSArray, queue_size = 0)
        #rospy.init_node('gui_ws')

        utils.GuiFrame.__init__(self)
        # dictionary in the shape of:
        # test_num: test_condition,actuation_method1,actuation_method2,texture1,texture2,freq1,freq2,amp1,amp2
        self.HYBRID_COUNT = 0
        self.TRESHOLD_COUNT = 0
        self.TEXTURE_COUNT = 0
        self.THRESH_FLIPS = 0

        self.CORRECT = True

        self.REPEAT_TESTS = 2
        self.TEST_CASE = 0

        self.test_conditions = None
        self.determine_next_test()
        self.determine_next_condition()
        

    def determine_next_test(self):
        # start hybridization test
        if self.HYBRID_COUNT < self.REPEAT_TESTS:
            self.hybridization_set()
            self.tc = self.test_conditions[0]
            self.HYBRID_COUNT += 1
            self.determine_next_condition()

    def determine_next_condition(self):
        if self.THRESH_FLIPS < 3:
            if !self.output:
                # Construct output in the form of, channel: actuation, amplitude, texture, frequency
                self.output = {0: [self.tc[1], 0.5, self.tc[3], self.tc[4],1], \
                               1: [self.tc[2], 1.0, self.tc[3], self.tc[4],0]}
            if self.CORRECT:
                # decrease amplitude of test condition
                self.output[0][1] += delta_amplitude
            else:
                # increase amplitude of test condition
                self.output[0][1] -= delta_amplitude

            self.randomize_output()
            self.define_correct_selection()
            self.generate_ws()

        else:
            # reset Threshold flips
            self.THRESH_FLIPS = 0
            # remove last test case from possible test_cases
            del self.test_conditions[self.TEST_CASE]
            self.TEST_CASE += 1
            #  last test case from possible test_cases
            try:
                self.tc = self.test_conditions[self.TEST_CASE]
                self.determine_next_condition()

            except KeyError as e:
                self.determine_next_test()
                
    def hybridization_set(self):
        self.test_conditions = {0:[1,"Hybrid","EV","Sinusoid",5], \
                                1:[1,"Hybrid","UFM","Sinusoid",5], \
                                2:[1,"UFM","Hybrid","Sinusoid",5], \
                                3:[1,"EV","Hybrid","Sinusoid",5]}

    def randomize_output(self):
        # randomize channel 0 and 1
        key1,key2 = random.sample(list(self.output),2)
        self.output[key1], self.output[key2] = self.output[0], self.output[1]


    def define_correct_selection(self):
        if self.output[0][-1] == 1:
            self.correct_selection = 0
        else:
            self.correct_selection = 1

    def option(self,event,selected,correct_selection):
        #print a message confirming whether option was correct or wrong
        if selected == correct_selection:
            message = wx.MessageDialog(self,"That is correct!","Answer",wx.OK)
            self.colorit()
        else:
            message = wx.MessageDialog(self,"Sorry, try again","Answer",wx.OK)
            self.colorit()

        message.ShowModal()
        #restart main page to try again
        self.textbox_color1 = "WHITE"
        self.textbox_color2 = "WHITE"
        self.layout()
    
#    def colorit(self):
#        #it paints the right answer
#        correct_selection=self.define_correct_selection()
#        if correct_selection==1:
#            self.textbox_color1 = "BLUE"
#        else:
#            self.textbox_color2 = "BLUE"
#        self.layout()

    

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()
