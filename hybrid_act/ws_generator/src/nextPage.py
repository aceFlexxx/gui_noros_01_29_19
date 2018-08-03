#!/usr/bin/python

import wx
import wx.xrc
import game
import numpy as np
from PIL import Image
import main
import math as m

class Frame (wx.Frame):

    def __init__(self,parent):
        wx.Frame.__init__(self,parent,style = wx.MAXIMIZE)
        bsizer = wx.BoxSizer(wx.VERTICAL)
        self.quitButton = wx.Button(self,wx.ID_ANY,u"Quit") #takes user home
        self.continueB = wx.Button(self,wx.ID_ANY,u"Continue")  #continue loops back to game
        bsizer.Add(self.quitButton,0,wx.ALIGN_RIGHT|wx.TOP,0)

        self.SetSizer(bsizer)
        self.width, self.height = wx.GetDisplaySize()

        self.Bind(wx.EVT_PAINT,self.OnPaintBumps)
        self.quitButton.Bind(wx.EVT_BUTTON,self.onQuit)
        self.continueB.Bind(wx.EVT_BUTTON,self.onCont)

    def OnPaintBumps(self,evt):  #runs when script is opened
        x = self.width
        y = self.height
        rad = int(m.ceil(self.width*.033))  #set radius to rounded up int

        dc = wx.PaintDC(self)
        dc.BeginDrawing()
        brush = wx.Brush('black')
        dc.SetBackground(brush)
        dc.Clear()
        color = wx.Colour(255,0,0)
        dc.SetBrush(wx.Brush(color))
        dc.DrawCircle((x/5),(y/5),rad)
        dc.DrawCircle((x*.75),(y*.6),rad)
        dc.DrawCircle((x*.5),(y*.25),rad)
        dc.DrawCircle((x*.33),(y*.33),rad)
        ##draws 4 circles in exact spots where bumps could occur
        dc.EndDrawing()


    def onQuit(self,evt): ##open home
        f = main.frameMain(None)
        self.Close()
        f.Show()

    def onCont(self,evt):  ##loops back to game for another test trial
        f = game.Frame(None)
        self.Close()
        f.Show()



        #b1 = game.generateBump(rad,x/5,x/5,x,y)
        #b2 = game.generateBump(rad,x*.75,y*.8,x,y)
        #b3 = game.generateBump(rad,x*.5,y*.5,x,y)
        #b4 = game.generateBump(rad,x*.33,y*.9,x,y)

        #a = np.zeros([self.height,self.width,3],dtype = np.uint8)
        #ev1 = b1.ev
        #ev2 = b2.ev
        #ev3 = b3.ev
        #ev4 = b4.ev

        #for i in range(self.width):
            #for j in range(self.height):
                #if ev1[i][j] != 0:
                #    val = ev1[i][j]
                #    a[j,i] = [int(val*255),0,0]
                #if ev2[i][j] != 0:
                #    val = ev2[i][j]
                #    a[j,i] = [int(val*255),0,0]
                #if ev3[i][j] != 0:
                #    val = ev3[i][j]
                #    a[j,i] = [int(val*255),0,0]
                #if ev4[i][j] != 0:
                #    val = ev4[i][j]
                #    a[j,i] = [int(val*255),0,0]

        #self.bumpDisplay(a)


    #def bumpDisplay(self,array):
    #    img = Image.fromarray(array)
    #    img.show()
    #    f = main.frameMain(None)
    #    f.Show()
