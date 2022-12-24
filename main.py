import client
import gui
from commandParser import  *

if __name__ == '__main__':
    clientObj = client.CleintClass()
    guiObj = gui.Mygui(clientObj)
    clientObj.addGui(guiObj)

    #Register all the commands here
    CommandParser.register(guiObj)

    #Lets start the gui it will be there for ever
    guiObj.startthread()