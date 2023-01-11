from socket import *
import threading as thread
import time
from commandParser import  *

SERVER_IP = '192.168.0.229'
SERVER_PORT = 10223  # Define port serial


class CleintClass:
    def __init__(self, ipAddress = None, serverPort = None, gui = None):
        self.m_guiHandler = gui
        self.m_tcpClicSock = None
        self.m_ipAddress = ipAddress
        self.m_serverPort = serverPort
        self.runThread = False

    def connection_thread(self):
        while 1:
            if self.runThread is True:
                try:
                    data = self.m_tcpClicSock.recv(1024)
                    if not data:
                        print("Nothing received")
                        continue
                    else:
                        print('Received from server')
                        print(data)
                        if self.m_guiHandler is not None:
                            print('Sending data to gui')
                            CommandParser.handleCommand(data)

                except:
                    pass
            else:
                break

    def sendPeriodicMessage(self):
        while 1:
            try:
                time.sleep(1)
                self.m_tcpClicSock.send(('Hello from client').encode())
            except:
                print('Cannot Send')
                pass

    def sendCommand(self, data):
        self.m_tcpClicSock.send(data)

    def addGui(self, gui):
        self.m_guiHandler = gui


    def socket_disconnect(self):
        self.runThread = False
        self.m_tcpClicSock.close()
        return True


    def socket_connect(self, servIp = None):  # Call this function to connect with the server


        serverIp = SERVER_IP
        serverPort = SERVER_PORT

        if servIp is not None:
            self.m_ipAddress = servIp

        if self.m_ipAddress is not None:
            serverIp = self.m_ipAddress

        if self.m_serverPort is not None:
            serverPort = self.m_serverPort

        ADDR = (serverIp, serverPort)

        try:
            self.m_tcpClicSock = socket(AF_INET, SOCK_STREAM)  # Set connection value for socket

            print("Connecting to server @ %s:%d..." % (SERVER_IP, SERVER_PORT))
            print("Connecting")
            self.m_tcpClicSock.connect(ADDR)  # Connection with the server
            print("Connected")

            self.runThread = True
            connection_threading = thread.Thread(target=self.connection_thread)
            connection_threading.daemon = True
            connection_threading.start()  # Thread starts

            return True

            # sending_threading = thread.Thread(target=self.sendPeriodicMessage)
            # sending_threading.daemon = True
            # sending_threading.start()  # Thread starts
        except:
            return False

if __name__ == '__main__':
    clentS = CleintClass()
    clentS.socket_connect()
    while 1:
        pass