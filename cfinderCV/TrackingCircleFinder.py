from cfinderCV import ACircleFinder, Circle


class TrackingCircleFinder(ACircleFinder):

    def __init__(self):
        self.params = dict()

    def init_params(self, params: dict):
        self.params = params

    def compute(self, image_input):
        # remove later
        print("compute image_input")
        return None, Circle(100, 100, 10)
