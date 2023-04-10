from enum import Enum


class ExecutablesStatus(Enum):

    NOT_STARTED = 1

    IN_PROGRESS = 2

    BEFORE_COMPENSATION = 3

    DONE = 4
    DONE_WITH_ERROR = 5
    DONE_WITH_COMPENSATION = 6
    COMPENSATION_FAILED = 7

    BEFORE_STOP = 8
    STOP_FAILED = 9
    FINISHED = 10

