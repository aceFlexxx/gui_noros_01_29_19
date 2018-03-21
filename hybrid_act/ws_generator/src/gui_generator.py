import wx
import rospy
from std_msgs.msg import String

##############################################################################80
class Texture:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, shape):
        """Constructor"""
        self.id = id
        self.shape = shape       


##############################################################################80
class Frame(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        #self.texture_pub = rospy.Publisher('/cursor_position/workspace_texture', String, queue_size = 0)
        #rospy.init_node('gui')
        
        wx.Frame.__init__(self, None, wx.ID_ANY, "Hybridization Comparison")
        self.Maximize(True)
        self.width, self.height = wx.GetDisplaySize()
        self.first_rectangle_y = 0.15*self.height
        self.rectangle_size = 0.2*self.height
        self.rectangle_seperation = (self.height-2*self.first_rectangle_y)/(3*self.rectangle_size)
        self.rectangle_color = "GREY"

        self.textbox_width = 0.25*self.width
        self.textbox_x = 0.15*self.width
        self.textbox_y = self.rectangle_size*0.35
        self.textbox_color = "WHITE"
        self.textbox_fontsize = 42 

        self.background_color = "BLACK"

        # Add a panel so it looks the correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)

        #self.panel.SetBackgroundColour('grey')
        #self.ufm_text = wx.StaticText(self, -1, label="UFM", pos=(0,self.first_rectangle_y))

        textures = [Texture(0, "Bump"),
                    Texture(1, "Sinusoidal"),
                    Texture(2, "Triangular")]

        sampleList = []

        self.cb = wx.ComboBox(self.panel,
                              size=wx.DefaultSize,
                              choices=sampleList,
                              pos=(.85*self.width,0.05*self.height))
        self.widgetMaker(self.cb, textures)

        self.Centre()
        self.Show()

        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self.cb, 0, wx.ALL, 5)
        #self.panel.SetSizer(sizer)

    #----------------------------------------------------------------------
    def widgetMaker(self, widget, objects):
        """"""
        for obj in objects:
            widget.Append(obj.shape, obj)
        widget.Bind(wx.EVT_COMBOBOX, self.onSelect)

    #----------------------------------------------------------------------
    def OnPaint(self, evt):
        """set up the device for painting"""
        dc = wx.PaintDC(self.panel)
        dc.BeginDrawing()
        brush = wx.Brush(self.background_color)
        dc.SetBackground(brush)
        dc.Clear()

        picture = wx.Bitmap("haptics_symp.png")
        width,height = picture.GetSize()

        dc.DrawBitmap(picture,(self.width-width)/2,(self.height-height)/2,True)
        font = wx.Font(self.textbox_fontsize, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL)
        dc.SetFont(font)

        """EV Rectangle"""
        dc.SetPen(wx.Pen(self.rectangle_color))
        dc.SetBrush(wx.Brush(self.rectangle_color))
        # set x, y, w, h for rectangle
        dc.DrawRectangle(0, self.first_rectangle_y, self.width, self.rectangle_size)
        dc.SetPen(wx.Pen(self.textbox_color))
        dc.SetBrush(wx.Brush(self.textbox_color))
        dc.DrawRectangle(0, self.first_rectangle_y, self.textbox_width, self.rectangle_size)
        dc.DrawText("EV", self.textbox_x, self.first_rectangle_y+self.textbox_y)
        #self.ufm_text.SetFont(self.font)

        dc.EndDrawing()
        del dc
        
    #----------------------------------------------------------------------
    def onSelect(self, event):
        """"""
        print "You selected: " + self.cb.GetStringSelection()
        obj = self.cb.GetClientData(self.cb.GetSelection())
        text = """
        The object's attributes are:
        %s  %s 

        """ % (obj.id, obj.shape)
        print text
        texture = self.cb.GetStringSelection()
        #self.texture_pub.publish(texture)

# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()
