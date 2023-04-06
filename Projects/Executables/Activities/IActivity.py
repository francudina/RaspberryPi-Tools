from abc import abstractmethod
from collections import deque
from datetime import timedelta
from typing import List

from Projects.Executables.Commands.ICommand import ICommand
from Projects.Executables.Compensating.ICompensating import ICompensating
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
from Projects.Queues.IQueue import IQueue


class IActivity(IQueue[ICommand], ICompensating):

    def __init__(self, pipeline_input_type: PipelineInputType, input_commands: List[ICommand],
                 queue_size: int = -1, blocking_queue: bool = True, blocking_timeout: timedelta = None):
        super(IActivity, self).__init__(queue_size, blocking_queue, blocking_timeout)
        # init vars
        self.activity_input_type: PipelineInputType = pipeline_input_type
        # - insert commands
        self.__add_commands(input_commands)
        # - executed
        self.__executed_commands: deque[ICommand] = deque[ICommand]()
        # - additional
        self.__stop_received: bool = False

    def start(self, **kwargs) -> bool:
        current_command: ICommand = self.next()
        while current_command is not None and not self.__stop_received:
            # for compensation process
            self.__executed_commands.appendleft(current_command)

            print(f"\n > command {current_command.activity_type}: START")
            started = current_command.start(activity=self)
            if not started:
                print(f" > command {current_command.activity_type} START => FAILED")
                return False

            ended = current_command.stop(activity=self)
            if not ended:
                print(f" > command {current_command.activity_type} END => FAILED")
                return False
            print(f" > command {current_command.activity_type}: END")

            current_command = self.next()

        # all passed if stop isn't received!
        return not self.__stop_received

    @abstractmethod
    def _pre_stop_method(self, **kwargs) -> bool:
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

# private
    def __add_commands(self, input_commands: List[ICommand]):
        for command in input_commands:
            self.add(command)
