import  wx

class Frame(wx.Frame):
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, title=title,
                style=(wx.DEFAULT_FRAME_STYLE | wx.WS_EX_CONTEXTHELP) ,
                pos=(20, 20))
    self.SetExtraStyle(wx.FRAME_EX_CONTEXTHELP)
    self.CreateStatusBar()
    self.createOtherStuffHere()
    self.Show()

  def createOtherStuffHere(self):
    panel = wx.Panel(self)
    panel.SetHelpText("This is a wx.Panel.")

    self.label = wx.StaticText(panel, style=wx.WS_EX_CONTEXTHELP, label="Click me I may provide some help?", size=(200,30))
    self.label.SetHelpText("This is the help though not so helpful!")

    self.edit = wx.TextCtrl(panel, pos=(20,50))
    self.edit.SetHelpText("i am a edit box")

    self.helpButton = wx.ContextHelpButton(panel, pos=(20,100))

provider = wx.SimpleHelpProvider()
wx.HelpProvider_Set(provider)

app = wx.PySimpleApp()
frame = Frame(None, "Test")
app.SetTopWindow(frame)
app.MainLoop()
