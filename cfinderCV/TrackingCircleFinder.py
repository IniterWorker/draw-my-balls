from cfinderCV import ACircleFinder, Circle

import argparse
import datetime
import imutils
import time
import cv2

class TrackingCircleFinder(ACircleFinder):

    def __init__ (self):
        self.params = dict()
        self.firstFrame = None
      
    def init_params(self, params: dict):
        self.params = params
      
    def compute(self, image_input):
        frame = image_input
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (25,25), 0)

        if self.firstFrame is None:
            self.firstFrame = gray

        frameDelta = cv2.absdiff(self.firstFrame, gray)

        #cv2.imshow("frameDelta", frameDelta)

        thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)

        #cv2.imshow("thresh", thresh)

        #detect circle
        circles = cv2.HoughCircles(image=thresh, method=cv2.HOUGH_GRADIENT, dp=8, minDist=thresh.shape[0] / 4, param1=100, param2=200, minRadius=10, maxRadius=100);

        if circles is not None:
            im2 = thresh.copy()
            for circle in circles[0]:
                cv2.circle(im2, (circle[0], circle[1]), 2, (0, 0, 255), 4)
                cv2.circle(im2, (circle[0], circle[1]), circle[2], (255, 0, 0), 4)
                return thresh, Circle(circle[0], circle[1], circle[2])

        return thresh, None
