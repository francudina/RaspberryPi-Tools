from abc import ABC
from datetime import datetime, timedelta

from Projects.Executables.Activities.ActivityType import ActivityType
from Projects.Executables.Compensating.ICompensating import ICompensating


class ICommand(ICompensating, ABC):

    def __init__(self, activity_type: ActivityType):
        super(ICommand, self).__init__()
        # init vars
        self.activity_type: ActivityType = activity_type
        # - execution
        self.execution_start: datetime = None
        self.execution_end: datetime = None

    def total_execution_time(self) -> timedelta:
        return self.execution_end - self.execution_start
