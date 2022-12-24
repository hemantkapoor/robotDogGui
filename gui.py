# This is a sample Python script.
import time
import tkinter as tk
import customtkinter
import threading
from observerBase import *
from commandlist import *
from commandParser import *

GUI_SOURCE = 0x01



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Mygui(ObserverBase):
    def __init__(self,serverHandler = None):
        # tk.set_appearance_mode("System")
        # tk.set_default_color_theme('blue')
        self.root = tk.Tk()
        #self.root = tk.() # create  window like the Tk window

        self.root.geometry("500x500")
        self.root.title("RaspClaws Control")

        self.label1 = tk.Label(self.root, text="RaspClaws Control GUI", font=('Arial', 18), anchor=tk.NW)
        self.label1.pack```(anchor = 'n')

        self.ipFrame = tk.Frame(self.root, highlightbackground="blue", highlightthickness=2, width=500)
        self.ipFrame.columnconfigure(0, weight=1)
        self.ipFrame.columnconfigure(1, weight=1)
        self.ipLabel = tk.Label(self.ipFrame, text="Enter Ip Address", font=('Arial', 10))
        self.ipEntry = tk.Entry(self.ipFrame)
        self.ipLabel.grid(row=0, column=0, sticky=tk.W)
        self.ipEntry.grid(row=0, column=1, sticky=tk.W)
        self.ipFrame.pack(fill=tk.X, pady=20)
        self.ipFrame.pack(fill=tk.X, pady=20)

        self.ipSubmitBtn = tk.Button(text="Connect", width=20, command=self.connectToClient)
        self.ipSubmitBtn.pack()

        self.cpuTempLabel = tk.Label(self.root, text="CPU Temperature", font=('Arial', 10), anchor=tk.NW, width=50)
        self.cpuTempLabel.pack()
        self.m_serverHandler = serverHandler
        self.m_connection = False


    def getSource(self):
        return 0x01

    def getSource1(self):
        print('Requesting my id')
        return 'h'

    def handleFunction(self, data):
        preamble = CommandHeader.from_buffer(data)
        if preamble.function == 0x01:
           message = CpuInformation.from_buffer(data)
           self.cpuTempLabel.config(text=('CPU Temperature ' + str(message.cpuTemp) + ' degree'))

    def connectToClient(self):
        if self.m_serverHandler is None:
            print("No Action as no client present")
        else:
            if self.m_connection is False:
                self.m_serverHandler.socket_connect()
                self.m_connection = True
                self.ipSubmitBtn.config(text='Disconnect')
            else:
                self.m_serverHandler.socket_disconnect()
                self.m_connection = False
                self.ipSubmitBtn.config(text='Connect')

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
    guiObj = Mygui()
    guiObj.startthread()


