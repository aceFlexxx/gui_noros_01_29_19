#! /usr/bin/env python
import wx
import os
import rospy

import random
import time

from ws_generator.msg import WSArray
from std_msgs.msg import String

#Other GUI utilites
import main
import utils


class Frame(utils.GuiFrame):
    #----------------------------------------------------------------------
    def __init__(self,csvfile):
        """"""
        self.ws_ufm_pub = rospy.Publisher('/cursor_position/workspace/ufm', WSArray, queue_size = 0)
        self.ws_ev_pub = rospy.Publisher('/cursor_position/workspace/ev', WSArray, queue_size = 0)
        rospy.init_node('start_ws')

        utils.GuiFrame.__init__(self)

        self.CSVFILE = csvfile

        # variables for the amount of times each testing condition is finished
        self.HYBRID_COUNT = 0
        self.TRESHOLD_COUNT = 0
        self.TEXTURE_COUNT = 0

        self.FINISH_FLAG = False
        
        self.THRESHOLD_FLIPS = 0   # variable to save the amount of times user has guessed wrong after guessing right
        self.SIG_THRESHOLDS = 1
        self.REP_INCORRECT = 0

        self.CORRECT = None     #variable to save correctness of user's guess

        self.REPEAT_TESTS = 1   #variable to determine repeat of same tests
        self.TEST_CASE = 0      #variable to iterate through tests of each testing condition

        self.AMPLITUDE_MAX = 1.0
        self.AMPLITUDE_MIN = 0.75
        self.DELTA_AMPLITUDE = 0.05

        self.ws_output = None
        self.rand_output = None
        
        self.test_conditions = None

        self.determine_next_test()
        self.determine_next_condition()
        # Generate Gui
        self.layout()
        self.Centre()
        self.Show()
        # Generate ws
        # self.generate_ws()

    def option(self,event,selected):
        #print a message to confirm if the user is happy with the option selected
        string = ''.join(["You have selected ",str(selected), "). Continue?"])
        message = wx.MessageDialog(self,string,"Confirmation",wx.YES_NO)
        result = message.ShowModal()
        # If User agrees with selection, save relevant user data to csvfile
        if result == wx.ID_YES:
            #OVERWRITE CORRECT GUESS
            if self.ws_output[0][1] > 0.85:
                self.CORRECT = False
                self.THRESHOLD_FLIPS += 1
            else:
                self.CORRECT = True

            #self.determine_correctness(selected)
            self.end_time = time.time()
            self.elapsed_time = self.end_time - self.start_time
            self.save_data()
            self.determine_next_condition()

    def determine_next_test(self):
        # start hybridization test
        if self.HYBRID_COUNT < self.REPEAT_TESTS:
            self.hybridization_set()
            self.tc = self.test_conditions[0]
            self.HYBRID_COUNT += 1

        else:
            f = main.frameMain(None)
            self.Close()
            f.Show()

    def determine_next_condition(self):
        if self.THRESHOLD_FLIPS < self.SIG_THRESHOLDS or self.FINISH_FLAG:
            if not self.ws_output:
                # Construct output in the form of, channel: actuation, amplitude, texture, frequency
                self.ws_output = {0: [self.tc[1], self.AMPLITUDE_MIN, self.tc[3], self.tc[4]], \
                                  1: [self.tc[2], 1.0, self.tc[3], self.tc[4]]}
            if self.CORRECT == True:
                # increase amplitude of test condition to make test harder
                self.ws_output[0][1] += self.DELTA_AMPLITUDE
            elif self.CORRECT == False:
                # decrease amplitude of test condition to make test easier
                self.ws_output[0][1] = min(self.AMPLITUDE_MIN,self.ws_output[0][1]-2*self.DELTA_AMPLITUDE)

            self.randomize_output()
            self.define_correct_selection()
            intensity, y_ws = self.generate_ws()
            print(self.rand_output)
            self.publish_intensity(intensity,y_ws)
            
        else:
            # reset Threshold flips
            self.THRESHOLD_FLIPS = 0
            self.FINISH_FLAG = False
            # remove last test case from possible test_cases
            del self.test_conditions[self.TEST_CASE]
            self.TEST_CASE += 1
            self.ws_output = None
            self.rand_output = None
            self.CORRECT = None
            try:
                self.tc = self.test_conditions[self.TEST_CASE]
                self.determine_next_condition()

            except KeyError as e:
                # Fall in here if self.test_conditions is empty
                self.TEST_CASE = 0
                self.determine_next_test()

    def save_data(self):
        with open(self.CSVFILE, 'a') as fout:
            l = [self.CORRECT, self.elapsed_time]
            l.extend(self.ws_output[0])
            l.extend(self.ws_output[1])
            l = [str(i) for i in l]
            s = ','.join(l) + '\n'
            fout.write(s)
            fout.close()

    def publish_intensity(self,intensity,y_ws):
        ufm_msg = WSArray()
        ufm_msg.y_ws1 = y_ws[0]
        ufm_msg.y_ws2 = y_ws[1]
        ufm_msg.intensity1 = intensity[0]
        ufm_msg.intensity2 = intensity[1]

        ev_msg = WSArray()
        ev_msg.y_ws1 = y_ws[0]
        ev_msg.y_ws2 = y_ws[1]
        ev_msg.intensity1 = intensity[2]
        ev_msg.intensity2 = intensity[3]

        self.ws_ufm_pub.publish(ufm_msg)
        self.ws_ev_pub.publish(ev_msg)
                
    def hybridization_set(self):
        # construct conditions in the form of, test#: test_id, test_actuation, control_actuation, texture, freq
        self.test_conditions = {0:[1,"Hybrid","EV","Sinusoid",5], \
                                1:[1,"Hybrid","UFM","Sinusoid",5], \
                                2:[1,"UFM","Hybrid","Sinusoid",5], \
                                3:[1,"EV","Hybrid","Sinusoid",5]}

    def randomize_output(self):
        # randomize channel 0 and 1
        key1,key2 = random.sample(list(self.ws_output),2)
        self.rand_output = {}
        self.rand_output[key1], self.rand_output[key2] = self.ws_output[0], self.ws_output[1]


    def define_correct_selection(self):
        # determine which output channel is the correct choice
        if self.rand_output[0][1] == self.tc[1]:
            self.correct_selection = 0
        else:
            self.correct_selection = 1

    def define_correctness(self,selected):
        if selected == self.correct_selection:
            if not self.CORRECT:
                self.CORRECT = True
            if self.ws_output[0][1] >= self.MAX_AMPLITUDE:
                self.FINISH_FLAG = True

            self.REP_INCORRECT = 0
        else:
            if self.CORRECT:
                self.THRESHOLD_FLIPS += 1
                self.CORRECT = False
            
            self.REP_INCORRECT +=1 
            
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()
