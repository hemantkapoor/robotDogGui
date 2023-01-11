# This is a sample Python script.
import time
import tkinter
import customtkinter as tk
import threading
from observerBase import *
from commandlist import *
import zmqClient
from commandParser import *

GUI_SOURCE = 0x01

GUI_FONT = ('Arial', 14)

class NewGui(ObserverBase):

    def __init__(self,serverHandler = None):
        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme('blue')
        self.root = tk.CTk()
        self.root.geometry("500x500")
        self.root.title("RaspClaws Control")
        self.label1 = tk.CTkLabel(self.root, text="RaspClaws Control GUI", font=('Arial', 18), anchor=tk.NW)
        self.label1.pack(anchor='n')

        #Frame for rest of the window
        self.topFrame = tk.CTkFrame(self.root)
        self._addIp(self.topFrame)


        #Add top frame
        self.topFrame.pack(fill=tk.X, pady=20)


    # ***************** Method to add IP Address ***************************
    def _addIp(self,frame):
        frame = tk.CTkFrame(frame)
        label1 = tk.CTkLabel(frame, text="Enter IP Address", font=('Arial', 18), anchor=tk.NW)


    def backgroundThread(self):
        while True:
            time.sleep(1)
            if self.m_serverHandler is not None:
                if self.m_connection is True:
                    #self.m_serverHandler.sendCommand('Test')
                    preamble = CommandHeader()
                    preamble.source = 0x01
                    preamble.function = 0x01
                    dataToSend = bytearray(preamble)
                    self.m_serverHandler.sendCommand(dataToSend)
                    print(dataToSend)

    def startthread(self):
        bk_threading = threading.Thread(target=self.backgroundThread)
        bk_threading.daemon = True
        bk_threading.start()
        self.root.mainloop()



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Mygui(ObserverBase):
    def __init__(self,serverHandler = None):
        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme('blue')
        self.root = tk.CTk()
        #self.root = tk.() # create  window like the Tk window

        self.root.geometry("500x500")
        self.root.title("RaspClaws Control")

        self.label1 = tk.CTkLabel(self.root, text="RaspClaws Control GUI", font=('Arial', 18), anchor=tk.NW)
        self.label1.pack(anchor = 'n')

        self.ipFrame = tk.CTkFrame(self.root, )
        self.ipFrame.columnconfigure(0, weight=1)
        self.ipFrame.columnconfigure(1, weight=1)
        self.ipLabel = tk.CTkLabel(self.ipFrame, text="Enter Ip Address", font=('Arial', 10))
        self.ipEntry = tk.CTkEntry(self.ipFrame)
        self.ipLabel.grid(row=0, column=0, sticky=tk.W)
        self.ipEntry.grid(row=0, column=1, sticky=tk.W)

        self.ipSubmitBtn = tk.CTkButton(master=self.ipFrame, text="Connect", width=20, command=self.connectToClient)
        self.ipSubmitBtn.grid(row=1, column=0, sticky=tk.W)
        self.ipFrame.pack(fill=tk.X, pady=20)

        self.camFrame = tk.CTkFrame(self.root)
        self.camSubmitBtn = tk.CTkButton(master=self.camFrame, text="Go Live", width=20, command=self.goLive)
        self.camSubmitBtn.grid(row=0, column=0, sticky=tk.W)
        self.camFrame.pack(fill=tk.X, pady=20)


        #self.ipSubmitBtn.pack()

        self.cpuTempLabel = tk.CTkLabel(self.root, text="CPU Temperature", font=GUI_FONT, anchor=tk.NW, width=50)
        self.cpuTempLabel.pack()
        self.m_serverHandler = serverHandler
        self.m_connection = False



    def goLive(self):
        zmqClientObj = zmqClient.ZmqClient()
        zmqClientObj.Startsubscribe()
        pass

    def getSource(self):
        return 0x01

    def getSource1(self):
        print('Requesting my id')
        return 'h'

    def handleFunction(self, data):
        preamble = CommandHeader.from_buffer(data)
        if preamble.function == 0x01:
            message = CpuInformation.from_buffer(data)
            print('Gui Temp received ' + str(message.cpuTemp))
            try:
                self.cpuTempLabel.configure(text=('CPU Temperature  {:.2f}'.format(message.cpuTemp) + ' degree'))
            except Exception as e:
                print(e)

    def connectToClient(self):
        if self.m_serverHandler is None:
            print("No Action as no client present")
        else:
            if self.m_connection is False:
                self.m_serverHandler.socket_connect()
                self.m_connection = True
                # self.ipSubmitBtn.config(text='Disconnect')
            else:
                self.m_serverHandler.socket_disconnect()
                self.m_connection = False
                # self.ipSubmitBtn.config(text='Connect')

    def updateIpSubmitBtn(self, value):
        self.ipSubmitBtn["Text"] = value

    def backgroundThread(self):
        while True:
            time.sleep(1)
            if self.m_serverHandler is not None:
                if self.m_connection is True:
                    #self.m_serverHandler.sendCommand('Test')
                    preamble = CommandHeader()
                    preamble.source = 0x01
                    preamble.function = 0x01
                    dataToSend = bytearray(preamble)
                    self.m_serverHandler.sendCommand(dataToSend)
                    print(dataToSend)




    def startthread(self):
        bk_threading = threading.Thread(target=self.backgroundThread)
        bk_threading.daemon = True
        bk_threading.start()
        self.root.mainloop()


        # fps_threading = threading.Thread(target=self.thread)         #Define a thread for FPV and OpenCV
        # #fps_threading.setDaemon(False)  #'True' means it is a front thread,it would close when the mainloop() closes
        # fps_threading.daemon = False
        # fps_threading.start()                                     #Thread starts

if __name__ == '__main__':
    # guiObj = Mygui()
    # guiObj.startthread()
    guiObj = NewGui()
    guiObj.startthread()


