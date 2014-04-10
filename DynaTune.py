import wx

class DynaTune(wx.Frame):
  
    def __init__(self, parent, title):
        super(DynaTune, self).__init__(parent, title=title, 
            size=(300, 500))
               
        self.InitUI()
        self.Centre()
        self.Show()     

    def OnConnect(self, e):
        print 'Connect'

    def OnDownload(self, e):
        print 'Download'

    def OnUpload(self, e):
        print 'Upload'

    def OnSetContiousMode(self, e):
        print "Continous Mode"
        self.min_pos_control.SetValue(0)
        self.max_pos_control.SetValue(0)

    def SetupToolbar(self):
        toolbar = self.CreateToolBar()
        connect_tool = toolbar.AddLabelTool(wx.ID_ANY, 'Connect', wx.Bitmap('icons/laptop_connect.png'))
        download_tool = toolbar.AddLabelTool(wx.ID_ANY, 'Connect', wx.Bitmap('icons/load_download.png'))
        upload_tool = toolbar.AddLabelTool(wx.ID_ANY, 'Connect', wx.Bitmap('icons/load_upload.png'))
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnConnect, connect_tool)
        self.Bind(wx.EVT_TOOL, self.OnDownload, download_tool)
        self.Bind(wx.EVT_TOOL, self.OnUpload, upload_tool)

    def InitUI(self):
        self.SetupToolbar()

        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(3, 2, 9, 25)

        self.servo_id_control = self.AddSpinControl(panel, fgs, "Servo ID", 1, 255, 1)

        self.SetupEepromFields(panel, fgs)
        self.SetupRamFields(panel, fgs)

        self.goal_pos_control = self.AddSpinControl(panel, fgs, "Goal position", 0, 1024, 512)

        self.AddEditField(panel, fgs, "Author")
        self.AddEditField(panel, fgs, "Review")
        self.AddButton(panel, fgs, "Continous Rotation", "Enable", "Set AX motor to continous rotation", self.OnSetContiousMode)


        # fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)

    def AddEditField(self, panel, fgs, label):
        text = wx.StaticText(panel, label=label)
        text_control = wx.TextCtrl(panel)
        fgs.AddMany([(text), (text_control, 1, wx.EXPAND)])
        return text_control

    def AddButton(self, panel, fgs, label, buttonText, hint, handlerFunc):
        text = wx.StaticText(panel, label=label)
        button = wx.Button(panel, 20, buttonText, (20, 80)) ##, (120, 45))
        self.Bind(wx.EVT_BUTTON, handlerFunc, button)
        button.SetToolTipString(hint)
        fgs.AddMany([(text), (button)])
        return button

    def AddSpinControl(self, panel, fgs, label, minVal, maxVal, default):
        text = wx.StaticText(panel, label=label)
        spin_control = wx.SpinCtrl(panel, -1, "", (30, 50))
        spin_control.SetRange(minVal, maxVal)
        spin_control.SetValue(default)
        fgs.AddMany([(text), (spin_control)])
        return spin_control

    def SetupEepromFields(self, panel, fgs):
        #define AX_MODEL_NUMBER_L           0
        #define AX_MODEL_NUMBER_H           1
        self.model_control = self.AddEditField(panel, fgs, "Model Number")
        #define AX_VERSION                  2
        self.version_control = self.AddEditField(panel, fgs, "Version")
        #define AX_ID                       3
        #define AX_BAUD_RATE                4
        self.baud_control = self.AddEditField(panel, fgs, "Baud Rate")
        #define AX_RETURN_DELAY_TIME        5
        self.return_delay_control = self.AddEditField(panel, fgs, "Return Delay Time")
        #define AX_CW_ANGLE_LIMIT_L         6
        #define AX_CW_ANGLE_LIMIT_H         7
        self.min_pos_control = self.AddSpinControl(panel, fgs, "CW Angle Limit", 0, 1024, 0)
        #define AX_CCW_ANGLE_LIMIT_L        8
        #define AX_CCW_ANGLE_LIMIT_H        9
        self.max_pos_control = self.AddSpinControl(panel, fgs, "CCW Angle Limit", 0, 1024, 1024)
        #define AX_SYSTEM_DATA2             10
        self.system_data2_control = self.AddEditField(panel, fgs, "System Data2")
        #define AX_LIMIT_TEMPERATURE        11
        self.limit_temperature_control = self.AddSpinControl(panel, fgs, "Limit Temperature", 0, 1024, 512)
        #define AX_DOWN_LIMIT_VOLTAGE       12
        self.down_limit_voltage_control = self.AddSpinControl(panel, fgs, "Down Limit Voltage", 0, 1024, 512)
        #define AX_UP_LIMIT_VOLTAGE         13
        self.up_limit_voltage_control = self.AddSpinControl(panel, fgs, "Up Limit Volta", 0, 1024, 512)
        #define AX_MAX_TORQUE_L             14
        #define AX_MAX_TORQUE_H             15
        self.up_limit_voltage_control = self.AddSpinControl(panel, fgs, "Max Torque", 0, 1024, 512)
        #define AX_RETURN_LEVEL             16
        #define AX_ALARM_LED                17
        #define AX_ALARM_SHUTDOWN           18
        #define AX_OPERATING_MODE           19
        #define AX_DOWN_CALIBRATION_L       20
        #define AX_DOWN_CALIBRATION_H       21
        #define AX_UP_CALIBRATION_L         22
        #define AX_UP_CALIBRATION_H         23

    def SetupRamFields(self, panel, fgs):
        #define AX_TORQUE_ENABLE            24
        #define AX_LED                      25
        #define AX_CW_COMPLIANCE_MARGIN     26
        #define AX_CCW_COMPLIANCE_MARGIN    27
        #define AX_CW_COMPLIANCE_SLOPE      28
        #define AX_CCW_COMPLIANCE_SLOPE     29
        #define AX_GOAL_POSITION_L          30
        #define AX_GOAL_POSITION_H          31
        #define AX_GOAL_SPEED_L             32
        #define AX_GOAL_SPEED_H             33
        #define AX_TORQUE_LIMIT_L           34
        #define AX_TORQUE_LIMIT_H           35
        #define AX_PRESENT_POSITION_L       36
        #define AX_PRESENT_POSITION_H       37
        #define AX_PRESENT_SPEED_L          38
        #define AX_PRESENT_SPEED_H          39
        #define AX_PRESENT_LOAD_L           40
        #define AX_PRESENT_LOAD_H           41
        #define AX_PRESENT_VOLTAGE          42
        #define AX_PRESENT_TEMPERATURE      43
        #define AX_REGISTERED_INSTRUCTION   44
        #define AX_PAUSE_TIME               45
        #define AX_MOVING                   46
        #define AX_LOCK                     47
        #define AX_PUNCH_L                  48
        #define AX_PUNCH_H                  49
        print "RAM"

if __name__ == '__main__':
    try:
        app = wx.App()
        DynaTune(None, title='DynaTune')
        app.MainLoop()
    except Exception as e:
        print e
