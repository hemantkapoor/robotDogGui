# This is a sample Python script.
import tkinter as tk
import threading


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Mygui:
    def __init__(self,webSock = None):
        self.root = tk.Tk()

        self.root.geometry("500x500")
        self.root.title("RaspClaws Control")

        self.label1 = tk.Label(self.root, text="RaspClaws Control GUI", font=('Arial', 18), anchor=tk.NW, width=50)
        self.label1.pack()

        self.ipFrame = tk.Frame(self.root)
        self.ipFrame.columnconfigure(0, weight=1)
        self.ipLabel = tk.Label(self.ipFrame, text="Enter Ip Address", font=('Arial', 10))
        self.ipEntry = tk.Entry(self.ipFrame)
        self.ipLabel.grid(row=0, column=0, columnspan=1)
        self.ipEntry.grid(row=0, column=1, sticky=tk.W)
        self.ipFrame.pack()

        self.ipSubmitBtn = tk.Button(text="Enter", width=20)
        self.ipSubmitBtn.pack()

    def updateIpSubmitBtn(self,value):
        self.ipSubmitBtn["Text"] = value



    def startthread(self):
        self.root.mainloop()
        # fps_threading = threading.Thread(target=self.thread)         #Define a thread for FPV and OpenCV
        # #fps_threading.setDaemon(False)  #'True' means it is a front thread,it would close when the mainloop() closes
        # fps_threading.daemon = False
        # fps_threading.start()                                     #Thread starts

if __name__ == '__main__':
    guiObj = Mygui()
    guiObj.startthread()


