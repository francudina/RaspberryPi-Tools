import logging
from queue import Queue
from typing import Any, Generic, TypeVar

# python generics:
#   https://docs.python.org/3/library/typing.html#user-defined-generic-types
PayloadType = TypeVar('PayloadType')


class IQueue(Generic[PayloadType]):

    def __init__(self, queue_size: int = -1, blocking_queue: bool = True, blocking_timeout: float = None):
        self.__queue: Queue[PayloadType] = Queue[PayloadType](maxsize=queue_size)
        self.__blocking_queue: bool = blocking_queue
        self.__blocking_timeout: float = blocking_timeout

# methods
    # public
    def add(self, payload: PayloadType) -> bool:
        try:
            self.__queue.put(payload, block=self.__blocking_queue, timeout=self.__blocking_timeout)
            return True
        except Exception as e:
            logging.error(f'Error in IQueue.add() method: {e}')
            return False

    def next(self) -> PayloadType:
        try:
            # don't block
            return self.__queue.get(False)
        except:
            return None
