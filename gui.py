# This is a sample Python script.
import time
import tkinter
import customtkinter as tk
import threading
from observerBase import *
from commandlist import *
import zmqClient
from commandParser import *

GUI_ADDRESS = 0x01

WINDOW_SIZE = "1200x1000"
GUI_FONT = ('Arial', 18)
ROW_PADDDING = (20, 20)
COLUMN_PADDDING = (20, 20)
STATUS_PADDDING = (20, 20)

BUTTON_SIZE = 150

class NewGui(ObserverBase):

    def __init__(self,serverHandler = None):

        self._serverHandler = serverHandler
        self._connection = False
        self.LiveView = False
        self.zmqClientObj = None

        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme('blue')
        self.root = tk.CTk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title("RaspClaws Control")
        self.label1 = tk.CTkLabel(self.root, text="RaspClaws Control GUI", font=('Arial', 18), anchor=tk.NW)
        self.label1.grid(row=0, column=0, sticky=tk.N, columnspan=3)

        #Frame for rest of the window
        self.topFrame = tk.CTkFrame(self.root, border_width=10)

        # Add Ip Entry
        self._addIp(self.topFrame, 0, 0)

        # Add control
        self._addMovementControl(self.topFrame, 1, 0)

        # Add Carera Control
        self._addCameraControl(self.topFrame, 6, 0)

        #Control mode
        self._addControlMode(self.topFrame, 11, 0)

        #Live View
        self._liveView(self.topFrame, 12, 0)


        #Add status
        self._addStatus(self.topFrame, 0, 7)

        #Add top frame
        self.topFrame.grid(row=1, column=0, sticky=tk.EW, pady=40, padx=20)



        # Control members
        self.m_serverHandler = None




    # ***************** Method to add IP Address ***************************
    def _addIp(self, frame, mainRow, mainColumn):
        localFrame = tk.CTkFrame(frame)
        label1 = tk.CTkLabel(localFrame, text="Enter IP Address", font=GUI_FONT, anchor=tk.NW)
        label1.grid(row=0, column=0, sticky=tk.W, padx=ROW_PADDDING)

        ent = tk.CTkEntry(localFrame)
        ent.insert(tk.END, "192.168.0.229")
        ent.grid(row=0, column=1, sticky=tk.W, padx=ROW_PADDDING)

        self._ipSubmitBtn = tk.CTkButton(master=localFrame, text="Connect", width=BUTTON_SIZE, command=self.connect_callback)
        self._ipSubmitBtn.grid(row=0, column=2, sticky=tk.W, padx=ROW_PADDDING)
        localFrame.grid(row=mainRow, column=mainColumn, sticky=tk.EW, columnspan=5, pady=20, padx=20)

    # ***************** Method to add Movement Control ***************************
    def _addMovementControl(self, frame, mainRow, mainColumn):
        localFrame = tk.CTkFrame(frame)
        label1 = tk.CTkLabel(localFrame, text="MOVEMENT CONTROL", font=GUI_FONT, anchor=tk.NW)
        label1.grid(row=0, column=0, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)


        ipSubmitBtn = tk.CTkButton(master=localFrame, text="FORWARD", width=BUTTON_SIZE, command=self.forward_callback)
        ipSubmitBtn.grid(row=1, column=2, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        ipSubmitBtn = tk.CTkButton(master=localFrame, text="LEFT", width=BUTTON_SIZE, command=self.left_callback)
        ipSubmitBtn.grid(row=2, column=1, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        ipSubmitBtn = tk.CTkButton(master=localFrame, text="STOP", width=BUTTON_SIZE, command=self.stop_callback)
        ipSubmitBtn.grid(row=2, column=2, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        ipSubmitBtn = tk.CTkButton(master=localFrame, text="RIGHT", width=BUTTON_SIZE, command=self.right_callback)
        ipSubmitBtn.grid(row=2, column=3, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        ipSubmitBtn = tk.CTkButton(master=localFrame, text="REVERSE", width=BUTTON_SIZE, command=self.reverse_callback)
        ipSubmitBtn.grid(row=3, column=2, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        localFrame.grid(row=mainRow, column=mainColumn, sticky=tk.EW, rowspan=4, columnspan=5, pady=COLUMN_PADDDING, padx=ROW_PADDDING)

    # ***************** Method to add Camera Control ***************************
    def _addCameraControl(self, frame, mainRow, mainColumn):
        localFrame = tk.CTkFrame(frame)
        label1 = tk.CTkLabel(localFrame, text="Camera CONTROL", font=GUI_FONT, anchor=tk.NW)
        label1.grid(row=0, column=0, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)


        ipSubmitBtn = tk.CTkButton(master=localFrame, text="UP", width=BUTTON_SIZE, command=self.cam_up_callback)
        ipSubmitBtn.grid(row=1, column=2, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        ipSubmitBtn = tk.CTkButton(master=localFrame, text="LEFT", width=BUTTON_SIZE, command=self.cam_left_callback)
        ipSubmitBtn.grid(row=2, column=1, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        # ipSubmitBtn = tk.CTkButton(master=localFrame, text="STOP", width=BUTTON_SIZE, command=self.cam_stop_callback)
        # ipSubmitBtn.grid(row=2, column=2, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        ipSubmitBtn = tk.CTkButton(master=localFrame, text="RIGHT", width=BUTTON_SIZE, command=self.cam_right_callback)
        ipSubmitBtn.grid(row=2, column=3, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        ipSubmitBtn = tk.CTkButton(master=localFrame, text="DOWN", width=BUTTON_SIZE, command=self.cam_down_callback)
        ipSubmitBtn.grid(row=3, column=2, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)

        localFrame.grid(row=mainRow, column=mainColumn, sticky=tk.EW, rowspan=4, columnspan=5, pady=COLUMN_PADDDING, padx=ROW_PADDDING)


    # ***************** Method to add Control MODE  ***************************
    def _addControlMode(self, frame, mainRow, mainColumn):
        localFrame = tk.CTkFrame(frame)
        label1 = tk.CTkLabel(localFrame, text="Select Mode", font=GUI_FONT, anchor=tk.W)
        label1.grid(row=0, column=0, sticky=tk.EW, padx=STATUS_PADDDING)

        # Leave one column blank
        localFrame.columnconfigure(0, weight=1)
        localFrame.columnconfigure(1, weight=1)
        localFrame.columnconfigure(2, weight=1)
        label1 = tk.CTkLabel(localFrame, text="", font=GUI_FONT, anchor=tk.W)
        label1.grid(row=0, column=1, sticky=tk.EW, padx=STATUS_PADDDING)

        combobox = tk.CTkComboBox(master=localFrame,
                                             values=["Manual", "Follow Object", "Line Follow", "Detect Object"],
                                             command=self.modeSelector_callback)
        combobox.set("Manual")  # set initial value

        combobox.grid(row=0, column=2, sticky=tk.EW, padx=STATUS_PADDDING)

        localFrame.grid(row=mainRow, column=mainColumn, sticky=tk.EW, columnspan=5, pady=COLUMN_PADDDING, padx=ROW_PADDDING)

    # ***************** Method to VIEW LIVE CAMERA MODE  ***************************
    def _liveView(self, frame, mainRow, mainColumn):
        localFrame = tk.CTkFrame(frame)
        self.liveViewBtn = tk.CTkButton(master=localFrame, text="LIVE VIEW", width=BUTTON_SIZE, command=self.liveView_callback)
        self.liveViewBtn.grid(row=0, column=0, sticky=tk.W, padx=ROW_PADDDING, pady=COLUMN_PADDDING)
        localFrame.grid(row=mainRow, column=mainColumn, sticky=tk.EW, columnspan=5, pady=COLUMN_PADDDING, padx=ROW_PADDDING)



    # ***************** Method to add Status ***************************
    def _addStatus(self, frame, mainRow, mainColumn):
        localFrame = tk.CTkFrame(frame)
        label1 = tk.CTkLabel(localFrame, text="STATUS", font=GUI_FONT, anchor=tk.N)
        label1.grid(row=0, column=0, sticky=tk.N, padx=STATUS_PADDDING, columnspan=2)

        currentRow = 1
        #CPU STATUS
        label1 = tk.CTkLabel(localFrame, text="CPU STATUS", font=GUI_FONT, anchor=tk.NW)
        label1.grid(row=currentRow, column=0, sticky=tk.W, padx=STATUS_PADDDING)
        self._onlineStatus = tk.CTkLabel(localFrame, text="Offline", font=GUI_FONT, anchor=tk.NW)
        self._onlineStatus.grid(row=currentRow, column=1, sticky=tk.W, padx=STATUS_PADDDING)

        #CPU TEMPERATURE
        currentRow = currentRow + 1
        label1 = tk.CTkLabel(localFrame, text="CPU Temperature", font=GUI_FONT, anchor=tk.NW)
        label1.grid(row=currentRow, column=0, sticky=tk.W, padx=STATUS_PADDDING)
        self._cpuTempLabel = tk.CTkLabel(localFrame, text="None", font=GUI_FONT, anchor=tk.NW)
        self._cpuTempLabel.grid(row=currentRow, column=1, sticky=tk.W, padx=STATUS_PADDDING)

        #CPU RAM
        currentRow = currentRow + 1
        label1 = tk.CTkLabel(localFrame, text="CPU RAM", font=GUI_FONT, anchor=tk.NW)
        label1.grid(row=currentRow, column=0, sticky=tk.W, padx=STATUS_PADDDING)
        self._cpuRamLabel = tk.CTkLabel(localFrame, text="None", font=GUI_FONT, anchor=tk.NW)
        self._cpuRamLabel.grid(row=currentRow, column=1, sticky=tk.W, padx=STATUS_PADDDING)

        #Movement
        currentRow = currentRow + 1
        label1 = tk.CTkLabel(localFrame, text="Movement", font=GUI_FONT, anchor=tk.NW)
        label1.grid(row=currentRow, column=0, sticky=tk.W, padx=STATUS_PADDDING)
        self._moveStatusLabel = tk.CTkLabel(localFrame, text="Stopped", font=GUI_FONT, anchor=tk.NW)
        self._moveStatusLabel.grid(row=currentRow, column=1, sticky=tk.W, padx=STATUS_PADDDING)

        localFrame.grid(row=mainRow, column=mainColumn, sticky=tk.N, rowspan=5, columnspan=2, pady=20, padx=20)




    #**************** CONTROL FUNCTIONS FOR BUTTONS AND DROPDOWN HERE  ***********************
    def connect_callback(self):
        if self._serverHandler is None:
            print('No server present bailing')
            return

        if self._connection is False:
            if self._serverHandler.socket_connect() is False:
                print('No server present')
                return
            self._helper_changeStatus(True)
        else:
            if self._serverHandler.socket_disconnect() is False:
                print('Error disconnecting')
                return
            self._helper_changeStatus(False)



        print("connect_callback")

    def forward_callback(self):
        cmd = ControlMovementCMD()
        cmd.movement = FORWARD
        dataToSend = bytearray(cmd)
        self._serverHandler.sendCommand(dataToSend)
        print("forward_callback")

    def left_callback(self):
        print("left_callback")

    def stop_callback(self):
        print("stop_callback")

    def right_callback(self):
        print("right_callback")

    def reverse_callback(self):
        print("reverse_callback")

    def cam_up_callback(self):
        print("forward_callback")

    def cam_left_callback(self):
        print("left_callback")

    def cam_stop_callback(self):
        print("stop_callback")

    def cam_right_callback(self):
        print("right_callback")

    def cam_down_callback(self):
        print("reverse_callback")


    def liveView_callback(self):
        if self.LiveView is False:
            self.zmqClientObj = zmqClient.ZmqClient()
            self.zmqClientObj.Startsubscribe()
            self.LiveView = True
        else:
            self.LiveView = False
            self.zmqClientObj.stopSubscribe()
            self.zmqClientObj = None



    def modeSelector_callback(self, choice):
        print("combobox dropdown clicked:", choice)


    def getSource(self):
        return GUI_ADDRESS


    # ************** COMMAND HANDLERS IMPLEMENTED HERE
    def handleFunction(self, data):
        print('Got data from server')
        preamble = CommandHeader.from_buffer(data)
        #cHECK IF cpu INFORMATION RECEIVED
        if preamble.function == RESP_CPU_STATUS_FUNC:
            message = CpuInformation.from_buffer(data)
            print('Gui Temp received ' + str(message.cpuTemp))
            try:
                self._cpuTempLabel.configure(text=('{:.2f}'.format(message.cpuTemp) + u'8\N{DEGREE SIGN}'))
                self._cpuRamLabel.configure(text=(str(message.cpuRAM)))
            except Exception as e:
                print(e)
        elif preamble.function == RESP_MOVEMENT:
            message = CameraStatus.from_buffer(data)
            print('Movement Status Received' + str(message.status))
            try:
                self._moveStatusLabel.configure(text=(str(message.status)))
            except Exception as e:
                print(e)
        elif preamble.function == RESP_CAMERA_STATUS_FUNC:
            message = CameraStatus.from_buffer(data)
            if message.status == 0:
                self.liveViewBtn.configure(text='Live View')
            if message.status == 1:
                self.liveViewBtn.configure(text='Please Wait... Receiving data ')
            if message.status == 2:
                self.liveViewBtn.configure(text='Disconnect')

    #******************** HELPER FUNCTIONS **************************
    def _helper_changeStatus(self,online):
        if online is True:
            self._connection = True
            self._ipSubmitBtn.configure(text='Disconnect')
            self._onlineStatus.configure(text='Online')
        else:
            self._connection = False
            self._ipSubmitBtn.configure(text='Connect')
            self._onlineStatus.configure(text='Offline')
            self._cpuTempLabel.configure(text='None')
            self._cpuRamLabel.configure(text='None')
            self._moveStatusLabel.configure(text='Stopped')


    def backgroundThread(self):
        while True:
            time.sleep(1)
            if self._serverHandler is not None:
                if self._connection is True:
                    preamble = CommandHeader()
                    preamble.source = 0x01
                    preamble.function = REQ_CPU_STATUS_FUNC
                    dataToSend = bytearray(preamble)
                    self._serverHandler.sendCommand(dataToSend)
                    print(dataToSend)

    def startthread(self):
        bk_threading = threading.Thread(target=self.backgroundThread)
        bk_threading.daemon = True
        bk_threading.start()
        self.root.mainloop()


if __name__ == '__main__':
    # guiObj = Mygui()
    # guiObj.startthread()
    guiObj = NewGui()
    guiObj.startthread()


