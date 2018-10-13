#!/usr/bin/python

###########################################################################
## Python code generated with wxFormBuilder (version Jul  2 2018)
## http://www.wxformbuilder.org/
## WX VERSION 3.0.2
## PYTHON VERSION 2.7
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import csv
import start # page that accesses "games"
import test  #page made by kyle "gui_generator"
###########################################################################
## Class frameMain  
###########################################################################

class frameMain ( wx.Frame ):

	def __init__ ( self, parent ):
	    wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Main", size = wx.GetDisplaySize(), style = wx.SYSTEM_MENU|wx.MAXIMIZE|wx.TAB_TRAVERSAL )

            #setting up buttons:
            self.submitBtn = wx.Button( self, wx.ID_ANY, label="Submit") 
            self.startBtn = wx.Button( self, wx.ID_ANY, label="Start") 
            self.testBtn = wx.Button( self, wx.ID_ANY, label="Test")
            self.closeBtn = wx.Button(self, wx.ID_ANY, label="X")
            self.minimizeBtn=wx.Button(self, wx.ID_ANY,label="_") 
            self.label = wx.StaticText(self, wx.ID_ANY, 'Name: ') 
            self.name = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString)

	    # Connect buttons to Events
            self.minimizeBtn.Bind( wx.EVT_BUTTON, self.onMinimize)
	    self.submitBtn.Bind( wx.EVT_BUTTON, self.onName )
	    self.startBtn.Bind( wx.EVT_BUTTON, self.onStart )
            self.testBtn.Bind( wx.EVT_BUTTON, self.onTest )
            self.closeBtn.Bind(wx.EVT_BUTTON, self.onClose)
            #set up screen	
            self.layout()

        def layout(self):
	    topBox = wx.BoxSizer( wx.HORIZONTAL )#box for buttons close and minimize 
	    nameBox = wx.BoxSizer( wx.HORIZONTAL ) #box for name and the text control
            mainBox = wx.BoxSizer( wx.VERTICAL )
            startBox = wx.BoxSizer( wx.HORIZONTAL )#box for buttons start and test
            
            #setting up boxes of buttons
            topBox.Add( self.minimizeBtn, 0, 0, 0)
            topBox.Add( self.closeBtn, 0, 0 , 0 )

            nameBox.Add( self.label, 2, 0, 0 )
            nameBox.Add( self.name,4,wx.CENTER|wx.EXPAND,0)
            nameBox.Add( self.submitBtn,2, 0, 0)
            
            startBox.Add( self.startBtn, 4, 0, 0 )
            startBox.Add( self.testBtn, 4, 0, 0 )

            mainBox.Add( topBox, 4, wx.ALIGN_RIGHT, 0 )
            mainBox.Add( nameBox, 0, wx.ALIGN_CENTER, 0 )
            mainBox.Add( startBox, 4, wx.ALIGN_CENTER, 0 )
	    
            self.SetSizer( mainBox )
	    self.Layout()
	    self.Centre( wx.BOTH )

        def __del__( self ):
	    pass
        
        def onName( self,event):
            #save on the csv file the name of the user
            Name=self.name.GetValue()
            with open('output.csv','w') as f:
                write=csv.writer(f, quoting=csv.QUOTE_ALL)
                write.writerow([Name,'correct answer'])
            self.name.SetValue("")
            f.close()

        def onMinimize( self, event ):
            self.Hide()

	def onTest( self, event ):
            f = test.Frame() #test page opens
	    self.Close()
            f.Show()

	def onStart( self, event ):
            f = start.Frame() #start page opens
            self.Close()
            f.Show()

        def onClose( self, event ):
            self.Close()         

if __name__ == '__main__':
    app = wx.App()# NECESSARY TO START UYSING WX LIBRARY 
    frame = frameMain(None) 
    frame.Show()
    app.MainLoop()
