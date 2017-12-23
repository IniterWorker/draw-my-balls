import random
from cfinderCV import ACircleFinder, Circle
import cv2
import numpy as np


class BasicCircleFinder(ACircleFinder):

    def __init__(self):
        self.params = dict()

        # kernel opencv
        self.kernel = np.ones((2, 2), np.uint8)

    def init_params(self, params: dict):
        self.params = params

    def compute(self, image_input):
        # gray scale

        gray = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.medianBlur(gray, 5)
        gray = cv2.Canny(gray, 0, 130)

        # Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it.
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3.5)

        gray = cv2.erode(gray, self.kernel, iterations=1)
        # gray = erosion

        gray = cv2.dilate(gray, self.kernel, iterations=1)

        # detect circles in the image
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.20, 200, param1=30, param2=63, minRadius=10, maxRadius=120)

        # init circles
        bigger = Circle(-1, -1, -1)

        if circles is not None:
            # round
            circles = np.round(circles[0, :]).astype("int")

            for (x, y, r) in circles:
                if bigger.radius < r:
                    bigger.x = x
                    bigger.y = y
                    bigger.radius = r

        return gray, bigger
