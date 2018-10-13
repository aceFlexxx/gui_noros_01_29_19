#! /usr/bin/env python
import wx
import os
import main
import numpy as np

##############################################################################80
#class Texture:
#    """"""
#    def __init__(self, id, shape):
#        """Constructor"""
#        self.id = id
#        self.shape = shape

##############################################################################80
class GuiFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent = None, id = wx.ID_ANY, title = wx.EmptyString,size = wx.GetDisplaySize(), style = wx.SYSTEM_MENU)
        
        self.width, self.height = wx.GetDisplaySize()
        self.width_half = self.width/2.0

        self.first_rectangle_y = 0.1*self.height
        self.bottom_space = 0.035*self.height
        
        self.rectangle_size = 0.175*self.height
        self.rectangle_seperation = int((self.height-self.first_rectangle_y-self.bottom_space-3*self.rectangle_size)/3.0)
        
        #set up textbox and lines 
        self.textbox_width = self.width
        self.textbox_x = 0.04*self.width
        self.textbox_y = self.rectangle_size*0.35
        self.rectangle_color = "WHITE"
        #self.rectangle_color2 = "WHITE"
        self.textbox_fontsize = int(42*((self.width*self.height)/(1794816)))
        
        self.haptic_width = self.width
        
        self.background_color = "BLACK"
        
        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint) 

    def layout(self):#set up buttons and texts
        if self.tc[0] == 1:
            gui_question = "Which rectangle felt stronger?"

        back_button = wx.Button(self.panel,wx.ID_ANY,'BACK')
        label = wx.StaticText(self.panel,wx.ID_ANY,label=gui_question,pos=(0,.7*self.height))
        label.SetFont(wx.Font(self.textbox_fontsize,wx.ROMAN,wx.NORMAL,wx.BOLD))
        button_1 = wx.Button(self.panel,wx.ID_ANY, '1',pos=(0,self.height*.8),size=(self.width_half,.2*self.height))
        button_2 = wx.Button(self.panel,wx.ID_ANY, '2',pos=(self.width_half,self.height*.8),size=(self.width_half,.2*self.height))
        
        #set up font
        button_1.SetFont(wx.Font(self.textbox_fontsize,wx.ROMAN,wx.NORMAL,wx.BOLD))
        button_2.SetFont(wx.Font(self.textbox_fontsize,wx.ROMAN,wx.NORMAL,wx.BOLD))

        ##connect buttons to functions
        back_button.Bind(wx.EVT_BUTTON,self.BackButton)
        #add arguments when connecting buttons to functions using lambda
        button_1.Bind(wx.EVT_BUTTON,lambda evt: self.option(evt,1))
        button_2.Bind(wx.EVT_BUTTON,lambda evt: self.option(evt,2))
        self.OnPaint(0)#draw again

    #go back
    def BackButton(self,event):
        f = main.frameMain(None)
        self.Close()
        f.Show()

    #----------------------------------------------------------------------
    def OnPaint(self, evt):
        """set up the device for painting"""
        dc = wx.PaintDC(self.panel)
        dc.BeginDrawing()
        brush = wx.Brush(self.background_color)
        dc.SetBackground(brush)
        dc.Clear()
        dc.SetFont(wx.Font(self.textbox_fontsize, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))

        """Rectangle 1"""
        rectangle_y = self.first_rectangle_y
        dc.SetPen(wx.Pen(self.rectangle_color))
        dc.SetBrush(wx.Brush(self.rectangle_color))
        dc.DrawRectangle(0,rectangle_y, self.width, self.rectangle_size)
        textbox = wx.Rect(self.textbox_x, rectangle_y+self.textbox_y)
        dc.DrawLabel("1)", textbox, alignment=1)

        """Rectangle 2"""
        rectangle_y = self.first_rectangle_y+(self.rectangle_size+self.rectangle_seperation)
        dc.DrawRectangle(0,rectangle_y, self.width, self.rectangle_size)
        textbox = wx.Rect(self.textbox_x, rectangle_y+self.textbox_y)
        dc.DrawLabel("2)", textbox, alignment=1)
        dc.EndDrawing()
        del dc
    
    def generate_ws(self):

        intensity_1 = np.zeros(int(self.width))
        intensity_2 = np.zeros(int(self.width))

        """Determine y workspace bounds"""
        y_ws1 = []
        y_ws2 = []

        rectangle_y = self.first_rectangle_y
        y_ws1.append(rectangle_y)
        y_ws1.append(rectangle_y+self.rectangle_size)

        rectangle_y = rectangle_y + self.rectangle_size + self.rectangle_seperation
        y_ws2.append(rectangle_y)
        y_ws2.append(rectangle_y + self.rectangle_size)

        if texture == "Sinusoid":

            for index in range(int(self.haptic_width)):
                sinusoid = np.sin(index/self.haptic_width*periods*2*np.pi)
                intensity.append(max(0,sinusoid))
                ev_intensity.append(max(0,-sinusoid))


        elif texture == "Square":
            
            for index in range(int(self.haptic_width)):
                sinusoid = np.sin(index/self.haptic_width*periods*2*np.pi)
                if (sinusoid > 0):
                    ufm_intensity.append(1.0)
                    ev_intensity.append(0.0)
                else:
                    ufm_intensity.append(0.0)
                    ev_intensity.append(1.0)
