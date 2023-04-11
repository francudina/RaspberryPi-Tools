from abc import abstractmethod
from collections import deque
from datetime import timedelta

from Projects.Executables.Activities.IActivity import IActivity
from Projects.Executables.Compensating.ICompensating import ICompensating
from Projects.Executables.ExecutablesStatus import ExecutablesStatus
from Projects.Executables.Pipelines.Inputs.PipelineInputType import PipelineInputType
from Projects.Queues.IQueue import IQueue


class IPipeline(IQueue[IActivity], ICompensating):

    def __init__(self, pipeline_input_type: PipelineInputType, queue_size: int = -1, blocking_queue: bool = True, blocking_timeout: timedelta = None):
        super(IPipeline, self).__init__(queue_size, blocking_queue, blocking_timeout)
        # init vars
        self.__pipeline_input_type: PipelineInputType = pipeline_input_type
        self.__executed_activities: deque[IActivity] = deque()
        # additional
        self.__stop_received: bool = False
        self.__pause_received: bool = False

# methods
    # public
    def start(self, **kwargs) -> bool:
        current_activity: IActivity = self.next()
        self.status = ExecutablesStatus.IN_PROGRESS
        while current_activity is not None and not self.__stop_received and not self.__pause_received:

            try:
                started = current_activity.start()
                if not started:
                    passed: bool = self.compensate()

                self.status = current_activity.status

                ended = current_activity.stop()
                self.status = current_activity.status

                if not ended:
                    return False

                # for compensation process
                self.__executed_activities.appendleft(current_activity)

                current_activity = self.next()

            except Exception as e:
                logging.info(f"(e) Exception: {e}")

                self.status = ExecutablesStatus.FAILED
                return False

        # all passed if stop isn't received!
        return not self.__stop_received or self.__pause_received

    def pause(self) -> bool:
        self.__pause_received = True
        # if pause var is changed will return True otherwise False
        return self.__pause_received

    def resume(self) -> bool:
        self.__pause_received = False
        return self.start()

    def stop(self, **kwargs) -> bool:
        self.__stop_received = True
        return self.compensate()

    def compensate(self, **kwargs) -> bool:
        total: int = len(self.__executed_activities)
        total_passed: int = 0

        try:
            current_activity: IActivity = self.__executed_activities.popleft()
        except:
            return True

        while current_activity is not None:
            passed = current_activity.compensate(pipeline=self)
            total_passed = total_passed + 1 if passed else total_passed

            try:
                current_activity = self.__executed_activities.popleft()
            except:
                break

        return total_passed == total
