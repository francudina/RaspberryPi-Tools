from abc import ABC

from Projects.AutonomousDriving.Services.Algorithm.DrivingAlgorithmType import DrivingAlgorithmType
from Projects.Executables.Algorithm.IAlgorithm import IAlgorithm


class DrivingAlgorithm(IAlgorithm, ABC):

    def __init__(self, driving_algorithm_type: DrivingAlgorithmType):
        super().__init__()
        # init
        self.driving_algorithm_type: DrivingAlgorithmType = driving_algorithm_type
