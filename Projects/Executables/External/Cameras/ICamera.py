import logging
from abc import abstractmethod

from Projects.Executables.IExecutable import IExecutable


class ICamera(IExecutable):

    def __init__(self):
        super(ICamera, self).__init__()
        # input values

    @abstractmethod
    def take_a_picture(self):
        pass

    @abstractmethod
    def record_video(self):
        pass

    @abstractmethod
    def analyze_picture(self):
        pass

    @abstractmethod
    def analyze_video(self):
        pass
