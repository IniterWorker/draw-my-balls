import random
from cfinderCV import ACircleFinder, Circle


class BasicCircleFinder(ACircleFinder):

    def compute(self, image_input) -> Circle:
        # remove later
        print("compute image_input")
        return Circle(random.randint(0, 100), random.randint(0, 100), 10)
