from datetime import datetime

from Projects.Executables.ExecutablesStatus import ExecutablesStatus


class LogData:

    def __init__(self, message: str, statues: ExecutablesStatus, occurred_at: datetime = datetime.now()):
        self.message: str = message
        self.statues: ExecutablesStatus = statues
        self.occurred_at: datetime = occurred_at

    def to_dict(self):
        return self.__dict__
