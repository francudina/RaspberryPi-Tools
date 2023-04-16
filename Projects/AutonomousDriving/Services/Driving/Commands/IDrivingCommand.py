from abc import abstractmethod, ABC

from Projects.AutonomousDriving.Services.Driving.Commands.DirectionType import DirectionType
from Projects.Executables.Activities.ActivityType import ActivityType
from Projects.Executables.Commands.ICommand import ICommand


class IDrivingCommand(ICommand, ABC):

    def __init__(self, direction_type: DirectionType, wheel_angle: float):
        super(IDrivingCommand, self).__init__(ActivityType.DRIVING)
        # init vars
        self.direction_type: DirectionType = direction_type
        self.wheel_angle: float = wheel_angle

    @abstractmethod
    def get_compensation_direction(self) -> DirectionType:
        pass
