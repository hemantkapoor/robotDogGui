import zmq
from socket import *
import base64
import cv2
import numpy as np
import threading
import time
import commandlist
import commandParser

host = "192.168.0.229"
# port = "4223"

class ZmqClient:
    def __init__(self):
        self.context = zmq.Context()
        self.frameSocket = self.context.socket(zmq.SUB)
        self.startReceiving = False
        self.stopReceiving = False

    def startSubscriptionThread(self):
        print("Waiting for connection")
        self.frameSocket.connect('tcp://%s:4233' % host)
        self.frameSocket.setsockopt_string(zmq.SUBSCRIBE, "")
        print("Connected")
        self.startReceiving = True

    def stopSubscribe(self):
        self.stopReceiving = True

    def renderVideoThread(self):
        print('Render Video thread')
        statusSent = False
        stat = commandlist.CameraStatus()
        stat.preamble.target = 0x01
        stat.status = 1
        commandParser.CommandParser.handleCommand(stat)

        # We listen from the published
        while True:
            if self.stopReceiving is True:
                print("Render Video thread stopped")
                break
            if self.startReceiving is False:
                print('Waiting for connection')
                time.sleep(1)
                continue
            if self.frameSocket is None:
                print('No data')
                time.sleep(1)
            else:
                # Lets just print what we get
                try:
                    print("Waiting for frame")
                    frame = self.frameSocket.recv_string()
                    print("Got frame")
                    if statusSent is False:
                        statusSent = True
                        stat.status = 2
                        commandParser.CommandParser.handleCommand(stat)
                    img = base64.b64decode(frame)
                    npimg = np.frombuffer(img, dtype=np.uint8)
                    source = cv2.imdecode(npimg, 1)
                    cv2.imshow("Stream", source)
                    if cv2.getWindowProperty('Stream', cv2.WND_PROP_VISIBLE) >= 0:
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            print('Closing window')
                            break;
                    else:
                        print('Close window now')
                        break
                except Exception as e:
                    print(e)
                    time.sleep(1)
        cv2.destroyAllWindows()
        stat.status = 0
        commandParser.CommandParser.handleCommand(stat)



    def Startsubscribe(self):
        start_subscriptionThread = threading.Thread(target=self.startSubscriptionThread)
        start_subscriptionThread.daemon = True
        start_subscriptionThread.start()

        start_renderThread = threading.Thread(target=self.renderVideoThread)
        start_renderThread.daemon = True
        start_renderThread.start()

if __name__ == '__main__':
    zmqClientObj = ZmqClient()
    zmqClientObj.Startsubscribe()
    while True:
        time.sleep(0.1)
    # while True:
    #     choice = input('Press Q to Quit')
    #     if choice == 'q':
    #         import sys
    #         exit(0)
