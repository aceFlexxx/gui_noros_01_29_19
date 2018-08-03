#!/usr/bin/python

###########################################################################
## Python code generated with wxFormBuilder (version Jul  2 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import startPage as start # page that accesses "games"
import test as guig #page made by kyle "gui_generator"
###########################################################################
## Class frameMain
###########################################################################

class frameMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Main", pos = wx.DefaultPosition, size = wx.Size( 1031,646 ), style = wx.SYSTEM_MENU|wx.MAXIMIZE|wx.TAB_TRAVERSAL )


		bSizerFrameMain = wx.BoxSizer( wx.VERTICAL )

		bSizerMainFrame = wx.BoxSizer( wx.VERTICAL )

		#goes to start page where the game button is accessed
		self.startButton = wx.Button( self, wx.ID_ANY, label="Start", pos=(600,150), size = wx.DefaultSize)
		bSizerMainFrame.Add( self.startButton, 0, 0, 0 )
		#goes to test page made by kyle
		self.testButton = wx.Button( self, wx.ID_ANY, label="Test", pos=(600,240), size = wx.DefaultSize)
		bSizerMainFrame.Add( self.testButton, 0, wx.ALL, 5 )


		bSizerFrameMain.Add( bSizerMainFrame, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizerFrameMain )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.startButton.Bind( wx.EVT_BUTTON, self.onStart )
		self.testButton.Bind( wx.EVT_BUTTON, self.onTest )

	def __del__( self ):
		pass


	def onTest( self, event ):
		f = guig.Frame() #test page opens
		self.Close()
		f.Show()

	def onStart( self, event ):
		f = start.Frame(None) #start page opens
		self.Close()
		f.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = frameMain(None) 
    frame.Show()
    app.MainLoop()
