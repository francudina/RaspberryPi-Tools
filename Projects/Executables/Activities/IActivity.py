from abc import abstractmethod
from collections import deque
from datetime import timedelta, datetime
from threading import Event
from typing import List

from Projects.Executables.Commands.ICommand import ICommand
from Projects.Executables.Compensating.ICompensating import ICompensating
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
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
        current_command: ICommand = self.next()
        while current_command is not None and not self.__stop_received:
            # for compensation process
            self.__executed_commands.appendleft(current_command)

            print(f"\n > command {current_command.activity_type}: START")

            current_command.execution_start = datetime.now()
            started: bool = current_command.start(activity=self)
            current_command.execution_end = datetime.now()

            # reset events if needed after command execution!
            self._event_reset(command=current_command)

            if not started:
                self.execution_end = datetime.now()
                print(f" > command {current_command.activity_type} START => FAILED")

                print(f" \t> compensating command: START")
                compensated: bool = current_command.compensate(activity=self)
                print(f" \t> compensating command: END {'=> FAILED again' if not compensated else ''}")

                # if failed to compensate then return IActivity execution failed
                return compensated

            ended: bool = current_command.stop(activity=self)
            if not ended:
                self.execution_end = datetime.now()
                print(f" > command {current_command.activity_type} END => FAILED")
                # todo do something if stop() fails
                return False
            print(f" > command {current_command.activity_type}: END")

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
