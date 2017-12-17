import random
from cfinderCV import ACircleFinder, Circle


class BasicCircleFinder(ACircleFinder):

    def __init__(self):
        self.params = dict()

    def init_params(self, params: dict):
        self.params = params

    def compute(self, image_input):
        # remove later
        print("compute image_input")
        return None, Circle(random.randint(0, 100), random.randint(0, 100), 10)
