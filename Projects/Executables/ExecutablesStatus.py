from enum import Enum


class ExecutablesStatus(Enum):

    NOT_STARTED = 1
    STARTED = 2
    IN_PROGRESS = 3
    DONE = 4
    DONE_WITH_ERROR = 5
