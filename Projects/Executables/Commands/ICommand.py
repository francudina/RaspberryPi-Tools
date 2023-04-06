from abc import ABC

from Projects.Executables.Activities.ActivityType import ActivityType
from Projects.Executables.Compensating.ICompensating import ICompensating


class ICommand(ICompensating, ABC):

    def __init__(self, activity_type: ActivityType):
        super(ICommand, self).__init__()
        # init vars
        self.activity_type: ActivityType = activity_type
