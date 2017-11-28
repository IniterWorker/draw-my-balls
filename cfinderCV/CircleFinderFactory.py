from cfinderCV.ACircleFinder import ACircleFinder
from cfinderCV.BasicCircleFinder import BasicCircleFinder
from cfinderCV.ColourCircleFinder import ColourCircleFinder
from cfinderCV.TrackingCircleFinder import TrackingCircleFinder


class CircleFinderFactory(object):
    @staticmethod
    def list() -> list:
        return ["Basic", "Colour", "Tracking"]

    @staticmethod
    def create(className: str) -> ACircleFinder:
        if className.lower() == "basic":
            return BasicCircleFinder()
        elif className.lower() == "colour":
            return ColourCircleFinder()
        elif className.lower() == "tracking":
            return TrackingCircleFinder()
        else:
            raise ValueError("invalid algorithm name")
