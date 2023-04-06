import logging

from Projects.Executables.External.Cameras.ICamera import ICamera


class CameraV13(ICamera):

    def __init__(self):
        super(CameraV13, self).__init__()
        # input values

    def take_a_picture(self):
        pass

    def record_video(self):
        pass

    def analyze_picture(self):
        pass

    def analyze_video(self):
        pass

    def start(self, **kwargs) -> bool:
        pass

    def stop(self, **kwargs) -> bool:
        pass
