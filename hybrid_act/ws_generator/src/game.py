#! /usr/bin/python


import wx
import wx.xrc
import startPage
import rospy
import numpy as np
from ws_generator.msg import WSArray
from std_msgs.msg import String
import random
import math as m
import time
import csv
import nextPage

class Frame(wx.Frame):

    def __init__(self,parent):
        wx.Frame.__init__(self,parent,style = wx.MAXIMIZE)
        self.SetBackgroundColour('black') ## BLANK SCREEN
        bsizer = wx.BoxSizer(wx.VERTICAL)
        #self.ws_ufm_pub = rospy.Publisher('/cursor_position/workspace/ufm',WSArray, queue_size = 0)
        #self.ws_ev_pub = rospy.Publisher('/cursor_postion/workspace/ev', WSArray, queue_size = 0)
        #rospy.init_node('gui_ws')
        start_time = time.time()

        self.width, self.height = wx.GetDisplaySize() ## pixel info

        ##print(self.width)
        ##print(self.height)

        self.backButton = wx.Button(self,wx.ID_ANY,u"Back") #back to start page
        self.nextPage = wx.Button(self,wx.ID_ANY,u"Next") ## takes you to frame with bumps drawn
        bsizer.Add(self.backButton,0,wx.ALIGN_RIGHT|wx.TOP,0)

        self.SetSizer(bsizer)
        self.Layout()

        self.randomSignal()  ##randomally generates one of the four possible bumps

        self.backButton.Bind(wx.EVT_BUTTON,self.onbackButton)
        self.nextPage.Bind(wx.EVT_BUTTON,lambda evt,name=start_time:self.onNextClick(evt,name))

    def onbackButton(self,event): ##start page
        f = startPage.Frame(None)
        self.Close()
        f.Show()


    def onNextClick(self,event,t):  ##next page draws out all bump possiblities and writes time taken to csv
        f = nextPage.Frame(None)
        end_time = time.time() - t
        et =  str(end_time)
        file = open('output.csv','a')
        file.write(et)
        f.Show()
        self.Close()


    def randomSignal(self):  #random generator decides one of the cases
        np.zeros(shape=(self.width,self.height))
        b_rad = m.ceil(self.width*.033)

        for x in range(1):
            i = random.randint(1,4)

        if i == 1:
            vertX = self.width/5
            vertY = self.height/5
            b = generateBump(b_rad,vertX,vertY,self.width,self.height)


        elif i == 2:
            vertX = self.width*.75
            vertY = self.height*.6
            b = generateBump(b_rad,vertX,vertY,self.width,self.height)


        elif i == 3:
            vertX = self.width*.5
            vertY = self.height*.25
            b = generateBump(b_rad,vertX,vertY,self.width,self.height)


        elif i == 4:
            vertX = self.width*(.33)
            vertY = self.height*(.33)
            b = generateBump(b_rad,vertX,vertY,self.width,self.height)


class generateBump():  ## called inside of random signal, one bump being picked each time script is called

    def __init__(self,radius,vertX,vertY,width,height):
        self.radius = radius #bump radius
        self.vertX = vertX    #centers of bump
        self.vertY = vertY
        self.width = width    #screen
        self.height = height   #screen
        dm = 2*radius
        begx = int(self.vertX - dm)  #next two lines are x dimensions of shrunk rectangle
        endx = int(self.vertX + dm)  #in order to increase loop efficiency
        begy = int(self.vertY - dm)  ##same but with y cordinates
        endy = int(self.vertY + dm)

        ev = np.zeros(shape=(self.width,self.height))  #bump is ev
        ufm = np.ones(shape=(self.width,self.height))  #rest of the screen is ufm

        for i in range(begx,endx+1):  #loop in smaller rectangluar region
            for j in range(begy,endy+1):  #same but in y direction
                pyx = m.pow(self.vertX - i,2)  #x^2
                pyy = m.pow(self.vertY - j,2)  #y^2
                pysum = pyx + pyy
                radsq = m.pow(self.radius,2)  #r^2
                a = 3*radsq  ##mathematically found value for coefficient

                if pysum >= radsq:  ##outside of bump region
                    ev[i][j] = 0  #ev off
                    z = (pysum - radsq)/a  #parabolic equation
                    ufm[i][j] = min(1,z)  #ufm increases outside bump at a parabolic rate

                else:  #at border or inside bump
                    z = m.sqrt(radsq - pysum) #spherical equation  
                    z = z*(1.25)/self.radius  #normalizing sphere
                    ev[i][j] = min(1,z)  #ev intensity takes spherical shape inside bump
                    ufm[i][j] = 0  #no ufm inside bump
