from cfinderCV import Circle
from abc import ABCMeta, abstractmethod


class ACircleFinder:
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_params(self, params: dict):
        raise NotImplementedError()

    @abstractmethod
    def compute(self, image_input):
        raise NotImplementedError()

