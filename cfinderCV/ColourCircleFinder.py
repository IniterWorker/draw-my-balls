from cfinderCV import ACircleFinder, Circle


class ColourCircleFinder(ACircleFinder):

    def compute(self, image_input) -> Circle:
        # remove later
        print("compute image_input")
        return Circle(100, 100, 10)
