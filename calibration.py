import time

import cv2
import numpy as np
import threading

WIDTH = 600
HEIGHT = 600

RECT_X = 200
RECT_Y = 50
RECT_WIDTH = 200
RECT_HEIGHT = 50
TEXT_X_ADJ = 60
TEXT_Y_ADJ = 30

CIRCLE_X = 200
CIRCLE_Y = 320
CIRCLE_RADIUS = 30

CIRCLE_X_ADJ = 210
CIRCLE_Y_ADJ = 100

CIRCLE_X_TEXT_ADJ = 10
CIRCLE_Y_TEXT_ADJ = 10


class Calibration:
    def __init__(self):
        self._xClicked = 0
        self._yClicked = 0
        self._xReleased = 0
        self._yReleased = 0

        self._frontFace = True

        self._img = cv2.imread("./img/frontDog.jpg")
        self._btnText = "BACK"
        self.drawImg()
        bk_threading = threading.Thread(target=self.calibThread)
        bk_threading.daemon = True
        bk_threading.start()

    def drawImg(self):

        self._img = cv2.resize(self._img, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
        self._img = cv2.rectangle(self._img, (RECT_X, RECT_Y), (RECT_X + RECT_WIDTH, RECT_Y + RECT_HEIGHT), (0, 0, 0), 7)
        cv2.putText(self._img, self._btnText, (RECT_X + TEXT_X_ADJ, RECT_Y + TEXT_Y_ADJ), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 0, 0), 2)

        circleCentre = (CIRCLE_X, CIRCLE_Y)
        self._img = cv2.circle(self._img, circleCentre, CIRCLE_RADIUS, (0, 0, 255), 3)
        cv2.putText(self._img, 'A', circleCentre, cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 0, 255), 2)

        circleCentre = (CIRCLE_X + CIRCLE_X_ADJ, CIRCLE_Y)
        self._img = cv2.circle(self._img, circleCentre, CIRCLE_RADIUS, (0, 0, 255), 3)
        cv2.putText(self._img, 'B', circleCentre, cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 0, 255), 2)

        circleCentre = (CIRCLE_X, CIRCLE_Y + CIRCLE_Y_ADJ)
        self._img = cv2.circle(self._img, circleCentre, CIRCLE_RADIUS, (0, 0, 255), 3)
        cv2.putText(self._img, 'C', circleCentre, cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 0, 255), 2)

        circleCentre = (CIRCLE_X + CIRCLE_X_ADJ, CIRCLE_Y + CIRCLE_Y_ADJ)
        self._img = cv2.circle(self._img, circleCentre, CIRCLE_RADIUS, (0, 0, 255), 3)
        cv2.putText(self._img, 'D', circleCentre, cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 0, 255), 2)



    def handleMouseEvent(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._xClicked = x
            self._yClicked = y
        if event == cv2.EVENT_LBUTTONUP:
            self._xReleased = x
            self._yReleased = y
            print("Distance = " + str(self._xReleased - self._xClicked) + ", " + str(self._yReleased - self._yClicked))
            self.handleButton()

    def inObject(self,x1, y1, x2, y2, queryX, queryY):
        if (queryX > x1) and (queryX < x2) and (queryY > y1) and (queryY < y2):
            return True
        return False


    def handleButton(self):
        if self.inObject(RECT_X, RECT_Y, RECT_X + RECT_WIDTH, RECT_Y + RECT_HEIGHT, self._xClicked, self._yClicked):
            print("Clicked inside button")
            if self._frontFace is True:
                self._frontFace = False
                self._img = cv2.imread("./img/backDog.jpg")
                self._btnText = "FRONT"
                self.drawImg()
            else:
                self._frontFace = True
                self._img = cv2.imread("./img/frontDog.jpg")
                self._btnText = "BACK"
                self.drawImg()


    def calibThread(self):
        cv2.namedWindow('calibration')
        cv2.setMouseCallback('calibration', self.handleMouseEvent)
        while True:

            cv2.imshow('calibration', self._img)
            print("Booo")
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break


if __name__ == '__main__':
    calib = Calibration()
    while True:
        time.sleep(0.5)