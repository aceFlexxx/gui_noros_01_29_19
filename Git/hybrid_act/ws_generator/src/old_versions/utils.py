#! /usr/bin/env python
import wx
import time
import numpy as np

import wx
import main
from ball import Ball

class GuiPanel(wx.Window):
    def __init__(self, parent, refresh, length, ball_starts):
        wx.Window.__init__(self, parent)
        self.ball = []
        self.parent = parent
        self.last_pos = self.ScreenToClient(wx.GetMousePosition())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour("WHITE")

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.WIDTH,self.HEIGHT = self.GetClientSize()
        self.BALL_RADIUS = 40
        self.BALL_VELOCITY = 10       #cm/s
        self.REFRESH = refresh
        self.LENGTH = length
        #self.BALL_STARTS = [[self.BALL_RADIUS+10,self.BALL_RADIUS], [self.BALL_RADIUS+10,self.BALL_RADIUS*4]]
        self.BALL_STARTS = ball_starts
        self.WAIT = 10
        
        self.wait_count = []
        for l in self.BALL_STARTS:
            self.ball.append(Ball(l,self.BALL_RADIUS,self.WIDTH-self.BALL_RADIUS*1.5))
            self.wait_count.append(0)

        wx.CallLater(200, self.SetFocus)
        self.update_drawing()

    def on_size(self, event):
        self.WIDTH, self.HEIGHT = self.GetClientSize()
        for ball in self.ball:
            ball.update_limit(self.WIDTH-2*self.BALL_RADIUS)
        self.BALL_MOVEX = int(self.BALL_VELOCITY*self.REFRESH*self.WIDTH/(2450.*self.LENGTH))

        self.WIDTH_half = self.WIDTH/2.0

        self.FIRST_RECTANGLE_Y = 0.1*self.HEIGHT
        self.bottom_space = 0.035*self.HEIGHT
        
        self.rectangle_size = 0.175*self.HEIGHT
        self.rectangle_seperation = int((self.HEIGHT-self.FIRST_RECTANGLE_Y-self.bottom_space-3*self.rectangle_size)/3.0)
        
        #set up textbox and lines 
        self.TEXTBOX_WIDTH = self.WIDTH
        self.TEXTBOX_X = 0.04*self.WIDTH
        self.TEXTBOX_Y = self.rectangle_size*0.35
        self.RECTANGLE_COLOR = "WHITE"
        self.TEXTBOX_FONTSIZE = int(42*((self.WIDTH*self.HEIGHT)/(1794816.)))
        
        self.HAPTIC_WIDTH = self.WIDTH

        self.parent.layout()
        
        self.update_drawing()

    def update_drawing(self):
        self.Refresh(True)        

    def on_paint(self, event):
        x, y = self.ScreenToClient(wx.GetMousePosition())
        dc = wx.AutoBufferedPaintDC(self)
        self.parent.on_paint(0,dc)
        
        for i,ball in enumerate(self.ball):
            if ball.x - self.BALL_RADIUS <= x <= ball.x + self.BALL_RADIUS:
                if ball.y - self.BALL_RADIUS <= y <= ball.y + self.BALL_RADIUS:
                    self.wait_count[i] = 0
                    dc.Clear()
                    ball.move_forward(dc,self.BALL_MOVEX)
                    break
            elif ball.x != self.BALL_STARTS[i][0]:
                if self.wait_count[i] < self.WAIT:
                    dc.Clear()
                    self.wait_count[i] += 1
                    ball.hold_ball(dc)
                    break
                else:
                    dc.Clear()
                    self.wait_count[i] = 0
                    ball.move_ball(dc,self.BALL_STARTS[i])
            else:
                ball.move_ball(dc,self.BALL_STARTS[i])

class GuiFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, parent = None, id = wx.ID_ANY, title = wx.EmptyString,size = wx.GetDisplaySize(), style = wx.SYSTEM_MENU)

        self.Bind(wx.EVT_TIMER, self.on_timer)

        self.REFRESH_RATE = 20
        self.SCREEN_LENGTH = 21.5625                    #in
        self.ball_starts = [[100,100]]
        self.panel = GuiPanel(self, self.REFRESH_RATE, self.SCREEN_LENGTH, self.ball_starts)
        self.timer = wx.Timer(self)
        self.timer.Start(self.REFRESH_RATE)
                    
    def on_timer(self, event):
        self.panel.update_drawing()

    #go back
    def back_button(self,event):
        f = main.frameMain(None)
        self.Close()
        f.Show()

    def layout(self):#set up buttons and texts
        if self.tc[0] == 1:
            gui_question = "Which Texture Felt Stronger?"

        textbox_fontsize = self.panel.TEXTBOX_FONTSIZE
        height = self.HEIGHT
        width = self.WIDTH
        width_half = width/2.0

        back_button = wx.Button(self.panel,wx.ID_ANY,'BACK')
        label = wx.StaticText(self.panel,wx.ID_ANY,label=gui_question,pos=(0,.7*height))
        label.SetFont(wx.Font(textbox_fontsize,wx.ROMAN,wx.NORMAL,wx.BOLD))
        button_1 = wx.Button(self.panel,wx.ID_ANY, '1',pos=(0,height*.8),size=(width_half,.2*height))
        button_2 = wx.Button(self.panel,wx.ID_ANY, '2',pos=(width_half,height*.8),size=(width_half,.2*height))
        
        #set up font
        button_1.SetFont(wx.Font(textbox_fontsize,wx.ROMAN,wx.NORMAL,wx.BOLD))
        button_2.SetFont(wx.Font(textbox_fontsize,wx.ROMAN,wx.NORMAL,wx.BOLD))

        ##connect buttons to functions
        back_button.Bind(wx.EVT_BUTTON,self.back_button)
        #add arguments when connecting buttons to functions using lambda
        button_1.Bind(wx.EVT_BUTTON,lambda evt: self.option(evt,1))
        button_2.Bind(wx.EVT_BUTTON,lambda evt: self.option(evt,2))

    def on_paint(self,evt,dc):
        """set up the device for painting"""
        brush = wx.Brush(self.panel.BACKGROUND_COLOR)
        dc.SetBackground(brush)
        dc.SetFont(wx.Font(self.panel.TEXTBOX_FONTSIZE, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL))

        """Rectangle 1"""
        rectangle_y = self.panel.FIRST_RECTANGLE_Y
        dc.SetPen(wx.Pen(self.panel.RECTANGLE_COLOR))
        dc.SetBrush(wx.Brush(self.panel.RECTANGLE_COLOR))
        dc.DrawRectangle(0,rectangle_y, self.panel.WIDTH, self.panel.RECTANGLE_SIZE)
        textbox = wx.Rect(self.panel.TEXTBOX_X, rectangle_y+self.textbox_y)
        dc.DrawLabel("1)", textbox, alignment=1)

        """Rectangle 2"""
        rectangle_y = self.panel.FIRST_RECTANGLE_Y+(self.panel.RECTANGLE_SIZE+self.panel.RECTANGLE_SEPERATION)
        dc.DrawRectangle(0,rectangle_y, self.panel.WIDTH, self.panel.RECTANGLE_SIZE)
        textbox = wx.Rect(self.panel.TEXTBOX_X, rectangle_y+self.panel.TEXTBOX_Y)
        dc.DrawLabel("2)", textbox, alignment=1)

    def generate_ws(self):
        intensity = np.zeros([4,self.panel.HAPTIC_WIDTH])
        """Determine y workspace bounds"""
        y_ws = np.zeros([2,2]) 
        rectangle_y = self.panel.FIRST_RECTANGLE_Y
        y_ws[0] = [rectangle_y,rectangle_y+self.panel.RECTANGLE_SIZE]
        rectangle_y = rectangle_y + self.panel.RECTANGLE_SIZE + self.rectangle_seperation
        y_ws[1] = [rectangle_y, rectangle_y + self.panel.RECTANGLE_SIZE]

        haptic_width = float(self.panel.HAPTIC_WIDTH)
        horizontal_pixels = np.arange(self.panel.HAPTIC_WIDTH)

        # output has form of channel: actuation, amplitude, texture, frequency
        for i,value in enumerate(self.rand_output.values()):
            print(len(self.rand_output.values()))
            print(self.rand_output.values()[0])
            amp = int(value[1]*100)
            if value[2] == "Sinusoid":
                if value[0] == "Hybrid":
                    sinusoid = amp*np.sin(horiz_pixels/haptic_width*value[3]*2*np.pi)
                    ind = [np.where(sinusoid>0)[0], np.where(sinusoid<=0)[0]]
                    intensity[2*i][ind[0]] = sinusoid[ind[0]]
                    intensity[2*i+1][ind[1]] = -sinusoid[ind[1]]
                elif value[0] == "UFM":
                    intensity[2*i] = amp/2*np.sin(horiz_pixels/haptic_width*value[3]*2*np.pi) + amp/2
                elif value[0] == "EV":
                    intensity[2*i+1] = amp/2*np.sin(horiz_pixels/haptic_width*value[3]*2*np.pi) + amp/2

            elif value[2]  == "Square":
                sinusoid = np.sin(horiz_pixels/haptic_width*value[3]*2*np.pi)
                ind = [np.where(sinusoid>0)[0], np.where(sinusoid<=0)[0]]

                if value[0] == "Hybrid":
                    intensity[2*i][ind[0]] = amp
                    intensity[2*i+1][ind[1]] = amp
                elif value[0] == "UFM":
                    intensity[2*i][ind[0]] = amp
                elif value[0] == "EV":
                    intensity[2*i+1][ind[1]] = amp

        self.start_time = time.time()
        return intensity.astype(int).tolist(), y_ws.astype(int).tolist()

if __name__ == '__main__':
    app = wx.App(False)
    frame = BallFrame(None, -1, "Balls!")
    frame.Show(True)
    app.MainLoop()

    del app
