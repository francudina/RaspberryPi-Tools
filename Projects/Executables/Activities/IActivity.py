import logging
from abc import abstractmethod
from collections import deque
from datetime import timedelta, datetime
from threading import Event
from typing import List

from Projects.Executables.Commands.ICommand import ICommand
from Projects.Executables.Compensating.ICompensating import ICompensating
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
from Projects.Executables.Utils import TimeUtils
from Projects.Queues.IQueue import IQueue


class IActivity(IQueue[ICommand], ICompensating):

    def __init__(self, pipeline_input_type: PipelineInputType, input_commands: List[ICommand], total_events: int,
                 queue_size: int = -1, blocking_queue: bool = True, blocking_timeout: timedelta = None):
        super(IActivity, self).__init__(queue_size, blocking_queue, blocking_timeout)
        # init vars
        self.activity_input_type: PipelineInputType = pipeline_input_type
        # - insert commands
        self.__add_commands(input_commands)
        # - executed
        self.__executed_commands: deque[ICommand] = deque()
        # - additional
        self.__stop_received: bool = False
        # - events for thread sync instead of using time.sleep(...)!
        self.events: List[Event] = [Event() for _ in range(total_events)]
        # - execution
        self.execution_start: datetime = None
        self.execution_end: datetime = None

    def start(self, **kwargs) -> bool:
        self.execution_start = datetime.now()
        self.status = ExecutablesStatus.IN_PROGRESS
        current_command: ICommand = self.next()
        while current_command is not None and not self.__stop_received:
            # for compensation process
            self.__executed_commands.appendleft(current_command)

            logging.info(f"\n > command {current_command.activity_type}: START ({TimeUtils.current_time()})")

            current_command.execution_start = datetime.now()
            started: bool = current_command.start(activity=self)
            current_command.execution_end = datetime.now()

            self.status = ExecutablesStatus.DONE if started \
                else ExecutablesStatus.BEFORE_COMPENSATION

            # reset events if needed after command execution!
            self._event_reset(command=current_command)

            if not started:
                self.execution_end = datetime.now()
                logging.info(f" > command {current_command.activity_type} START => FAILED ({TimeUtils.current_time()})")

                logging.info(f" \t> compensating command: START ({TimeUtils.current_time()})")
                compensated: bool = current_command.compensate(activity=self)
                logging.info(f" \t> compensating command: END {'=> FAILED again' if not compensated else ''} "
                             f"({TimeUtils.current_time()})")

                self.status = ExecutablesStatus.DONE_WITH_COMPENSATION if compensated \
                    else ExecutablesStatus.COMPENSATION_FAILED

                current_command.status = self.status

                # if failed to compensate then return IActivity execution failed
                return compensated

            self.status = ExecutablesStatus.BEFORE_STOP

            ended: bool = current_command.stop(activity=self)
            self.status = ExecutablesStatus.FINISHED if ended \
                else ExecutablesStatus.STOP_FAILED

            current_command.status = self.status

            if not ended:
                self.execution_end = datetime.now()
                logging.info(f" > command {current_command.activity_type} END => FAILED ({TimeUtils.current_time()})")
                # todo do something if stop() fails
                return False
            logging.info(f" > command {current_command.activity_type}: END ({TimeUtils.current_time()})")

            current_command = self.next()

        self.execution_end = datetime.now()

        # all passed if stop isn't received!
        return not self.__stop_received

    @abstractmethod
    def _pre_stop_method(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def _event_reset(self, command: ICommand) -> None:
        pass

    def stop(self, **kwargs) -> bool:
        self.__stop_received = True
        return self._pre_stop_method(**kwargs)
        # return self.compensate(activity=self)

    def compensate(self, **kwargs) -> bool:
        total: int = len(self.__executed_commands)
        total_passed: int = 0

        try:
            current_command: ICommand = self.__executed_commands.popleft()
        except:
            return True

        while current_command is not None:
            passed = current_command.compensate(activity=self)
            total_passed = total_passed + 1 if passed else total_passed

            try:
                current_command = self.__executed_commands.popleft()
            except:
                break

        return total_passed == total

    def total_execution_time(self):
        return self.execution_end - self.execution_start

# private
    def __add_commands(self, input_commands: List[ICommand]):
        for command in input_commands:
            self.add(command)
