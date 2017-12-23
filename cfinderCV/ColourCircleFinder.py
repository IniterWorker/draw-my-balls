from cfinderCV import ACircleFinder, Circle
import cv2


class ColourCircleFinder(ACircleFinder):
    def __init__(self):
        self.params = dict()

    def init_params(self, params: dict):
        self.params = params
        self.params["lower"] = tuple(self.params["lower"])
        self.params["upper"] = tuple(self.params["upper"])

    def compute(self, image_input):
        # colour conversion
        hsv = cv2.cvtColor(image_input, cv2.COLOR_BGR2HSV)

        # mask with palette
        mask = cv2.inRange(hsv, self.params["lower"], self.params["upper"])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        # only proceed if at least one contour was found
        if len(contours) > 0:
            # find the big circle
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = \
                (
                    int(M["m10"] / M["m00"]),
                    int(M["m01"] / M["m00"])
                )

            if radius > 10:
                return mask, Circle(center[0], center[1], int(radius))

        return mask, Circle(0, 0, 0)
