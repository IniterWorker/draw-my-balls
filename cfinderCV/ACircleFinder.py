from cfinderCV import Circle
from abc import ABCMeta, abstractmethod


class ACircleFinder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def compute(self, image_input) -> Circle:
        raise NotImplementedError()

